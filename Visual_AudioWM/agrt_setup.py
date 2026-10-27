"""適用於 2x2 適應式 GRT 實驗的「知覺均勻色彩軸」。

AGRT 適應式程序(Glavan et al.)每個 trial 會在一條連續的純量座標上提出一個
刺激值,而它的模型假設:

    (a) 知覺平均數等於物理座標,而且
    (b) 知覺標準差在整個範圍上是同一個常數。

CIELAB 的色相角**並非**知覺均勻:h=250 附近的一度跟 h=310 附近的一度,
在知覺距離上差很多(見 validate(),目前設定下大約有 54% 的落差)。
若直接把「度數」餵給 AGRT,就會默默違反假設 (b)。

因此本模組把色彩維度定義成**以錨點色相為起點、帶正負號的 CIEDE2000(dE00)
弧長**。座標 0 就是錨點色;+1 表示朝色相角增加的方向再走一個 dE00 單位,
-1 則是反方向。L* 與 C* 全程固定,沿著這條軸唯一變動的只有色相角 ——
這正是讓它成為一條「純色相」一維向度的關鍵(排除亮度/彩度混淆)。

設計與常數沿用 generate_bv_candidates_for_advisor.py(老闆已定案的藍紫色區域),
兩個檔案對同一組 (L, C, h) 會產生完全一致的 sRGB。

對外 API
--------
de00_to_hex(arc)        -> '#RRGGBB'(本實驗的 Builder 元件用 colorSpace='hex')
de00_to_rgb(arc)        -> np.ndarray,3 個 0..1 的浮點數
hue_for(arc)            -> 該弧長座標對應的 CIELCh 色相角(度)
arc_range()             -> LUT 可表示的 (min, max) 弧長座標
arc_range_in_gamut()    -> 其中「不需裁切就能顯示」的子範圍(建議用這個限制 AGRT)
is_in_gamut(arc)        -> bool,該座標是否無需裁切即可顯示
validate()              -> 印出完整的設定檢查報告

PsychoPy Builder 典型用法(Begin Routine):

    import agrt_setup
    colour_patch.fillColor = agrt_setup.de00_to_hex(agrt_proposed_value)

色彩管理全程使用 D65 / CIE 1931 2 度觀察者。

注意:變數名、函式名一律保持 ASCII 英文(後續要用 R 做 GRT 分析,
中文欄位名會出問題);只有給人看的註解與輸出文字用繁體中文。
"""

import csv
import os

import numpy as np
import colour

# ---------------------------------------------------------------------------
# 設定區 —— 要換色彩區域,只改這一塊就好。
# ---------------------------------------------------------------------------
# 下游的一切(LUT、色域、弧長範圍)都由這四個數字推導出來,
# 改完之後執行 `python3 agrt_setup.py` 重新檢查色域與可用範圍。

# 錨點色相角(CIELCh,度),弧長座標 0 就落在這裡。
#
# ★ 這是最可能要調整的參數,但目前這個值是有理由選定的,不要隨手改。
#
#   選 303.0 的依據:colorWM.md 的 Q2 段落(以及 Bae et al., 2015)。
#
#   ⚠⚠ 不要改回 283.0 ⚠⚠
#      283 度是「藍/紫」的類別邊界。範疇知覺(categorical perception)文獻的
#      核心發現是:跨類別的配對即使物理色差一樣小,也會因為兩色「有不同的
#      顏色名字」(一個叫藍、一個叫紫)而變得更容易區分。本研究的前提正是
#      「口語分不出來、但知覺上可辨」,若把刺激放在邊界上,等於直接送給
#      受試者一個現成的語言標籤去區分,與研究目的直接矛盾。
#
#   為什麼是 303 而不是 293:
#      兩者都在「紫」這個類別內側,但 293 度的藍色分量仍偏高(#787FC1 那種),
#      部分受試者仍會標成「藍紫」甚至「藍」,還是落在邊界的模糊區;
#      303 度(#887BBC 那種)已明顯偏紫/薰衣草,同一類別標籤的一致性較高。
#      距離上 293 離邊界只有 10 度,303 有 20 度,安全邊際較大 —— 個體之間
#      對類別邊界的位置本來就有落差,303 比較不會因為個別受試者把邊界劃在
#      不同地方,而讓其中一色被當成跨類別。
#
#   generate_bv_candidates_for_advisor.py 裡已驗證過的候選值(H_CENTERS)
#   為 263 / 273 / 283 / 293 / 303;上述理由排除了 283(邊界)與 293(太近),
#   更偏藍的 263 / 273 離邊界更遠但在另一側(藍的類別內),若要改用務必重跑
#   validate() —— 越往偏藍那端 sRGB 色域越窄,可用弧長會明顯縮短。
ANCHOR_H = 303.0

