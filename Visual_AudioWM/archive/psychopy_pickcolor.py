"""
PsychoPy 用的顏色挑選函式(單檔、零外部相依)。

可直接貼進 Builder 的 Code component(Begin Experiment),或放在 .psyexp 同資料夾
用 `from psychopy_pickcolor import make_color_pool` 匯入。只用標準庫 math / random,
不需要 colour-science、skimage、numpy —— PsychoPy standalone 直接可跑。

--------------------------------------------------------------------------
標籤定義(已依新規則把數值互換)
--------------------------------------------------------------------------
  ct : 目標色 (target)
  CH : **High salience** = 遠探針,ΔE 大、好分辨   <- 原本 CL 的數值
  CL : **Low  salience** = 近探針,ΔE 小、難分辨   <- 原本 CH 的數值

  (舊版 color_control.py / getcolor.py 是 CH=近、CL=遠,此檔已對調。)

--------------------------------------------------------------------------
取樣設計:等彩度色相圈(對應 color_control.py / generate_colors_isochroma.py)
--------------------------------------------------------------------------
  固定 L* 與 C*,所有顏色落在同一個色相圈上,只用「色相角差」定義遠近,
  彩度與亮度完全不混淆,色相 360° 均勻。

    ct : 隨機色相角 h0(make_color_pool 預設會分層取樣,讓整圈覆蓋均勻)
    CH : h0 ± U(39, 60)°  -> ΔE76 ≈ 25 ~ 38   (high salience)
    CL : h0 ± U(15, 30)°  -> ΔE76 ≈ 10 ~ 20   (low  salience)

  弦長關係: ΔE76 = 2 * C* * sin(Δh/2)
  L*=70 / C*=38 時整圈色相都在 sRGB 色域內(見 hue_gaps / max_safe_chroma)。

--------------------------------------------------------------------------
PsychoPy 用法
--------------------------------------------------------------------------
  # --- Begin Experiment ---
  from psychopy_pickcolor import make_color_pool
  color_pool = make_color_pool(180, seed=11)      # 整份實驗先產生好

  # --- Begin Routine ---
  c = color_pool[trials.thisN]          # 或 pick_color_triplet() 每 trial 現抽
  target_stim.fillColor = c['ct_hex']   # PsychoPy 直接吃 '#RRGGBB'
  probeH_stim.fillColor = c['CH_hex']   # high salience(遠、好分辨)
  probeL_stim.fillColor = c['CL_hex']   # low  salience(近、難分辨)
  thisExp.addData('ct_hex', c['ct_hex'])
  thisExp.addData('CH_hex', c['CH_hex'])
  thisExp.addData('CL_hex', c['CL_hex'])
  thisExp.addData('dE76_ct_CH', c['dE76_ct_CH'])
  thisExp.addData('dE76_ct_CL', c['dE76_ct_CL'])

  # 若 stimulus 設 colorSpace='rgb',改用 c['ct_rgb'] (-1~1 三元組);
  # colorSpace='rgb1' 則用 c['ct_rgb1'] (0~1)。
  # 不想多一個檔案的話,把整份貼進 Begin Experiment 也可以(零相依)。
"""

import math
import random

# ---------------- 參數(改這裡即可切換版本)----------------
L_FIXED = 70.0           # 固定亮度
C_FIXED = 38.0           # 固定彩度:L*=70 時整圈色相都還在 sRGB 色域內的最大值
                         # (舊腳本用 39,色相 204~225° 會超出色域被 clip,
                         #  那段的實際彩度會被壓低 -> 等彩度假設失效)
# 想要更高彩度就把亮度往上調(整圈都在 sRGB 內的安全組合,由 max_safe_chroma() 掃出來):
#   L*=70 -> C* <= 38.2 | L*=72 -> 39.2 | L*=73 -> 39.7 | L*=74 -> 40.0(整圈最大)
#   L*=75 以上 C* 反而掉下來(紅/藍區先出色域)。
# 另一條路:要更大的 ΔE 時,加大 Δh 比加大 C* 有效 —— ΔE76 = 2*C*sin(Δh/2),
#   例如 C*=38 時 Δh 60°->70° 可讓 ΔE76 由 38.0 升到 43.6,完全不動彩度。
DH_HIGH = (39.0, 60.0)   # CH = high salience 的色相角差範圍(度) -> ΔE76 ≈ 25~38
                         # (C*=38 時 Δh 要 >= 38.6° 才有 ΔE76 >= 25,故下緣取 39)
