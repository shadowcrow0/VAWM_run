#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
debug_adaptivesft.py —— 在 PsychoPy Coder 裡一鍵診斷「adaptiveSFT 校準」整條鏈。

怎麼用：Coder 開這個檔 → Run。不用參數（Coder 沒有 argv），要調的開關都在下面「設定」區。
它會依序做：
  0. 環境：Python / numpy / scipy / PsychoPy / PyMC 有沒有、目前工作目錄、刺激檔在不在
  1. 找 adaptiveSFT fork：ADAPTIVESFT_PATH → 隔壁 ../adaptiveSFT → 已知的 Windows/WSL 位置，
     哪一個真的有 adaptivesft/psi.py（⚠ 隔壁那個常常是 Houpt 原版 R/Stan repo，沒有 psi.py）
  2. import adaptive_vawm（它在 import 當下就會去載 psi.py，找不到會直接炸）
  3. METHOD 能力檢查：lnrm 需要 PyMC + 完整 adaptivesft 套件；psi 只要 numpy + scipy
  4. 無視窗模擬：PsiCalibrator colour / audio 各跑 N_SIM 試，模擬受試者作答，逐試印出 Psi 的內部狀態
  5. （有 PyMC 才跑）LNRMCalibrator 縮短版擬合
  6. （RUN_WINDOW_TRIALS > 0 才跑）開一個小視窗，用 VAWM_calibrate.py 完全相同的試次流程跑幾試，你實際按 y/n
