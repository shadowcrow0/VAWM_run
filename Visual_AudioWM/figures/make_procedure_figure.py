"""
畫 Figure 1（實驗流程圖）：A 整場流程、B 單一試次時間軸、C 探測類型與 2×2 設計。
所有數字來自 VAWM_nobox.py（study 4.3 s、probe 3.3 s、每組 9 個探測、6 blocks × 24 組）與 VAWM_calibrate.py（72 試、回饋 0.8 s）。

    python figures/make_procedure_figure.py      # 產生 figures/experiment_procedure.svg / .png
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
plt.rcParams["font.family"] = ["DejaVu Sans"]
plt.rcParams["font.size"] = 9
GREY, DARK, LIGHT = "#555555", "#222222", "#f2f2f2"

fig = plt.figure(figsize=(12, 11))
gs = fig.add_gridspec(3, 1, height_ratios=[1.05, 1.5, 1.45], hspace=0.30)

# ───────────────────────────── A. Session structure ─────────────────────────────
ax = fig.add_subplot(gs[0]); ax.set_xlim(0, 100); ax.set_ylim(0, 11); ax.axis("off")
ax.text(0, 10.9, "A  Session structure", fontsize=12, fontweight="bold", va="top")
phases = [
    (0,  16, "Calibration 1\nColour", "72 trials\n6 ΔE levels × 8\n+ 24 match trials\nfeedback every trial", "#cfe2f3"),
    (16, 4,  "fit", "lnrm2\n20–40 s", "#dddddd"),
    (20, 16, "Calibration 2\nSound", "72 trials\n6 confusion levels × 8\n+ 24 match trials\nfeedback every trial", "#cfe2f3"),
    (36, 4,  "fit", "lnrm2\n20–40 s", "#dddddd"),
    (40, 13, "Practice", "5 study sets\n× 9 probes\nfeedback 1 s", "#fde9c9"),
    (53, 47, "Main task", "6 blocks × 24 study sets × 9 probes = 1296 probes\nno feedback; self-paced rest between blocks", "#d9ead3"),
]
for x, w, title, sub, fill in phases:
    ax.add_patch(FancyBboxPatch((x + 0.3, 5.0), w - 0.6, 3.2, boxstyle="round,pad=0.02,rounding_size=0.3", fc=fill, ec=DARK, lw=1))
    ax.text(x + w / 2, 6.6, title, ha="center", va="center", fontsize=9.5 if title != "fit" else 8.5, fontweight="bold")
    ax.text(x + w / 2, 4.6, sub, ha="center", va="top", fontsize=7.0, color=GREY)
ax.annotate("", xy=(100, 0.9), xytext=(0, 0.9), arrowprops=dict(arrowstyle="->", lw=1.2, color=DARK))
ax.text(50, 0.1, "time (one session, roughly 75–90 min)", ha="center", va="bottom", fontsize=8, color=GREY)
ax.text(26.5, 9.2, "H and L levels for colour and sound are set per participant here, then used in the main task",
        ha="center", va="center", fontsize=7.5, color=GREY, style="italic")
ax.annotate("", xy=(60, 8.3), xytext=(52, 8.9), arrowprops=dict(arrowstyle="->", lw=0.8, color=GREY, connectionstyle="arc3,rad=-0.3"))

# ───────────────────────────── B. Trial procedure ─────────────────────────────
ax = fig.add_subplot(gs[1]); ax.set_xlim(0, 100); ax.set_ylim(0, 10); ax.axis("off")
ax.text(0, 9.8, "B  Trial procedure", fontsize=12, fontweight="bold", va="top")


def screen(ax, x, y, w, h, label_below, content):
    ax.add_patch(Rectangle((x, y), w, h, fc="black", ec=DARK, lw=1))
    for kind, args in content:
        if kind == "fix":
            ax.text(x + w / 2, y + h / 2, "+", color="white", ha="center", va="center", fontsize=14)
        elif kind == "patch":
            px, colour = args
            ax.add_patch(Rectangle((x + px * w - 0.09 * w, y + h / 2 - 0.18 * h), 0.18 * w, 0.36 * h, fc=colour, ec="#888888", lw=0.6))
        elif kind == "sound":
            ax.text(x + w / 2, y + h / 2, "♪ " + args, color="white", ha="center", va="center", fontsize=9)
        elif kind == "text":
            ax.text(x + w / 2, y + h / 2, args, color="white", ha="center", va="center", fontsize=7)
    ax.text(x + w / 2, y - 0.4, label_below, ha="center", va="top", fontsize=7.2, color=DARK)


sw, sh, sy = 9.3, 2.5, 5.3
ax.text(0, 8.5, "Study (4.3 s, once per set)", fontsize=9, fontweight="bold", va="center")
study = [("fixation\n300 ms", [("fix", None)]),
         ("colour 1, left\n1000 ms", [("patch", (0.3, "#c4603b"))]),
         ("colour 2, right\n1000 ms", [("patch", (0.7, "#3b8fc4"))]),
         ("sound 1\n1000 ms", [("sound", "/pa/")]),
         ("sound 2\n1000 ms", [("sound", "/ka/")])]
x = 0
for lab, content in study:
    screen(ax, x, sy, sw, sh, lab, content); x += sw + 1.0
px0 = 57
ax.text(px0, 8.5, "Probe (3.3 s, 9 per set)", fontsize=9, fontweight="bold", va="center")
probe = [("fixation\n300 ms", [("fix", None)]),
         ("colour + sound\n1000 ms", [("patch", (0.5, "#c4603b")), ("text", "\n\n\n♪ /ka/")]),
         ("response\n500–2500 ms\ny = same\nn = different", [("text", "y / n")]),
         ("feedback 1000 ms\n(practice and\ncalibration only)", [("text", "Correct")])]
x = px0
for lab, content in probe:
    screen(ax, x, sy, sw, sh, lab, content); x += sw + 1.0
ax.annotate("", xy=(px0 - 0.8, sy + sh / 2), xytext=(52.6, sy + sh / 2), arrowprops=dict(arrowstyle="-|>", lw=1.5, color=DARK))
ax.annotate("", xy=(px0 + 0.2, sy - 2.6), xytext=(x - 1.0, sy - 2.6), arrowprops=dict(arrowstyle="-|>", lw=1.0, color=GREY))
ax.text((px0 + x) / 2, sy - 2.9, "repeat with a new probe type, 9 times", ha="center", va="top", fontsize=7.5, color=GREY, style="italic")
ax.text(0, 1.2, "One study set = study + 9 probes, about 34 s.  Calibration trials use the same study screen, then one probe with a "
                "response window of up to 3 s and 0.8 s feedback.", fontsize=7.5, color=GREY, va="center")
ax.text(0, 0.4, "The 0.3 s fixation before the probe is where GRTv3_ada inserts its 0.3 s audiovisual mask; VAWM shows no mask.",
        fontsize=7.5, color=GREY, va="center")

# ───────────────────────────── C. Probe types / design ─────────────────────────────
ax = fig.add_subplot(gs[2]); ax.set_xlim(0, 100); ax.set_ylim(0, 10); ax.axis("off")
ax.text(0, 9.8, "C  Probe types and the 2 × 2 double-factorial design", fontsize=12, fontweight="bold", va="top")
ax.text(0, 8.5, "Per study set (9 probes, shuffled)", fontsize=9, fontweight="bold", va="center")
rows = [("AA", "colour and sound both match a studied item; correct answer: same", "× 2"),
        ("HA / LA", "colour differs (H = easy, L = hard), sound matches", "× 1 each"),
        ("AH / AL", "sound differs (H / L), colour matches", "× 1 each"),
        ("HH / HL / LH / LL", "both differ: the double-factorial (DFP) cells", "× 3")]
y = 7.5
for code, desc, n in rows:
    ax.add_patch(Rectangle((0, y - 0.55), 14, 1.1, fc=LIGHT, ec=DARK, lw=0.8))
    ax.text(7, y, code, ha="center", va="center", fontsize=8, fontweight="bold")
    ax.text(15, y, desc, va="center", fontsize=7.5)
    ax.text(57, y, n, va="center", ha="right", fontsize=8)
    y -= 1.45
ax.text(0, 1.5, "Condition codes in the data file: AA 0–1, HA 2–3, LA 4–5, AH 6–7, HH 8–9, LH 10–11, AL 12–13, HL 14–15, LL 16–17\n"
                "(first letter = colour, second = sound; A = same as studied).\n"
                "Per session: 1296 probes, 432 of them DFP, about 108 per cell.",
        fontsize=7.2, color=GREY, va="center")
gx, gy, cw, ch = 70, 2.6, 13, 2.2
ax.text(gx + cw, gy + 2 * ch + 1.4, "Sound difference", ha="center", va="center", fontsize=8.5, fontweight="bold")
ax.text(gx - 7.5, gy + ch, "Colour difference", ha="center", va="center", fontsize=8.5, fontweight="bold", rotation=90)
for j, slab in enumerate(["H (easy)", "L (hard)"]):
    ax.text(gx + cw * (j + 0.5), gy + 2 * ch + 0.5, slab, ha="center", va="center", fontsize=8)
for i, clab in enumerate(["H (easy)", "L (hard)"]):
    ax.text(gx - 0.8, gy + ch * (1.5 - i), clab, ha="right", va="center", fontsize=8)
cells = [["HH", "HL"], ["LH", "LL"]]
for i in range(2):
    for j in range(2):
        ax.add_patch(Rectangle((gx + j * cw, gy + (1 - i) * ch), cw, ch, fc="#d9ead3", ec=DARK, lw=1))
        ax.text(gx + j * cw + cw / 2, gy + (1 - i) * ch + ch / 2, cells[i][j], ha="center", va="center", fontsize=11, fontweight="bold")
ax.text(gx + cw, gy - 0.5, "RT in these four cells → SIC and MIC → processing architecture", ha="center", va="top", fontsize=7.4, color=GREY)
ax.text(gx + cw, gy - 1.2, "H / L: colour = ΔE_H / ΔE_L, sound = count_H / count_L,\nset in Calibration 1 and 2",
        ha="center", va="top", fontsize=7.2, color=GREY, style="italic")

fig.savefig(os.path.join(HERE, "experiment_procedure.svg"), bbox_inches="tight")
fig.savefig(os.path.join(HERE, "experiment_procedure.png"), dpi=200, bbox_inches="tight")
print("saved")