DH_LOW = (15.0, 30.0)    # CL = low  salience 的色相角差範圍(度) -> ΔE76 ≈ 10~20
MIN_DE76_CT_HIGH = 25.0  # ct 與 CH 的最小 ΔE76(原本掛在 CL 上的 MIN_DE_CT_CL)
MAX_TRY = 20000          # 拒絕取樣上限,超過就丟例外(不會在實驗中無限迴圈)


# ================= 色彩空間轉換(D65 / 2°, sRGB) =================

_XN, _YN, _ZN = 95.047, 100.000, 108.883


def _f_inv(t):
    return t ** 3 if t > 6.0 / 29.0 else 3.0 * (6.0 / 29.0) ** 2 * (t - 4.0 / 29.0)


def _gamma(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055


def lab_to_rgb01(lab):
    """CIELAB -> sRGB(0~1,未裁切,超出 0~1 表示落在色域外)。"""
    L, a, b = lab
    fy = (L + 16.0) / 116.0
    fx = fy + a / 500.0
    fz = fy - b / 200.0
    x = _XN * _f_inv(fx) / 100.0
    y = _YN * _f_inv(fy) / 100.0
    z = _ZN * _f_inv(fz) / 100.0
    r = 3.2404542 * x - 1.5371385 * y - 0.4985314 * z
    g = -0.9692660 * x + 1.8760108 * y + 0.0415560 * z
    bl = 0.0556434 * x - 0.2040259 * y + 1.0572252 * z
    return tuple(_gamma(v) if v > 0 else -_gamma(-v) for v in (r, g, bl))


def in_gamut(lab, tol=1e-6):
    """三個通道都落在 [0,1] 才算在 sRGB 色域內。"""
    return all(-tol <= v <= 1.0 + tol for v in lab_to_rgb01(lab))


def lab_to_hex(lab):
    r, g, b = (int(round(min(max(v, 0.0), 1.0) * 255)) for v in lab_to_rgb01(lab))
    return "#{:02X}{:02X}{:02X}".format(r, g, b)


def lab_to_psychopy_rgb(lab):
    """PsychoPy colorSpace='rgb' 用的 -1 ~ 1 三元組。"""
    return tuple(min(max(v, 0.0), 1.0) * 2 - 1 for v in lab_to_rgb01(lab))


def lab_to_rgb1(lab):
    """PsychoPy colorSpace='rgb1' 用的 0 ~ 1 三元組。"""
    return tuple(min(max(v, 0.0), 1.0) for v in lab_to_rgb01(lab))


def lch_to_lab(L, C, h_deg):
    """色相角(度) + 固定 L*、C* -> Lab。"""
    h = math.radians(h_deg)
    return (L, C * math.cos(h), C * math.sin(h))


# ================= 色差 =================

def delta_e76(lab1, lab2):
    """CIE 1976 ΔE*ab = Lab 空間歐氏距離。"""
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(lab1, lab2)))