每一步失敗都會印「為什麼」和「怎麼修」，然後能繼續的就繼續。
"""
import os
import sys
import time
import traceback

for _stream in (sys.stdout, sys.stderr):          # Windows 主控台預設 cp950，印 ✔/中文會炸
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ───────────────────────────── 設定 ─────────────────────────────
N_SIM = 48                 # 第 4 步每個維度模擬幾試（正式是 72）
SIM_SEED = 7
RUN_WINDOW_TRIALS = 0      # 第 6 步：開視窗實跑幾試（0 = 跳過；建議先 0 跑通無視窗部分，再改 3）
WINDOW_DIM = "colour"      # 第 6 步用哪個維度："colour" 或 "audio"
TRY_LNRM = True            # 第 5 步：有 PyMC 就試一次縮短版 lnrm 擬合
LNRM_FIT_KW = dict(tune=200, draws=200, chains=1, nuts_sampler="nutpie")   # 縮短版；正式是 1000/1000/4。沒裝 nutpie 就拿掉那個參數（會慢 4 倍以上）
# 已知的 fork 位置（找不到時依序嘗試；可自行加一行）
KNOWN_FORK_PATHS = [
    r"C:\Users\spt904\OneDrive - University of Texas at San Antonio\Desktop\adaptiveSFT",
    "/mnt/c/Users/spt904/OneDrive - University of Texas at San Antonio/Desktop/adaptiveSFT",
]
# ────────────────────────────────────────────────────────────────

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)             # Coder 的工作目錄常常不是腳本所在；stimuli/… 都是相對路徑
W = 72


def hdr(n, title):
    print("\n" + "=" * W)
    print(f"[{n}] {title}")
    print("=" * W)


def ok(msg):
    print("  ✔ " + msg)


def bad(msg):
    print("  ✘ " + msg)


def fix(msg):
    print("    → 修法：" + msg)


# ───────────────────────────── 0. 環境 ─────────────────────────────
hdr(0, "環境")
print(f"  Python   {sys.version.split()[0]}  ({sys.executable})")
print(f"  cwd      {os.getcwd()}")
import site as _site
print(f"  user-site {_site.getusersitepackages()}  在 sys.path: {_site.getusersitepackages() in sys.path}"
      f"  (python -s 啟動: {bool(sys.flags.no_user_site)})")
try:
    import numpy as np
    import scipy
    ok(f"numpy {np.__version__}  scipy {scipy.__version__}")
except Exception as e:
    bad(f"numpy/scipy 載入失敗：{e}")
    raise SystemExit
try:
    import psychopy
    ok(f"psychopy {psychopy.__version__}")
    HAVE_PSYCHOPY = True
except Exception as e:
    bad(f"psychopy 不在這個 Python 裡（{type(e).__name__}）—— 第 6 步會跳過")
    HAVE_PSYCHOPY = False
try:
    import pymc
    ok(f"pymc {pymc.__version__}（lnrm 擬合可用）")
    HAVE_PYMC = True
except Exception as e:
    bad(f"pymc 沒有（{type(e).__name__}）→ METHOD='lnrm' 會在 72 試跑完、畫面「計算中」時炸掉")
    fix("在 PsychoPy Coder 這個環境只能用 METHOD='psi'；要用 lnrm 請照 adaptive_vawm.md 開 conda 環境")
    HAVE_PYMC = False
for f in ("adaptive_vawm.py", "generate_trials.py", "stimuli/T01_b3.wav", "stimuli/T12_p3.wav"):
    (ok if os.path.exists(f) else bad)(f"{f}")

# ───────────────────────────── 1. 找 fork ─────────────────────────────
hdr(1, "找 adaptiveSFT fork（要有 adaptivesft/psi.py）")
cands = []
if os.environ.get("ADAPTIVESFT_PATH"):
    cands.append(("環境變數 ADAPTIVESFT_PATH", os.environ["ADAPTIVESFT_PATH"]))
cands.append(("隔壁 ../adaptiveSFT", os.path.join(os.path.dirname(HERE), "adaptiveSFT")))
cands += [("已知位置", p) for p in KNOWN_FORK_PATHS]
found = None
for label, p in cands:
    has_psi = os.path.isfile(os.path.join(p, "adaptivesft", "psi.py"))
    exists = os.path.isdir(p)
    if has_psi:
        ok(f"{label}: {p}")
        if found is None:
            found = p
    elif exists:
        hint = ""
        if os.path.isfile(os.path.join(p, "adaptiveSFT_functions.R")) and not os.path.isdir(os.path.join(p, "adaptivesft")):
            hint = "  ← 這是 Houpt 原版（R/Stan），不是 shadowcrow0 的 fork"
        bad(f"{label}: {p} 存在但沒有 adaptivesft/psi.py{hint}")
    else:
        print(f"  · {label}: {p}（不存在）")
if found is None:
    bad("沒有任何位置有 adaptivesft/psi.py")
    fix("git clone https://github.com/shadowcrow0/adaptiveSFT.git 放在本 repo 隔壁，"
        "或在本檔 KNOWN_FORK_PATHS 加上它的路徑，或設環境變數 ADAPTIVESFT_PATH")
    raise SystemExit
if not os.environ.get("ADAPTIVESFT_PATH"):
    os.environ["ADAPTIVESFT_PATH"] = found       # adaptive_vawm 在 import 時讀這個
    print(f"  （本次自動設定 ADAPTIVESFT_PATH = {found}）")
try:
    import subprocess
    sha = subprocess.run(["git", "-C", found, "log", "--oneline", "-1"], capture_output=True, text=True).stdout.strip()
    print(f"  fork 版本：{sha or '（不是 git repo）'}")
except Exception:
    pass

# ───────────────────────────── 2. import adaptive_vawm ─────────────────────────────
hdr(2, "import adaptive_vawm")
try:
    import adaptive_vawm as A
    _psi_src = getattr(getattr(A, "psi_module", None), "__file__", "（舊版：沒有 psi_module 屬性）")
    ok(f"import 成功；psi.py 來自 {_psi_src}")
except Exception:
    bad("import adaptive_vawm 失敗：")
    traceback.print_exc()
    raise SystemExit
if not hasattr(A, "PsiCalibrator"):
    bad("這份 adaptive_vawm.py 是舊版 API（有 ColourCalibrator/AudioCalibrator，沒有 PsiCalibrator/LNRMCalibrator）")
    print(f"    檔案：{A.__file__}")
    fix("這個資料夾不是 GitHub main 的最新版（2026-10-02 之前的 ZIP）。"
        "請重新 clone / 下載 main 到新資料夾再跑；舊資料夾裡手改過的 VAWM_calibrate.py 先另存")
    raise SystemExit
for name in ("next_intensity", "update_at", "nearest_index", "estimate"):
    (ok if hasattr(A.Psi, name) or name == "next_intensity" else bad)(f"Psi.{name}")
try:
    conf = A.load_confusion()
    ok(f"confusion 表：{len(conf)} 個子音（來自 generate_trials.py）")
except Exception as e:
    bad(f"load_confusion 失敗：{e}")
    raise SystemExit

# ───────────────────────────── 3. METHOD 能力 ─────────────────────────────
hdr(3, "METHOD 能力檢查")
ok("psi：只要 psi.py + numpy + scipy → 可用")
LNRM_OK = False
try:
    A.load_full_package()
    from adaptivesft.models_v2 import fit_lnrm_v2      # noqa: F401
    from adaptivesft.salience import find_salience  # noqa: F401
    ok("lnrm：完整 adaptivesft 套件 + PyMC 都在 → 可用")
    LNRM_OK = True
except Exception as e:
    bad(f"lnrm：{type(e).__name__}: {str(e)[:90]}")
    fix("VAWM_calibrate.py 第 73 行 METHOD = \"lnrm\" 改成 \"psi\"，或在有 PyMC 的環境跑")

# ───────────────────────────── 4. 無視窗模擬 Psi ─────────────────────────────
hdr(4, f"無視窗模擬：PsiCalibrator，每維 {N_SIM} 試")
from scipy.stats import norm


def psi_observer(alpha, beta, fa, lapse=0.02):
    """模擬受試者：P(答「不同」| x) = fa + (1 − fa − lapse)·Φ((x − α)/β)。"""
    def respond(trial, rng):
        p = fa if trial["is_match"] else fa + (1 - fa - lapse) * norm.cdf(trial["x"], alpha, beta)
        return "n" if rng.uniform() < p else "y"
    return respond


TRUE = {"colour": dict(alpha=12.0, beta=8.0, fa=0.15),
        "audio": dict(alpha=-1.5, beta=0.6, fa=0.15)}
missing_wavs = set()
sim_results = {}
for dim in ("colour", "audio"):
    print(f"\n  ── {dim}  真值 α={TRUE[dim]['alpha']} β={TRUE[dim]['beta']} FA={TRUE[dim]['fa']} ──")
    rng = np.random.default_rng(SIM_SEED)
    respond = psi_observer(**TRUE[dim])
    try:
        cal = A.PsiCalibrator(dim, p_high=0.90, p_low=0.75, p_match=1 / 3, seed=SIM_SEED)
    except Exception:
        bad("PsiCalibrator 建立失敗：")
        traceback.print_exc()
        continue
    print(f"  {'#':>3} {'x_psi':>7} {'x':>7} {'AA':>3} {'key':>3} {'r':>2} {'ok':>2} {'α̂':>7} {'β̂':>6}  probe_sound")
    t0 = time.time()
    for _ in range(N_SIM):
        t = cal.next_trial()
        for k in ("audio1_target_file", "audio2_target_file", "probe_sound"):
            if not os.path.exists(t[k]):
                missing_wavs.add(t[k])
        key = respond(t, rng)
        r, c = cal.record(key, 0.6)
        a_hat, b_hat = cal.psi.estimate()
        print(f"  {t['trial_no']:>3} {t['x_psi']:>7.2f} {t['x']:>7.2f} {'AA' if t['is_match'] else '  ':>3} "
              f"{key:>3} {str(r):>2} {str(c):>2} {a_hat:>7.2f} {b_hat:>6.2f}  {t['probe_sound']}")
    try:
        res = cal.finish()
        sim_results[dim] = res
        print(f"  finish(): α̂={res['alpha']:.2f} β̂={res['beta']:.2f} FA={res['false_alarm']:.2f}  "
              f"H={res['high']:.2f} L={res['low']:.2f}  in_range={res['in_range']}  "
              f"warnings={res['warnings']}  ({time.time()-t0:.1f}s)")
        (ok if res["low"] < res["high"] else bad)("H > L")
        (ok if res["in_range"] else bad)("H/L 在範圍內")
        if dim == "colour":
            (ok if abs(res["alpha"] - 12) < 6 else bad)(f"α̂ 接近真值 12（差 {abs(res['alpha']-12):.1f}）")
    except Exception:
        bad("finish() 失敗：")
        traceback.print_exc()
if missing_wavs:
    bad(f"{len(missing_wavs)} 個被引用的刺激檔不存在，例如 {sorted(missing_wavs)[:3]}")
    fix("確認 stimuli/ 齊全（T01–T12 × 16 子音 × *3.wav）")
else:
    ok("兩個維度模擬中引用到的刺激 wav 全部存在")

# ───────────────────────────── 5. lnrm 縮短版 ─────────────────────────────
hdr(5, "LNRMCalibrator 縮短版擬合")
if not (TRY_LNRM and LNRM_OK):
    print("  跳過（TRY_LNRM=False 或 lnrm 不可用）")
else:
    try:
        from adaptivesft.race import lnrm_random
        dim = "colour"
        rng = np.random.default_rng(SIM_SEED)
        cal = A.LNRMCalibrator(dim, n_per_level=6, seed=SIM_SEED, **LNRM_FIT_KW)
        print(f"  計畫 {cal.n_trials} 試（6 層 × 6 + AA）")

        def respond(trial):
            if trial["is_match"]:
                return ("n" if rng.uniform() < 0.1 else "y"), 0.8
            u = A.to_model_units(dim, trial["x"])
            rt, correct = lnrm_random([1.0 * u - 0.12 * u * u], 1.0, 0.5, 0.2, rng)
            return ("n" if correct[0] == 1 else "y"), float(rt[0])

        for _ in range(cal.n_trials):
            t = cal.next_trial()
            cal.record(*respond(t))
        t0 = time.time()
        print("  擬合中（縮短版，約 10–60 s）…")
        res = cal.finish()
        print(f"  α̂={res['alpha']:.2f} α̂₂={res['beta']:.2f} H={res['high']:.2f} L={res['low']:.2f} "
              f"in_range={res['in_range']} divergences={res['extra']['divergences']} ({time.time()-t0:.0f}s)")
        ok("lnrm 流程跑通")
    except Exception:
        bad("lnrm 失敗：")
        traceback.print_exc()

# ───────────────────────────── 6. 開視窗實跑 ─────────────────────────────
hdr(6, f"開視窗實跑 {RUN_WINDOW_TRIALS} 試（{WINDOW_DIM}）")
if RUN_WINDOW_TRIALS <= 0 or not HAVE_PSYCHOPY:
    print("  跳過（RUN_WINDOW_TRIALS = 0 或沒有 psychopy）。要試就把 RUN_WINDOW_TRIALS 改成 3。")
else:
    from psychopy import core, event, sound, visual
    from psychopy.hardware import keyboard
    win = visual.Window(size=(1000, 700), fullscr=False, color="black", units="pix")
    fixs = visual.TextStim(win, text="+", height=40, color="white")
    msg = visual.TextStim(win, text="", height=24, color="white", wrapWidth=900)
    patch_l = visual.Rect(win, width=100, height=100, pos=(-200, 0), colorSpace="hex", lineColor="#808080")
    patch_r = visual.Rect(win, width=100, height=100, pos=(200, 0), colorSpace="hex", lineColor="#808080")
    probe = visual.Rect(win, width=100, height=100, pos=(0, 0), colorSpace="hex", lineColor="#808080")
    try:
        snd = sound.Sound("A", secs=1, stereo=True, hamming=True)
        ok("sound.Sound 開得起來")
    except Exception as e:
        bad(f"sound.Sound 失敗：{type(e).__name__}: {e}")
        fix("先跑 python audio_pick.py 看有哪些輸出裝置，再用 python audio_pick.py --set \"名稱\" 指定耳機")
        snd = None
    kb = keyboard.Keyboard()
    clock = core.Clock()

    def present(draw, secs, play=None):
        if play and snd is not None:
            snd.setSound(play, secs=1, hamming=True)
            snd.play()
        t0 = core.getTime()
        while core.getTime() - t0 < secs:
            if draw:
                draw()
            win.flip()
            if kb.getKeys(["escape"]):
                win.close()
                core.quit()
        if play and snd is not None:
            snd.stop()

    def run_trial(trial):
        present(fixs.draw, 0.3)
        patch_l.fillColor = trial["color1_target"]
        present(patch_l.draw, 1.0)
        patch_r.fillColor = trial["color2_target"]
        present(patch_r.draw, 1.0)
        present(None, 1.0, play=trial["audio1_target_file"])
        present(None, 1.0, play=trial["audio2_target_file"])
        present(fixs.draw, 0.3)
        probe.fillColor = trial["probe_colour"]
        kb.clearEvents()
        clock.reset()
        present(probe.draw, 1.0, play=trial["probe_sound"])
        keys = kb.getKeys(["y", "n"], waitRelease=False)
        while not keys and clock.getTime() < 3.0:
            win.flip()
            keys = kb.getKeys(["y", "n"], waitRelease=False)
            if kb.getKeys(["escape"]):
                win.close()
                core.quit()
        return (keys[0].name, keys[0].rt) if keys else (None, None)

    msg.text = f"DEBUG：{WINDOW_DIM} {RUN_WINDOW_TRIALS} 試\n相同按 y、不同按 n\n按空白鍵開始（esc 離開）"
    msg.draw(); win.flip()
    if "escape" in event.waitKeys(keyList=["space", "escape"]):
        win.close(); core.quit()
    cal = A.PsiCalibrator(WINDOW_DIM, seed=SIM_SEED)
    for i in range(RUN_WINDOW_TRIALS):
        t = cal.next_trial()
        print(f"  trial {t['trial_no']}: x_psi={t['x_psi']:.2f} x={t['x']:.2f} AA={t['is_match']} "
              f"probe={t['probe_colour']} {t['probe_sound']}")
        key, rt = run_trial(t)
        r, c = cal.record(key, rt)
        print(f"           key={key} rt={rt} r={r} correct={c}  α̂,β̂={cal.psi.estimate()}")
        msg.text = "沒有作答" if key is None else ("正確" if c else "錯誤")
        present(msg.draw, 0.8)
    win.close()
    ok("視窗流程跑完（沒有 finish()，試次太少）")

# ───────────────────────────── 7. VAWM_calibrate.py 開頭 dry-run ─────────────────────────────
hdr(7, "VAWM_calibrate.py 開頭 dry-run（import、挑音訊裝置、建 calibrator；停在對話框之前）")
if not HAVE_PSYCHOPY:
    print("  跳過（沒有 psychopy）")
else:
    try:
        _src = open("VAWM_calibrate.py", encoding="utf-8").read().split("expInfo = {")[0]
        _ns = {"__name__": "_vawm_head", "__file__": os.path.abspath("VAWM_calibrate.py")}
        exec(compile(_src, "VAWM_calibrate.py(head)", "exec"), _ns)
        ok(f"METHOD={_ns['METHOD']!r}  FIT_KW={_ns.get('FIT_KW')}")
        if _ns["METHOD"] == "lnrm" and not LNRM_OK:
            bad("METHOD 是 lnrm 但這個環境擬合不了（見第 3 步）")
        _cal = (A.LNRMCalibrator("colour", n_per_level=_ns["N_PER_LEVEL"], p_match=_ns["P_MATCH"], seed=1,
                                 **_ns.get("FIT_KW", {})) if _ns["METHOD"] == "lnrm"
                else A.PsiCalibrator("colour", seed=1))
        _t = _cal.next_trial()
        ok(f"第一試可建：probe {_t['probe_colour']} + {_t['probe_sound']}"
           f"（{'檔案存在' if os.path.exists(_t['probe_sound']) else '檔案缺 ✘'}）")
        print("  ↑ 上面 [audio] 那行是實驗會用的喇叭/耳機；不對就去 PsychoPy 偏好設定改 audioDevice")
    except SystemExit:
        bad("VAWM_calibrate.py 開頭呼叫了 core.quit()（多半是音訊裝置或視窗問題，看上面訊息）")
    except Exception:
        bad("VAWM_calibrate.py 開頭失敗：")
        traceback.print_exc()

print("\n" + "=" * W)
print("DEBUG 結束。沒看到 ✘ 就代表校準鏈在這個環境是通的。")
print("=" * W)
