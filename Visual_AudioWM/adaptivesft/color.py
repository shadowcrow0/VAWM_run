"""把校準出來的 ΔE00 換成實際色票。

設計原則(沿用 generate_bv_candidates_for_advisor.py 的作法):
固定 L* 與 C*、**只在色相角上取點**,用 CIEDE2000 當強度。

這樣做的理由是排除混淆變項 —— 舊的 colorpool.py 用 random_lab() 讓
L* ∈ U(40,60)、C* ∈ U(40,60) 自由浮動,又在 Lab 空間隨機方向找 foil,
所以同一個 ΔE 值背後可能是「差在亮度」「差在彩度」「差在色相」三種
完全不同的知覺差異,無法當成單一心理物理維度來擬合心理測量函數。

強度一律用 **CIEDE2000 (ΔE00)**,不用 ΔE76。ΔE76 在藍紫區段
嚴重高估知覺差異,拿它當強度會讓心理測量函數被扭曲。
"""

from __future__ import annotations

import colorsys

import colour
import numpy as np

__all__ = [
    "L_FIXED",
    "C_FIXED",
    "lch_to_lab",
    "lab_to_srgb",
    "in_gamut",
    "to_hex",
    "to_hsv",
    "de00",
    "de76",
    "de00_between_hues",
    "foil_hue_for_de00",
    "make_pair",
    "build_ladder",
]

# 跟 generate_bv_candidates_for_advisor.py 一致,方便兩邊互通
L_FIXED = 55.0
C_FIXED = 38.0


def lch_to_lab(L, C, h_deg):
    h = np.radians(h_deg)
    return np.array([L, C * np.cos(h), C * np.sin(h)], dtype=float)


def lab_to_srgb(lab):
    return colour.XYZ_to_sRGB(colour.Lab_to_XYZ(np.asarray(lab, dtype=float)))


def in_gamut(rgb, tol=1e-6):
    rgb = np.asarray(rgb, dtype=float)
    return bool(np.all(rgb >= -tol) and np.all(rgb <= 1.0 + tol))


def to_hex(rgb):
    r, g, b = np.round(np.clip(np.asarray(rgb, float), 0, 1) * 255).astype(int)
    return f"#{r:02X}{g:02X}{b:02X}"


def to_hsv(rgb):
    r, g, b = np.clip(np.asarray(rgb, float), 0, 1)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return round(h * 360, 1), round(s * 100, 1), round(v * 100, 1)


def de00(lab1, lab2):
    return float(
        colour.delta_E(
            np.asarray(lab1, float), np.asarray(lab2, float), method="CIE 2000"
        )
    )


def de76(lab1, lab2):
    return float(
        colour.delta_E(
            np.asarray(lab1, float), np.asarray(lab2, float), method="CIE 1976"
        )
    )


def de00_between_hues(h1, h2, L=L_FIXED, C=C_FIXED):
    return de00(lch_to_lab(L, C, h1), lch_to_lab(L, C, h2))


def foil_hue_for_de00(
    h_target,
    target_de00,
    L=L_FIXED,
    C=C_FIXED,
    direction=+1,
    max_dh=90.0,
    tol=0.01,
    max_iter=80,
):
    """**單邊**二分搜尋:固定 target 色相不動,找出 ΔE00 剛好等於目標的 foil 色相。

    這跟 generate_bv_candidates_for_advisor.py 的 find_dh_for_target() 不同 ——
    那支是把中心色相往兩邊各推 dh/2(對稱配對),適合「兩個都是刺激」的情境;
    本實驗的 target 是**學過的顏色**、foil 是**探測的顏色**,target 必須固定,
    所以要單邊推。

    回傳 (foil_hue_deg, achieved_de00)。
    """
    if target_de00 <= 0:
        return float(h_target) % 360.0, 0.0

    lab_t = lch_to_lab(L, C, h_target)
    lo, hi = 0.0, float(max_dh)
    mid, achieved = 0.0, 0.0
    for _ in range(max_iter):
        mid = (lo + hi) / 2.0
        achieved = de00(lab_t, lch_to_lab(L, C, h_target + direction * mid))
        if abs(achieved - target_de00) < tol:
            break
        if achieved < target_de00:
            lo = mid
        else:
            hi = mid
    if abs(achieved - target_de00) > 10 * tol:
        raise ValueError(
            f"在 max_dh={max_dh}° 內找不到 ΔE00={target_de00} "
            f"(最接近 {achieved:.3f});請放大 max_dh 或提高 C*。"
        )
    return float((h_target + direction * mid) % 360.0), float(achieved)


def make_pair(h_target, target_de00, L=L_FIXED, C=C_FIXED, direction=+1):
    """回傳一組 (target, foil) 色票 dict,含 hex / Lab / 實際達到的 ΔE00。"""
    h_foil, achieved = foil_hue_for_de00(
        h_target, target_de00, L=L, C=C, direction=direction
    )
    lab_t, lab_f = lch_to_lab(L, C, h_target), lch_to_lab(L, C, h_foil)
    rgb_t, rgb_f = lab_to_srgb(lab_t), lab_to_srgb(lab_f)
    if not (in_gamut(rgb_t) and in_gamut(rgb_f)):
        raise ValueError(
            f"色票超出 sRGB 色域 (h_target={h_target}, ΔE00={target_de00}, "
            f"L*={L}, C*={C});請降低 C* 或換色相區段。"
        )
    return {
        "target_hue": float(h_target % 360.0),
        "foil_hue": h_foil,
        "target_hex": to_hex(rgb_t),
        "foil_hex": to_hex(rgb_f),
        "target_lab": tuple(round(v, 2) for v in lab_t),
        "foil_lab": tuple(round(v, 2) for v in lab_f),
        "de00": round(achieved, 3),
        "de76": round(de76(lab_t, lab_f), 3),
        "dhue": round(abs(((h_foil - h_target + 180) % 360) - 180), 3),
    }


def build_ladder(
    de00_levels,
    hue_centers,
    L=L_FIXED,
    C=C_FIXED,
    both_directions=True,
):
    """產生 MOC 校準用的階梯刺激。

    參數
    ----
    de00_levels : 序列
        強度層級(ΔE00)。含 0 的話會產生 match trial(target 與 probe 同色)。
    hue_centers : 序列
        要用哪些色相當 target。多個色相可以平均掉個別色相的特異性。
    both_directions : bool
        True 時每個 (色相, ΔE00) 都產生順時針與逆時針兩個 foil,
        避免受試者學到「probe 總是偏紫的那邊」這種方向性策略。

    回傳
    ----
    list[dict],每個 dict 是一個刺激條件,可直接寫成 PsychoPy 的
    conditions CSV(欄位:intensity, target_hex, foil_hex, is_match, ...)。
    """
    directions = (+1, -1) if both_directions else (+1,)
    rows = []
    for h in hue_centers:
        for d in de00_levels:
            if d <= 0:
                lab = lch_to_lab(L, C, h)
                hex_ = to_hex(lab_to_srgb(lab))
                rows.append(
                    {
                        "intensity": 0.0,
                        "target_hue": float(h % 360.0),
                        "foil_hue": float(h % 360.0),
                        "target_hex": hex_,
                        "foil_hex": hex_,
                        "de00": 0.0,
                        "de76": 0.0,
                        "dhue": 0.0,
                        "direction": 0,
                        "is_match": 1,
                    }
                )
                continue
            for sign in directions:
                p = make_pair(h, d, L=L, C=C, direction=sign)
                p.update(intensity=float(d), direction=sign, is_match=0)
                rows.append(p)
    return rows
