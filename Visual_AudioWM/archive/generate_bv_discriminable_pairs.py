"""
在藍紫色(blue-violet)區域產生 10 組「可區辨」的顏色對，供類別學習作業使用。
跟先前「口語分不出來」的組合(ΔE00 ~ 2)方向相反：這裡要求兩色明顯可辨，
但同屬藍紫色系(不會跑出範圍太多)，所以把 ΔE00 上限設在 10。

作法比照 generate_colors.py：固定 L*, C*（避免亮度/彩度變成混淆線索），
只在色相角(h)上取兩點，用 CIEDE2000 當作感知色差指標去搜尋 Δh，
讓每組的 ΔE00 落在 [6, 10] 之間(明顯可辨、但不超過類別學習標準上限 10)。
10 組的中心色相角在藍紫色帶內展開，讓整批色票涵蓋從偏藍到偏紫的範圍。
"""
import numpy as np
import colour
import colorsys
import csv

L_FIXED = 55.0
C_FIXED = 38.0
H_LOW, H_HIGH = 265.0, 308.0   # 藍紫色帶(LCh 色相角): 265≈偏藍 ~ 308≈偏紫
N_PAIRS = 10
DE00_MIN, DE00_MAX = 6.0, 10.0
SEED = 11

rng = np.random.default_rng(SEED)


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


def find_dh_for_target(h_center, target_de00, max_dh=45.0, tol=0.05, max_iter=60):
    """二分搜尋 Δh，讓 h_center±Δh/2 兩色的 dE00 逼近 target_de00。"""
    lo, hi = 0.0, max_dh
    for _ in range(max_iter):
        mid = (lo + hi) / 2
        lab1 = lch_to_lab(L_FIXED, C_FIXED, h_center - mid / 2)
        lab2 = lch_to_lab(L_FIXED, C_FIXED, h_center + mid / 2)
        d = de00(lab1, lab2)
        if abs(d - target_de00) < tol:
            return mid, d
        if d < target_de00:
            lo = mid
        else:
            hi = mid
    return mid, d


rows = []
h_centers = np.linspace(H_LOW, H_HIGH, N_PAIRS)
targets = rng.uniform(DE00_MIN, DE00_MAX, N_PAIRS)

for i, (h_c, target) in enumerate(zip(h_centers, targets), start=1):
    dh, achieved = find_dh_for_target(h_c, target)
    h1, h2 = h_c - dh / 2, h_c + dh / 2
    lab1, lab2 = lch_to_lab(L_FIXED, C_FIXED, h1), lch_to_lab(L_FIXED, C_FIXED, h2)
    rgb1, rgb2 = lab_to_srgb(lab1), lab_to_srgb(lab2)

    assert in_gamut(rgb1) and in_gamut(rgb2), f"pair {i} out of sRGB gamut"

    hsv1, hsv2 = to_hsv(rgb1), to_hsv(rgb2)
    hsl1, hsl2 = to_hsl(rgb1), to_hsl(rgb2)
    d76 = float(colour.delta_E(lab1, lab2, method="CIE 1976"))

    rows.append({
        "pair": i,
        "L_star": L_FIXED, "C_star": C_FIXED,
        "h_center_deg": round(float(h_c), 1),
        "A_h_deg": round(float(h1), 2), "A_hex": to_hex(rgb1),
        "A_hsv": f"{hsv1[0]:.1f},{hsv1[1]:.1f},{hsv1[2]:.1f}",
        "A_hsl": f"{hsl1[0]:.1f},{hsl1[1]:.1f},{hsl1[2]:.1f}",
        "A_Lab": f"{lab1[0]:.2f},{lab1[1]:.2f},{lab1[2]:.2f}",
        "B_h_deg": round(float(h2), 2), "B_hex": to_hex(rgb2),
        "B_hsv": f"{hsv2[0]:.1f},{hsv2[1]:.1f},{hsv2[2]:.1f}",
        "B_hsl": f"{hsl2[0]:.1f},{hsl2[1]:.1f},{hsl2[2]:.1f}",
        "B_Lab": f"{lab2[0]:.2f},{lab2[1]:.2f},{lab2[2]:.2f}",
        "dE00": round(achieved, 2),
        "dE76": round(d76, 2),
    })

out_path = "/home/yyc/symmetry/AVWM/data/blue_violet_discriminable_pairs.csv"
with open(out_path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

print(f"寫入 {out_path}\n")
print(f'{"pair":>4} {"h_c":>6} | {"A_hex":>8} {"B_hex":>8} | {"dE00":>6} {"dE76":>6}')
for r in rows:
    print(f'{r["pair"]:>4} {r["h_center_deg"]:>6} | {r["A_hex"]:>8} {r["B_hex"]:>8} | {r["dE00"]:>6} {r["dE76"]:>6}')