# L* 與 C* 刻意全程固定,讓這條向度是「純色相角」的操弄,
# 排除亮度與彩度的混淆。數值取自 generate_bv_candidates_for_advisor.py。
LSTAR = 55.0    # = L_FIXED
CSTAR = 38.0    # = C_FIXED

# LUT 涵蓋的色相弧半寬(ANCHOR_H +/- 這個度數)。
#
# ⚠ 注意:在 L*=55 / C*=38 / 錨點 303 度這組設定下,+/-60 度**並不是**整段
#   都在 sRGB 色域內。偏藍那一側大約到 h=250.3 就出界了(該處最大可用 C*
#   只有約 32,小於 38);偏紫那一側 +60 度則完全沒問題。
#   LUT 仍然完整建到 +/-60 度,但請用 arc_range_in_gamut() 而不是 arc_range()
#   去限制 AGRT 的提議值。validate() 會把實際可用的窗口印出來。
SPAN_DEG = 60.0

# LUT 取樣點數。20001 點涵蓋 120 度約為每步 0.006 度,
# 累積 dE00 的弧長積分誤差遠小於 1e-3 單位。
LUT_N = 20001

# 判定出界的容忍值:落在 [0,1] 這個範圍附近的微小誤差只是 XYZ 來回轉換的
# 數值雜訊,不算真的出色域。沿用 generate_bv_candidates_for_advisor.py 的 1e-6。
GAMUT_TOL = 1e-6


# ---------------------------------------------------------------------------
# 色彩轉換 —— 沿用 generate_bv_candidates_for_advisor.py 的慣例
# ---------------------------------------------------------------------------
# lab_to_srgb() 跟該檔一樣,不傳 illuminant,直接吃 colour-science 的預設值。
# 這點已實際驗證過:在 colour-science 0.4.7 裡,Lab_to_XYZ 與 XYZ_to_sRGB 的
# 預設 illuminant 都是 D65 / CIE 1931 2 度觀察者 (0.3127, 0.3290),
# 跟明確傳入 CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['D65']
# 在整段弧上的差異是 0.0(完全相同)。因此「沿用預設」與「明確指定 D65」
# 兩條路徑等價,這裡選擇沿用預設,好讓兩個檔案的寫法一致。

D65 = colour.CCS_ILLUMINANTS["CIE 1931 2 Degree Standard Observer"]["D65"]


def lch_to_lab(L, C, h_deg):
    """CIELCh -> CIELab。與 generate_bv_candidates_for_advisor.py 同義,

    但額外支援 h_deg 傳入陣列(純量輸入時回傳 shape (3,),與該檔行為一致)。
    """
    h = np.radians(np.asarray(h_deg, dtype=float))
    L_arr = np.broadcast_to(np.asarray(L, dtype=float), h.shape)
    C_arr = np.broadcast_to(np.asarray(C, dtype=float), h.shape)
    return np.stack([L_arr, C_arr * np.cos(h), C_arr * np.sin(h)], axis=-1)


def lab_to_srgb(lab):
    """CIELab -> 未裁切的 gamma 編碼 sRGB(可能落在 [0,1] 之外)。"""
    return colour.XYZ_to_sRGB(colour.Lab_to_XYZ(lab))


