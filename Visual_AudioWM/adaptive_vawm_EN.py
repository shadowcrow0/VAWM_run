"""
Adaptive calibration for VAWM_nobox.py: each participant first calibrates the colour distance (block 1) and the consonant confusability (block 2) with LNRMCalibrator (original adaptiveSFT, needs PyMC) or PsiCalibrator (numpy + scipy), and the calibrated H / L then produce stimuli/block1..6.csv; this file does not touch PsychoPy (the screen is in VAWM_calibrate.py).
"""
import ast
import csv
import importlib
import importlib.util
import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


# ============================================================================================
# ============================================================================================

def _ensure_user_site():
    """Add the real Python user-site back to sys.path, because pymc / nutpie / the editable adaptiveSFT live there and it is hidden when started with python -s or after psychopy overrides site.USER_SITE."""
    import site
    import sysconfig
    cands = []
    try:
        cands.append(sysconfig.get_path("purelib", "nt_user" if os.name == "nt" else "posix_user"))
    except Exception:
        pass
    try:
        cands.append(site.getusersitepackages())
    except Exception:
        pass
    for usp in cands:
        if usp and os.path.isdir(usp) and usp not in sys.path:
            site.addsitedir(usp)


_ensure_user_site()


def _editable_install_root():
    """Repo path of an editable-installed (pip install -e) adaptiveSFT, read from the dist-info direct_url.json."""
    try:
        from importlib.metadata import distribution
        from urllib.parse import unquote, urlparse
        info = json.loads(distribution("adaptivesft").read_text("direct_url.json") or "{}")
        if info.get("dir_info", {}).get("editable"):
            path = unquote(urlparse(info["url"]).path)
            if os.name == "nt" and path.startswith("/") and path[2:3] == ":":
                path = path[1:]                                   # file:///C:/... -> C:/...
            return path
    except Exception:
        pass
    return None


def adaptivesft_root():
    """Directory of the adaptiveSFT repo, in order: ADAPTIVESFT_PATH env var -> ../adaptiveSFT next to this folder -> the pip install -e copy -> adaptivesft_path.txt in this folder."""
    cfg = os.path.join(HERE, "adaptivesft_path.txt")
    from_file = open(cfg, encoding="utf-8").read().strip() if os.path.isfile(cfg) else None
    candidates = [os.environ.get("ADAPTIVESFT_PATH"), os.path.join(os.path.dirname(HERE), "adaptiveSFT"),
                  _editable_install_root(), from_file]
    for c in candidates:
        if c and os.path.isfile(os.path.join(c, "adaptivesft", "psi.py")):
            return c
    raise ImportError("adaptiveSFT not found: clone it next to this folder, set ADAPTIVESFT_PATH=<path>, pip install -e it, "
                      "or put adaptivesft_path.txt in this folder (one line: the path to adaptiveSFT)")


