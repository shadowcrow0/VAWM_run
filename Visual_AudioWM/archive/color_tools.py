"""
AVWM 顏色工具模組(企劃書階段 C0)。零外部相依,只用標準庫 math / random,
PsychoPy standalone 直接可跑,也可整份貼進 Code component。

--------------------------------------------------------------------------
設計要點(來源:adaptiveSFT_顏色salience校準_企劃書.md)
--------------------------------------------------------------------------
* 強度量尺一律用 **CIEDE2000(ΔE00)**,同時記錄 ΔE76 供對照。
  舊刺激池用 ΔE76 的後果(§2.2):ΔE76 與 ΔE00 只有 r = .598,
  25.4% 的「高 salience」foil 在知覺上其實比「低 salience」還近。
* 顏色參數化:L* 固定,C* 固定或小幅隨機,**只有色相是變動維度**,
  強度才是一維、心理測量函數才有意義。
* foil 不再用「Δh 落在某個帶狀範圍」去挑,而是**給定 ΔE00 反解出色相偏移**
  (find_hue_offset 單邊二分搜尋),並把**實際達成的 ΔE00 / ΔE76 記錄下來**。
  同一個 ΔE00 在不同色相位置需要不同的 Δh(差 1.27~1.31 倍),這正是
  CIEDE2000 在補償人眼對不同色相區辨識力的差異。

--------------------------------------------------------------------------
色域(gamut)硬約束
--------------------------------------------------------------------------
L* = 55 時整圈色相都在 sRGB 內的最大 C* 是 **31.5**(C* = 32 起有色相出界)。
超界的色相會被 clip 成彩度較低的顏色 -> 等彩度假設失效。
用 max_safe_chroma(L) / hue_gaps(L, C) 查任何 L*/C* 組合。

--------------------------------------------------------------------------
PsychoPy / 分析用法
--------------------------------------------------------------------------
  from color_tools import random_target_color, color_at_dE00

  tgt = random_target_color(rng, L=55.0, C_range=(28.0, 31.0))
  foil = color_at_dE00(tgt['lab'], 6.8, direction=+1)
  stim.fillColor = tgt['hex']; probe.fillColor = foil['hex']
  thisExp.addData('foil_dE00_actual', foil['dE00_actual'])   # 實際達成值

  # 重新分析既有 CSV 的顏色(把 hex 還原成 Lab 再算 ΔE00)
  from color_tools import hex_to_lab, delta_e00
  delta_e00(hex_to_lab('#6282CD'), hex_to_lab('#AF60D1'))
"""

import math
import random

# ---------------- 預設參數(企劃書 §5.1) ----------------
L_STAR = 55.0                 # 固定亮度
C_STAR_RANGE = (28.0, 31.0)   # C* 小幅隨機的範圍(上限必須 <= max_safe_chroma(L))
HUE_CENTER = 303.0            # 校準作業用的色相中心(離藍/紫命名邊界 283° 有 20°)
MAX_DH = 170.0                # 單邊色相偏移的搜尋上限(度)
DE_TOL = 0.02                 # 二分搜尋的 ΔE00 容忍度


# ================= 色彩空間轉換(D65 / 2°, sRGB) =================

_XN, _YN, _ZN = 95.047, 100.000, 108.883
_DELTA = 6.0 / 29.0


def _f_inv(t):
    return t ** 3 if t > _DELTA else 3.0 * _DELTA ** 2 * (t - 4.0 / 29.0)


def _f_fwd(t):
    return t ** (1.0 / 3.0) if t > _DELTA ** 3 else t / (3.0 * _DELTA ** 2) + 4.0 / 29.0


