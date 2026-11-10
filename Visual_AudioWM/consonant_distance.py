"""Perceptual distance between any two of the 16 Miller & Nicely (1955) English consonants.

Intended as the "sound dissimilarity" axis of the audiovisual working-memory experiment
(see adaptive_vawm_EN.py: audio_x / foil_for / LEVELS_AUDIO). Imports only numpy and the
standard library, so PsychoPy's bundled Python can use it; scipy is never required.

Consonant codes (ASCII, same as adaptive_vawm_EN.MN_FEATURES and the stimulus files):

    p t k f theta s sh b d g v eth z zh m n
    p t k f  θ    s ʃ  b d g v  ð  z ʒ  m n

Data: review/data/miller_nicely_1955_tables_I-VI.json — the six 16x16 confusion matrices
for S/N = -18, -12, -6, 0, +6, +12 dB (200-6500 cps band), rows = spoken, cols = heard,
~250 presentations per row, 4000 per table.

Five metrics, each a symmetric 16x16 matrix with zero diagonal (larger = more different); the default
metric of distance() / foil_nearest() is "luce" (see review/consonant_distance_how.md for why):

  "hamming"    Number of Miller-Nicely articulatory features on which a and b differ
               (voicing, nasality, affrication, duration, place), 0-5. Place is three-valued
               (front/middle/back) but counts as 1 whenever it differs. Baseline.

  "weighted"   Same count, but each differing feature f is weighted by how robustly that
               feature survives noise, measured as the relative information transmitted
               about it in the Miller-Nicely covariance analysis (their Table XXI):

                   T(f)      = I(spoken feature ; heard feature)
                             = Σᵢⱼ pᵢⱼ · log₂( pᵢⱼ / (pᵢ· · p·ⱼ) )
                   H(f)      = − Σᵢ pᵢ· · log₂ pᵢ·            (entropy of the spoken feature)
                   T_rel(f)  = T(f) / H(f)                     ∈ [0, 1]

               where pᵢⱼ is the proportion of trials with spoken feature value i and heard
               feature value j, obtained by collapsing the 16x16 matrix onto the feature's
               2 (or 3, for place) values. The weight is T_rel averaged over a set of SNRs
               (default -12, -6, 0, +6 dB; -18 is pure guessing and +12 is near ceiling):

                   d_weighted(a, b) = Σ_f  T_rel(f) · [ f(a) ≠ f(b) ]

               Voicing and nasality get the largest weights, place the smallest, so a
               voicing-only pair (p-b) is "further apart" than a place-only pair (p-k).

  "confusion"  Empirical distance from the matrices. For each SNR,

                   r_ab = (n_ab + n_ba) / (N_a + N_b)        symmetric confusion rate
                   d_ab = − ln( r_ab + ε ),   ε = 0.5 / (N_a + N_b)

               i.e. a half-count continuity correction, so an unobserved confusion
               (n_ab = n_ba = 0) maps to the finite value −ln(0.5/500) ≈ 6.9 instead of ∞.
               The default averages d over -12, -6 and 0 dB: at -18 dB responses are nearly
               uniform (0.06 bits transmitted; all pairs look equally confusable), while at
               +6/+12 dB most off-diagonal cells are empty (175 and 199 of 240 are zero), so
               distances there saturate at the ε floor. Single-SNR versions are available via
               confusion_distance(snrs=(x,)).

  "mds"        Shepard-style multidimensional scaling. Counts are pooled over the same SNR
               set as "confusion", the similarity is

                   s_ab = (n_ab + n_ba) / (n_aa + n_bb)                      (Shepard 1972)

               converted to a distance d_ab = −ln(s_ab) (same half-count floor), and classical
               (Torgerson) MDS is run on d. The metric is the Euclidean distance in the first
               k dimensions (default k = 3). mds_fit() reports the Pearson correlation between
               the fitted and input distances, Kruskal's stress-1, and how strongly each
               dimension correlates with each articulatory feature.

  "luce"       Similarity-choice (biased-choice) model, Luce (1963) / Shepard (1957):

                   P(respond j | stimulus i) = b_j · η_ij / Σ_k b_k · η_ik ,   η_ii = 1, η_ij = η_ji

               η is the pairwise similarity, b the response bias; the model separates the two,
               which the raw confusion rate cannot. Per SNR the 120 η and 15 free biases are
               fitted by maximum likelihood (multinomial likelihood of the 16 rows; gradient
               ascent from the closed-form start). The closed-form estimate

                   η_ij ≈ √( p_ij · p_ji / (p_ii · p_jj) )

               (Shepard 1957; Luce 1963) is also available (luce_closed_form). Both use the
               usual +0.5 added to every cell, so empty cells give a finite η. The distance is
               Shepard's (1987) exponential law inverted, d_ij = −ln η_ij, averaged over the
               same default SNR set as "confusion" (-12, -6, 0 dB). At +6/+12 dB most
               off-diagonal cells are 0 and η is dominated by the smoothing constant; see the
               per-SNR report in the summary.

Self-check / report:  python consonant_distance.py
writes review/data/consonant_distance_all_pairs.csv and review/data/consonant_distance_summary.txt
and prints the summary.
"""
import ast
import csv
import itertools
import json
import os
import re

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TABLES_JSON = os.path.join(HERE, "review", "data", "miller_nicely_1955_tables_I-VI.json")
CONFUSION_PY = os.path.join(HERE, "generate_trials.py")
OUT_CSV = os.path.join(HERE, "review", "data", "consonant_distance_all_pairs.csv")
OUT_TXT = os.path.join(HERE, "review", "data", "consonant_distance_summary.txt")