def load_psi_module():
    """Load only adaptiveSFT/adaptivesft/psi.py (numpy + scipy only), without running the package __init__.py, which imports PyMC."""
    path = os.path.join(adaptivesft_root(), "adaptivesft", "psi.py")
    spec = importlib.util.spec_from_file_location("adaptivesft_psi", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_full_package():
    """The full adaptivesft package (needed for the lnrm fit and the analysis; requires PyMC). Returns the adaptivesft.experiment module."""
    for name in list(sys.modules):
        if name == "adaptivesft" or name.startswith("adaptivesft."):
            del sys.modules[name]
    root = adaptivesft_root()
    if root not in sys.path:
        sys.path.insert(0, root)
    return importlib.import_module("adaptivesft.experiment")


psi_module = load_psi_module()
Psi = psi_module.Psi
salience_levels = psi_module.salience_levels


# ============================================================================================
# ============================================================================================

CSV_COLUMNS = ["trial",
               "color1_target", "color1_H", "color1_L", "color1_H_deltaE", "color1_L_deltaE", "color1_HL_deltaE",
               "color2_target", "color2_H", "color2_L", "color2_H_deltaE", "color2_L_deltaE", "color2_HL_deltaE",
               "audio1_target", "audio1_H", "audio1_L", "audio1_H_count", "audio1_L_count",
               "audio1_target_talker", "audio1_H_talker", "audio1_L_talker",
               "audio1_target_file", "audio1_H_file", "audio1_L_file",
               "audio2_target", "audio2_H", "audio2_L", "audio2_H_count", "audio2_L_count",
               "audio2_target_talker", "audio2_H_talker", "audio2_L_talker",
               "audio2_target_file", "audio2_H_file", "audio2_L_file"]
TALKERS = ["T01", "T02", "T03", "T04", "T05", "T06", "T07", "T08", "T09", "T10", "T11", "T12"]

LEVELS_COLOUR = [2.0, 6.0, 12.0, 20.0, 30.0, 45.0]
LEVELS_AUDIO = [-2.6, -2.1, -1.6, -1.1, -0.7, -0.3]
H_TARG_DEFAULT = 2.0
L_TARG_DEFAULT = 0.5
AUDIO_SHIFT = 2.7


# ============================================================================================
# ============================================================================================

def lab_to_rgb(lab):
    L, a, b = float(lab[0]), float(lab[1]), float(lab[2])
    fy = (L + 16.0) / 116.0
    fx = fy + a / 500.0
    fz = fy - b / 200.0
    eps = 216.0 / 24389.0
    kap = 24389.0 / 27.0

    def finv(t):
        if t ** 3 > eps:
            return t ** 3
        return (116.0 * t - 16.0) / kap

    X = 0.95047 * finv(fx)
    if L > kap * eps:
        Y = ((L + 16.0) / 116.0) ** 3
    else:
        Y = L / kap
    Z = 1.08883 * finv(fz)
    r = 3.2404542 * X - 1.5371385 * Y - 0.4985314 * Z
    g = -0.9692660 * X + 1.8760108 * Y + 0.0415560 * Z
    bb = 0.0556434 * X - 0.2040259 * Y + 1.0572252 * Z

    def gamma(c):
        if c <= 0.0031308:
            return 12.92 * c
        return 1.055 * c ** (1 / 2.4) - 0.055

    return np.array([gamma(r), gamma(g), gamma(bb)])


def is_in_gamut(lab):
    rgb = lab_to_rgb(lab)
    return bool(np.all(rgb >= 0.0) and np.all(rgb <= 1.0))


def lab_to_hex(lab):
    rgb = np.clip(lab_to_rgb(lab), 0, 1)
    r, g, b = [int(v * 255) for v in rgb]
    return "#{:02X}{:02X}{:02X}".format(r, g, b)


def delta_e(c1, c2):
    """colorpool.py:7-8: CIELAB Euclidean distance (ΔE76)."""
    diff = np.asarray(c1, float) - np.asarray(c2, float)
    return float(np.sqrt(np.sum(diff ** 2)))


def random_lab(rng):
    """colorpool.py:18-22: L 40–60, chroma 40–60, any hue."""
    L = rng.uniform(40, 60)
    C = rng.uniform(40, 60)
    h = rng.uniform(0, 2 * np.pi)
    return np.array([L, C * np.cos(h), C * np.sin(h)])


def random_target(rng, avoid=(), min_sep=20.0, max_tries=500):
    """Draw an in-gamut target colour at least min_sep away from every colour in avoid."""
    for _ in range(max_tries):
        c = random_lab(rng)
        if is_in_gamut(c) and all(delta_e(c, other) >= min_sep for other in avoid):
            return c
    raise RuntimeError("no in-gamut target colour found")


def find_colour_at(target, de, rng, tol=0.5, max_tries=2000):
    """An in-gamut colour de (±tol) away from the target in a random direction; returns None if none is found."""
    for _ in range(max_tries):
        direction = rng.standard_normal(3)
        direction = direction / np.linalg.norm(direction)
        cand = np.asarray(target, float) + direction * de
        if is_in_gamut(cand) and abs(delta_e(target, cand) - de) <= tol:
            return cand
    return None


# ============================================================================================
# ============================================================================================

def load_confusion(path=None):
    """Read CONFUSION_DATA from generate_trials.py (without importing it, since it imports pandas). Returns {consonant: [(foil, count), …]}."""
    path = path or os.path.join(HERE, "generate_trials.py")
    src = open(path, encoding="utf-8").read()
    m = re.search(r"CONFUSION_DATA\s*=\s*(\[.*?\n\])", src, re.S)
    table = {}
    for row in ast.literal_eval(m.group(1)):
        table.setdefault(row["sound"], []).append((row["target"], int(row["count"])))
    return table


def audio_x(count):
    """Confusion count → dissimilarity axis. count 1 → −0.3; count 451 → −2.66. Larger = easier to discriminate."""
    return -np.log10(float(count) + 1.0)


def count_from_x(x):
    return 10.0 ** (-float(x)) - 1.0


def sound_file(talker, cons):
    return "stimuli/{}_{}3.wav".format(talker, cons)


def foil_for(confusion, cons, x):
    """Among the foils of target consonant cons, the one whose dissimilarity is closest to x. Returns (foil, count)."""
    cands = confusion[cons]
    dist = [abs(audio_x(count) - x) for _, count in cands]
    return cands[int(np.argmin(dist))]


# ============================================================================================
# ============================================================================================

def make_colour_trial(rng, x, is_match, sounds):
    """One block-1 trial: two target colours (>= 20 apart) and two target sounds (different consonants, random talkers); the probe is one target's colour ± x with that target's own sound (probe colour = target colour when is_match)."""
    t1 = random_target(rng)
    t2 = random_target(rng, avoid=[t1])
    which = int(rng.integers(2))
    target = [t1, t2][which]
    s1, s2 = rng.choice(sounds, 2, replace=False)
    k1, k2 = rng.choice(TALKERS, 2)
    if is_match:
        probe = target
    else:
        probe = find_colour_at(target, x, rng)
        if probe is None:
            target = random_target(rng)
            probe = find_colour_at(target, x, rng)
            if probe is None:
                probe = target
    return dict(color1_target=lab_to_hex(t1), color2_target=lab_to_hex(t2),
                audio1_target_file=sound_file(k1, s1), audio2_target_file=sound_file(k2, s2),
                probe_colour=lab_to_hex(probe), probe_sound=sound_file([k1, k2][which], [s1, s2][which]),
                probe_of=which + 1, is_match=is_match, x=delta_e(target, probe))


def make_audio_trial(rng, x, is_match, confusion):
    """One block-2 trial: two target colours and two target sounds; the probe is one target's colour with its foil consonant (same talker), the foil snapped from x to that consonant's available foils; the returned x is the snapped value."""
    sounds = sorted(confusion)
    t1 = random_target(rng)
    t2 = random_target(rng, avoid=[t1])
    s1, s2 = rng.choice(sounds, 2, replace=False)
    k1, k2 = rng.choice(TALKERS, 2)
    which = int(rng.integers(2))
    target_sound = [s1, s2][which]
    talker = [k1, k2][which]
    if is_match:
        foil, count, x_actual = target_sound, 0, 0.0
    else:
        foil, count = foil_for(confusion, target_sound, x)
        x_actual = audio_x(count)
    return dict(color1_target=lab_to_hex(t1), color2_target=lab_to_hex(t2),
                audio1_target_file=sound_file(k1, s1), audio2_target_file=sound_file(k2, s2),
                probe_colour=lab_to_hex([t1, t2][which]), probe_sound=sound_file(talker, foil),
                probe_of=which + 1, is_match=is_match, foil=foil, count=count, x=x_actual)


def make_trial(dim, rng, x, is_match, confusion):
    if dim == "colour":
        return make_colour_trial(rng, x, is_match, sorted(confusion))
    return make_audio_trial(rng, x, is_match, confusion)


def score(trial, key):
    """key: 'y' = same, 'n' = different, None = no response. Returns (r, correct); both None when there is no response."""
    if key not in ("y", "n", None):
        raise ValueError("key must be 'y' / 'n' / None")
    if key is None:
        return None, None
    r = 1 if key == "n" else 0
    if trial["is_match"]:
        correct = 1 if key == "y" else 0
    else:
        correct = 1 if key == "n" else 0
    return r, correct


def false_alarm_rate(log, fallback):
    """Proportion of 'different' responses on AA trials; uses fallback when there are fewer than 5 AA trials."""
    aa = [t["r"] for t in log if t["is_match"] and t["r"] is not None]
    if len(aa) < 5:
        return fallback
    return float(np.mean(aa))


def to_model_units(dim, x):
    """Scale before the lnrm fit: colour ΔE/10, sound shifted to >= 0, so α and α₂ land on the scale of the lnrm2.stan priors and the inverse solution avoids negative roots."""
    if dim == "colour":
        return x / 10.0
    return x + AUDIO_SHIFT


def from_model_units(dim, u):
    if dim == "colour":
        return u * 10.0
    return u - AUDIO_SHIFT


def make_result(dim, log, fa, alpha, beta, high, low, target_high, target_low, x_range, warnings, extra):
    """Calibration result: a plain dict, written straight to json."""
    in_range = bool(np.isfinite(high) and np.isfinite(low)
                    and x_range[0] <= high <= x_range[1] and x_range[0] <= low <= x_range[1])
    if not in_range:
        warnings = warnings + ["H={:.3f} / L={:.3f} is outside the range [{}, {}]".format(high, low, x_range[0], x_range[1])]
    result = dict(dim=dim, n_trials=len(log), n_match=sum(t["is_match"] for t in log), false_alarm=fa,
                  alpha=alpha, beta=beta, high=high, low=low, p_high=target_high, p_low=target_low,
                  x_range=list(x_range), in_range=in_range, warnings=warnings, extra=dict(extra))
    if dim == "audio":
        result["extra"]["count_high"] = count_from_x(high)
        result["extra"]["count_low"] = count_from_x(low)
    return result


# ============================================================================================
# ============================================================================================

class PsiCalibrator:
    """
    Psi calibrator: picks x trial by trial by minimum entropy, using accuracy only; the targets are the probabilities p_high / p_low of answering 'different'.

        cal = PsiCalibrator("colour", p_high=0.90, p_low=0.75, seed=1)
        for _ in range(72):
            trial = cal.next_trial()          # dict: colours to draw, wav to play, is_match ...
            key, rt = ...                     # the participant presses y / n, with seconds
            cal.record(key, rt)
        result = cal.finish()                 # dict: high / low / false_alarm / alpha / beta ...
    """

    def __init__(self, dim, p_high=0.90, p_low=0.75, p_match=1 / 3, floor_guess=0.10, lapse=0.02, seed=None,
                 x=None, a=None, b=None, confusion=None):
        if dim == "colour":
            grids = dict(x=(2.0, 50.0, 1.0), a=(0.0, 45.0, 1.0), b=(1.0, 25.0, 1.0))
        elif dim == "audio":
            grids = dict(x=(-2.7, 0.0, 0.05), a=(-2.7, 0.0, 0.05), b=(0.05, 2.0, 0.05))
        else:
            raise ValueError("dim must be 'colour' or 'audio'")
        self.dim = dim
        self.psi = Psi(x or grids["x"], a or grids["a"], b or grids["b"], d=lapse, lower=floor_guess, upper=lapse / 2)
        self.p_high, self.p_low, self.p_match = p_high, p_low, p_match
        self.floor_guess = floor_guess
        self.confusion = confusion or load_confusion()
        self.rng = np.random.default_rng(seed)
        self.log = []
        self.current = None

    def next_trial(self):
        is_match = self.rng.uniform() < self.p_match
        x = float(self.psi.next_intensity)
        trial = make_trial(self.dim, self.rng, x, is_match, self.confusion)
        trial["trial_no"] = len(self.log) + 1
        trial["x_psi"] = x
        trial["x_index"] = self.psi.nearest_index(trial["x"])
        self.current = trial
        return trial

    def record(self, key, rt):
        trial = self.current
        if trial is None:
            raise RuntimeError("call next_trial() first")
        r, correct = score(trial, key)
        if r is not None and not trial["is_match"]:
            self.psi.update_at(trial["x_index"], r)
        trial.update(key=key, rt=rt, r=r, correct=correct)
        self.log.append(trial)
        self.current = None
        return r, correct

    def finish(self):
        alpha, beta = self.psi.estimate()
        fa = false_alarm_rate(self.log, self.floor_guess)
        x_range = (float(self.psi.x.min()), float(self.psi.x.max()))
        (high, low), warnings = salience_levels(alpha, beta, self.psi.d, [self.p_high, self.p_low],
                                                x_range=x_range, lower=fa, upper=self.psi.upper)
        return make_result(self.dim, self.log, fa, alpha, beta, high, low, self.p_high, self.p_low, x_range,
                           list(warnings), dict(method="psi"))


# ============================================================================================
# ============================================================================================

class LNRMCalibrator:
    """
    Same usage as PsiCalibrator, but x is fixed at a few levels with n_per_level trials each (shuffled), and finish() fits lnrm2 (PyMC, 20–40 s) and solves for the drift-separation targets h_targ / l_targ.

        cal = LNRMCalibrator("colour", h_targ=2.0, l_targ=0.5, seed=1)
        for _ in range(cal.n_trials):
            ...
    """

    def __init__(self, dim, levels=None, n_per_level=8, p_match=1 / 3, h_targ=H_TARG_DEFAULT, l_targ=L_TARG_DEFAULT,
                 link="quadratic", seed=None, rt_min=0.15, rt_max=3.0, floor_guess=0.10, alpha2_rule="filter",
                 confusion=None, **fit_kwargs):
        if dim not in ("colour", "audio"):
            raise ValueError("dim must be 'colour' or 'audio'")
        if levels is None:
            levels = LEVELS_COLOUR if dim == "colour" else LEVELS_AUDIO
        self.dim = dim
        self.levels = [float(v) for v in levels]
        self.h_targ, self.l_targ, self.link = h_targ, l_targ, link
        self.p_match = p_match
        self.rt_min, self.rt_max = rt_min, rt_max
        self.floor_guess = floor_guess
        self.alpha2_rule = alpha2_rule
        self.fit_kwargs = fit_kwargs
        self.confusion = confusion or load_confusion()
        self.rng = np.random.default_rng(seed)
        self.log = []
        self.current = None
        n_diff = len(self.levels) * n_per_level
        n_match = int(round(n_diff * p_match / (1 - p_match)))
        plan = []
        for x in self.levels:
            plan += [x] * n_per_level
        plan += [None] * n_match
        self.rng.shuffle(plan)
        self.plan = plan
        self.n_trials = len(plan)

    def next_trial(self):
        if len(self.log) >= self.n_trials:
            raise StopIteration
        x = self.plan[len(self.log)]
        is_match = x is None
        trial = make_trial(self.dim, self.rng, 0.0 if is_match else x, is_match, self.confusion)
        trial["trial_no"] = len(self.log) + 1
        trial["x_planned"] = x
        self.current = trial
        return trial

    def record(self, key, rt):
        trial = self.current
        if trial is None:
            raise RuntimeError("call next_trial() first")
        r, correct = score(trial, key)
        trial.update(key=key, rt=rt, r=r, correct=correct)
        self.log.append(trial)
        self.current = None
        return r, correct

    def finish(self):
        load_full_package()
        from adaptivesft.models import make_data
        from adaptivesft.models_v2 import fit_lnrm_v2 as fit_lnrm   # PyMC built-in LogNormal logp/logcdf version (DECISIONS 14)
        from adaptivesft.salience import find_salience

        rows = []
        for t in self.log:
            if t["is_match"] or t["r"] is None or t["rt"] is None:
                continue
            if self.rt_min <= t["rt"] <= self.rt_max:
                rows.append(t)
        if len(rows) < 10:
            raise RuntimeError("only {} usable 'different' trials; cannot fit".format(len(rows)))
        intensity = [to_model_units(self.dim, t["x"]) for t in rows]
        data = make_data(intensity, [t["rt"] for t in rows], [t["correct"] for t in rows])

        trace = fit_lnrm(data, link=self.link, **self.fit_kwargs)
        if self.link == "quadratic":
            res = find_salience(trace, h_targ=self.h_targ, l_targ=self.l_targ, alpha2_rule=self.alpha2_rule)
        else:
            res = find_salience(trace, h_targ=self.h_targ, l_targ=self.l_targ)
        high = from_model_units(self.dim, res["high"]["intensity"])
        low = from_model_units(self.dim, res["low"]["intensity"])

        params = {}
        for name in trace.posterior.data_vars:
            if name != "log_likelihood":
                params[name] = float(trace.posterior[name].values.mean())
        n_diff = sum(1 for t in self.log if not t["is_match"])
        extra = dict(method="lnrm_" + self.link, targets="drift separation (z2 - z1)", params=params,
                     implied_acc_high=res["high"].get("implied_accuracy"), implied_acc_low=res["low"].get("implied_accuracy"),
                     high_median=from_model_units(self.dim, res["high"]["median"]),
                     low_median=from_model_units(self.dim, res["low"]["median"]),
                     n_used=len(rows), n_trimmed=n_diff - len(rows),
                     divergences=int(trace.sample_stats["diverging"].sum()),
                     alpha2_rule=self.alpha2_rule, levels=self.levels)
        self.trace = trace
        fa = false_alarm_rate(self.log, self.floor_guess)
        x_range = (min(self.levels), max(self.levels))
        return make_result(self.dim, self.log, fa, params.get("alpha", float("nan")), params.get("alpha2", float("nan")),
                           high, low, self.h_targ, self.l_targ, x_range, list(res["warnings"]), extra)


# ============================================================================================
# ============================================================================================

def save_calibration(path, colour, audio, info=None):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dict(info=info or {}, colour=colour, audio=audio), f, ensure_ascii=False, indent=2)