def delta_e00(lab1, lab2, kL=1.0, kC=1.0, kH=1.0):
    """CIEDE2000 色差(Sharma, Wu & Dalal, 2005 的公式)。"""
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2
    C1 = math.hypot(a1, b1)
    C2 = math.hypot(a2, b2)
    Cbar = (C1 + C2) / 2.0
    G = 0.5 * (1 - math.sqrt(Cbar ** 7 / (Cbar ** 7 + 25.0 ** 7))) if Cbar > 0 else 0.0
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360 if (b1 or a1p) else 0.0
    h2p = math.degrees(math.atan2(b2, a2p)) % 360 if (b2 or a2p) else 0.0

    dLp = L2 - L1
    dCp = C2p - C1p
    if C1p * C2p == 0:
        dhp = 0.0
    else:
        dhp = h2p - h1p
        if dhp > 180:
            dhp -= 360
        elif dhp < -180:
            dhp += 360
    dHp = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dhp) / 2)

    Lbp = (L1 + L2) / 2.0
    Cbp = (C1p + C2p) / 2.0
    if C1p * C2p == 0:
        hbp = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hbp = (h1p + h2p) / 2.0
    elif h1p + h2p < 360:
        hbp = (h1p + h2p + 360) / 2.0
    else:
        hbp = (h1p + h2p - 360) / 2.0

    T = (1
         - 0.17 * math.cos(math.radians(hbp - 30))
         + 0.24 * math.cos(math.radians(2 * hbp))
         + 0.32 * math.cos(math.radians(3 * hbp + 6))
         - 0.20 * math.cos(math.radians(4 * hbp - 63)))
    dtheta = 30 * math.exp(-(((hbp - 275) / 25.0) ** 2))
    Rc = 2 * math.sqrt(Cbp ** 7 / (Cbp ** 7 + 25.0 ** 7)) if Cbp > 0 else 0.0
    Sl = 1 + (0.015 * (Lbp - 50) ** 2) / math.sqrt(20 + (Lbp - 50) ** 2)
    Sc = 1 + 0.045 * Cbp
    Sh = 1 + 0.015 * Cbp * T
    Rt = -math.sin(math.radians(2 * dtheta)) * Rc

    tL, tC, tH = dLp / (kL * Sl), dCp / (kC * Sc), dHp / (kH * Sh)
    return math.sqrt(tL ** 2 + tC ** 2 + tH ** 2 + Rt * tC * tH)


def chord_dE76(dh_deg, C=C_FIXED):
    """等彩度圈上的理論弦長 ΔE76 = 2*C*sin(Δh/2)。"""
    return 2 * C * math.sin(math.radians(dh_deg) / 2)


def hue_gaps(L=L_FIXED, C=C_FIXED, step=0.2):
    """
    掃整個色相圈,回傳「超出 sRGB 色域」的色相區段 [(起, 迄), ...]。

    回傳空 list = 整圈都可用,取樣不會有色相偏差。若非空,那些色相會被拒絕取樣
    (或在舊腳本裡被 clip 成彩度較低的顏色),等彩度假設在該區段不成立。
    """
    n = int(round(360 / step))
    bad = [i * step for i in range(n) if not in_gamut(lch_to_lab(L, C, i * step))]
    if not bad:
        return []
    segs, start, prev = [], bad[0], bad[0]
    for h in bad[1:]:
        if h - prev > step * 1.5:
            segs.append((round(start, 1), round(prev, 1)))
            start = h
        prev = h
    segs.append((round(start, 1), round(prev, 1)))
    return segs


def max_safe_chroma(L=L_FIXED, step=0.5, hue_step=0.5):
    """回傳在亮度 L 下,整圈色相都還在 sRGB 色域內的最大 C*。"""
    C = 0.0
    while C + step < 128 and not hue_gaps(L, C + step, hue_step):
        C += step
    return C


# ================= 主函式:產生一組 (ct, CH, CL) =================

