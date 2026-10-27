"""Find the audio output device on whatever machine the experiment runs on.

Why this exists
---------------
The experiment scripts play speech in noise; the data are only valid through
headphones. On a remote or borrowed PC nobody knows in advance what the output
devices are called, and PsychoPy's saved preference (userPrefs.cfg,
hardware/audioDevice) may name a device that is not plugged in. Listing a device
is also not the same as being able to open it (an empty headphone jack is listed
but the stream fails to start), so candidates are opened for real before use.

Step 1 - on the new machine, before any experiment, run this file alone:

    python audio_pick.py                      table of every output device, and the one that would be chosen
    python audio_pick.py --probe              also try to open each device (slow, but tells the truth)
    python audio_pick.py --beep               play a 1 s tone on the chosen device ("do you hear it in the headphones?")
    python audio_pick.py --set "Headphones"   remember that device for the experiment scripts (writes audio_device.txt
                                              next to this file and the PsychoPy preference)
    python audio_pick.py --json out.json      save the table, e.g. to send back from the remote machine

Step 2 - run the experiment. The scripts call ``setup_from_argv(sys.argv)``, which
takes the device from the first of these that is set:

    1. ``--audio-device "Headphones"`` on the command line
    2. the environment variable ``VAWM_AUDIO_DEVICE``
    3. ``audio_device.txt`` written by ``--set``
    4. automatic choice: a name that looks like headphones, else the saved
       PsychoPy preference, else anything that opens

Add ``--require-headphones`` to stop the script instead of falling back to a
speaker when step 4 finds no headphone-like name. A device named explicitly
(1-3) must exist, or the script stops with the list of what is available; it is
never silently replaced.

``--list-audio`` on an experiment script prints the table and exits.
"""
import json
import os
import platform
import sys

HEADPHONE_WORDS = ("headphone", "headset", "earphone", "earbud", "airpods", "buds", "耳機", "耳机")
CHOICE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio_device.txt")
ENV_VAR = "VAWM_AUDIO_DEVICE"


# ---------------------------------------------------------------------------------------------
# pure helpers (no PsychoPy; these are what the tests cover)
# ---------------------------------------------------------------------------------------------
def looks_like_headphones(name):
    low = str(name).lower()
    return any(w in low for w in HEADPHONE_WORDS)


def unique_names(devices):
    """Device names in listing order, duplicates removed (the same card shows up once per host API on Windows)."""
    seen = []
    for d in devices:
        n = d.get("name")
        if n and n not in seen:
            seen.append(n)
    return seen


def find_named(names, wanted):
    """Devices whose name contains ``wanted`` (case-insensitive). An exact match goes first."""
    w = wanted.lower().strip()
    exact = [n for n in names if n.lower().strip() == w]
    partial = [n for n in names if w in n.lower() and n not in exact]
    return exact + partial


def rank_names(names, saved=()):
    """Order for the automatic choice: headphone-like names, then the saved PsychoPy preference, then the rest."""
    saved = [saved] if isinstance(saved, str) else list(saved or [])
    head = [n for n in names if looks_like_headphones(n)]
    pref = [n for n in saved if n in names and n not in head]
    rest = [n for n in names if n not in head and n not in pref]
    return head + pref + rest


def parse_argv(argv):
    """Return (device name or "", require_headphones, list_only) from the command line, environment and choice file."""
    name = ""
    args = list(argv)
    for i, a in enumerate(args):
        if a.startswith("--audio-device="):
            name = a.split("=", 1)[1]
        elif a == "--audio-device" and i + 1 < len(args):
            name = args[i + 1]
    if not name:
        name = os.environ.get(ENV_VAR, "")
    if not name and os.path.exists(CHOICE_FILE):
        with open(CHOICE_FILE, encoding="utf-8") as f:
            name = f.read().strip()
    return name.strip(), "--require-headphones" in args, "--list-audio" in args