def srgb_to_lab(rgb):
    """gamma 編碼 sRGB(0..1)-> CIELab,是 lab_to_srgb 的反向路徑。"""
    return colour.XYZ_to_Lab(colour.sRGB_to_XYZ(np.asarray(rgb, dtype=float)))


def de00(lab1, lab2):
    """兩個 CIELab 之間的 CIEDE2000 色差(與該檔同名同義)。"""
    return colour.delta_E(np.asarray(lab1, dtype=float),
                          np.asarray(lab2, dtype=float), method="CIE 2000")


def in_gamut(rgb, tol=GAMUT_TOL):
    """判斷(未裁切的)sRGB 值是否落在色域內。"""
    rgb = np.asarray(rgb, dtype=float)
    return bool(np.all(rgb >= -tol) and np.all(rgb <= 1.0 + tol))


def to_hex(rgb):
    """0..1 浮點 sRGB -> '#RRGGBB'(取整方式與該檔完全相同)。"""
    r, g, b = np.round(np.clip(np.asarray(rgb, dtype=float), 0, 1) * 255).astype(int)
    return f"#{r:02X}{g:02X}{b:02X}"


# ---------------------------------------------------------------------------
# 在 import 時建立弧長 LUT(這是本模組唯一的 import 副作用)
# ---------------------------------------------------------------------------
# 做法:密集取樣色相角 -> 量相鄰樣本之間的 dE00 -> 累加積分 ->
# 平移使錨點色相恰好落在座標 0。得到「色相角 <-> 帶號 dE00 弧長」的對照表。
# 兩個陣列都是嚴格遞增的,所以用 np.interp 可以雙向內插。

_HUE_GRID = np.linspace(ANCHOR_H - SPAN_DEG, ANCHOR_H + SPAN_DEG, LUT_N)
_LAB_GRID = lch_to_lab(LSTAR, CSTAR, _HUE_GRID)
_RGB_GRID = lab_to_srgb(_LAB_GRID)
_STEP_DE00 = de00(_LAB_GRID[:-1], _LAB_GRID[1:])
_ARC_GRID = np.concatenate([[0.0], np.cumsum(_STEP_DE00)])
_ARC_GRID = _ARC_GRID - np.interp(ANCHOR_H, _HUE_GRID, _ARC_GRID)

_ARC_MIN = float(_ARC_GRID[0])
_ARC_MAX = float(_ARC_GRID[-1])

# 錨點色本身,供 round-trip 檢查與報告使用。
ANCHOR_LAB = lch_to_lab(LSTAR, CSTAR, ANCHOR_H)
ANCHOR_HEX = to_hex(np.clip(lab_to_srgb(ANCHOR_LAB), 0, 1))

# 找出「包含錨點、且連續不出色域」的那一段,換算成弧長座標。
# 這才是實際能用的範圍;超出這段的座標仍可算出顏色,但會被裁切。
_OK_GRID = np.all((_RGB_GRID >= -GAMUT_TOL) & (_RGB_GRID <= 1.0 + GAMUT_TOL), axis=-1)
_ANCHOR_IDX = int(np.argmin(np.abs(_HUE_GRID - ANCHOR_H)))
if not _OK_GRID[_ANCHOR_IDX]:
    # 錨點自己就出界的話,整個設定沒有意義,但不在 import 時丟例外
    # (Builder 匯入會直接掛掉),交給 validate() 大聲報告。
    _GAMUT_LO_IDX = _GAMUT_HI_IDX = _ANCHOR_IDX
else:
    _GAMUT_LO_IDX = _ANCHOR_IDX
    while _GAMUT_LO_IDX > 0 and _OK_GRID[_GAMUT_LO_IDX - 1]:
        _GAMUT_LO_IDX -= 1
    _GAMUT_HI_IDX = _ANCHOR_IDX
    while _GAMUT_HI_IDX < LUT_N - 1 and _OK_GRID[_GAMUT_HI_IDX + 1]:
        _GAMUT_HI_IDX += 1

