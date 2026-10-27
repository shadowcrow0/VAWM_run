"""audio_pick: the choice logic, with fake device lists (PsychoPy is not needed)."""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import audio_pick as ap  # noqa: E402

DEVS = [
    {"name": "Speakers (Realtek(R) Audio)", "index": 4, "host_api": "WASAPI", "channels": 2, "sample_rate": 48000},
    {"name": "Headphones (Realtek(R) Audio)", "index": 7, "host_api": "WASAPI", "channels": 2, "sample_rate": 48000},
    {"name": "Headphones (Realtek(R) Audio)", "index": 1, "host_api": "MME", "channels": 2, "sample_rate": 44100},
    {"name": "DELL U2722D (NVIDIA High Definition Audio)", "index": 9, "host_api": "WASAPI", "channels": 2, "sample_rate": 48000},
]
ALL_OK = lambda n: (True, "opened")  # noqa: E731


def test_unique_names_keeps_order_and_drops_duplicates():
    assert ap.unique_names(DEVS) == ["Speakers (Realtek(R) Audio)", "Headphones (Realtek(R) Audio)",
                                     "DELL U2722D (NVIDIA High Definition Audio)"]


def test_auto_prefers_headphones_over_saved_preference():
    info = ap.select_output_device("", devices=DEVS, probe=ALL_OK, saved=["DELL U2722D (NVIDIA High Definition Audio)"], verbose=False)
    assert info["name"] == "Headphones (Realtek(R) Audio)" and info["is_headphones"] and not info["explicit"]


def test_auto_falls_back_to_saved_then_rest_when_headphones_do_not_open():
    probe = lambda n: (not n.startswith("Headphones"), "x")  # noqa: E731
    info = ap.select_output_device("", devices=DEVS, probe=probe, saved=["DELL U2722D (NVIDIA High Definition Audio)"], verbose=False)
    assert info["name"] == "DELL U2722D (NVIDIA High Definition Audio)"
    assert [t[0] for t in info["tried"]] == ["Headphones (Realtek(R) Audio)", "DELL U2722D (NVIDIA High Definition Audio)"]


def test_require_headphones_refuses_speakers():
    devs = [d for d in DEVS if "Headphones" not in d["name"]]
    with pytest.raises(RuntimeError, match="looks like headphones"):
        ap.select_output_device("", require_headphones=True, devices=devs, probe=ALL_OK, saved=[], verbose=False)


def test_explicit_name_substring_case_insensitive():
    info = ap.select_output_device("dell", devices=DEVS, probe=ALL_OK, saved=[], verbose=False)
    assert info["name"] == "DELL U2722D (NVIDIA High Definition Audio)" and info["explicit"]


def test_explicit_name_is_trusted_even_with_require_headphones():
    info = ap.select_output_device("Speakers", require_headphones=True, devices=DEVS, probe=ALL_OK, saved=[], verbose=False)
    assert info["name"] == "Speakers (Realtek(R) Audio)"


def test_explicit_name_missing_raises_with_list():
    with pytest.raises(RuntimeError, match="Available"):
        ap.select_output_device("Bluetooth", devices=DEVS, probe=ALL_OK, saved=[], verbose=False)


def test_nothing_opens_raises():
    with pytest.raises(RuntimeError, match="could be opened"):
        ap.select_output_device("", devices=DEVS, probe=lambda n: (False, "no stream"), saved=[], verbose=False)


def test_parse_argv_priority(tmp_path, monkeypatch):
    monkeypatch.setattr(ap, "CHOICE_FILE", str(tmp_path / "audio_device.txt"))
    monkeypatch.delenv(ap.ENV_VAR, raising=False)
    assert ap.parse_argv(["x.py"]) == ("", False, False)
    (tmp_path / "audio_device.txt").write_text("FromFile\n", encoding="utf-8")
    assert ap.parse_argv(["x.py"])[0] == "FromFile"
    monkeypatch.setenv(ap.ENV_VAR, "FromEnv")
    assert ap.parse_argv(["x.py"])[0] == "FromEnv"
    assert ap.parse_argv(["x.py", "--audio-device", "FromArg", "--require-headphones"]) == ("FromArg", True, False)
    assert ap.parse_argv(["x.py", "--audio-device=A B", "--list-audio"]) == ("A B", False, True)


def test_print_table_marks_headphones(capsys):
    ap.print_table(DEVS, saved=[])
    out = capsys.readouterr().out
    assert "<- headphones?" in out and "automatic choice would try" in out