# ---------------------------------------------------------------------------------------------
# PsychoPy side
# ---------------------------------------------------------------------------------------------
def list_output_devices():
    """Every output device as a dict: name, index, host_api, channels, sample_rate.

    Uses the full profile from the audio backend when PsychoPy exposes it (host API and channel
    count help tell "Headphones (Realtek)" under WASAPI from the same card under MME); otherwise
    falls back to SpeakerDevice.getAvailableDevices(), then to sounddevice / psychtoolbox directly.
    """
    try:
        from psychopy.hardware.speaker import SpeakerDevice
    except Exception:
        SpeakerDevice = None

    profiles = None
    if SpeakerDevice is not None:
        try:
            backend = SpeakerDevice.resolveBackend() if hasattr(SpeakerDevice, "resolveBackend") else SpeakerDevice
            getter = getattr(backend, "_getDevicesPsychtoolbox", None) or getattr(backend, "_getDevicesSoundDevice", None)
            profiles = getter() if getter else None
        except Exception:
            profiles = None
    if profiles is None:
        # Same rule as SpeakerDevice.createStream (PsychoPy 2026.1): on Windows only WASAPI devices
        # (device_type=13) unless the preference audioWASAPIOnly is off. Listing other host APIs would show
        # names (MME "Microsoft Sound Mapper", WDM-KS "Headphones 1 ...") that SpeakerDevice then cannot open.
        try:
            import psychtoolbox.audio as ptb
            wasapi_only = True
            try:
                from psychopy import prefs
                wasapi_only = bool(prefs.hardware["audioWASAPIOnly"])
            except Exception:
                pass
            profiles = ptb.get_devices(device_type=13 if sys.platform == "win32" and wasapi_only else None)
        except Exception:
            profiles = None
    if profiles is None:
        try:
            import sounddevice as sd
            profiles = []
            for dev in sd.query_devices():
                profiles.append({"DeviceIndex": dev["index"], "DeviceName": dev["name"],
                                 "HostAudioAPIName": sd.query_hostapis(dev["hostapi"])["name"],
                                 "NrOutputChannels": dev["max_output_channels"],
                                 "DefaultSampleRate": dev["default_samplerate"]})
        except Exception:
            profiles = None

    out = []
    if profiles is not None:
        for p in profiles:
            if p.get("NrOutputChannels", 1) == 0:          # input-only (microphones)
                continue
            out.append({"name": p.get("DeviceName"), "index": p.get("DeviceIndex"),
                        "host_api": p.get("HostAudioAPIName", ""), "channels": p.get("NrOutputChannels"),
                        "sample_rate": p.get("DefaultSampleRate")})
    elif SpeakerDevice is not None:
        for d in SpeakerDevice.getAvailableDevices():
            name = d.get("deviceName") or d.get("name") if isinstance(d, dict) else getattr(d, "deviceName", None)
            out.append({"name": name, "index": d.get("index") if isinstance(d, dict) else None,
                        "host_api": "", "channels": None, "sample_rate": None})
    return [d for d in out if d["name"]]


def probe_device(name):
    """Try to open the device for real. Returns (ok, message). The stream stays open for the experiment to reuse."""
    try:
        from psychopy.hardware.speaker import SpeakerDevice
        SpeakerDevice(name=name)              # the first positional argument is index: always pass name=
        return True, "opened"
    except (KeyboardInterrupt, SystemExit):
        raise
    except BaseException as e:                # PsychoPy's DeviceNotConnectedError derives from BaseException, not Exception
        return False, f"{type(e).__name__}: {e}"


def saved_preference():
    try:
        from psychopy import prefs
        want = prefs.hardware.get("audioDevice") or []
        return [want] if isinstance(want, str) else list(want)
    except Exception:
        return []


def apply_preference(name, save=False):
    """Point PsychoPy's hardware/audioDevice preference at ``name`` so sound.Sound() uses it. ``save`` writes userPrefs.cfg."""
    try:
        from psychopy import prefs
    except Exception:
        return False
    prefs.hardware["audioDevice"] = [name]
    if save:
        prefs.saveUserPrefs()
    return True


def select_output_device(name="", require_headphones=False, devices=None, probe=None, saved=None, verbose=True):
    """Choose the output device and point PsychoPy at it.

    name                 explicit device name (substring is enough). Must exist; raises RuntimeError otherwise.
    require_headphones   when choosing automatically, refuse anything that does not look like headphones.
                         An explicit name is trusted as is (your headphones may be called "USB Audio").
    devices / probe / saved   injection points for tests; the defaults talk to PsychoPy.

    Returns {"name", "is_headphones", "explicit", "candidates", "tried"}.
    """
    devices = list_output_devices() if devices is None else devices
    probe = probe_device if probe is None else probe
    saved = saved_preference() if saved is None else saved
    names = unique_names(devices)
    host = platform.node()
    if not names:
        raise RuntimeError(f"[audio] no audio output device found on {host}; check the sound driver and the "
                           "headphone plug, and PsychoPy's audio library setting (ptb)")

    explicit = bool(name)
    if explicit:
        order = find_named(names, name)
        if not order:
            listing = "\n".join(f"    - {n}" for n in names)
            raise RuntimeError(f"[audio] no output device on {host} matches {name!r}. Available:\n{listing}\n"
                               "  Run `python audio_pick.py` to see the table, then pass one of these names.")
    else:
        order = rank_names(names, saved)
        if require_headphones:
            order = [n for n in order if looks_like_headphones(n)]
            if not order:
                listing = "\n".join(f"    - {n}" for n in names)
                raise RuntimeError(f"[audio] no device on {host} looks like headphones. Available:\n{listing}\n"
                                   "  Plug in headphones, or name the device: --audio-device \"...\" "
                                   "(or VAWM_AUDIO_DEVICE, or python audio_pick.py --set \"...\")")

    tried = []
    for cand in order:
        ok, msg = probe(cand)
        tried.append((cand, ok, msg))
        if ok:
            apply_preference(cand)
            info = {"name": cand, "is_headphones": looks_like_headphones(cand), "explicit": explicit,
                    "candidates": names, "tried": tried, "host": host}
            if verbose:
                how = "named" if explicit else "auto"
                print(f"[audio] {host}: using {cand!r} ({how})")
                if not info["is_headphones"] and not explicit:
                    print(f"[audio] WARNING: {cand!r} does not look like headphones. Plug in headphones, "
                          "or name the device with --audio-device / audio_pick.py --set")
            return info
        if verbose:
            print(f"[audio] {cand!r} could not be opened ({msg}); trying the next one")
    failed = "\n".join(f"    - {n}: {m}" for n, ok, m in tried)
    raise RuntimeError(f"[audio] none of the candidate devices on {host} could be opened:\n{failed}")


