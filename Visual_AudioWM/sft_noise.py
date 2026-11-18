"""Speech-shaped noise for the SFT consonant tokens (stimuli/T??_<cons>3.wav): one fixed SNR for the whole session,
one deterministic noise sample per PRESENTATION.

Why (DECISIONS 24): the d' table has almost nothing below d' 0.8, so the sound L level sits at the listener's ceiling.
Noise compresses every pair's d' towards 0 and moves the whole scale left; it is the same manipulation Miller & Nicely
(1955) used to produce the matrices the scale comes from. The SNR is a session constant (like viewing distance for the
colour axis), NOT a level: H and L still differ only by consonant pair.

Seeds. The noise sample is a nuisance variable; it must not be tied to any condition. The seed of each presentation is
    seed_for(<phase>, <trial identifiers>, <slot>)          e.g. seed_for("study", block, set, "s1")
a stable 64-bit hash of those strings (blake2b, not Python's salted hash()). Consequences:
  * every participant hears the same noise in the same trial/slot (a fixed stimulus set, as sound_pairs.csv is);
  * the probe gets a different seed from the studied item, so a "same" probe is the same CONSONANT in a different noise
    sample, never a bit-identical waveform that could be matched on noise texture;
  * nothing needs to be stored to rebuild a stimulus: rebuild(wav, snr_db, seed) is bit-identical, and the seed is
    still written into every data row (snd_seed_* columns) so the analysis never has to recompute it.

Level. SNR is speech RMS over the token's active region (acoustic onset to offset, -40 dB re peak) against noise RMS over
the same span; the mixed signal is normalised to snr_audio.OUTPUT_RMS so loudness is not a cue. Noise starts 150 ms
before the token and runs 100 ms after it (onset uncertainty, as in snr_audio), which keeps every file under 1 s.

Pure numpy; no PsychoPy. `python sft_noise.py` runs the self-check.
"""
import glob
import hashlib
import os

import numpy as np

import snr_audio as sa

HERE = os.path.dirname(os.path.abspath(__file__))
STIM_GLOB = os.path.join(HERE, "stimuli", "T??_*3.wav")
NOISE_LEAD_MS = 150.0
NOISE_TAIL_MS = 100.0
LTAS_NFFT = 1024

_WAV_CACHE = {}
_LTAS_CACHE = None


def seed_for(*parts):
    """Deterministic 63-bit seed from the presentation's identifiers. Same inputs -> same seed on every machine."""
    key = ":".join(str(p) for p in parts).encode("utf-8")
    return int.from_bytes(hashlib.blake2b(key, digest_size=8).digest(), "little") >> 1


def _load(wav_rel):
    """(sr, x, onset, offset) for one token, cached. Paths are relative to this folder (as in the data files)."""
    if wav_rel not in _WAV_CACHE:
        path = wav_rel if os.path.isabs(wav_rel) else os.path.join(HERE, wav_rel)
        sr, x = sa._read_wav(path)
        thr = np.abs(x).max() * 10 ** (sa.ONSET_THRESH_DB / 20.0)
        above = np.flatnonzero(np.abs(x) > thr)
        _WAV_CACHE[wav_rel] = (sr, x, int(above[0]), int(above[-1]) + 1)
    return _WAV_CACHE[wav_rel]


