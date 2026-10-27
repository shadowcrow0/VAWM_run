"""比較候選 L*/C*: 以「繞錨點對稱可用範圍」為準的實用指標。

產出的數字記錄在 review/決策脈絡_跨色相圈類推.md;直接在 repo 根目錄執行即可。
"""
import numpy as np
import agrt_setup as A

ANCHOR, SPAN, STEP = 303.0, 60.0, 0.005
HUES = np.arange(ANCHOR - SPAN, ANCHOR + SPAN + 1e-9, STEP)
AI = int(np.argmin(np.abs(HUES - ANCHOR)))


def profile(L, C):
    lab = A.lch_to_lab(L, C, HUES)
    rgb = A.lab_to_srgb(lab)
    ok = np.all((rgb >= -A.GAMUT_TOL) & (rgb <= 1.0 + A.GAMUT_TOL), axis=-1)
    d = A.de00(lab[:-1], lab[1:])
    arc = np.concatenate([[0.0], np.cumsum(d)])
    arc = arc - arc[AI]

    # 含錨點且連續不出界的區段
    lo = AI
    while lo > 0 and ok[lo - 1]:
        lo -= 1
    hi = AI
    while hi < len(ok) - 1 and ok[hi + 1]:
        hi += 1
    half = min(abs(arc[lo]), abs(arc[hi]))          # 對稱可用半長

    sel = (arc >= -half) & (arc <= half)
    hexes = [A.to_hex(np.clip(r, 0, 1)) for r in rgb[sel]]
    a_sel = arc[sel]
    first = {}
    for h_, a_ in zip(hexes, a_sel):
        first.setdefault(h_, a_)
    pos = np.array(sorted(first.values()))
    gaps = np.diff(pos)
    per_deg = d / STEP
    return dict(
        full_in_gamut=bool(ok.all()),
        blue_edge=float(HUES[lo]), purple_edge=float(HUES[hi]),
        half=float(half), n_hex=len(first),
        med_gap=float(np.median(gaps)), max_gap=float(gaps.max()),
        nonunif=float(per_deg.max() / per_deg.min()),
        beta_max=float(half / 2.3107),
        anchor_hex=A.to_hex(np.clip(A.lab_to_srgb(A.lch_to_lab(L, C, ANCHOR)), 0, 1)),
    )


CANDS = [(55.0, 38.0, '現行'), (71.0, 42.5, '相異色最大'),
         (71.0, 40.0, '最大 - 3.5 邊際'), (65.0, 39.5, '較保守 L*'),
         (60.0, 37.0, '接近現行 L*, 取該 L* 上限')]

print(f"{'設定':<22} {'全段':>5} {'對稱半長':>9} {'相異色':>7} {'中位間距':>9} "
      f"{'最大缺口':>9} {'非均勻':>7} {'beta上限':>9} {'錨點色':>9}")
for L, C, tag in CANDS:
    p = profile(L, C)
    print(f"L*={L:<4.0f} C*={C:<5.1f} {tag:<8} {str(p['full_in_gamut']):>5} "
          f"{p['half']:9.2f} {p['n_hex']:7d} {p['med_gap']:9.4f} {p['max_gap']:9.4f} "
          f"{p['nonunif']:7.2f} {p['beta_max']:9.2f} {p['anchor_hex']:>9}")

print("\n=== 現行設定的出界點 ===")
p = profile(55.0, 38.0)
print(f"  偏藍側到 h={p['blue_edge']:.1f} 度出界, 偏紫側到 h={p['purple_edge']:.1f} 度")
print(f"  (錨點 303 度, 所以偏藍只剩 {303 - p['blue_edge']:.1f} 度可用, 不足 60)")

print("\n=== L*=71 時各色相的色域上限(找出綁死的那一端) ===")
for h in [243., 253., 263., 283., 303., 333., 363.]:
    print(f"  h={h:6.1f}  最大 C* = {A.max_in_gamut_chroma(h, 71.0)[0]:.1f}")