def _gamma(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055


def _gamma_inv(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


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


def rgb01_to_lab(rgb):
    """sRGB(0~1) -> CIELAB。"""
    r, g, b = (_gamma_inv(min(max(v, 0.0), 1.0)) for v in rgb)
    x = (0.4124564 * r + 0.3575761 * g + 0.1804375 * b) * 100.0 / _XN
    y = (0.2126729 * r + 0.7151522 * g + 0.0721750 * b) * 100.0 / _YN
    z = (0.0193339 * r + 0.1191920 * g + 0.9503041 * b) * 100.0 / _ZN
    fx, fy, fz = _f_fwd(x), _f_fwd(y), _f_fwd(z)
    return (116.0 * fy - 16.0, 500.0 * (fx - fy), 200.0 * (fy - fz))


def in_gamut(lab, tol=1e-6):
    """三個通道都落在 [0,1] 才算在 sRGB 色域內。"""
    return all(-tol <= v <= 1.0 + tol for v in lab_to_rgb01(lab))


def lab_to_hex(lab):
    r, g, b = (int(round(min(max(v, 0.0), 1.0) * 255)) for v in lab_to_rgb01(lab))
    return "#{:02X}{:02X}{:02X}".format(r, g, b)


def hex_to_lab(hex_str):
    """'#RRGGBB' -> CIELAB(用來把既有 CSV 的色碼還原回 Lab 重算色差)。"""
    s = hex_str.lstrip("#")
    return rgb01_to_lab(tuple(int(s[i:i + 2], 16) / 255.0 for i in (0, 2, 4)))


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


def lab_to_lch(lab):
    """Lab -> (L, C, h_deg)。"""
    L, a, b = lab
    return (L, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360)


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


def hue_dist(h1, h2):
    """兩個色相角的環狀距離(0~180)。"""
    d = abs(h1 - h2) % 360
    return min(d, 360 - d)


# ================= 色域檢查 =================

def hue_gaps(L=L_STAR, C=30.0, step=0.5):
    """
    掃整個色相圈,回傳「超出 sRGB 色域」的色相區段 [(起, 迄), ...]。
    回傳空 list = 整圈都可用。
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


def n_hues_out_of_gamut(L=L_STAR, C=30.0, step=0.5):
    """整圈中有幾個取樣點出色域(給診斷用)。"""
    n = int(round(360 / step))
    return sum(1 for i in range(n) if not in_gamut(lch_to_lab(L, C, i * step)))


def max_safe_chroma(L=L_STAR, step=0.5, hue_step=0.5):
    """回傳在亮度 L 下,整圈色相都還在 sRGB 色域內的最大 C*。"""
    C = 0.0
    while C + step < 128 and not hue_gaps(L, C + step, hue_step):
        C += step
    return C


def check_chroma_range(L, c_range):
    """C* 範圍是否整段都在色域安全區內;不是就丟 ValueError(附建議上限)。"""
    lo, hi = (c_range, c_range) if isinstance(c_range, (int, float)) else c_range
    safe = max_safe_chroma(L)
    if hi > safe:
        raise ValueError(
            "C* 上限 {} 超過 L*={} 的安全值 {:.1f}(C*={} 時有 {} / 720 個色相出 sRGB 色域,"
            "會被 clip 成彩度較低的顏色)。請把上限降到 {:.1f} 以下。".format(
                hi, L, safe, hi, n_hues_out_of_gamut(L, hi), safe))
    if lo <= 0:
        raise ValueError("C* 下限必須 > 0(C*=0 是灰色,沒有色相可言)")
    return True


# ================= 給定 ΔE00 反解顏色(核心) =================

def max_dE00_reachable(h_center, L=L_STAR, C=30.0, direction=1, max_dh=MAX_DH):
    """
    從 h_center 往 direction 方向最多走 max_dh 度時,可達到的最大 ΔE00。
    要求的 ΔE00 超過這個值時就無解(find_hue_offset 會明確報錯)。
    """
    base = lch_to_lab(L, C, h_center)
    return delta_e00(base, lch_to_lab(L, C, h_center + direction * max_dh))


def find_hue_offset(h_center, target_dE00, L=L_STAR, C=30.0, direction=1,
                    max_dh=MAX_DH, tol=DE_TOL, max_iter=80):
    """
    單邊二分搜尋:從 h_center 往 direction(+1 / -1)方向找出色相偏移 Δh,
    使該色與 h_center 的 CIEDE2000 色差 = target_dE00。

    回傳 Δh(度,恆為正的大小;方向由 direction 決定)。

    為什麼要二分搜尋:ΔE00 不是色相角的線性函數(S_H、T、R_T 項會隨色相變),
    同樣的 ΔE00 在不同色相位置需要的 Δh 差到 1.27~1.31 倍。
    """
    if target_dE00 <= 0:
        raise ValueError("target_dE00 必須 > 0")
    reachable = max_dE00_reachable(h_center, L, C, direction, max_dh)
    if target_dE00 > reachable:
        raise ValueError(
            "h={:.1f}° 往 {:+d} 方向、Δh 上限 {}° 時最多只能達到 ΔE00 = {:.2f},"
            "無法達到要求的 {:.2f}。請放寬 max_dh、提高 C*,或降低目標 ΔE00。".format(
                h_center, direction, max_dh, reachable, target_dE00))

    base = lch_to_lab(L, C, h_center)
    lo, hi = 0.0, max_dh
    mid = hi
    for _ in range(max_iter):
        mid = (lo + hi) / 2
        d = delta_e00(base, lch_to_lab(L, C, h_center + direction * mid))
        if abs(d - target_dE00) < tol:
            return mid
        if d < target_dE00:
            lo = mid
        else:
            hi = mid
    return mid


def color_at_dE00(target_lab, target_dE00, direction=1, max_dh=MAX_DH,
                  tol=DE_TOL, max_iter=80):
    """
    給定 target 顏色與想要的 ΔE00,沿色相環解出 foil 顏色。
    target 的 L*、C* 會被沿用(所以 foil 與 target 只差色相)。

    回傳 dict:
      hex / lab / rgb / rgb1 / hue / dhue / direction
      dE00_actual / dE76_actual   <- 實際達成的色差(務必記錄進資料)
      dE00_requested / in_gamut
    """
    L, C, h0 = lab_to_lch(target_lab)
    dh = find_hue_offset(h0, target_dE00, L, C, direction, max_dh, tol, max_iter)
    h_foil = (h0 + direction * dh) % 360
    lab = lch_to_lab(L, C, h_foil)
    return {
        "hex": lab_to_hex(lab),
        "lab": tuple(round(v, 4) for v in lab),
        "rgb": tuple(round(v, 4) for v in lab_to_psychopy_rgb(lab)),
        "rgb1": tuple(round(v, 4) for v in lab_to_rgb1(lab)),
        "hue": round(h_foil, 3),
        "dhue": round(direction * dh, 3),
        "direction": direction,
        "L_star": round(L, 3),
        "C_star": round(C, 3),
        "dE00_requested": target_dE00,
        "dE00_actual": round(delta_e00(target_lab, lab), 4),
        "dE76_actual": round(delta_e76(target_lab, lab), 4),
        "in_gamut": in_gamut(lab),
    }


def random_target_color(rng=None, L=L_STAR, C_range=C_STAR_RANGE, hue_range=(0.0, 360.0)):
    """
    隨機抽一個 target 顏色:色相在 hue_range 內均勻隨機,
    C* 在 C_range 內小幅隨機(單一數值則固定),L* 固定。

    C* 隨機只在 trial 之間變動 —— target 與它的 foil 共用同一個 C*,
    所以 trial 內的區辨仍然只靠色相,不會多出彩度線索。
    """
    rng = rng or random
    check_chroma_range(L, C_range)
    lo, hi = (C_range, C_range) if isinstance(C_range, (int, float)) else C_range
    C = rng.uniform(lo, hi)
    h = rng.uniform(*hue_range) % 360
    lab = lch_to_lab(L, C, h)
    return {
        "hex": lab_to_hex(lab),
        "lab": tuple(round(v, 4) for v in lab),
        "rgb": tuple(round(v, 4) for v in lab_to_psychopy_rgb(lab)),
        "rgb1": tuple(round(v, 4) for v in lab_to_rgb1(lab)),
        "hue": round(h, 3),
        "L_star": round(L, 3),
        "C_star": round(C, 3),
        "in_gamut": in_gamut(lab),
    }


# ================= 自我檢查 =================

if __name__ == "__main__":
    import csv
    import os

    HERE = os.path.dirname(os.path.abspath(__file__))
    ok = lambda b: "OK" if b else "FAIL"

    # --- 1) CIEDE2000 對 Sharma, Wu & Dalal (2005) 的標準測試值 ---
    print("1) CIEDE2000 對 Sharma et al. (2005) 標準值:")
    for lab1, lab2, expect in [
            ((50.0000, 2.6772, -79.7751), (50.0000, 0.0000, -82.7485), 2.0425),
            ((50.0000, 3.1571, -77.2803), (50.0000, 0.0000, -82.7485), 2.8615),
            ((50.0000, 2.4900, -0.0010), (50.0000, -2.4900, 0.0009), 7.1792),
            ((50.0000, -1.3802, -84.2814), (50.0000, 0.0000, -82.7485), 1.0000),
            ((60.2574, -34.0099, 36.2677), (60.4626, -34.1751, 39.4387), 1.2644)]:
        got = delta_e00(lab1, lab2)
        print("   expect {:.4f}  got {:.4f}  {}".format(expect, got, ok(abs(got - expect) < 1e-3)))
        assert abs(got - expect) < 1e-3

    # --- 2) 對 colour-science 產出的 CSV 逐列比對(企劃書 §10 階段 C0 驗收條件) ---
    ref_csv = os.path.join(HERE, "data", "bv_candidates_for_advisor.csv")
    print("\n2) 對 data/bv_candidates_for_advisor.csv 重算 ΔE00 / ΔE76(金標準 = colour 套件):")
    if os.path.exists(ref_csv):
        worst00 = worst76 = 0.0
        n_rows = 0
        with open(ref_csv) as f:
            for row in csv.DictReader(f):
                lab1 = tuple(float(v) for v in row["A_Lab"].split(","))
                lab2 = tuple(float(v) for v in row["B_Lab"].split(","))
                worst00 = max(worst00, abs(delta_e00(lab1, lab2) - float(row["dE00"])))
                worst76 = max(worst76, abs(delta_e76(lab1, lab2) - float(row["dE76"])))
                n_rows += 1
        print("   {} 列,ΔE00 最大誤差 {:.5f}、ΔE76 最大誤差 {:.5f}  {}".format(
            n_rows, worst00, worst76, ok(worst00 < 0.01 and worst76 < 0.01)))
        assert n_rows > 0 and worst00 < 0.01 and worst76 < 0.01
    else:
        print("   跳過(找不到 {})".format(ref_csv))

    # --- 3) 重現企劃書 §6.1 的 MOC 網格 ---
    print("\n3) 重現企劃書 §6.1 網格(L*=55, C*=30, h=303°,兩邊各走 Δh/2):")
    for dE_t, dh_doc in [(1.50, 3.47), (2.92, 6.75), (5.68, 13.15),
                         (11.05, 25.72), (21.51, 51.14), (30.00, 73.68)]:
        lo, hi = 0.0, MAX_DH
        for _ in range(80):
            mid = (lo + hi) / 2
            d = delta_e00(lch_to_lab(55, 30, 303 - mid / 2), lch_to_lab(55, 30, 303 + mid / 2))
            lo, hi = (mid, hi) if d < dE_t else (lo, mid)
        print("   ΔE00={:<6} 企劃書 Δh={:<6} 重算 Δh={:.2f}  差 {:+.4f}  {}".format(
            dE_t, dh_doc, mid, mid - dh_doc, ok(abs(mid - dh_doc) < 0.01)))
        assert abs(mid - dh_doc) < 0.01

    # --- 4) 色域上限 ---
    print("\n4) 色域檢查(L* = 55):")
    print("   max_safe_chroma(55) = {:.1f}   (企劃書 §5.2 建議用 30,留有餘裕)".format(
        max_safe_chroma(55.0)))
    print("   C*=30 出界色相數 {} / 720   C*=32 出界 {} / 720 (= 企劃書的 16 / 360)".format(
        n_hues_out_of_gamut(55.0, 30.0), n_hues_out_of_gamut(55.0, 32.0)))
    assert max_safe_chroma(55.0) == 31.5
    assert n_hues_out_of_gamut(55.0, 30.0) == 0
    assert n_hues_out_of_gamut(55.0, 32.0) == 32
    try:
        check_chroma_range(55.0, (28.0, 33.0))
        raise AssertionError("C* 超界時應該要報錯")
    except ValueError:
        print("   C* 範圍超界時正確拋出 ValueError  OK")

    # --- 5) ΔE00 沿色相環是否單調(二分搜尋的前提) ---
    print("\n5) ΔE00 隨 Δh 單調性檢查(二分搜尋的前提):")
    bad_mono = []
    for h0 in range(0, 360, 15):
        for C in (28.0, 30.0, 31.0):
            base = lch_to_lab(55.0, C, h0)
            prev = -1.0
            for i in range(int(MAX_DH * 2) + 1):
                d = delta_e00(base, lch_to_lab(55.0, C, h0 + i * 0.5))
                if d < prev - 1e-9:
                    bad_mono.append((h0, C, i * 0.5))
                    break
                prev = d
    print("   掃 24 個色相 × 3 個 C* × Δh 0~170°:非單調的組合 {} 個  {}".format(
        len(bad_mono), ok(not bad_mono)))
    assert not bad_mono, "ΔE00 非單調,二分搜尋不保證唯一解:{}".format(bad_mono[:5])

    # --- 6) find_hue_offset / color_at_dE00 回代 ---
    print("\n6) 反解回代檢查(要求 ΔE00 -> 解出顏色 -> 重算 ΔE00):")
    rng = random.Random(11)
    worst = 0.0
    for _ in range(200):
        tgt = random_target_color(rng, L=55.0, C_range=(28.0, 31.0))
        want = rng.uniform(1.5, 25.0)
        foil = color_at_dE00(tgt["lab"], want, direction=rng.choice((-1, 1)))
        worst = max(worst, abs(foil["dE00_actual"] - want))
        assert foil["in_gamut"]
    print("   200 次隨機 target × ΔE00 1.5~25:最大偏差 {:.4f}(tol={})  {}".format(
        worst, DE_TOL, ok(worst < DE_TOL)))
    assert worst < DE_TOL

    # --- 7) hex <-> Lab 往返 ---
    print("\n7) Lab -> hex -> Lab 往返(誤差應在 8-bit 量化範圍內):")
    worst_rt = 0.0
    for h in range(0, 360, 7):
        lab = lch_to_lab(55.0, 30.0, h)
        worst_rt = max(worst_rt, delta_e76(lab, hex_to_lab(lab_to_hex(lab))))
    print("   最大往返 ΔE76 = {:.4f}  {}".format(worst_rt, ok(worst_rt < 0.6)))
    assert worst_rt < 0.6

    # --- 8) 同一個 ΔE00 在不同色相需要不同 Δh(企劃書 §5.3 的核心論點) ---
    print("\n8) 同一 ΔE00 在不同色相位置所需的 Δh(L*=55, C*=30):")
    print("   {:>8} {:>8} {:>8} {:>8} {:>8} {:>8}".format(
        "dE00", "h=0°", "h=90°", "h=180°", "h=270°", "max/min"))
    for want in (2.0, 6.0, 10.0, 20.0):
        dhs = [find_hue_offset(h, want, 55.0, 30.0, +1) for h in (0, 90, 180, 270)]
        print("   {:>8} {:>8.2f} {:>8.2f} {:>8.2f} {:>8.2f} {:>8.2f}".format(
            want, dhs[0], dhs[1], dhs[2], dhs[3], max(dhs) / min(dhs)))

    print("\n全部檢核通過。")