CONSONANTS = ["p", "t", "k", "f", "theta", "s", "sh", "b", "d", "g", "v", "eth", "z", "zh", "m", "n"]
IPA = {"p": "p", "t": "t", "k": "k", "f": "f", "theta": "θ", "s": "s", "sh": "ʃ", "b": "b", "d": "d", "g": "g",
       "v": "v", "eth": "ð", "z": "z", "zh": "ʒ", "m": "m", "n": "n"}
INDEX = {c: i for i, c in enumerate(CONSONANTS)}

# Miller & Nicely (1955) Table XIX: voicing, nasality, affrication, duration, place (0 front, 1 middle, 2 back).
FEATURE_NAMES = ("voicing", "nasality", "affrication", "duration", "place")
FEATURES = {"p": (0, 0, 0, 0, 0), "t": (0, 0, 0, 0, 1), "k": (0, 0, 0, 0, 2), "f": (0, 0, 1, 0, 0),
            "theta": (0, 0, 1, 0, 1), "s": (0, 0, 1, 1, 1), "sh": (0, 0, 1, 1, 2),
            "b": (1, 0, 0, 0, 0), "d": (1, 0, 0, 0, 1), "g": (1, 0, 0, 0, 2), "v": (1, 0, 1, 0, 0),
            "eth": (1, 0, 1, 0, 1), "z": (1, 0, 1, 1, 1), "zh": (1, 0, 1, 1, 2),
            "m": (1, 1, 0, 0, 0), "n": (1, 1, 0, 0, 1)}
FEATURE_ARRAY = np.array([FEATURES[c] for c in CONSONANTS])          # 16 x 5

SNRS = (-18, -12, -6, 0, 6, 12)
DEFAULT_SNRS_WEIGHT = (-12, -6, 0, 6)
DEFAULT_SNRS_CONFUSION = (-12, -6, 0)
DEFAULT_MDS_DIMS = 3
METRICS = ("hamming", "weighted", "confusion", "mds", "luce")

# Table XXI of the paper (bits per stimulus, conditions 1-6 = the 200-6500 cps band) for cross-checking the
# recomputation. Last row = maximum possible = H(feature) with the 16 syllables equiprobable.
PAPER_TABLE_XXI = {-18: (0.061, 0.021, 0.008, 0.000, 0.001, 0.001),
                   -12: (0.959, 0.516, 0.264, 0.069, 0.087, 0.058),
                   -6: (1.834, 0.797, 0.397, 0.279, 0.249, 0.249),
                   0: (2.797, 0.944, 0.495, 0.620, 0.483, 0.578),
                   6: (3.226, 0.951, 0.543, 0.782, 0.636, 0.856),
                   12: (3.546, 0.956, 0.555, 0.853, 0.751, 1.090),
                   "max": (4.000, 0.989, 0.544, 1.000, 0.811, 1.546)}


# ------------------------------------------------------------------------------------------------ data

