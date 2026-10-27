"""
固定 L*,在 a*-b* 平面產生 N 組 (ct, CH, CL) 顏色三元組,並計算色差。

  ct : 中心目標色(色域內隨機)
  CH : 距 ct 的圓盤內   (0   < r <= R_CH)    近探針(高相似)
  CL : 距 ct 的甜甜圈內 (R_CH < r <= R_CL_OUT) 遠探針(低相似)

每組額外計算:
  dE76_ct_CH / dE76_ct_CL  : CIE 1976 色差(L 固定時 = a-b 平面歐氏距離 = 取樣半徑)
  dE00_ct_CH / dE00_ct_CL  : CIEDE2000 色差(感知更準)

所有點皆保證落在 sRGB 色域內(拒絕取樣)。需要: pip install colour-science
"""
import numpy as np
import colour
import csv

# ---- 參數(改這裡即可切換版本)----
L_FIXED   = 55.0           # 固定亮度
R_CH      = 20.0           # CH 圓盤半徑(近)
R_CL_IN   = 20.0           # CL 甜甜圈內半徑(= R_CH,兩區不重疊)
R_CL_OUT  = 40.0           # CL 甜甜圈外半徑(遠)
CT_MIN_C  = 18.0           # ct 最小彩度(避免太接近灰)
CT_MAX_C  = 90.0           # ct 最大彩度
N_TRIALS  = 180
SEED      = 11             # 固定種子 -> 刺激集可重現
MAX_TRY   = 5000

rng = np.random.default_rng(SEED)


def lab_to_rgb(L, a, b):
    return colour.XYZ_to_sRGB(colour.Lab_to_XYZ([L, a, b]))


def in_gamut(L, a, b, tol=1e-9):
    rgb = lab_to_rgb(L, a, b)
    return bool(np.all(rgb >= -tol) and np.all(rgb <= 1.0 + tol))


def to_hex(L, a, b):
    r, g, bl = np.round(np.clip(lab_to_rgb(L, a, b), 0, 1) * 255).astype(int)
    return f"#{r:02X}{g:02X}{bl:02X}"


def delta_E(lab1, lab2, method):
    return float(colour.delta_E(np.asarray(lab1, float),
                                np.asarray(lab2, float), method=method))


def sample_annulus(ct, r_in, r_out, L=L_FIXED, max_try=MAX_TRY):
    a0, b0 = ct
    for _ in range(max_try):
        r = np.sqrt(rng.uniform(r_in**2, r_out**2))
        th = rng.uniform(0, 2 * np.pi)
        a, b = a0 + r * np.cos(th), b0 + r * np.sin(th)
        if in_gamut(L, a, b):
            return np.array([a, b])
    return None


def make_triplet(L=L_FIXED):
    while True:
        ct = rng.uniform(-CT_MAX_C, CT_MAX_C, 2)
        c = np.hypot(*ct)
        if c < CT_MIN_C or c > CT_MAX_C or not in_gamut(L, *ct):
            continue
        ch = sample_annulus(ct, 0.0,     R_CH)
        cl = sample_annulus(ct, R_CL_IN, R_CL_OUT)
        if ch is None or cl is None:
            continue
        return ct, ch, cl


def generate(n=N_TRIALS):
    rows = []
    for i in range(n):
        ct, ch, cl = make_triplet()
        lab_ct = [L_FIXED, *ct]; lab_ch = [L_FIXED, *ch]; lab_cl = [L_FIXED, *cl]
        rows.append({
            "trial": i + 1, "L": L_FIXED,
            "ct_a": round(float(ct[0]), 3), "ct_b": round(float(ct[1]), 3), "ct_hex": to_hex(*lab_ct),
            "CH_a": round(float(ch[0]), 3), "CH_b": round(float(ch[1]), 3), "CH_hex": to_hex(*lab_ch),
            "CL_a": round(float(cl[0]), 3), "CL_b": round(float(cl[1]), 3), "CL_hex": to_hex(*lab_cl),
            # CIELAB 色差(CIE 1976,ΔE*ab):L 固定時 = a-b 平面歐氏距離 = 取樣半徑
            "dE_ct_CH": round(delta_E(lab_ct, lab_ch, "CIE 1976"), 2),
            "dE_ct_CL": round(delta_E(lab_ct, lab_cl, "CIE 1976"), 2),
            # 彩度 C* = sqrt(a^2 + b^2)(離中性灰的距離);用來檢查彩度混淆
            "C_ct":      round(float(np.hypot(*ct)), 2),
            "C_CH":      round(float(np.hypot(*ch)), 2),
            "C_CL":      round(float(np.hypot(*cl)), 2),
            "dC_ct_CH":  round(float(np.hypot(*ch) - np.hypot(*ct)), 2),
            "dC_ct_CL":  round(float(np.hypot(*cl) - np.hypot(*ct)), 2),
        })
    return rows


if __name__ == "__main__":
    rows = generate()
    out = "color_triplets.csv"
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f"已產生 {len(rows)} 組,寫入 {out}\n")
    print(f'{"#":>3}  {"ct":>8} {"CH":>8} {"CL":>8} |  dE(CIELAB) CH / CL')
    for r in rows[:8]:
        print(f'{r["trial"]:>3}  {r["ct_hex"]:>8} {r["CH_hex"]:>8} {r["CL_hex"]:>8} | '
              f'{r["dE_ct_CH"]:>6} / {r["dE_ct_CL"]:<6}')
    import statistics as st
    print()
    for k in ["dE_ct_CH","dE_ct_CL"]:
        v=[r[k] for r in rows]; print(f'{k}: mean {st.mean(v):.1f}, min {min(v):.1f}, max {max(v):.1f}')
    # 彩度混淆檢查:CH、CL 相對 ct 的平均彩度差(理想接近 0)
    print("\n--- 彩度(C*)混淆檢查 ---")
    for k in ["C_ct","C_CH","C_CL"]:
        v=[r[k] for r in rows]; print(f'{k}: mean {st.mean(v):.1f}')
    for k in ["dC_ct_CH","dC_ct_CL"]:
        v=[r[k] for r in rows]
        print(f'{k}: mean {st.mean(v):+.2f}  (正=探針更鮮豔, 負=探針更接近灰)')
