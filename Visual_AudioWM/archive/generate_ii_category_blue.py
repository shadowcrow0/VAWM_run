"""
Information-integration(II)類別學習用的顏色刺激。
固定色相(藍, h=270),只在彩度 C* x 明度 L* 平面上放兩個類別,
兩類別中心用對角線分開,決策邊界跟兩軸都不平行 -> 單一維度規則(只看彩度或只看明度)
無法完美分類,必須整合兩個維度才能區分,同時因為色相固定,不會產生「比較藍/比較紫」
這種可語言化的類別線索。

方法比照 generate_colors.py 的風格:固定色相角,在色彩空間內用常態分布抽樣、
拒絕不在 sRGB 色域內的點,直到湊滿每類需要的數量。
"""
import numpy as np
import colour
import colorsys
import csv

H_FIXED = 270.0     # 固定色相角(藍),避免色相命名成為分類線索
SEED = 11
N_PER_CAT = 10
MAX_TRY = 20000

# 兩類別中心呈對角線分布(C*, L*),各自圓形共變異(isotropic)。
# SD 刻意調大,讓「只看 C*」或「只看 L*」單一維度時,兩類別會明顯重疊(d' ~ 1.3),
# 只有把兩個維度合併(對角線方向)才會有較好的可分性(d' ~ 2.0) -> 強迫整合兩維度。
CAT_A = {"name": "A", "mean": (25.0, 35.0), "sd": (18.0, 18.0)}   # 低彩度、偏暗
CAT_B = {"name": "B", "mean": (48.0, 62.0), "sd": (18.0, 18.0)}   # 高彩度、偏亮

rng = np.random.default_rng(SEED)


def lch_to_lab(L, C, h_deg=H_FIXED):
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


def sample_category(cat, n=N_PER_CAT):
    Cm, Lm = cat["mean"]
    Cs, Ls = cat["sd"]
    out = []
    tries = 0
    while len(out) < n and tries < MAX_TRY:
        tries += 1
        C = rng.normal(Cm, Cs)
        L = rng.normal(Lm, Ls)
        if C < 0 or L <= 0 or L >= 100:
            continue
        lab = lch_to_lab(L, C)
        rgb = lab_to_srgb(lab)
        if in_gamut(rgb):
            out.append((C, L, lab, rgb))
    if len(out) < n:
        raise RuntimeError(f"category {cat['name']} only got {len(out)}/{n} in-gamut samples")
    return out


rows = []
for cat in (CAT_A, CAT_B):
    samples = sample_category(cat)
    for i, (C, L, lab, rgb) in enumerate(samples, start=1):
        hsv = to_hsv(rgb)
        hsl = to_hsl(rgb)
        rows.append({
            "category": cat["name"],
            "item": i,
            "hue_deg": H_FIXED,
            "C_star": round(float(C), 2),
            "L_star": round(float(L), 2),
            "hex": to_hex(rgb),
            "hsv": f"{hsv[0]:.1f},{hsv[1]:.1f},{hsv[2]:.1f}",
            "hsl": f"{hsl[0]:.1f},{hsl[1]:.1f},{hsl[2]:.1f}",
            "Lab": f"{lab[0]:.2f},{lab[1]:.2f},{lab[2]:.2f}",
        })

out_path = "/home/yyc/symmetry/AVWM/data/ii_category_blue_CL.csv"
with open(out_path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print(f"寫入 {out_path}  (共 {len(rows)} 筆, 每類 {N_PER_CAT} 筆)\n")

for r in rows:
    print(f'{r["category"]}{r["item"]:>2}  C*={r["C_star"]:>5}  L*={r["L_star"]:>5}  {r["hex"]}')

# ---- 可分性檢查: 單一維度 d' vs 對角線合併後的 d' ----
mA = np.array(CAT_A["mean"]); mB = np.array(CAT_B["mean"])
sd = np.array(CAT_A["sd"])  # 兩類別 sd 相同
delta = mB - mA
dprime_C = abs(delta[0]) / sd[0]
dprime_L = abs(delta[1]) / sd[1]
dprime_combined = np.linalg.norm(delta / sd)
print(f"\n可分性(d'): 只看 C* = {dprime_C:.2f}   只看 L* = {dprime_L:.2f}   對角線合併 = {dprime_combined:.2f}")
print("(單一維度 d' 明顯小於合併後的 d' -> 光看一個維度分不清楚,要整合兩維度才好分)")

# ---- 視覺化: C*-L* 平面上的兩類分布 + 對角線決策邊界 ----
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6, 6))
for cat, marker, color in [(CAT_A, "o", "#3355AA"), (CAT_B, "s", "#8855CC")]:
    pts = [(r["C_star"], r["L_star"]) for r in rows if r["category"] == cat["name"]]
    xs, ys = zip(*pts)
    ax.scatter(xs, ys, marker=marker, s=80, color=color, edgecolor="black", label=f'Category {cat["name"]}', zorder=3)
    ax.scatter(*cat["mean"], marker="x", s=150, color=color, linewidths=3, zorder=4)

# 對角線決策邊界: 兩類中心連線的垂直平分線
mA = np.array(CAT_A["mean"]); mB = np.array(CAT_B["mean"])
mid = (mA + mB) / 2
direction = mB - mA
normal = np.array([-direction[1], direction[0]])
normal = normal / np.linalg.norm(normal)
t = np.linspace(-40, 40, 2)
line = mid[None, :] + t[:, None] * normal[None, :]
ax.plot(line[:, 0], line[:, 1], "k--", label="optimal diagonal bound", zorder=2)

ax.set_xlabel("C* (chroma)")
ax.set_ylabel("L* (lightness)")
ax.set_title(f"Information-integration category structure (hue={H_FIXED}° blue fixed)")
ax.legend()
ax.set_xlim(0, 70)
ax.set_ylim(10, 90)
fig.tight_layout()
fig_path = "/home/yyc/symmetry/AVWM/figure/ii_category_blue_CL.png"
fig.savefig(fig_path, dpi=150)
print(f"\n圖存到 {fig_path}")
