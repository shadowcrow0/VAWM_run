"""
中文版 Figure 1（照 GRTv3_ada 流程圖的版式）：A 整場流程、B 單一試次斜階梯螢幕序列、C 時間軸。
數字來自 VAWM_nobox.py（study 4.3 s、探測 3.3 s、作答窗 0.5–2.5 s、每組 9 個探測、6 blocks × 24 組）
與 VAWM_calibrate.py（72 試 / 區塊、作答最長 3 s、回饋 0.8 s）。

    python figures/make_procedure_figure_zh.py     # → figures/experiment_procedure_zh.svg / .png
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle, Arc

HERE = os.path.dirname(os.path.abspath(__file__))
for p in ("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",):
    if os.path.exists(p):
        font_manager.fontManager.addfont(p)
plt.rcParams["font.family"] = ["WenQuanYi Zen Hei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

INK, GREY, SCREEN = "#333333", "#666666", "#7a7a7a"
C1, C2 = "#9b59b6", "#3f51b5"          # 兩個學習顏色（示意）

fig = plt.figure(figsize=(20, 12.5))
gs = fig.add_gridspec(3, 1, height_ratios=[1.0, 5.4, 0.9], hspace=0.10)

# ───────────────────────────── A. 整場流程 ─────────────────────────────
ax = fig.add_subplot(gs[0]); ax.set_xlim(0, 100); ax.set_ylim(0, 10); ax.axis("off")
ax.text(0, 9.6, "A. 整場流程（VAWM_calibrate.py → make_adaptive_blocks.py → VAWM_nobox.py）", fontsize=12, va="top", color=INK)
stages = [
    (0,   7,  "說明",          "Intro + 指導語",                                   "#eeeeee"),
    (9,   15, "Part 1 顏色校準", "72 試 · 6 個 ΔE 層級 × 8 + 24 試 AA\n聲音 = 目標音 · 有回饋",  "#dde3f3"),
    (26,  5,  "擬合",          "lnrm2\n20–40 s",                                   "#e6e6e6"),
    (33,  15, "Part 2 聲音校準", "72 試 · 6 個混淆層級 × 8 + 24 試 AA\n顏色 = 目標色 · 有回饋", "#e8dcf0"),
    (50,  5,  "擬合",          "lnrm2\n20–40 s",                                   "#e6e6e6"),
    (57,  11, "練習",          "5 組 × 9 探測\n有回饋 1 s",                         "#f3e8d3"),
    (70,  22, "主實驗",        "6 blocks × 24 組 × 9 探測 = 1296\n無回饋 · block 間休息", "#dcefd9"),
    (94,  6,  "結束",          "存檔",                                             "#eeeeee"),
]
for x, w, t, s, c in stages:
    ax.add_patch(FancyBboxPatch((x, 3.2), w, 5.0, boxstyle="round,pad=0,rounding_size=0.4", fc=c, ec=GREY, lw=1))
    ax.text(x + w / 2, 7.2, t, ha="center", va="center", fontsize=10, color=INK)
    ax.text(x + w / 2, 5.0, s, ha="center", va="center", fontsize=7.2, color=GREY)
for i in range(len(stages) - 1):
    x0 = stages[i][0] + stages[i][1]; x1 = stages[i + 1][0]
    ax.add_patch(FancyArrowPatch((x0 + 0.2, 5.7), (x1 - 0.2, 5.7), arrowstyle="-|>", mutation_scale=12, color=INK, lw=1.2))
    if stages[i + 1][2] in ("練習", "主實驗") or stages[i][2].startswith("Part"):
        ax.text((x0 + x1) / 2, 6.5, "rest", ha="center", va="bottom", fontsize=6.5, color=GREY)
ax.text(0, 1.6, "每個階段的每一試都是同一套流程 (B)。校準試次只有 1 個探測、只變被校的那一維（Part 1 變顏色、Part 2 變聲音），"
                "另一維與目標相同；主實驗每組 study 後連續 9 個探測。回饋只在校準與練習。", fontsize=8.5, color=INK, va="center")

# ───────────────────────────── B. 單一試次（斜階梯） ─────────────────────────────
ax = fig.add_subplot(gs[1]); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
ax.text(0, 99, "B. 單一試次（主實驗示例；時間為螢幕上的相對時間，y = 相同、n = 不同）", fontsize=12, va="top", color=INK)

W, H = 9.2, 13.0           # 螢幕寬高（軸座標）
DX, DY = 10.6, 6.0         # 階梯位移（DX > W：相鄰螢幕不重疊）


def speaker(ax, x, y, s=1.0, strike=False):
    body = Polygon([(x, y - 0.5 * s), (x + 0.5 * s, y - 0.5 * s), (x + 1.2 * s, y - 1.1 * s), (x + 1.2 * s, y + 1.1 * s),
                    (x + 0.5 * s, y + 0.5 * s), (x, y + 0.5 * s)], closed=True, fc="white", ec="white")
    ax.add_patch(body)
    for r in (0.9, 1.5):
        ax.add_patch(Arc((x + 1.3 * s, y), r * s, 1.6 * r * s, theta1=-45, theta2=45, color="white", lw=1.0))


def patch(ax, x, y, colour, s=1.0):
    ax.add_patch(Rectangle((x - 1.1 * s, y - 1.6 * s), 2.2 * s, 3.2 * s, fc=colour, ec="#bbbbbb", lw=0.5))


def screen(ax, i, title, t, note="", content=None, dashed=False, frame=None):
    x = 1 + i * DX; y = 86 - i * DY
    ax.add_patch(Rectangle((x + 0.4, y - H - 0.4), W, H, fc="#bdbdbd", ec="none"))          # 陰影
    ax.add_patch(Rectangle((x, y - H), W, H, fc=SCREEN, ec=INK, lw=1.2, ls="--" if dashed else "-"))
    cx, cy = x + W / 2, y - H / 2
    for kind, args in (content or []):
        if kind == "fix":
            ax.text(cx, cy, "+", color="white", ha="center", va="center", fontsize=16)
        elif kind == "patchL":
            patch(ax, x + 0.28 * W, cy, args)
        elif kind == "patchR":
            patch(ax, x + 0.72 * W, cy, args)
        elif kind == "patchC":
            patch(ax, cx - 0.6, cy + 0.6, args)
        elif kind == "spk":
            speaker(ax, cx + 0.2 if args is None else args[0], cy if args is None else args[1])
        elif kind == "text":
            ax.text(cx, cy, args, color="white", ha="center", va="center", fontsize=9)
        elif kind == "yn":
            ax.text(cx, cy + 2.2, "相同？", color="white", ha="center", va="center", fontsize=8)
            ax.text(cx, cy - 1.6, "[y] 相同   [n] 不同", color="white", ha="center", va="center", fontsize=7.5)
    if frame:
        ax.add_patch(Rectangle((cx - 2.0, cy - 2.4), 4.0, 4.6, fc="none", ec="white", lw=1.6))
    ax.text(cx, y - H - 1.6, title, ha="center", va="top", fontsize=10, color=INK)
    ax.text(cx, y - H - 4.6, t, ha="center", va="top", fontsize=8, color=GREY)
    if note:
        ax.text(cx, y - H - 7.4, note, ha="center", va="top", fontsize=7, color=GREY, linespacing=1.25)
    return x, y


screens = [
    ("注視",      "0 – 0.3 s",   "",                       [("fix", None)], False),
    ("學習 顏色 1", "0.3 – 1.3 s", "左側，1 s",             [("patchL", C1)], False),
    ("學習 顏色 2", "1.3 – 2.3 s", "右側，1 s",             [("patchR", C2)], False),
    ("學習 聲音 1", "2.3 – 3.3 s", "子音 1，螢幕空白",       [("spk", None)], False),
    ("學習 聲音 2", "3.3 – 4.3 s", "子音 2，螢幕空白",       [("spk", None)], False),
    ("注視",      "0 – 0.3 s",   "探測前",                 [("fix", None)], False),
    ("探測",      "0.3 – 1.3 s", "一個色塊 + 一個子音\n同時出現", [("patchC", C1), ("spk", (None, None))], False),
    ("作答",      "0.5 – 2.5 s", "y = 相同，n = 不同\n（校準最長 3 s）", [("yn", None)], False),
    ("回饋",      "1 s",         "只在校準與練習\n（校準 0.8 s）", [("text", "Correct")], True),
]
pos = []
for i, (title, t, note, content, dashed) in enumerate(screens):
    if title == "探測":
        content = [("patchC", C1), ("spk", (1 + i * DX + W / 2 + 1.0, 86 - i * DY - H / 2 + 0.6))]
    pos.append(screen(ax, i, title, t, note, content, dashed))

# 學習期：橫線在螢幕 1–4 上方
x1_, y1_ = pos[1]; x4_, y4_ = pos[4]
ax.plot([x1_, x4_ + W], [y1_ + 1.5, y1_ + 1.5], color=INK, lw=1)
ax.plot([x1_, x1_], [y1_ + 1.5, y1_ + 0.5], color=INK, lw=1); ax.plot([x4_ + W, x4_ + W], [y1_ + 1.5, y1_ + 0.5], color=INK, lw=1)
ax.text((x1_ + x4_ + W) / 2, y1_ + 2.3, "學習期 4.3 s：兩個顏色（左、右各 1 s）+ 兩個子音（各 1 s）；四個項目每試重抽，兩色相距 ≥ 20 ΔE，兩個子音不同",
        ha="center", va="bottom", fontsize=8, color=INK)
# 探測段：橫線在螢幕 5–8 上方
x5, y5 = pos[5]; x8, y8 = pos[8]
ax.plot([x5, x8 + W], [y5 + 1.5, y5 + 1.5], color=INK, lw=1)
ax.plot([x5, x5], [y5 + 1.5, y5 + 0.5], color=INK, lw=1); ax.plot([x8 + W, x8 + W], [y5 + 1.5, y5 + 0.5], color=INK, lw=1)
ax.text((x5 + x8 + W) / 2, y5 + 2.3, "探測段 3.3 s：主實驗每組重複 9 次（每次換一種探測類型，順序打散）；校準只做 1 次",
        ha="center", va="bottom", fontsize=8, color=INK)
# 細節說明：放在階梯左下方的空白
notes = [
    "探測內容",
    "  主實驗：九種之一 —— AA（色、音都與某個學習項目相同）、",
    "    HA / LA（只有顏色不同，H 易 / L 難）、AH / AL（只有聲音不同）、",
    "    HH / HL / LH / LL（兩者都不同，2 × 2 雙因子格）",
    "  校準 Part 1（顏色）：顏色 = 某個目標色 ± x，聲音 = 該目標自己的子音",
    "  校準 Part 2（聲音）：聲音 = 某個目標子音的 foil，顏色 = 該目標自己的顏色",
    "  兩個校準都夾 1/3 的 AA 試（探測 = 目標），用來估假警報率",
    "作答：探測出現後 0.5 s 開放；主實驗最長 2 s，校準最長 3 s",
    "回饋：校準 0.8 s、練習 1 s；主實驗沒有回饋",
]
for k, line in enumerate(notes):
    ax.text(1, 29 - k * 3.3, line, ha="left", va="top", fontsize=8, color=INK if not line.startswith("  ") else GREY)
# 時間箭頭（對角線，在螢幕下方）
x0_, y0_ = pos[0]
x2_, y2_ = pos[2]
ax.add_patch(FancyArrowPatch((x2_, y2_ - H - 12), (x8 + W + 1, y8 - H - 12), arrowstyle="-|>", mutation_scale=14, color="#999999", lw=1))   # 與階梯平行
ax.text(x8 + W + 1.5, y8 - H - 12.8, "時間 →", ha="left", va="top", fontsize=8, color=GREY)
# 下一試
ax.add_patch(FancyArrowPatch((x8 + W + 0.5, y8 - H / 2), (x8 + W + 3.5, y8 - H / 2), arrowstyle="-|>", mutation_scale=12, color=INK, lw=1.2))
ax.text(x8 + W + 4, y8 - H / 2 + 0.8, "下一個探測 / 下一組", ha="left", va="bottom", fontsize=8, color=INK)
ax.text(x8 + W + 4, y8 - H / 2 - 0.8, "（9 個探測後換下一組 study；\nblock 結束則休息）", ha="left", va="top", fontsize=7, color=GREY)

# ───────────────────────────── C. 時間軸 ─────────────────────────────
ax = fig.add_subplot(gs[2]); ax.set_xlim(0, 100); ax.set_ylim(0, 10); ax.axis("off")
ax.text(0, 9.6, "C. 時間軸（一組 study + 一個探測；主實驗探測段 ×9）", fontsize=12, va="top", color=INK)
segs = [("注視", 0.3, "#f2f2f2"), ("學習（4 × 1 s：色 1、色 2、音 1、音 2）", 4.0, "#dde3f3"),
        ("注視", 0.3, "#f2f2f2"), ("探測 色+音", 1.0, "#e8dcf0"), ("作答（0.5 s 起，至 2.5 s）", 1.5, "#f3e8d3"),
        ("回饋（校準 / 練習）", 1.0, "#dcefd9")]
scale = 70 / sum(s for _, s, _ in segs)
x = 0
ticks = [0.0]
for lab, dur, c in segs:
    w = dur * scale
    ax.add_patch(Rectangle((x, 3.5), w, 3.5, fc=c, ec=GREY, lw=1, ls="--" if lab.startswith("回饋") else "-"))
    ax.text(x + w / 2, 5.25, lab, ha="center", va="center", fontsize=8 if w > 6 else 7, color=INK)
    x += w
    ticks.append(ticks[-1] + dur)
labels = ["0", "0.3", "4.3", "4.6", "5.6", "7.1", "8.1 s"]
for i, tk in enumerate(ticks):
    dx = 1.2 if labels[i] in ("0.3", "4.6") else 0.0          # 短段的刻度往右挪一點，免得跟前一個刻度疊在一起
    ax.text(tk * scale + dx, 3.0, labels[i], ha="center", va="top", fontsize=7, color=GREY)
ax.text(0, 0.6, "校準試次：同一條軸，探測只做 1 次、作答最長 3 s、回饋 0.8 s。主實驗：沒有回饋，探測段（注視 → 探測 → 作答）連續 9 次。",
        fontsize=8, color=INK, va="center")

fig.savefig(os.path.join(HERE, "experiment_procedure_zh.svg"), bbox_inches="tight")
fig.savefig(os.path.join(HERE, "experiment_procedure_zh.png"), dpi=170, bbox_inches="tight")
print("saved")
