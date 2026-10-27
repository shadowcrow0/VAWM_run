"""
給老闆挑選用的候選藍紫色配對(20組)。
5 個中心色相(涵蓋偏藍 -> 邊界 -> 偏紫) x 4 種 ΔE00 目標(從接近 JND 到明顯可辨),
固定 L*、C*(排除亮度/彩度混淆),只在色相角上取點,搭配 CIEDE2000 搜尋 Δh。
用意:讓老闆同時看到「色相位置」跟「色差大小」兩個維度的效果,選出最適合拿來測試
「口語分不出來、但知覺上是否可辨」這個研究問題的一組。
"""
import numpy as np
import colour
import colorsys
import csv

L_FIXED = 55.0
C_FIXED = 38.0
H_CENTERS = [263.0, 273.0, 283.0, 293.0, 303.0]   # 偏藍 -> 藍紫邊界 -> 偏紫
DE00_TARGETS = [2.0, 4.0, 6.0, 10.0]               # 近JND(口語難辨) -> 明顯可辨


def lch_to_lab(L, C, h_deg):
    h = np.radians(h_deg)
    return np.array([L, C * np.cos(h), C * np.sin(h)])


def lab_to_srgb(lab):
    return colour.XYZ_to_sRGB(colour.Lab_to_XYZ(lab))


def in_gamut(rgb, tol=1e-6):
    return bool(np.all(rgb >= -tol) and np.all(rgb <= 1 + tol))


def to_hex(rgb):
    r, g, b = np.round(np.clip(rgb, 0, 1) * 255).astype(int)
    return f"#{r:02X}{g:02X}{b:02X}"


def to_hsv(rgb):
    r, g, b = np.clip(rgb, 0, 1)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return round(h * 360, 1), round(s * 100, 1), round(v * 100, 1)


def to_hsl(rgb):
    r, g, b = np.clip(rgb, 0, 1)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return round(h * 360, 1), round(s * 100, 1), round(l * 100, 1)


def de00(lab1, lab2):
    return float(colour.delta_E(np.asarray(lab1, float), np.asarray(lab2, float), method="CIE 2000"))


def find_dh_for_target(h_center, target, max_dh=45.0, tol=0.03, max_iter=60):
    lo, hi = 0.0, max_dh
    for _ in range(max_iter):
        mid = (lo + hi) / 2
        lab1 = lch_to_lab(L_FIXED, C_FIXED, h_center - mid / 2)
        lab2 = lch_to_lab(L_FIXED, C_FIXED, h_center + mid / 2)
        d = de00(lab1, lab2)
        if abs(d - target) < tol:
            return mid, d
        if d < target:
            lo = mid
        else:
            hi = mid
    return mid, d


rows = []
set_id = 0
for h_c in H_CENTERS:
    for target in DE00_TARGETS:
        set_id += 1
        dh, achieved = find_dh_for_target(h_c, target)
        h1, h2 = h_c - dh / 2, h_c + dh / 2
        lab1, lab2 = lch_to_lab(L_FIXED, C_FIXED, h1), lch_to_lab(L_FIXED, C_FIXED, h2)
        rgb1, rgb2 = lab_to_srgb(lab1), lab_to_srgb(lab2)
        assert in_gamut(rgb1) and in_gamut(rgb2), f"set {set_id} out of gamut"
        hsv1, hsv2 = to_hsv(rgb1), to_hsv(rgb2)
        hsl1, hsl2 = to_hsl(rgb1), to_hsl(rgb2)
        d76 = float(colour.delta_E(lab1, lab2, method="CIE 1976"))
        rows.append({
            "set": set_id,
            "h_center_deg": h_c,
            "target_dE00": target,
            "A_hex": to_hex(rgb1), "A_hsv": f"{hsv1[0]:.1f},{hsv1[1]:.1f},{hsv1[2]:.1f}",
            "A_hsl": f"{hsl1[0]:.1f},{hsl1[1]:.1f},{hsl1[2]:.1f}",
            "A_Lab": f"{lab1[0]:.2f},{lab1[1]:.2f},{lab1[2]:.2f}",
            "B_hex": to_hex(rgb2), "B_hsv": f"{hsv2[0]:.1f},{hsv2[1]:.1f},{hsv2[2]:.1f}",
            "B_hsl": f"{hsl2[0]:.1f},{hsl2[1]:.1f},{hsl2[2]:.1f}",
            "B_Lab": f"{lab2[0]:.2f},{lab2[1]:.2f},{lab2[2]:.2f}",
            "dE00": round(achieved, 2), "dE76": round(d76, 2),
        })

out_path = "/home/yyc/symmetry/AVWM/data/bv_candidates_for_advisor.csv"
with open(out_path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print(f"寫入 {out_path} (共 {len(rows)} 組)\n")
print(f'{"set":>3} {"h_c":>5} {"target":>6} | {"A_hex":>8} {"B_hex":>8} | {"dE00":>6}')
for r in rows:
    print(f'{r["set"]:>3} {r["h_center_deg"]:>5} {r["target_dE00"]:>6} | {r["A_hex"]:>8} {r["B_hex"]:>8} | {r["dE00"]:>6}')

# ---- 視覺化: 5x4 色票網格,方便老闆一次看完全部 ----
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, axes = plt.subplots(len(H_CENTERS), len(DE00_TARGETS), figsize=(10, 12))
for row in rows:
    ri = H_CENTERS.index(row["h_center_deg"])
    ci = DE00_TARGETS.index(row["target_dE00"])
    ax = axes[ri, ci]
    ax.add_patch(mpatches.Rectangle((0, 0), 0.5, 1, color=row["A_hex"]))
    ax.add_patch(mpatches.Rectangle((0.5, 0), 0.5, 1, color=row["B_hex"]))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(f'#{row["set"]}  dE00={row["dE00"]}', fontsize=9)
    if ci == 0:
        ax.set_ylabel(f'h={row["h_center_deg"]:.0f}°', fontsize=10)
    if ri == 0:
        ax.set_xlabel('')
for ci, target in enumerate(DE00_TARGETS):
    axes[0, ci].annotate(f'target dE00={target}', xy=(0.5, 1.15), xycoords='axes fraction',
                          ha='center', fontsize=10, fontweight='bold')
fig.suptitle("Blue-violet candidate pairs for advisor review (rows=hue center, cols=ΔE00 target)", y=0.995)
fig.tight_layout()
fig_path = "/home/yyc/symmetry/AVWM/figure/bv_candidates_for_advisor.png"
fig.savefig(fig_path, dpi=150)
print(f"\n圖存到 {fig_path}")