def read_calibration(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def foil_near_count(confusion, cons, count):
    """Among the foils of target consonant cons, the one whose confusion count (log scale) is closest to count."""
    cands = confusion[cons]
    dist = [abs(np.log10(c + 1) - np.log10(count + 1)) for _, c in cands]
    return cands[int(np.argmin(dist))]


def pick_two_targets_with_foils(rng, de_h, de_l, prev, min_target_sep, min_hl_sep):
    """Draw two target colours and their H / L foils (ΔE_H / ΔE_L ± 0.5, all in gamut). Returns (t1, h1, l1, t2, h2, l2)."""
    for _ in range(200):
        t1 = random_target(rng, avoid=prev, min_sep=30.0)
        t2 = random_target(rng, avoid=[t1] + prev, min_sep=min_target_sep)
        h1 = find_colour_at(t1, de_h, rng)
        l1 = find_colour_at(t1, de_l, rng)
        h2 = find_colour_at(t2, de_h, rng)
        l2 = find_colour_at(t2, de_l, rng)
        if h1 is None or l1 is None or h2 is None or l2 is None:
            continue
        if delta_e(h1, l1) < min_hl_sep or delta_e(h2, l2) < min_hl_sep:
            continue
        return t1, h1, l1, t2, h2, l2
    raise RuntimeError("no in-gamut colours found at ΔE_H / ΔE_L; the calibrated ΔE is too large or too small")


def write_blocks(calib, out_dir, n_blocks=6, trials_per_block=24, seed=None, min_target_sep=20.0, min_hl_sep=0.0):
    """Generate stimuli/block1..6.csv (columns = CSV_COLUMNS) from a calibration result (the dict read back by read_calibration)."""
    rng = np.random.default_rng(seed)
    confusion = load_confusion()
    sounds = sorted(confusion)
    de_h = float(calib["colour"]["high"])
    de_l = float(calib["colour"]["low"])
    count_h = float(calib["audio"]["extra"]["count_high"])
    count_l = float(calib["audio"]["extra"]["count_low"])

    os.makedirs(out_dir, exist_ok=True)
    paths = []
    prev = []
    for b in range(1, n_blocks + 1):
        rows = []
        for t in range(1, trials_per_block + 1):
            t1, h1, l1, t2, h2, l2 = pick_two_targets_with_foils(rng, de_h, de_l, prev, min_target_sep, min_hl_sep)
            prev = [t1, t2]
            s1, s2 = rng.choice(sounds, 2, replace=False)
            k1, k2 = rng.choice(TALKERS, 2)
            h1s, h1c = foil_near_count(confusion, s1, count_h)
            l1s, l1c = foil_near_count(confusion, s1, count_l)
            h2s, h2c = foil_near_count(confusion, s2, count_h)
            l2s, l2c = foil_near_count(confusion, s2, count_l)
            rows.append(dict(
                trial=t,
                color1_target=lab_to_hex(t1), color1_H=lab_to_hex(h1), color1_L=lab_to_hex(l1),
                color1_H_deltaE=round(delta_e(t1, h1), 2), color1_L_deltaE=round(delta_e(t1, l1), 2),
                color1_HL_deltaE=round(delta_e(h1, l1), 2),
                color2_target=lab_to_hex(t2), color2_H=lab_to_hex(h2), color2_L=lab_to_hex(l2),
                color2_H_deltaE=round(delta_e(t2, h2), 2), color2_L_deltaE=round(delta_e(t2, l2), 2),
                color2_HL_deltaE=round(delta_e(h2, l2), 2),
                audio1_target=s1, audio1_H=h1s, audio1_L=l1s, audio1_H_count=h1c, audio1_L_count=l1c,
                audio1_target_talker=k1, audio1_H_talker=k1, audio1_L_talker=k1,
                audio1_target_file=sound_file(k1, s1), audio1_H_file=sound_file(k1, h1s), audio1_L_file=sound_file(k1, l1s),
                audio2_target=s2, audio2_H=h2s, audio2_L=l2s, audio2_H_count=h2c, audio2_L_count=l2c,
                audio2_target_talker=k2, audio2_H_talker=k2, audio2_L_talker=k2,
                audio2_target_file=sound_file(k2, s2), audio2_H_file=sound_file(k2, h2s), audio2_L_file=sound_file(k2, l2s),
            ))
        path = os.path.join(out_dir, "block{}.csv".format(b))
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
            w.writeheader()
            w.writerows(rows)
        paths.append(path)
    return paths


# ============================================================================================
# ============================================================================================

#   AA=0,1  HA=2,3  LA=4,5  AH=6,7  HH=8,9  LH=10,11  AL=12,13  HL=14,15  LL=16,17
COND_TO_CELL = {8: (2, 2), 9: (2, 2), 14: (2, 1), 15: (2, 1), 10: (1, 2), 11: (1, 2), 16: (1, 1), 17: (1, 1)}
COND_MATCH = (0, 1)


def vawm_to_dfp_rows(path, subject=None, rt_col="ResponseBox.rt", key_col="ResponseBox.keys", cond_col="condition"):
    """Read the csv saved by VAWM_nobox.py (one row per probe) into the rows adaptivesft.experiment.analyze_participant expects; returns (dfp_rows, other_rows), the former HH / HL / LH / LL, the latter AA and single-channel trials."""
    dfp_rows, other_rows = [], []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            try:
                cond = int(float(r[cond_col]))
            except (KeyError, TypeError, ValueError):
                continue
            key = (r.get(key_col) or "").strip()
            try:
                rt = float(r[rt_col])
            except (KeyError, TypeError, ValueError):
                rt = None
            if key not in ("y", "n"):
                correct = None
            elif cond in COND_MATCH:
                correct = 1 if key == "y" else 0
            else:
                correct = 1 if key == "n" else 0
            rec = dict(subject=subject or r.get("participant", ""), condition="DFP", cond_code=cond, key=key,
                       correct=correct, rt=rt)
            if cond in COND_TO_CELL:
                rec["channel1"], rec["channel2"] = COND_TO_CELL[cond]
                rec["block"] = r.get("block1.thisN", r.get("block", ""))
                rec["trial"] = len(dfp_rows) + 1
                dfp_rows.append(rec)
            else:
                other_rows.append(rec)
    return dfp_rows, other_rows


def analyze_vawm(path, subject=None, **kw):
    """VAWM_nobox.py csv → correct RTs in the four cells → SIC / MIC / dominance → inferred architecture (via adaptivesft.experiment)."""
    experiment = load_full_package()
    dfp_rows, other_rows = vawm_to_dfp_rows(path, subject)
    for r in dfp_rows:
        if r["correct"] is None:
            r["correct"] = ""
        if r["rt"] is None:
            r["rt"] = ""
    res = experiment.analyze_participant(dfp_rows, **kw)
    acc_other = {}
    for r in other_rows:
        if r["correct"] is not None:
            acc_other.setdefault(r["cond_code"], []).append(r["correct"])
    acc_other = {c: float(np.mean(v)) for c, v in sorted(acc_other.items())}
    return dict(result=res, report=experiment.report(res), n_dfp=len(dfp_rows), accuracy_other=acc_other)