def load_tables(path=TABLES_JSON):
    """{snr: 16x16 float array}, rows = spoken, cols = heard, in CONSONANTS order."""
    with open(path, encoding="utf-8") as fh:
        raw = json.load(fh)
    assert list(raw["order"]) == CONSONANTS, "consonant order in the json differs from CONSONANTS"
    out = {}
    for key, table in raw["tables"].items():
        m = np.zeros((16, 16))
        for a in CONSONANTS:
            for b in CONSONANTS:
                m[INDEX[a], INDEX[b]] = table[a].get(b, 0)
        out[int(key)] = m
    return out


_TABLES = None


def tables():
    global _TABLES
    if _TABLES is None:
        _TABLES = load_tables()
    return _TABLES


def pairs():
    """The 120 unordered pairs, in CONSONANTS order."""
    return list(itertools.combinations(CONSONANTS, 2))


# ------------------------------------------------------------------------------------------------ feature transmission

def mutual_information_bits(joint):
    """T(x;y) and H(x) in bits from a joint count table (rows = x, cols = y)."""
    p = joint / joint.sum()
    px = p.sum(axis=1, keepdims=True)
    py = p.sum(axis=0, keepdims=True)
    nz = p > 0
    t = float(np.sum(p[nz] * np.log2(p[nz] / (px @ py)[nz])))
    hx = float(-np.sum(px[px > 0] * np.log2(px[px > 0])))
    return t, hx


def feature_transmission(snr):
    """{feature: (T bits, H bits, T_rel)} for one SNR, plus 'all' for the full 16x16 channel."""
    m = tables()[snr]
    out = {}
    t_all, h_all = mutual_information_bits(m)
    out["all"] = (t_all, h_all, t_all / h_all)
    for k, name in enumerate(FEATURE_NAMES):
        vals = FEATURE_ARRAY[:, k]
        nv = int(vals.max()) + 1
        joint = np.zeros((nv, nv))
        for i in range(nv):
            for j in range(nv):
                joint[i, j] = m[np.ix_(vals == i, vals == j)].sum()
        t, h = mutual_information_bits(joint)
        out[name] = (t, h, t / h)
    return out


def feature_weights(snrs=DEFAULT_SNRS_WEIGHT):
    """{feature: mean T_rel over snrs} — the weights of the 'weighted' metric."""
    acc = {name: [] for name in FEATURE_NAMES}
    for snr in snrs:
        tr = feature_transmission(snr)
        for name in FEATURE_NAMES:
            acc[name].append(tr[name][2])
    return {name: float(np.mean(v)) for name, v in acc.items()}


# ------------------------------------------------------------------------------------------------ metrics

def _differs():
    """16x16x5 boolean: feature k differs between a and b."""
    return FEATURE_ARRAY[:, None, :] != FEATURE_ARRAY[None, :, :]


def hamming_matrix():
    return _differs().sum(axis=2).astype(float)


def weighted_matrix(weights=None, snrs=DEFAULT_SNRS_WEIGHT):
    w = weights or feature_weights(snrs)
    wv = np.array([w[name] for name in FEATURE_NAMES])
    return (_differs() * wv).sum(axis=2)


def confusion_rate(snr):
    """Symmetric confusion rate r_ab = (n_ab + n_ba) / (N_a + N_b) at one SNR (diagonal = 0)."""
    m = tables()[snr]
    n_row = m.sum(axis=1)
    r = (m + m.T) / (n_row[:, None] + n_row[None, :])
    np.fill_diagonal(r, 0.0)
    return r


def confusion_distance(snrs=DEFAULT_SNRS_CONFUSION, eps=None):
    """Mean over snrs of −ln(r_ab + ε); ε defaults to the half-count floor 0.5 / (N_a + N_b)."""
    acc = np.zeros((16, 16))
    for snr in snrs:
        m = tables()[snr]
        n_row = m.sum(axis=1)
        e = eps if eps is not None else 0.5 / (n_row[:, None] + n_row[None, :])
        acc += -np.log(confusion_rate(snr) + e)
    d = acc / len(snrs)
    np.fill_diagonal(d, 0.0)
    return d


def shepard_similarity(snrs=DEFAULT_SNRS_CONFUSION):
    """s_ab = (n_ab + n_ba) / (n_aa + n_bb) on counts pooled over snrs (Shepard 1972); diagonal = 1."""
    m = sum(tables()[s] for s in snrs)
    diag = np.diag(m)
    s = (m + m.T) / (diag[:, None] + diag[None, :])
    np.fill_diagonal(s, 1.0)
    return s