_ARC_GAMUT_MIN = float(_ARC_GRID[_GAMUT_LO_IDX])
_ARC_GAMUT_MAX = float(_ARC_GRID[_GAMUT_HI_IDX])


# ---------------------------------------------------------------------------
# 對外 API
# ---------------------------------------------------------------------------

def arc_range():
    """回傳 LUT 可表示的 (min, max) 弧長座標。

    這是 LUT 的完整範圍。注意即使色相弧是對稱的 +/-SPAN_DEG,弧長範圍也**不**
    對稱於 0 —— 錨點兩側的色相壓縮程度不同,而這正是本模組要吸收掉的非均勻性。

    ⚠ 這個範圍不保證全部在 sRGB 色域內。要限制 AGRT 的提議值,
      請用 arc_range_in_gamut()。
    """
    return (_ARC_MIN, _ARC_MAX)


def arc_range_in_gamut():
    """回傳「不需裁切就能正確顯示」的 (min, max) 弧長座標。

    這是包含錨點的最大連續區間。實驗上真正可用的就是這一段,
    建議直接拿它來夾住 AGRT 的提議範圍。
    """
    return (_ARC_GAMUT_MIN, _ARC_GAMUT_MAX)


# AGRT 推導 beta(知覺標準差)搜尋上限時用的除數。出處是 AGRT.py 的
#   dim1betaRange = [0, (np.average(dim1range) - dim1range[0]) / (sqrt(2)*erfinv(...))]
# 分子 np.average(dim1range) - dim1range[0] 是「半範圍」,不是全範圍。
# 分母在 lapse=0.08 時等於 2.3107。
BETA_MAX_DIVISOR = 2.3107


def usable_half_length():
    """回傳以錨點為中心、左右對稱且不出色域的最大半長(dE00)。

    AGRT 會用「半範圍 / 2.3107」當作 beta(知覺標準差)的搜尋上限,
    所以能支撐的最大知覺 SD = 這個半長 / 2.3107。
    注意分子是半範圍 —— 用全範圍去除會把可支撐的 SD 高估一倍。
    """
    return min(-_ARC_GAMUT_MIN, _ARC_GAMUT_MAX)


def max_supportable_sd():
    """回傳這個色彩軸能讓 AGRT 估到的最大知覺標準差(dE00)。

    受試者真實的 SD 若超過這個值,beta 的網格夾不住真值,Psi 會收斂到
    邊界並給出偏誤的估計 —— 就像量程只到 40 度的溫度計量不出 42 度。
    """
    return usable_half_length() / BETA_MAX_DIVISOR


def _check_arc(arc):
    """檢查並轉換弧長座標;超出範圍就明確報錯,不做無聲夾擠。"""
    try:
        arc = float(arc)
    except (TypeError, ValueError):
        raise TypeError(f"arc 必須是單一實數,收到的是 {arc!r}")
    if not np.isfinite(arc):
        raise ValueError(f"arc 必須是有限數值,收到的是 {arc!r}")
    if arc < _ARC_MIN or arc > _ARC_MAX:
        raise ValueError(
            f"弧長座標 {arc:.4f} 超出 LUT 可表示的範圍 "
            f"({_ARC_MIN:.4f}, {_ARC_MAX:.4f}) dE00。"
            f"請加大 SPAN_DEG(目前 {SPAN_DEG:.1f} 度)或限制適應式程序的提議值;"
            f"這裡刻意不做無聲夾擠,以免默默改掉刺激值。")
    return arc


def hue_for(arc):
    """回傳弧長座標 arc 對應的 CIELCh 色相角(度)。

    回傳的角度是「未取模」的:它會落在 ANCHOR_H +/- SPAN_DEG 之間,
    因此可能超出 [0, 360)。這是刻意的 —— 這樣色相角才會隨 arc 嚴格遞增,
    monotonicity 檢查才有意義。後續轉換都只用到角度的 cos/sin,
    未取模的值與其 mod 360 的等價值轉出來的顏色完全相同。
    """
    arc = _check_arc(arc)
    return float(np.interp(arc, _ARC_GRID, _HUE_GRID))