def setup_from_argv(argv=None, require_headphones=False, verbose=True):
    """What the experiment scripts call. Reads --audio-device / --require-headphones / --list-audio, env var, choice file.

    ``require_headphones=True`` is the script's own policy (GRTv3_ada: an SNR task, speakers make the data
    worthless); the command-line flag can only add the requirement, not remove it.
    """
    argv = sys.argv if argv is None else argv
    name, require, list_only = parse_argv(argv)
    if list_only:
        print_table(list_output_devices())
        sys.exit(0)
    return select_output_device(name, require_headphones=require or require_headphones, verbose=verbose)


def register_label(name, label="Laptop"):
    """Make PsychoPy's DeviceManager label ``label`` point at device ``name`` (Builder scripts use deviceLabel='Laptop')."""
    from psychopy.hardware import DeviceManager
    if DeviceManager.hasDevice(label):
        DeviceManager.removeDevice(label)
    DeviceManager.addDevice(deviceClass="psychopy.hardware.speaker.SpeakerDevice", deviceName=label, index=name)


# ---------------------------------------------------------------------------------------------
# command line
# ---------------------------------------------------------------------------------------------
def print_table(devices, saved=None, file=None):
    saved = saved_preference() if saved is None else saved
    file = sys.stdout if file is None else file
    print(f"host: {platform.node()}   ({platform.system()} {platform.release()})", file=file)
    print(f"saved PsychoPy preference: {saved or 'none'}", file=file)
    print(f"choice file: {CHOICE_FILE if os.path.exists(CHOICE_FILE) else 'none'}", file=file)
    print(f"\n{len(devices)} output device(s):", file=file)
    print(f"  {'idx':>4}  {'ch':>2}  {'rate':>6}  {'host API':<14}  name", file=file)
    for d in devices:
        tag = "  <- headphones?" if looks_like_headphones(d["name"]) else ""
        rate = f"{int(d['sample_rate'])}" if d.get("sample_rate") else "?"
        print(f"  {str(d.get('index', '?')):>4}  {str(d.get('channels', '?')):>2}  {rate:>6}  "
              f"{str(d.get('host_api', '')):<14}  {d['name']}{tag}", file=file)
    names = unique_names(devices)
    if names:
        order = rank_names(names, saved)
        print(f"\nautomatic choice would try, in order: {order}", file=file)


def beep(name, secs=1.0):
    from psychopy import core, sound
    apply_preference(name)
    snd = sound.Sound("A", secs=secs, stereo=True)
    print(f"[audio] playing a {secs:.1f} s tone on {name!r} ...")
    snd.play()
    core.wait(secs + 0.2)


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--probe", action="store_true", help="try to open every device")
    ap.add_argument("--beep", action="store_true", help="play a 1 s tone on the chosen device")
    ap.add_argument("--set", metavar="NAME", help="remember NAME for the experiment scripts (audio_device.txt + PsychoPy preference)")
    ap.add_argument("--clear", action="store_true", help="forget the remembered device")
    ap.add_argument("--json", metavar="FILE", help="also write the table to FILE")
    ap.add_argument("--audio-device", metavar="NAME", default="", help="name to choose (substring)")
    ap.add_argument("--require-headphones", action="store_true")
    a = ap.parse_args(argv)

    if a.clear and os.path.exists(CHOICE_FILE):
        os.remove(CHOICE_FILE)
        print(f"[audio] removed {CHOICE_FILE}")

    devices = list_output_devices()
    print_table(devices)
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump({"host": platform.node(), "devices": devices, "saved_preference": saved_preference()},
                      f, ensure_ascii=False, indent=2)
        print(f"\nwrote {a.json}")

    if a.probe:
        print("\nopening each device:")
        for n in unique_names(devices):
            ok, msg = probe_device(n)
            print(f"  {'OK ' if ok else 'FAIL'}  {n}  ({msg})")

    name = a.set or a.audio_device or parse_argv([])[0]
    if a.set or a.beep or a.audio_device or a.require_headphones:
        info = select_output_device(name, require_headphones=a.require_headphones)
        if a.set:
            with open(CHOICE_FILE, "w", encoding="utf-8") as f:
                f.write(info["name"] + "\n")
            apply_preference(info["name"], save=True)
            print(f"[audio] remembered {info['name']!r} in {CHOICE_FILE} and in the PsychoPy preferences")
        if a.beep:
            beep(info["name"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