def classical_mds(d, ndim):
    """Torgerson MDS: coordinates (16 x ndim) and the eigenvalues of the double-centred matrix."""
    n = d.shape[0]
    j = np.eye(n) - np.ones((n, n)) / n
    b = -0.5 * j @ (d ** 2) @ j
    vals, vecs = np.linalg.eigh(b)
    order = np.argsort(vals)[::-1]
    vals, vecs = vals[order], vecs[:, order]
    pos = np.clip(vals[:ndim], 0, None)
    coords = vecs[:, :ndim] * np.sqrt(pos)
    # sign convention: orient each axis so that it correlates positively with the best-matching feature
    for k in range(ndim):
        c = coords[:, k]
        corrs = [np.corrcoef(c, FEATURE_ARRAY[:, f])[0, 1] for f in range(5)]
        best = int(np.argmax(np.abs(corrs)))
        if corrs[best] < 0:
            coords[:, k] = -c
    return coords, vals


def mds_input_distance(snrs=DEFAULT_SNRS_CONFUSION):
    """−ln(s_ab) with the half-count floor, the input to classical MDS."""
    m = sum(tables()[s] for s in snrs)
    diag = np.diag(m)
    s = shepard_similarity(snrs)
    floor = 0.5 / (diag[:, None] + diag[None, :])
    d = -np.log(np.maximum(s, floor))
    np.fill_diagonal(d, 0.0)
    return d


def mds_fit(ndim=DEFAULT_MDS_DIMS, snrs=DEFAULT_SNRS_CONFUSION):
    """Run MDS; returns dict(distance, coords, eigenvalues, r_fit, stress1, alignment, input)."""
    d_in = mds_input_distance(snrs)
    coords, vals = classical_mds(d_in, ndim)
    diff = coords[:, None, :] - coords[None, :, :]
    d_fit = np.sqrt((diff ** 2).sum(axis=2))
    iu = np.triu_indices(16, 1)
    x, y = d_in[iu], d_fit[iu]
    r_fit = float(np.corrcoef(x, y)[0, 1])
    stress1 = float(np.sqrt(((x - y) ** 2).sum() / (x ** 2).sum()))
    alignment = np.array([[abs(np.corrcoef(coords[:, k], FEATURE_ARRAY[:, f])[0, 1]) for f in range(5)]
                          for k in range(ndim)])
    return dict(distance=d_fit, coords=coords, eigenvalues=vals, r_fit=r_fit, stress1=stress1,
                alignment=alignment, input=d_in)


def mds_matrix(ndim=DEFAULT_MDS_DIMS, snrs=DEFAULT_SNRS_CONFUSION):
    return mds_fit(ndim, snrs)["distance"]


# ------------------------------------------------------------------------------------------------ similarity-choice model

def _smoothed(snr, add=0.5):
    return tables()[snr] + add


def luce_closed_form(snr, add=0.5):
    """Closed-form η_ij = sqrt(p_ij p_ji / (p_ii p_jj)) (Shepard 1957 / Luce 1963) on +add-smoothed counts."""
    m = _smoothed(snr, add)
    p = m / m.sum(axis=1, keepdims=True)
    d = np.diag(p)
    eta = np.sqrt(p * p.T / (d[:, None] * d[None, :]))
    np.fill_diagonal(eta, 1.0)
    return eta