def de00_to_rgb(arc, return_clipped=False):
    """回傳弧長座標 arc 對應的 sRGB,3 個 0..1 的浮點數。

    結果會被裁切到 [0, 1],所以一定畫得出來。把 return_clipped 設成 True
    可以額外拿到一個 bool,說明是否真的發生了裁切 —— 出色域的要求必須是
    「可被偵測」的,而不是無聲無息的。
    """
    rgb_raw = lab_to_srgb(lch_to_lab(LSTAR, CSTAR, hue_for(arc)))
    rgb = np.clip(rgb_raw, 0.0, 1.0)
    if return_clipped:
        return rgb, (not in_gamut(rgb_raw))
    return rgb


def de00_to_hex(arc, return_clipped=False):
    """回傳弧長座標 arc 對應的 '#RRGGBB'。

    本實驗的 PsychoPy Builder 元件就是用 colorSpace='hex',所以這是預設要用的
    形式。return_clipped 的意義同 de00_to_rgb。

    注意 hex 只有 8 bit,量化會損失一點精度;來回轉換的誤差量級約 0.1 dE00
    (實測值見 validate() 說明)。
    """
    if return_clipped:
        rgb, clipped = de00_to_rgb(arc, return_clipped=True)
        return to_hex(rgb), clipped
    return to_hex(de00_to_rgb(arc))


def is_in_gamut(arc):
    """該弧長座標是否無需裁切就能在 sRGB 顯示。"""
    _, clipped = de00_to_rgb(arc, return_clipped=True)
    return not clipped


# ---------------------------------------------------------------------------
# 檢查與報告
# ---------------------------------------------------------------------------

def max_in_gamut_chroma(hue_deg=None, lstar=None, c_max=150.0, step=0.01):
    """回傳在指定 L* 下,各色相角還留在 sRGB 色域內的最大 C*。

    hue_deg 預設是整段設定弧(每 0.5 度取一點)。這個數字告訴你目前的
    C* 還有多少餘裕。
    """
    lstar = LSTAR if lstar is None else lstar
    if hue_deg is None:
        hue_deg = np.arange(ANCHOR_H - SPAN_DEG, ANCHOR_H + SPAN_DEG + 1e-9, 0.5)
    hue_deg = np.atleast_1d(np.asarray(hue_deg, dtype=float))
    chromas = np.arange(0.0, c_max, step)

    out = np.empty(hue_deg.shape, dtype=float)
    for i, h in enumerate(hue_deg):
        rgb = lab_to_srgb(lch_to_lab(lstar, chromas, np.full_like(chromas, h)))
        ok = np.all((rgb >= -GAMUT_TOL) & (rgb <= 1.0 + GAMUT_TOL), axis=-1)
        bad = np.flatnonzero(~ok)
        out[i] = chromas[bad[0] - 1] if bad.size else chromas[-1]
    return out


def de00_per_degree():
    """回傳 (色相角中點, 每度 dE00),取樣自整段設定弧。"""
    step = _HUE_GRID[1] - _HUE_GRID[0]
    mids = 0.5 * (_HUE_GRID[:-1] + _HUE_GRID[1:])
    return mids, _STEP_DE00 / step


def hex_resolution(n_samples=60001):
    """量化色域內可用弧段上,8-bit hex 實際能呈現幾種相異顏色。

    AGRT 提議的是連續值,但螢幕只畫得出有限多個 8-bit 顏色。
    回傳 (相異色數, 相鄰相異色的弧長間距中位數, 最大間距),單位 dE00。
    這決定了這條色彩軸的實際解析度。
    """
    lo, hi = arc_range_in_gamut()
    vals = np.linspace(lo, hi, int(n_samples))
    hues = np.interp(vals, _ARC_GRID, _HUE_GRID)
    rgb = np.clip(lab_to_srgb(lch_to_lab(LSTAR, CSTAR, hues)), 0, 1)
    codes = np.round(rgb * 255).astype(int)
    changed = np.any(np.diff(codes, axis=0) != 0, axis=-1)
    edges = vals[1:][changed]
    if edges.size < 2:
        return int(changed.sum()) + 1, float("nan"), float("nan")
    steps = np.diff(edges)
    return int(changed.sum()) + 1, float(np.median(steps)), float(steps.max())