def pick_color_triplet(rng=None, L=L_FIXED, C=C_FIXED,
                       dh_high=DH_HIGH, dh_low=DH_LOW,
                       min_de76_high=MIN_DE76_CT_HIGH,
                       hue_range=None, max_try=MAX_TRY):
    """
    產生一組 (ct, CH, CL) 顏色三元組。

    CH = high salience(色相角差大 -> ΔE 大 -> 好分辨)
    CL = low  salience(色相角差小 -> ΔE 小 -> 難分辨)
    正負號隨機,CH/CL 可順時針或逆時針偏離 ct。

    Parameters
    ----------
    rng : random.Random 或 None
        傳入自己的亂數產生器可重現(例如 random.Random(11));None 則用全域 random。
    L, C : float
        固定的亮度與彩度。
    dh_high, dh_low : (min, max)
        CH / CL 的色相角差範圍(度)。
    min_de76_high : float
        ct 與 CH 之間要求的最小 ΔE76。
    hue_range : (lo, hi) 或 None
        限制 ct 的色相角只在此區間內抽(make_color_pool 的 stratify 用);None = 0~360。
    max_try : int
        拒絕取樣上限,超過丟 RuntimeError。

    Returns
    -------
    dict,含:
      ct_hex / CH_hex / CL_hex             : '#RRGGBB'
      ct_rgb / CH_rgb / CL_rgb             : PsychoPy colorSpace='rgb'  (-1~1)
      ct_rgb1 / CH_rgb1 / CL_rgb1          : PsychoPy colorSpace='rgb1' (0~1)
      ct_lab / CH_lab / CL_lab             : (L, a, b)
      ct_hue / CH_hue / CL_hue             : 色相角(度)
      CH_dHue / CL_dHue                    : 相對 ct 的色相角差(帶正負號)
      dE76_ct_CH / dE76_ct_CL              : CIE 1976 色差
      dE00_ct_CH / dE00_ct_CL              : CIEDE2000 色差
      dE76_CH_CL                           : 兩個探針之間的色差
      CH_salience='high' / CL_salience='low'
      high_sal_hex / low_sal_hex           : CH_hex / CL_hex 的別名
    """
    rng = rng or random
    lo, hi = hue_range if hue_range else (0.0, 360.0)
    for _ in range(max_try):
        h0 = rng.uniform(lo, hi) % 360
        d_ch = rng.uniform(*dh_high) * rng.choice((-1, 1))   # high salience: 遠
        d_cl = rng.uniform(*dh_low) * rng.choice((-1, 1))    # low  salience: 近
        ct = lch_to_lab(L, C, h0)
        ch = lch_to_lab(L, C, (h0 + d_ch) % 360)
        cl = lch_to_lab(L, C, (h0 + d_cl) % 360)
        if delta_e76(ct, ch) < min_de76_high:
            continue
        if not (in_gamut(ct) and in_gamut(ch) and in_gamut(cl)):
            continue

        out = {
            "L": L, "C": C,
            "CH_salience": "high",   # CH = 遠探針,ΔE 大
            "CL_salience": "low",    # CL = 近探針,ΔE 小
            "ct_hue": round(h0, 2),
            "CH_hue": round((h0 + d_ch) % 360, 2), "CH_dHue": round(d_ch, 2),
            "CL_hue": round((h0 + d_cl) % 360, 2), "CL_dHue": round(d_cl, 2),
            "dE76_ct_CH": round(delta_e76(ct, ch), 2),
            "dE76_ct_CL": round(delta_e76(ct, cl), 2),
            "dE00_ct_CH": round(delta_e00(ct, ch), 2),
            "dE00_ct_CL": round(delta_e00(ct, cl), 2),
            "dE76_CH_CL": round(delta_e76(ch, cl), 2),
        }
        for name, lab in (("ct", ct), ("CH", ch), ("CL", cl)):
            out[name + "_lab"] = tuple(round(v, 3) for v in lab)
            out[name + "_hex"] = lab_to_hex(lab)
            out[name + "_rgb"] = tuple(round(v, 4) for v in lab_to_psychopy_rgb(lab))
            out[name + "_rgb1"] = tuple(round(v, 4) for v in lab_to_rgb1(lab))
        out["high_sal_hex"] = out["CH_hex"]
        out["low_sal_hex"] = out["CL_hex"]
        return out

    raise RuntimeError(
        "取樣失敗:檢查 L={}/C={} 是否讓整圈色相超出 sRGB 色域,或 min_de76_high={} "
        "是否大於 dh_high 上限能達到的最大色差({:.1f})。".format(
            L, C, min_de76_high, chord_dE76(dh_high[1], C)))


# ================= 整份實驗的色票清單 =================

