"""
等彩度設計:固定 L* 與彩度 C*,所有顏色落在同一色相圈上,
僅以「色相角」定義近/遠探針。彻底消除彩度混淆,色相 360° 完全均勻。

  ct : 色相圈上隨機一個色相角 h0
  CH : h0 ± U(0,  ΔH_CH)        近探針(高相似)
  CL : h0 ± U(ΔH_CH, ΔH_CL)     遠探針(低相似)
  (正負號隨機,讓 CH/CL 可順時針或逆時針偏離 ct)

弦長關係:ΔE76 = 2 * C* * sin(Δh/2)
  Δh=30° -> ΔE≈20.2 ; Δh=60° -> ΔE≈39.0  (見下方輸出)

需要: pip install colour-science
"""
import numpy as np
import colour
import csv

# ---- 參數 ----
L_FIXED  = 70.0     # 固定亮度
C_FIXED  = 39.0     # 固定彩度(此 L 下整個色相圈仍在 sRGB 色域內的安全值)
DH_CH    = 30.0     # CH 色相角半徑(度): 0 ~ 30
DH_CL_IN = 38.0     # CL 色相角內緣(度): 確保 ΔE >= 25 (需 Δh >= 37.4°)
DH_CL_OUT= 60.0     # CL 色相角外緣(度): 38 ~ 60 的環帶
MIN_DE_CT_CL = 25.0 # ct 與 CL 之間的最小 Delta E
N_TRIALS = 180
SEED     = 11

rng = np.random.default_rng(SEED)


def hue_to_lab(h_deg, L=L_FIXED, C=C_FIXED):
    """色相角(度)-> Lab,固定 L 與 C*。"""
    h = np.radians(h_deg)
    return np.array([L, C * np.cos(h), C * np.sin(h)])


def lab_to_rgb(lab):
    return colour.XYZ_to_sRGB(colour.Lab_to_XYZ(lab))


def to_hex(lab):
    r, g, b = np.round(np.clip(lab_to_rgb(lab), 0, 1) * 255).astype(int)
    return f"#{r:02X}{g:02X}{b:02X}"


def dE76(lab1, lab2):
    return float(colour.delta_E(lab1, lab2, method="CIE 1976"))


def chord_dE(dh_deg, C=C_FIXED):
    """理論弦長 ΔE = 2*C*sin(Δh/2)。"""
    return 2 * C * np.sin(np.radians(dh_deg) / 2)


def make_triplet():
    """產生一組 (ct, CH, CL)，確保 ct-CL 的 ΔE >= MIN_DE_CT_CL"""
    while True:
        h0 = rng.uniform(0, 360)                       # ct 色相角
        dh_ch = rng.uniform(0, DH_CH) * rng.choice([-1, 1])
        dh_cl = rng.uniform(DH_CL_IN, DH_CL_OUT) * rng.choice([-1, 1])

        lab_ct = hue_to_lab(h0)
        lab_cl = hue_to_lab((h0 + dh_cl) % 360)

        # 檢查 ct-CL 的 Delta E 是否 >= 25
        if dE76(lab_ct, lab_cl) >= MIN_DE_CT_CL:
            return h0, (h0 + dh_ch) % 360, (h0 + dh_cl) % 360, dh_ch, dh_cl


def generate(n=N_TRIALS):
    rows = []
    for i in range(n):
        h0, hch, hcl, dh_ch, dh_cl = make_triplet()
        lab_ct = hue_to_lab(h0); lab_ch = hue_to_lab(hch); lab_cl = hue_to_lab(hcl)
        rows.append({
            "trial": i + 1, "L": L_FIXED, "C": C_FIXED,
            "ct_hue": round(h0, 2),  "ct_hex": to_hex(lab_ct),
            "CH_hue": round(hch, 2), "CH_hex": to_hex(lab_ch), "CH_dHue": round(dh_ch, 2),
            "CL_hue": round(hcl, 2), "CL_hex": to_hex(lab_cl), "CL_dHue": round(dh_cl, 2),
            # CIELAB 色差(CIE 1976)
            "dE_ct_CH": round(dE76(lab_ct, lab_ch), 2),
            "dE_ct_CL": round(dE76(lab_ct, lab_cl), 2),
        })
    return rows


if __name__ == "__main__":
    rows = generate()
    with open("color_triplets_isochroma.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f"已產生 {len(rows)} 組 (L={L_FIXED}, C*={C_FIXED}),寫入 color_triplets_isochroma.csv\n")
    print("理論換算: Δh=30° -> ΔE %.1f ;  Δh=60° -> ΔE %.1f" % (chord_dE(30), chord_dE(60)))
    print(f'\n{"#":>3} {"ct":>8} {"CH":>8} {"CL":>8} |  dE CH/CL   | Δhue CH/CL')
    for r in rows[:8]:
        print(f'{r["trial"]:>3} {r["ct_hex"]:>8} {r["CH_hex"]:>8} {r["CL_hex"]:>8} | '
              f'{r["dE_ct_CH"]:>5}/{r["dE_ct_CL"]:<5} | {r["CH_dHue"]:>+6}/{r["CL_dHue"]:<+6}')
    import statistics as st
    print()
    for k in ["dE_ct_CH", "dE_ct_CL"]:
        v = [r[k] for r in rows]; print(f'{k}: mean {st.mean(v):.1f}, min {min(v):.1f}, max {max(v):.1f}')
    # 色相均勻檢查
    ang = [r["ct_hue"] for r in rows]
    print("\nct 色相 8 區間分布 (理想 22.5):",
          [sum(1 for a in ang if lo <= a < lo+45) for lo in range(0, 360, 45)])