def pair_for_de00(target):
    """產生一組以錨點為中心、色差約為 target 的色對。

    做法是取弧長座標 -target/2 與 +target/2,也就是在**弧長**上對稱。
    回傳 (hexA, hexB, 實際 dE00)。注意實際 dE00 會比 target 略小:
    弧長是沿著色相路徑的積分長度,而兩端點之間的直線 dE00 是弦長,
    CIEDE2000 沿路徑不可加,色差越大兩者差越多。
    """
    a, b = -0.5 * float(target), 0.5 * float(target)
    lab_a = lch_to_lab(LSTAR, CSTAR, hue_for(a))
    lab_b = lch_to_lab(LSTAR, CSTAR, hue_for(b))
    return to_hex(de00_to_rgb(a)), to_hex(de00_to_rgb(b)), float(de00(lab_a, lab_b))


# 既有候選色票 CSV,用來跟本模組的 LUT 對照(見 validate())。
CANDIDATES_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "data", "bv_candidates_for_advisor.csv")


def _compare_with_candidates_csv():
    """把 LUT 產生的色對跟 bv_candidates_for_advisor.csv 對照。

    只比對 CSV 裡 h_center_deg 等於目前 ANCHOR_H 的那幾組
    (錨點 303 度時就是 set 17/18/19,ΔE00 = 2/4/6)。
    這是本模組與既有刺激之間最直接的一致性驗證。
    """
    if not os.path.exists(CANDIDATES_CSV):
        print(f"  (找不到 {CANDIDATES_CSV},略過此項比對)")
        return
    with open(CANDIDATES_CSV, newline="") as f:
        rows = [r for r in csv.DictReader(f)
                if abs(float(r["h_center_deg"]) - ANCHOR_H) < 1e-9]
    if not rows:
        print(f"  (CSV 裡沒有 h_center_deg = {ANCHOR_H:.1f} 的組別,略過此項比對)")
        return

    print(f"  對照 {os.path.basename(CANDIDATES_CSV)} 中 h={ANCHOR_H:.1f} 的組別:")
    print(f"    {'set':>3} {'目標':>5} | {'CSV A':>8} {'LUT A':>8} "
          f"{'CSV B':>8} {'LUT B':>8} | {'CSV dE':>6} {'LUT dE':>6} {'色相差':>8}")
    for r in rows:
        target = float(r["target_dE00"])
        hex_a, hex_b, achieved = pair_for_de00(target)
        # 他們是在「色相角」上對稱取點,本模組是在「弧長」上對稱,
        # 兩者在小色差下幾乎一致,這裡把色相角的差距也印出來。
        lab_csv_a = np.array([float(x) for x in r["A_Lab"].split(",")])
        h_csv_a = np.degrees(np.arctan2(lab_csv_a[2], lab_csv_a[1])) % 360.0
        dh = abs(h_csv_a - (hue_for(-target / 2) % 360.0))
        flag_a = "同" if hex_a.upper() == r["A_hex"].upper() else "異"
        flag_b = "同" if hex_b.upper() == r["B_hex"].upper() else "異"
        print(f"    {r['set']:>3} {target:>5.1f} | {r['A_hex']:>8} {hex_a:>8}{flag_a} "
              f"{r['B_hex']:>8} {hex_b:>8}{flag_b} | {float(r['dE00']):>6.2f} "
              f"{achieved:>6.2f} {dh:>7.3f}度")