def make_color_pool(n, seed=None, stratify=True, min_dHue_prev=None,
                    n_prev_check=1, max_retry_per_trial=500, **kw):
    """
    一次產生 n 組三元組(建議放在 Begin Experiment 跑一次,不要每個 trial 現算)。

    n                   : 組數
    seed                : 固定亂數種子 -> 刺激集可重現
    stratify            : True(預設)把 ct 色相切成 n 等分再各自加抖動,
                          保證整份實驗的色相覆蓋均勻(之後再洗牌打散順序);
                          False 則每組完全隨機抽色相(等同舊腳本行為)。
    min_dHue_prev       : 若設定,ct 色相與「前 n_prev_check 組」的環狀角距需 >= 此值(度),
                          避免連續 trial 出現幾乎一樣的目標色。
    n_prev_check        : 往前檢查幾組(預設 1 = 只比上一組)。
    max_retry_per_trial : 重試上限;用完就接受當下這組,並把該筆 'spacing_ok' 標為 False。
    其餘 **kw 轉給 pick_color_triplet(L / C / dh_high / dh_low / min_de76_high)。

    注意:等彩度圈上 8-bit 量化後只有數百個不同的 hex,所以這裡「不」強制全域顏色
    不重複(在固定 L*/C* 的設計下不可能達成);用色相間距來控制刺激分散度。

    回傳 list[dict],每筆多 'trial'(1-based)與 'spacing_ok' 兩個欄位。
    """
    rng = random.Random(seed)
    L = kw.get("L", L_FIXED)
    C = kw.get("C", C_FIXED)
    gaps = hue_gaps(L, C)
    if gaps:
        print("[psychopy_pickcolor] 警告:L*={} C*={} 有色相超出 sRGB 色域 {},"
              "這些色相會被跳過,色相分布不會均勻。建議 C* <= {:.1f}。".format(
                  L, C, gaps, max_safe_chroma(L)))

    rows, prev_hues = [], []
    for i in range(n):
        spacing_ok = True
        # stratify: 第 i 組的 ct 色相限制在第 i 個等分區間內(區間內隨機)
        band = (360.0 * i / n, 360.0 * (i + 1) / n) if stratify else None
        for _ in range(max_retry_per_trial):
            t = pick_color_triplet(rng=rng, hue_range=band, **kw)
            if min_dHue_prev is not None and any(
                    _hue_dist(t["ct_hue"], h) < min_dHue_prev
                    for h in prev_hues[-n_prev_check:]):
                continue    # 跟最近幾組的目標色太接近
            break
        else:
            spacing_ok = False   # 用完重試次數,接受最後一組(放棄間距限制)
        prev_hues.append(t["ct_hue"])
        t["trial"] = i + 1
        t["spacing_ok"] = spacing_ok
        rows.append(t)

    n_relaxed = sum(1 for r in rows if not r["spacing_ok"])
    if n_relaxed:
        print("[psychopy_pickcolor] 注意:{}/{} 組放寬了 min_dHue_prev 限制"
              "(spacing_ok=False)。".format(n_relaxed, n))
    if stratify:
        rng.shuffle(rows)        # 打散呈現順序,但每筆的 'trial' 保留原始編號
        for i, r in enumerate(rows, start=1):
            r["trial"] = i
    return rows


def _hue_dist(h1, h2):
    """兩個色相角的環狀距離(0~180)。"""
    d = abs(h1 - h2) % 360
    return min(d, 360 - d)


def save_pool_csv(rows, path):
    """把 make_color_pool 的結果寫成 CSV(可當 PsychoPy conditions file)。"""
    import csv
    keys = ["trial", "ct_hex", "CH_hex", "CL_hex",
            "dE76_ct_CH", "dE76_ct_CL", "dE00_ct_CH", "dE00_ct_CL"]
    keys += [k for k in rows[0] if k not in keys]
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in keys})
    return path


# ================= 自我檢查 =================