def luce_fit(snr, add=0.5, iters=4000, lr=0.05, tol=1e-4):
    """Maximum-likelihood similarity-choice model for one SNR.

    Parameters: log η_ij for the 120 unordered pairs (η_ii = 1) and log b_j for 15 responses (b_p = 1).
    Likelihood: Π_i Multinomial(n_i· ; P(·|i)). Gradients are closed form
        ∂LL/∂log η_ij = (n_ij + n_ji) − (N_i P_ij + N_j P_ji),   ∂LL/∂log b_j = n_·j − Σ_i N_i P_ij
    and the ascent is Adam from the closed-form start. Returns dict(eta, bias, loglik, loglik_saturated,
    converged, max_grad)."""
    m = _smoothed(snr, add)
    n_row = m.sum(axis=1)
    iu = np.triu_indices(16, 1)
    theta = np.log(luce_closed_form(snr, add)[iu])
    logb = np.zeros(16)
    mt_th, vt_th, mt_b, vt_b = np.zeros_like(theta), np.zeros_like(theta), np.zeros(16), np.zeros(16)
    b1, b2, e = 0.9, 0.999, 1e-8

    def probs(theta, logb):
        eta = np.eye(16)
        eta[iu] = np.exp(theta)
        eta = eta + eta.T - np.eye(16)
        u = eta * np.exp(logb)[None, :]
        return eta, u / u.sum(axis=1, keepdims=True)

    converged, max_grad = False, np.inf
    for t in range(1, iters + 1):
        eta, p = probs(theta, logb)
        expct = n_row[:, None] * p
        g_eta = (m + m.T - expct - expct.T)[iu]
        g_b = m.sum(axis=0) - expct.sum(axis=0)
        g_b[0] = 0.0                                              # b_p fixed to 1: the scale of b is arbitrary
        max_grad = float(max(np.abs(g_eta).max(), np.abs(g_b).max()))
        if max_grad < tol:
            converged = True
            break
        mt_th = b1 * mt_th + (1 - b1) * g_eta
        vt_th = b2 * vt_th + (1 - b2) * g_eta ** 2
        mt_b = b1 * mt_b + (1 - b1) * g_b
        vt_b = b2 * vt_b + (1 - b2) * g_b ** 2
        theta += lr * (mt_th / (1 - b1 ** t)) / (np.sqrt(vt_th / (1 - b2 ** t)) + e)
        logb += lr * (mt_b / (1 - b1 ** t)) / (np.sqrt(vt_b / (1 - b2 ** t)) + e)
    eta, p = probs(theta, logb)
    ll = float(np.sum(m * np.log(p)))
    p_sat = m / n_row[:, None]
    ll_sat = float(np.sum(m * np.log(p_sat)))
    return dict(eta=eta, bias=np.exp(logb), loglik=ll, loglik_saturated=ll_sat, converged=converged,
                max_grad=max_grad, iterations=t)


_LUCE = {}


def luce_result(snr):
    """Cached luce_fit(snr) with the default settings."""
    if snr not in _LUCE:
        _LUCE[snr] = luce_fit(snr)
    return _LUCE[snr]


def luce_eta(snr, method="ml"):
    return luce_result(snr)["eta"] if method == "ml" else luce_closed_form(snr)


def luce_distance(snrs=DEFAULT_SNRS_CONFUSION, method="ml"):
    """Mean over snrs of −ln η_ij (Shepard 1987: similarity = exp(−distance)).

    η is clipped at 1 first: at -18 dB a few fitted η exceed 1 (a pair confused more often than the diagonal
    predicts, which the model allows but a distance cannot), and that would give a negative distance."""
    d = np.zeros((16, 16))
    for snr in snrs:
        d += -np.log(np.minimum(luce_eta(snr, method), 1.0))
    d /= len(snrs)
    np.fill_diagonal(d, 0.0)
    return d


_CACHE = {}


def matrix(metric="luce", **kwargs):
    """The 16x16 symmetric distance matrix for one metric (cached for the default arguments)."""
    if metric not in METRICS:
        raise ValueError("metric must be one of {}".format(METRICS))
    key = (metric, tuple(sorted(kwargs.items())))
    if key not in _CACHE:
        fn = {"hamming": hamming_matrix, "weighted": weighted_matrix,
              "confusion": confusion_distance, "mds": mds_matrix, "luce": luce_distance}[metric]
        _CACHE[key] = fn(**kwargs)
    return _CACHE[key]


def distance(a, b, metric="luce", **kwargs):
    """Perceptual distance between consonants a and b (ASCII codes) under the given metric."""
    return float(matrix(metric, **kwargs)[INDEX[a], INDEX[b]])


def foils_by_distance(cons, metric="luce", **kwargs):
    """The other 15 consonants sorted by increasing distance from cons: [(foil, d), …]."""
    m = matrix(metric, **kwargs)
    i = INDEX[cons]
    return sorted(((c, float(m[i, INDEX[c]])) for c in CONSONANTS if c != cons), key=lambda t: t[1])