def validate():
    """印出設定檢查報告。每次改完設定區都應該跑一次。"""
    line = "=" * 72
    print(line)
    print("agrt_setup —— 適應式 GRT 的知覺色彩軸設定檢查")
    print(line)
    print(f"設定:錨點色相 h = {ANCHOR_H:.1f} 度,L* = {LSTAR:.1f},"
          f"C* = {CSTAR:.1f},弧半寬 = +/-{SPAN_DEG:.1f} 度")
    print(f"色相涵蓋範圍:{ANCHOR_H - SPAN_DEG:.1f} ~ {ANCHOR_H + SPAN_DEG:.1f} 度")
    print(f"LUT:{LUT_N} 點,每步 {_HUE_GRID[1] - _HUE_GRID[0]:.5f} 度")
    print(f"觀察者/光源:CIE 1931 2 度,D65 {np.round(D65, 4)}(colour-science 預設值)")
    print(f"錨點色:{ANCHOR_HEX}  (Lab {np.round(ANCHOR_LAB, 2)})")
    print()

    # --- 色域 --------------------------------------------------------------
    hues = np.arange(ANCHOR_H - SPAN_DEG, ANCHOR_H + SPAN_DEG + 1e-9, 0.5)
    max_c = max_in_gamut_chroma(hue_deg=hues)
    worst = int(np.argmin(max_c))
    print("-- 色域 ---------------------------------------------------------")
    print(f"L*={LSTAR:.1f} 下整段弧的最大可用 C*:"
          f"最小 {max_c[worst]:.2f}(在 h={hues[worst]:.1f} 度),最大 {max_c.max():.2f}")
    headroom = max_c[worst] - CSTAR
    print(f"目前設定 C* = {CSTAR:.1f} -> 最緊處餘裕 {headroom:+.2f}")

    excursion = max(float(-_RGB_GRID.min()), float(_RGB_GRID.max() - 1.0), 0.0)
    all_ok = bool(np.all(_OK_GRID))
    print(f"整段 +/-{SPAN_DEG:.0f} 度的弧是否都在 sRGB 色域內(不需裁切):"
          f"{'是' if all_ok else '否'}")
    if not all_ok:
        frac = 100.0 * float(np.mean(_OK_GRID))
        print(f"  ⚠ 超出 [0,1] 的最大幅度:{excursion:.6f};"
              f"整段弧只有 {frac:.1f}% 在色域內。")
        print(f"  ⚠ 包含錨點的連續可用色相窗口:"
              f"{_HUE_GRID[_GAMUT_LO_IDX]:.3f} ~ {_HUE_GRID[_GAMUT_HI_IDX]:.3f} 度")
        print(f"    (相對錨點為 -{ANCHOR_H - _HUE_GRID[_GAMUT_LO_IDX]:.3f} / "
              f"+{_HUE_GRID[_GAMUT_HI_IDX] - ANCHOR_H:.3f} 度)")
        print(f"  ⚠ 若要對稱且完全不裁切,SPAN_DEG 最大只能設到 "
              f"{min(ANCHOR_H - _HUE_GRID[_GAMUT_LO_IDX], _HUE_GRID[_GAMUT_HI_IDX] - ANCHOR_H):.2f} 度;"
              f"或降低 C*。")
        print("  ⚠ 請用 arc_range_in_gamut() 而非 arc_range() 來限制 AGRT 的提議值。")
    print()

    # --- 單調性 ------------------------------------------------------------
    d_arc = np.diff(_ARC_GRID)
    mono = bool(np.all(d_arc > 0.0))
    print("-- 弧長 LUT -----------------------------------------------------")
    print(f"是否嚴格單調遞增:{'是' if mono else '否'}"
          f"(最小步長 {d_arc.min():.3e} dE00)")
    print(f"LUT 完整弧長範圍:({_ARC_MIN:.4f}, {_ARC_MAX:.4f}) dE00,"
          f"總長 {_ARC_MAX - _ARC_MIN:.4f}")
    print(f"色域內可用範圍:({_ARC_GAMUT_MIN:.4f}, {_ARC_GAMUT_MAX:.4f}) dE00,"
          f"總長 {_ARC_GAMUT_MAX - _ARC_GAMUT_MIN:.4f}")
    half = usable_half_length()
    print(f"以錨點為中心、對稱可用的半長:{half:.4f} dE00"
          f"(對稱總範圍 {2 * half:.4f} dE00)")
    print(f"AGRT 的 beta 搜尋上限 = 半範圍 / {BETA_MAX_DIVISOR}"
          f"(源自 AGRT.py 的 np.average(dim1range) - dim1range[0]):")
    print(f"  半範圍 {half:.2f} dE00 -> 可支撐的最大知覺 SD 約 "
          f"{max_supportable_sd():.2f} dE00")
    print(f"  分子是「半範圍」而非全範圍;用全範圍去除會把可支撐的 SD 高估一倍。")
    print(f"  參考:視覺工作記憶延宕比較的顏色 SD 文獻範圍約 3~8 dE00,"
          f"因此餘裕{'充足' if max_supportable_sd() >= 8 else '不足'}。")
    n_hex, med_step, max_step = hex_resolution()
    span_g = _ARC_GAMUT_MAX - _ARC_GAMUT_MIN
    print(f"8-bit hex 實際解析度:可用弧段上共 {n_hex} 種相異顏色,"
          f"相鄰間距中位數 {med_step:.4f}(最大 {max_step:.4f})dE00")
    print(f"  也就是每 1 dE00 約 {n_hex / span_g:.1f} 階;"
          f"最小預定色差 2.0 dE00 之內約有 {2.0 * n_hex / span_g:.0f} 階可用。")
    print(f"  AGRT 提議值的精度若細於約 {med_step:.2f} dE00,螢幕上畫出來會是同一個顏色。")
    print()

    # --- 非均勻性 ----------------------------------------------------------
    _, per_deg = de00_per_degree()
    lo, hi = float(per_deg.min()), float(per_deg.max())
    print("-- 色相非均勻性(本模組存在的理由)-----------------------------")
    print(f"每度 dE00:最小 {lo:.4f},最大 {hi:.4f}")
    print(f"整段弧的變異:{100.0 * (hi - lo) / lo:.1f}%(最大/最小 = {hi / lo:.2f} 倍)")
    print(f"也就是說,同樣一度的色相角,在弧的一端所值的知覺距離是另一端的 "
          f"{hi / lo:.2f} 倍 ——")
    print("這正是「直接餵度數給 AGRT」會違反的等變異數假設。")
    print()

    # --- 與既有候選色票對照 ------------------------------------------------
    print("-- 與既有候選色票的一致性 --------------------------------------")
    _compare_with_candidates_csv()
    print(line)


if __name__ == "__main__":
    validate()


# ──────────────────────────────────────────────────────────────
# 匯出查表檔給 PsychoPy 用
# ──────────────────────────────────────────────────────────────

def export_lut(path='agrt_colour_lut.json', step=0.01):
    """把弧長→hex 的對照表寫成 JSON,讓實驗執行時不必安裝 colour-science。

    PsychoPy 內建的 Python 沒有 colour;在實驗裡 import 它會讓整個實驗開不起來。
    離線算好、執行期只用 numpy 查表,就少一個失敗點。
    """
    import json
    lo, hi = arc_range_in_gamut()
    arcs = np.arange(lo, hi + step / 2, step)
    data = {
        'anchor_h': ANCHOR_H, 'lstar': LSTAR, 'cstar': CSTAR,
        'arc_min': float(arcs[0]), 'arc_max': float(arcs[-1]), 'step': step,
        'hex': [de00_to_hex(float(a)) for a in arcs],
    }
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    uniq = len(set(data['hex']))
    print(f"寫入 {path}:{len(arcs)} 點,弧長 {arcs[0]:.3f}~{arcs[-1]:.3f} dE00,"
          f"{uniq} 種相異顏色")
    return path
