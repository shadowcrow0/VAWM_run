"""搜尋在 h=303±60 整段弧上都不出 sRGB 色域、且 8-bit 相異色數最大的 L*/C*。

產出的數字記錄在 review/決策脈絡_跨色相圈類推.md;直接在 repo 根目錄執行即可。
"""
import numpy as np
import agrt_setup as A

ANCHOR, SPAN = 303.0, 60.0
HUES = np.arange(ANCHOR - SPAN, ANCHOR + SPAN + 1e-9, 0.02)   # 6001 點, 每步 0.02 度


def max_chroma_for_L(L, c_grid):
    """該 L* 下, 整段弧上共同可用的最大 C*(受最緊的色相綁死)。"""
    hh, cc = np.meshgrid(HUES[::10], c_grid, indexing='ij')     # 粗一點的色相夠找上限
    rgb = A.lab_to_srgb(A.lch_to_lab(L, cc.ravel(), hh.ravel())).reshape(hh.shape + (3,))
    ok = np.all((rgb >= -A.GAMUT_TOL) & (rgb <= 1.0 + A.GAMUT_TOL), axis=-1)
    # 每個色相: 由 0 往外第一個出界處之前的最後一個 C*
    per_hue = np.where(ok.all(axis=1), c_grid[-1],
                       c_grid[np.argmin(ok, axis=1) - 1])
    return per_hue.min()


def metrics(L, C):
    """回傳整段弧的: 是否全在色域內, 弧長, 8-bit 相異色數, 相異色中位間距, 每度非均勻性。"""
    lab = A.lch_to_lab(L, C, HUES)
    rgb = A.lab_to_srgb(lab)
    inside = bool(np.all((rgb >= -A.GAMUT_TOL) & (rgb <= 1.0 + A.GAMUT_TOL)))
    step = A.de00(lab[:-1], lab[1:])
    arc = float(step.sum())
    hexes = [A.to_hex(np.clip(r, 0, 1)) for r in rgb]
    cum = np.concatenate([[0.0], np.cumsum(step)])
    first = {}
    for h_, a_ in zip(hexes, cum):
        first.setdefault(h_, a_)
    pos = np.array(sorted(first.values()))
    gaps = np.diff(pos)
    per_deg = step / 0.02
    return dict(inside=inside, arc=arc, n_hex=len(first),
                med_gap=float(np.median(gaps)) if gaps.size else float('nan'),
                nonunif=float(per_deg.max() / per_deg.min()))


c_grid = np.arange(0.0, 120.0, 0.05)
print(f"{'L*':>5} {'可用C*上限':>10} {'弧長dE00':>10} {'相異色':>7} {'中位間距':>9} {'非均勻':>7}")
rows = []
for L in np.arange(30.0, 86.0, 1.0):
    cmax = max_chroma_for_L(L, c_grid)
    if cmax < 5:
        continue
    C = np.floor(cmax * 2) / 2 - 0.5          # 留一點安全邊際, 取到 0.5
    m = metrics(L, C)
    if not m['inside']:
        C = np.floor(cmax) - 1.0
        m = metrics(L, C)
    rows.append((L, C, cmax, m))
    print(f"{L:5.0f} {cmax:10.1f} {m['arc']:10.2f} {m['n_hex']:7d} "
          f"{m['med_gap']:9.4f} {m['nonunif']:7.2f}  (取 C*={C})")

best = max(rows, key=lambda r: r[3]['n_hex'])
print("\n=== 相異色數最大 ===")
L, C, cmax, m = best
print(f"L*={L:.0f}  C*={C:.1f}  (該 L* 的色域上限 {cmax:.1f})")
print(f"  整段 ±60 度全在色域內: {m['inside']}")
print(f"  弧長 {m['arc']:.2f} dE00, 相異 8-bit 色 {m['n_hex']}, "
      f"中位間距 {m['med_gap']:.4f} dE00, 非均勻性 {m['nonunif']:.2f}x")

print("\n=== 現行設定對照 (L*=55, C*=38) ===")
cur = metrics(55.0, 38.0)
print(f"  整段 ±60 度全在色域內: {cur['inside']}")
print(f"  弧長 {cur['arc']:.2f} dE00, 相異 8-bit 色 {cur['n_hex']}, "
      f"中位間距 {cur['med_gap']:.4f} dE00, 非均勻性 {cur['nonunif']:.2f}x")