def foil_nearest(cons, x, metric="luce", **kwargs):
    """The consonant whose distance from cons is closest to x: (foil, d). Drop-in for adaptive_vawm_EN.foil_for."""
    cands = foils_by_distance(cons, metric, **kwargs)
    return min(cands, key=lambda t: abs(t[1] - x))


# ------------------------------------------------------------------------------------------------ current axis

def load_current_axis(path=CONFUSION_PY):
    """{(a, b): count} from generate_trials.CONFUSION_DATA (directional: a = sound, b = target foil)."""
    src = open(path, encoding="utf-8").read()
    m = re.search(r"CONFUSION_DATA\s*=\s*(\[.*?\n\])", src, re.S)
    return {(row["sound"], row["target"]): int(row["count"]) for row in ast.literal_eval(m.group(1))}


def current_audio_x(count):
    """adaptive_vawm_EN.audio_x: −log10(count + 1)."""
    return -np.log10(float(count) + 1.0)


# ------------------------------------------------------------------------------------------------ statistics

def rankdata(x):
    x = np.asarray(x, float)
    order = np.argsort(x, kind="mergesort")
    ranks = np.empty(len(x))
    sx = x[order]
    i = 0
    while i < len(x):
        j = i
        while j + 1 < len(x) and sx[j + 1] == sx[i]:
            j += 1
        ranks[order[i:j + 1]] = 0.5 * (i + j) + 1
        i = j + 1
    return ranks


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    return float(np.corrcoef(rankdata(x[ok]), rankdata(y[ok]))[0, 1])


def upper(m):
    return m[np.triu_indices(16, 1)]


# ------------------------------------------------------------------------------------------------ binning

def partners_per_level(m, edges):
    """edges: n_levels+1 monotone cut points; returns 16 x n_levels counts of partners of each consonant in each level."""
    n_levels = len(edges) - 1
    lvl = np.searchsorted(edges[1:-1], m, side="right")
    off = ~np.eye(16, dtype=bool)
    return np.stack([np.bincount(lvl[i][off[i]], minlength=n_levels) for i in range(16)])


def propose_bins(m, n_levels, n_candidates=30):
    """Choose cut points (from n_candidates quantiles of the 120 pair values) that maximise the minimum number of
    partners any consonant has in any level, then the evenness of level sizes. Returns dict(edges, partners, min)."""
    vals = np.sort(upper(m))
    cands = np.unique(np.quantile(vals, np.linspace(0, 1, n_candidates + 2)[1:-1]))
    best = None
    for cuts in itertools.combinations(cands, n_levels - 1):
        edges = np.concatenate([[vals[0]], cuts, [vals[-1]]])
        pp = partners_per_level(m, edges)
        sizes = pp.sum(axis=0) / 2
        score = (int(pp.min()), -float(sizes.std()))
        if best is None or score > best[0]:
            best = (score, edges, pp)
    score, edges, pp = best
    return dict(edges=edges, partners=pp, min=score[0], sizes=[int(v) for v in pp.sum(axis=0) // 2])


# ------------------------------------------------------------------------------------------------ report

def fmt_pair(a, b):
    return "{}-{}".format(IPA[a], IPA[b])


def build_rows():
    """One dict per pair with every metric (used for the csv and the summary)."""
    mats = {"hamming": matrix("hamming"), "weighted": matrix("weighted"), "confusion": matrix("confusion")}
    per_snr = {snr: confusion_distance((snr,)) for snr in SNRS}
    mds = {k: mds_matrix(k) for k in (2, 3, 4)}
    luce = matrix("luce")
    luce_cf = luce_distance(method="closed")
    luce_snr = {snr: luce_distance((snr,)) for snr in SNRS}
    cur = load_current_axis()
    rows = []
    for a, b in pairs():
        i, j = INDEX[a], INDEX[b]
        diff = [n for n, k in zip(FEATURE_NAMES, range(5)) if FEATURES[a][k] != FEATURES[b][k]]
        cab, cba = cur.get((a, b)), cur.get((b, a))
        xs = [current_audio_x(c) for c in (cab, cba) if c is not None]
        rows.append(dict(a=a, b=b, pair=fmt_pair(a, b), hamming=mats["hamming"][i, j],
                         weighted=mats["weighted"][i, j], confusion=mats["confusion"][i, j],
                         **{"confusion_{}".format(str(s).replace("-", "m")): per_snr[s][i, j] for s in SNRS},
                         mds2=mds[2][i, j], mds3=mds[3][i, j], mds4=mds[4][i, j],
                         luce=luce[i, j], luce_closed_form=luce_cf[i, j],
                         **{"luce_{}".format(str(s).replace("-", "m")): luce_snr[s][i, j] for s in SNRS},
                         features_differing="+".join(diff),
                         cur_count_ab=cab, cur_count_ba=cba,
                         cur_axis=(float(np.mean(xs)) if xs else None)))
    return rows


def write_csv(rows, path=OUT_CSV):
    cols = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if v is None else ("{:.4f}".format(v) if isinstance(v, float) else v))
                        for k, v in r.items()})