def _ltas():
    """Long-term average spectrum pooled over all 192 tokens on a common frequency grid (the tokens are not all at the
    same sample rate: 15000-15500 Hz, talker-specific). Same window/hop as snr_audio._ltas."""
    global _LTAS_CACHE
    if _LTAS_CACHE is None:
        files = sorted(glob.glob(STIM_GLOB))
        if not files:
            raise FileNotFoundError("no stimuli/T??_*3.wav found for the LTAS")
        win = np.hanning(LTAS_NFFT)
        f_grid = np.linspace(0.0, 8000.0, 513)
        acc, cnt = np.zeros_like(f_grid), 0
        for f in files:
            sr, x, on, off = _load(os.path.relpath(f, HERE))
            seg = x[on:off]
            f_file = np.fft.rfftfreq(LTAS_NFFT, 1.0 / sr)
            for i in range(0, len(seg) - LTAS_NFFT, LTAS_NFFT // 2):
                acc += np.interp(f_grid, f_file, np.abs(np.fft.rfft(seg[i:i + LTAS_NFFT] * win)), right=0.0)
                cnt += 1
        _LTAS_CACHE = (f_grid, acc / cnt)
    return _LTAS_CACHE


def _shaped_noise(n, sr, rng):
    f_ltas, ltas = _ltas()
    w = rng.standard_normal(n)
    y = np.fft.irfft(np.fft.rfft(w) * np.interp(np.fft.rfftfreq(n, 1.0 / sr), f_ltas, ltas, right=0.0), n=n)
    return y / sa._rms(y)


def mix_components(wav_rel, snr_db, seed):
    """(sr, speech, noise, span): the two components already at output level, so speech + noise is the signal and the
    SNR can be measured on the components (snr_audio.mix_components does the same)."""
    sr, x, on, off = _load(wav_rel)
    lead = int(round(NOISE_LEAD_MS * sr / 1000.0))
    tail = int(round(NOISE_TAIL_MS * sr / 1000.0))
    total = lead + len(x) + tail
    noise = _shaped_noise(total, sr, np.random.default_rng(int(seed)))
    span = slice(lead + on, lead + off)
    noise *= (sa._rms(x[on:off]) / 10.0 ** (float(snr_db) / 20.0)) / sa._rms(noise[span])
    sp = np.zeros(total)
    sp[lead:lead + len(x)] = x
    gain = sa.OUTPUT_RMS / sa._rms(sp + noise)
    return sr, sp * gain, noise * gain, span


def mix(wav_rel, snr_db, seed):
    sr, sp, nz, _ = mix_components(wav_rel, snr_db, seed)
    return sr, sp + nz


def realised_snr(wav_rel, snr_db, seed):
    sr, sp, nz, span = mix_components(wav_rel, snr_db, seed)
    return 20.0 * np.log10(sa._rms(sp[span]) / sa._rms(nz[span]))


def rebuild(wav_rel, snr_db, seed, path):
    """Write the exact stimulus that was presented (same wav, dB and seed -> same bytes)."""
    sr, y = mix(wav_rel, snr_db, seed)
    sa.write_wav(path, sr, y)
    return path


class NoiseMixer:
    """Renders mixed tokens on demand into `outdir` (data/<subj>_snr/, gitignored) and returns the path to play."""

    def __init__(self, outdir, snr_db):
        self.outdir = outdir
        self.snr_db = float(snr_db)
        self.log = []
        os.makedirs(outdir, exist_ok=True)

    def render(self, wav_rel, seed):
        path = os.path.join(self.outdir, f"{int(seed)}_{os.path.basename(wav_rel)}")
        if not os.path.exists(path):
            rebuild(wav_rel, self.snr_db, seed, path)
        self.log.append((wav_rel, self.snr_db, int(seed), path))
        return path


def validate():
    import tempfile
    wavs = sorted(glob.glob(STIM_GLOB))
    assert wavs, "no stimuli"
    w = os.path.relpath(wavs[0], HERE)
    s1, s2 = seed_for("study", 1, 1, "s1"), seed_for("probe", 1, 1, 1)
    assert s1 != s2 and seed_for("study", 1, 1, "s1") == s1
    for db in (-12.0, -6.0, 0.0):
        r = realised_snr(w, db, s1)
        assert abs(r - db) < 0.05, (db, r)
    sr, a = mix(w, -6.0, s1)
    assert np.array_equal(a, mix(w, -6.0, s1)[1]) and not np.array_equal(a, mix(w, -6.0, s2)[1])
    assert len(a) / sr < 1.0 and np.abs(a).max() <= sa.PEAK_LIMIT + 1e-9
    with tempfile.TemporaryDirectory() as d:
        p1 = rebuild(w, -6.0, s1, os.path.join(d, "a.wav"))
        p2 = NoiseMixer(d, -6.0).render(w, s1)
        assert open(p1, "rb").read() == open(p2, "rb").read()
    longest = max(len(_load(os.path.relpath(f, HERE))[1]) / _load(os.path.relpath(f, HERE))[0] for f in wavs) + (NOISE_LEAD_MS + NOISE_TAIL_MS) / 1000
    assert longest < 1.0, longest      # the experiment plays every sound with secs=1
    print(f"sft_noise OK: {len(wavs)} tokens, LTAS pooled, realised SNR within 0.05 dB, seeds deterministic, "
          f"rebuild bit-identical, longest mixed file {longest:.3f} s")


if __name__ == "__main__":
    validate()