if __name__ == "__main__":
    # 1) CIEDE2000 對照 Sharma et al. (2005) 的標準測試值
    ref = [((50.0000, 2.6772, -79.7751), (50.0000, 0.0000, -82.7485), 2.0425),
           ((50.0000, 3.1571, -77.2803), (50.0000, 0.0000, -82.7485), 2.8615),
           ((50.0000, 2.4900, -0.0010), (50.0000, -2.4900, 0.0009), 7.1792),
           ((50.0000, -1.3802, -84.2814), (50.0000, 0.0000, -82.7485), 1.0000),
           ((60.2574, -34.0099, 36.2677), (60.4626, -34.1751, 39.4387), 1.2644)]
    print("CIEDE2000 檢核(對 Sharma et al. 2005):")
    for lab1, lab2, expect in ref:
        got = delta_e00(lab1, lab2)
        ok = abs(got - expect) < 1e-3
        print("  expect {:.4f}  got {:.4f}  {}".format(expect, got, "OK" if ok else "FAIL"))
        assert ok, "CIEDE2000 實作與標準值不符"

    # 2) Lab -> hex 檢核
    print("\nLab->hex 檢核: white ->", lab_to_hex((100.0, 0.0, 0.0)),
          " mid-gray ->", lab_to_hex((53.585, 0.0, 0.0)))
    assert lab_to_hex((100.0, 0.0, 0.0)) == "#FFFFFF"

    # 3) 理論弦長
    print("\n理論換算: Δh=15° -> ΔE76 {:.1f} | Δh=30° -> {:.1f} | "
          "Δh=38° -> {:.1f} | Δh=60° -> {:.1f}".format(
              chord_dE76(15), chord_dE76(30), chord_dE76(38), chord_dE76(60)))

    # 4) 色域檢查:整圈色相是否都可用
    print("\n色域檢查: L*={} C*={} 的出色域色相區段 = {} (空 list = 整圈可用)".format(
        L_FIXED, C_FIXED, hue_gaps()))
    print("        L*={} 下整圈可用的最大 C* = {:.1f}".format(
        L_FIXED, max_safe_chroma(L_FIXED)))
    assert not hue_gaps(), "預設 L*/C* 有色相超出色域,色相取樣會有偏差"

    # 5) 產生一組色票並檢查 CH 一律比 CL 遠
    rows = make_color_pool(12, seed=11)
    print("\n{:>3}  {:>8} {:>8} {:>8} |  dE76 CH/CL   |  dE00 CH/CL   | Δhue CH/CL".format(
        "#", "ct", "CH(hi)", "CL(lo)"))
    for r in rows:
        print("{:>3}  {:>8} {:>8} {:>8} | {:>5}/{:<5}  | {:>5}/{:<5}  | {:>+6}/{:<+6}".format(
            r["trial"], r["ct_hex"], r["CH_hex"], r["CL_hex"],
            r["dE76_ct_CH"], r["dE76_ct_CL"], r["dE00_ct_CH"], r["dE00_ct_CL"],
            r["CH_dHue"], r["CL_dHue"]))

    hi = [r["dE76_ct_CH"] for r in rows]
    lo = [r["dE76_ct_CL"] for r in rows]
    print("\nhigh salience (CH) ΔE76: min {:.1f}  max {:.1f}".format(min(hi), max(hi)))
    print("low  salience (CL) ΔE76: min {:.1f}  max {:.1f}".format(min(lo), max(lo)))
    assert min(hi) > max(lo), "CH 應該一律比 CL 遠(high salience > low salience)"
    assert min(hi) >= MIN_DE76_CT_HIGH - 1e-6, "ct-CH 未達最小 ΔE76"

    # 6) 大量取樣:色相分布是否均勻、是否有色域外的色
    big = make_color_pool(180, seed=11)
    ang = [r["ct_hue"] for r in big]
    bins = [sum(1 for a in ang if lo_ <= a < lo_ + 45) for lo_ in range(0, 360, 45)]
    print("\nct 色相 8 區間分布 (stratify=True, 180 組, 理想 22.5):", bins)
    rand_ang = [r["ct_hue"] for r in make_color_pool(180, seed=11, stratify=False)]
    print("ct 色相 8 區間分布 (stratify=False,純隨機)        :",
          [sum(1 for a in rand_ang if lo_ <= a < lo_ + 45) for lo_ in range(0, 360, 45)])
    assert all(in_gamut(r[k + "_lab"]) for r in big for k in ("ct", "CH", "CL"))
    assert max(bins) - min(bins) <= 2, "stratify 後色相覆蓋應該接近均勻"

    print("\n全部檢核通過:CH = high salience(遠、大 ΔE), CL = low salience(近、小 ΔE)。")