def summary_text(rows):
    L = []
    P = L.append
    P("consonant_distance.py — summary (Miller & Nicely 1955, Tables I-VI, 200-6500 cps)")
    P("")
    # ---- weights
    P("1. Relative information transmitted per feature, T_rel = T/H (recomputed from the matrices)")
    P("   paper Table XXI in brackets (bits; T_rel = bits / max possible)")
    P("   SNR     " + "".join("{:>22}".format(n) for n in FEATURE_NAMES) + "{:>18}".format("all (16x16)"))
    for snr in SNRS:
        tr = feature_transmission(snr)
        cells = []
        for k, n in enumerate(FEATURE_NAMES):
            paper = PAPER_TABLE_XXI[snr][k + 1] / PAPER_TABLE_XXI["max"][k + 1]
            cells.append("{:>11.3f} [{:.3f}]".format(tr[n][2], paper))
        cells.append("{:>8.3f} [{:.3f}]".format(tr["all"][2], PAPER_TABLE_XXI[snr][0] / 4.0))
        P("   {:>4d} dB  ".format(snr) + "   ".join(cells))
    P("   H(feature) bits: " + ", ".join("{} {:.3f}".format(n, feature_transmission(0)[n][1]) for n in FEATURE_NAMES))
    w = feature_weights()
    P("")
    P("   default weights = mean T_rel over {} dB:".format(DEFAULT_SNRS_WEIGHT))
    P("   " + "  ".join("{} {:.3f}".format(n, w[n]) for n in FEATURE_NAMES))
    P("   max weighted distance (all five differ) = {:.3f}; a voicing-only pair = {:.3f}, a place-only pair = {:.3f}"
      .format(sum(w.values()), w["voicing"], w["place"]))
    # ---- correlations
    P("")
    P("2. Spearman correlations between metrics over the 120 pairs (cur_axis: the {} pairs in CONFUSION_DATA)"
      .format(sum(r["cur_axis"] is not None for r in rows)))
    names = ["hamming", "weighted", "confusion", "confusion_m12", "confusion_m6", "confusion_0", "confusion_6",
             "mds2", "mds3", "mds4", "luce", "luce_closed_form", "luce_m12", "luce_m6", "luce_0", "luce_6",
             "cur_axis"]
    col = {n: np.array([np.nan if r[n] is None else r[n] for r in rows], float) for n in names}
    short = {n: n.replace("confusion", "conf").replace("closed_form", "cf").replace("cur_axis", "current") for n in names}
    P("   " + " " * 10 + "".join("{:>9}".format(short[n]) for n in names))
    for n in names:
        P("   {:<10}".format(short[n]) + "".join("{:>9.2f}".format(spearman(col[n], col[m])) for m in names))
    # ---- extremes
    P("")
    P("3. Ten most distant / ten least distant pairs per metric")
    for n in ("hamming", "weighted", "confusion", "mds3", "luce", "cur_axis"):
        rs = [r for r in rows if r[n] is not None]
        rs.sort(key=lambda r: -r[n])
        P("   {:<10} far : ".format(n) + ", ".join("{} {:.2f}".format(r["pair"], r[n]) for r in rs[:10]))
        P("   {:<10} near: ".format(n) + ", ".join("{} {:.2f}".format(r["pair"], r[n]) for r in rs[-10:][::-1]))
    # ---- MDS
    P("")
    P("4. Classical MDS on −ln s_ab, counts pooled over {} dB".format(DEFAULT_SNRS_CONFUSION))
    for k in (2, 3, 4):
        f = mds_fit(k)
        ev = f["eigenvalues"]
        P("   {} dims: r(fit, input) = {:.3f}, stress-1 = {:.3f}, variance of first {} eigenvalues = {:.1f}%"
          .format(k, f["r_fit"], f["stress1"], k, 100 * ev[:k].sum() / ev[ev > 0].sum()))
    f = mds_fit(4)
    P("   |corr(dimension, feature)| for the 4-dim solution:")
    P("   dim   " + "".join("{:>12}".format(n) for n in FEATURE_NAMES))
    for k in range(4):
        P("   {:<6}".format(k + 1) + "".join("{:>12.2f}".format(v) for v in f["alignment"][k]))
    P("   coordinates (3-dim solution):")
    f3 = mds_fit(3)
    for c in CONSONANTS:
        P("   {:>5} {:>2}  ".format(c, IPA[c]) + " ".join("{:>7.2f}".format(v) for v in f3["coords"][INDEX[c]]))
    # ---- Luce
    P("")
    P("4b. Similarity-choice model per SNR (+0.5 smoothing; ML fit by gradient ascent from the closed-form start)")
    P("    SNR  zero off-diag cells  converged  LL(model)   LL(saturated)   G²(df=105)   median −ln η  max −ln η"
      "   corr(ML, closed form)  bias range")
    for snr in SNRS:
        f = luce_result(snr)
        zeros = int((tables()[snr] == 0).sum() - np.sum(np.diag(tables()[snr]) == 0))
        g2 = 2 * (f["loglik_saturated"] - f["loglik"])
        d_ml, d_cf = -np.log(f["eta"][np.triu_indices(16, 1)]), -np.log(luce_closed_form(snr)[np.triu_indices(16, 1)])
        P("    {:>3d}  {:>19d}  {:>9}  {:>10.1f}  {:>13.1f}  {:>11.1f}  {:>12.2f}  {:>9.2f}  {:>21.3f}  {:.2f}-{:.2f}"
          .format(snr, zeros, str(f["converged"]), f["loglik"], f["loglik_saturated"], g2, float(np.median(d_ml)),
                  float(d_ml.max()), float(np.corrcoef(d_ml, d_cf)[0, 1]), f["bias"].min(), f["bias"].max()))
    P("    Usable: -12, -6, 0 dB (few empty cells, η spans a wide range). -18 dB: responses nearly uniform, all η≈1.")
    P("    +6/+12 dB: most off-diagonals are 0, so −ln η there is mostly the smoothing constant (ceiling).")
    P("    Default 'luce' = mean of −ln η over {} dB.".format(DEFAULT_SNRS_CONFUSION))
    # ---- binning
    P("")
    P("5. Binning proposals (cut points chosen to maximise the minimum partners per consonant per level)")
    for n in ("weighted", "confusion", "luce"):
        m = matrix(n)
        for n_levels in ((5, 6) if n != "luce" else (4, 5, 6)):
            b = propose_bins(m, n_levels)
            P("   {} metric, {} levels: edges {}".format(n, n_levels,
                                                        " | ".join("{:.2f}".format(e) for e in b["edges"])))
            P("      pairs per level {} ; min partners of any consonant in any level = {}"
              .format(list(b["sizes"]), b["min"]))
            P("      partners per consonant per level:")
            for c in CONSONANTS:
                pp = b["partners"][INDEX[c]]
                flag = "  <-- lacks a partner in level(s) {}".format([i + 1 for i, v in enumerate(pp) if v == 0]) \
                    if pp.min() == 0 else ""
                P("        {:>5} {:>2}  {}{}".format(c, IPA[c], " ".join("{:>2d}".format(v) for v in pp), flag))
    # ---- uniqueness of weighted values
    vals = np.unique(np.round(upper(matrix("weighted")), 6))
    P("")
    P("   The weighted metric takes only {} distinct values ({}), so its natural levels are those values;"
      .format(len(vals), ", ".join("{:.2f}".format(v) for v in vals)))
    P("   the confusion metric is continuous (120 distinct values) and bins freely.")
    return "\n".join(L) + "\n"


def main():
    rows = build_rows()
    write_csv(rows)
    txt = summary_text(rows)
    with open(OUT_TXT, "w", encoding="utf-8") as fh:
        fh.write(txt)
    print(txt)
    print("wrote", OUT_CSV)
    print("wrote", OUT_TXT)


if __name__ == "__main__":
    main()
