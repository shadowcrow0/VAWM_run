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
MIN_DE_CT_CL = 25.0        # ct 與 CL 之間的最小 Delta E (CIEDE2000)

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


def make_triplet(L=L_FIXED, min_dE_ct_cl=MIN_DE_CT_CL):
    """
    產生一組 (ct, CH, CL) 顏色三元組
    確保 ct 與 CL 之間的 CIEDE2000 色差 >= min_dE_ct_cl
    """
    while True:
        ct = rng.uniform(-CT_MAX_C, CT_MAX_C, 2)
        c = np.hypot(*ct)
        if c < CT_MIN_C or c > CT_MAX_C or not in_gamut(L, *ct):
            continue
        ch = sample_annulus(ct, 0.0,     R_CH)
        cl = sample_annulus(ct, R_CL_IN, R_CL_OUT)
        if ch is None or cl is None:
            continue

        # 檢查 ct 與 CL 的 Delta E (CIEDE2000) 是否夠大
        lab_ct = [L, *ct]
        lab_cl = [L, *cl]
        dE00 = delta_E(lab_ct, lab_cl, "CIE 2000")
        if dE00 < min_dE_ct_cl:
            continue  # Delta E 不夠大，重新找

        return ct, ch, cl


def generate(n=N_TRIALS, min_dE_between_ct=None, max_retry_per_trial=500, verbose=True):
    """
    產生 n 組顏色三元組

    Parameters:
        n: 組數
        min_dE_between_ct: 若設定，則每組 ct 之間的 CIEDE2000 色差必須 >= 此值
        max_retry_per_trial: 每組最大嘗試次數（超過則放棄 ct 間距限制）
        verbose: 是否顯示進度
    """
    import sys
    rows = []
    used_hex = set()  # 記錄已使用的顏色，避免重複
    used_ct_labs = []  # 記錄已使用的 ct Lab 值（用於計算 ct 間色差）

    for i in range(n):
        retry_count = 0
        gave_up_spacing = False
        # 持續嘗試直到找到符合條件的三元組
        while True:
            retry_count += 1
            ct, ch, cl = make_triplet()
            lab_ct = [L_FIXED, *ct]; lab_ch = [L_FIXED, *ch]; lab_cl = [L_FIXED, *cl]

            hex_ct = to_hex(*lab_ct)
            hex_ch = to_hex(*lab_ch)
            hex_cl = to_hex(*lab_cl)

            # 檢查三個顏色是否都沒用過，且彼此不同
            new_colors = {hex_ct, hex_ch, hex_cl}
            if len(new_colors) != 3 or (new_colors & used_hex):
                continue  # 有重複，重新找

            # 若要求 ct 之間色差 > 門檻，檢查與所有已有 ct 的色差
            if min_dE_between_ct is not None and retry_count < max_retry_per_trial:
                too_close = False
                for prev_ct_lab in used_ct_labs:
                    dE = delta_E(lab_ct, prev_ct_lab, "CIE 2000")
                    if dE < min_dE_between_ct:
                        too_close = True
                        break
                if too_close:
                    continue  # 與某個已有 ct 太近，重新找
            elif retry_count >= max_retry_per_trial:
                gave_up_spacing = True

            break  # 所有條件都符合

        # 加入已使用集合
        used_hex.update(new_colors)
        used_ct_labs.append(lab_ct)

        if verbose:
            status = " (放棄間距)" if gave_up_spacing else ""
            print(f"  {i + 1}/{n}{status}", end="\r", flush=True)

        rows.append({
            "trial": i + 1, "L": L_FIXED,
            "ct_a": round(float(ct[0]), 3), "ct_b": round(float(ct[1]), 3), "ct_hex": hex_ct,
            "CH_a": round(float(ch[0]), 3), "CH_b": round(float(ch[1]), 3), "CH_hex": hex_ch,
            "CL_a": round(float(cl[0]), 3), "CL_b": round(float(cl[1]), 3), "CL_hex": hex_cl,
            # CIELAB 色差(CIE 1976,ΔE*ab):L 固定時 = a-b 平面歐氏距離 = 取樣半徑
            "dE_ct_CH": round(delta_E(lab_ct, lab_ch, "CIE 1976"), 2),
            "dE_ct_CL": round(delta_E(lab_ct, lab_cl, "CIE 1976"), 2),
            # CIEDE2000 色差(感知更準)
            "dE00_ct_CH": round(delta_E(lab_ct, lab_ch, "CIE 2000"), 2),
            "dE00_ct_CL": round(delta_E(lab_ct, lab_cl, "CIE 2000"), 2),
        })
    if verbose:
        print()  # 換行
    return rows


def save_and_report(rows, filename, title, check_ct_spacing=False):
    """儲存 CSV 並輸出統計報告"""
    import statistics as st

    with open(filename, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"已產生 {len(rows)} 組，寫入 {filename}\n")

    print(f'{"#":>3}  {"ct":>8} {"CH":>8} {"CL":>8} |  dE(CIELAB) CH / CL')
    for r in rows[:5]:
        print(f'{r["trial"]:>3}  {r["ct_hex"]:>8} {r["CH_hex"]:>8} {r["CL_hex"]:>8} | '
              f'{r["dE_ct_CH"]:>6} / {r["dE_ct_CL"]:<6}')

    print("\nCIE 1976 色差:")
    for k in ["dE_ct_CH", "dE_ct_CL"]:
        v = [r[k] for r in rows]
        print(f'  {k}: mean {st.mean(v):.1f}, min {min(v):.1f}, max {max(v):.1f}')

    print("\nCIEDE2000 色差:")
    for k in ["dE00_ct_CH", "dE00_ct_CL"]:
        v = [r[k] for r in rows]
        print(f'  {k}: mean {st.mean(v):.1f}, min {min(v):.1f}, max {max(v):.1f}')

    # 計算 ct 之間的色差統計
    if check_ct_spacing:
        ct_labs = [[L_FIXED, r["ct_a"], r["ct_b"]] for r in rows]
        ct_dEs = []
        for i in range(len(ct_labs)):
            for j in range(i+1, len(ct_labs)):
                ct_dEs.append(delta_E(ct_labs[i], ct_labs[j], "CIE 2000"))
        print(f"\nct 間 CIEDE2000 色差:")
        print(f'  mean {st.mean(ct_dEs):.1f}, min {min(ct_dEs):.1f}, max {max(ct_dEs):.1f}')


if __name__ == "__main__":
    # 產生 10 組不同種子的版本，讓使用者挑選
    for seed in range(1, 11):
        rng = np.random.default_rng(seed)
        rows = generate(n=180, min_dE_between_ct=None, verbose=False)
        filename = f"color_triplets_seed{seed}.csv"
        save_and_report(rows, filename, f"種子 {seed}", check_ct_spacing=True)