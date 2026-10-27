#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VAWM 的校準程式（跑在 VAWM_nobox.py 之前）：區塊 1 校顏色差距、區塊 2 校子音混淆度，
作業與 VAWM_nobox.py 完全相同（注視 .3 s → 左色 1 s → 右色 1 s → 音 1 → 音 2 → 注視 .3 s → 探測色+音 1 s → y/n），
每試作答後給回饋。結束寫 data/<participant>_calib.json，接著：

兩種方法（METHOD）：
    "lnrm"  原始 adaptiveSFT（Houpt）：固定 6 個強度層級各 N_PER_LEVEL 試 + 1/3 AA 試，收正確率 + RT，
            區塊結束時擬合 lnrm2（PyMC NUTS，約 20–40 s，畫面顯示「計算中」），反解漂移差 H_TARG / L_TARG。
            需要實驗機器裝有完整的 adaptivesft 套件（Python ≥ 3.10 + PsychoPy + PyMC 同一個環境）。
    "psi"   Psi 逐試選強度，只用正確率，目標是「答不同」機率 P_HIGH / P_LOW。只要 numpy + scipy。

    python make_adaptive_blocks.py data/<participant>_calib.json     # 產生 stimuli/block1..6.csv
    python VAWM_nobox.py                                              # 主實驗照舊

需要 adaptivesft 套件：pip install -e <adaptiveSFT 的路徑>。本檔在沒有 PsychoPy 的容器裡只做過 py_compile。
參數為什麼是這些值：DECISIONS.md。
"""
import csv
import os
import sys

from psychopy import core, data, event, gui, sound, visual
from psychopy.hardware import keyboard

# 音訊輸出裝置：交給 audio_pick.py（列出裝置、實際試開、優先耳機）。
# 換到新電腦先跑 `python audio_pick.py` 看有哪些裝置；指定裝置三選一：
#   --audio-device "名稱"、環境變數 VAWM_AUDIO_DEVICE、或 `python audio_pick.py --set "名稱"`。
# --require-headphones = 自動挑時找不到耳機就停下，不退回喇叭；--list-audio = 只列裝置就結束。
from audio_pick import setup_from_argv
AUDIO = setup_from_argv(sys.argv)


from adaptive_vawm import LNRMCalibrator, PsiCalibrator, save_calibration

# ───────────── 參數 ─────────────
METHOD = "lnrm"            # "lnrm" = 原始 adaptiveSFT（LNRM，要 PyMC）；"psi" = Psi 版
P_MATCH = 1 / 3            # AA（探測 = 目標）試的比例，用來估假警報率
# lnrm
N_PER_LEVEL = 8            # 每個強度層級的「不同」試數；6 層 × 8 + 24 AA = 72 試 / 區塊
H_TARG, L_TARG = 2.0, 0.5  # H / L 的漂移差目標（z2 − z1）。Houpt 原設定 8.0 / 1.3；見 adaptiveSFT/results/power_scan.csv
LINK = "quadratic"         # "quadratic" = lnrm2（原檔，已對 Stan 驗證）；"ogival" = lnrm2a（adaptiveSFT 的重建：½L·inv_logit, L = 10）
                           # 兩者都用漂移差目標 —— decisions_for_author.md 的 B（2026-10-02 定案）
FIT_KW = dict(tune=1000, draws=1000, chains=4,   # PyMC NUTS；機器慢就 chains=2
              nuts_sampler="nutpie")              # 實驗機沒有 g++：PyMC 預設採樣器退回純 Python，這組設定要 20 分鐘以上；
                                                  # nutpie（pip install nutpie，numba 後端）實測 69 s，參數回復一樣。見 adaptive_vawm.md
# psi
N_COLOUR = 72              # 區塊 1 試次（含 1/3 的 AA 試）
N_AUDIO = 72               # 區塊 2 試次
P_HIGH, P_LOW = 0.90, 0.75  # H / L 的目標「答不同」機率（yes/no 作業的正確率）
RESP_KEYS = ["y", "n"]     # 同 VAWM_nobox.py：y = 相同、n = 不同
RESP_WINDOW = 3.0
# ─────────────────────────────────

expInfo = {"participant": "", "session": "001"}
if not gui.DlgFromDict(expInfo, title="VAWM calibration").OK:
    core.quit()
subj = expInfo["participant"]
expInfo["audio_device"] = AUDIO["name"]      # 寫進每一列資料
os.makedirs("data", exist_ok=True)
log_path = f"data/{subj}_calib_trials.csv"
# PsychoPy 標準三種輸出（與 Builder 腳本一致）：<檔名>.csv 寬表、.psydat、.log
from psychopy import logging as _plog
thisExp = data.ExperimentHandler(name="VAWM_calib", extraInfo=dict(expInfo),
                                 dataFileName=f"data/{subj}_VAWM_calib_{data.getDateStr()}",
                                 savePickle=True, saveWideText=True)
_plog.LogFile(thisExp.dataFileName + ".log", level=_plog.EXP)

win = visual.Window(fullscr=True, color="black", units="pix")
fix = visual.TextStim(win, text="+", height=40, color="white")
msg = visual.TextStim(win, text="", height=28, color="white", wrapWidth=1000)
patch_l = visual.Rect(win, width=100, height=100, pos=(-200, 0), colorSpace="hex", lineColor="#808080")
patch_r = visual.Rect(win, width=100, height=100, pos=(200, 0), colorSpace="hex", lineColor="#808080")
probe = visual.Rect(win, width=100, height=100, pos=(0, 0), colorSpace="hex", lineColor="#808080")
snd = sound.Sound("A", secs=1, stereo=True, hamming=True)
clock = core.Clock()
kb = keyboard.Keyboard(clock=clock)   # RT 以這個 clock 為準；每題探測前 clock.reset()
rows = []


def save_trial_log():
    """每試寫一次，中途當掉也留得住。"""
    columns = []
    for r in rows:
        for k in r:
            if k not in columns:
                columns.append(k)
    with open(log_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=columns)
        w.writeheader()
        w.writerows(rows)


def show(text):
    msg.text = text
    msg.draw()
    win.flip()
    keys = event.waitKeys(keyList=["space", "escape"])
    if "escape" in keys:
        core.quit()


def present(stim_draw, secs, play=None):
    """畫 stim_draw() secs 秒（play 給 wav 路徑就同時播）。"""
    if play:
        snd.setSound(play, secs=1, hamming=True)
        snd.play()
    t0 = core.getTime()
    while core.getTime() - t0 < secs:
        if stim_draw:
            stim_draw()
        win.flip()
        if kb.getKeys(["escape"]):
            core.quit()
    if play:
        snd.stop()


def run_trial(trial):
    # study：同 VAWM_nobox.py study_stage 的時間軸
    present(fix.draw, 0.3)
    patch_l.fillColor = trial["color1_target"]
    present(patch_l.draw, 1.0)
    patch_r.fillColor = trial["color2_target"]
    present(patch_r.draw, 1.0)
    present(None, 1.0, play=trial["audio1_target_file"])
    present(None, 1.0, play=trial["audio2_target_file"])
    # probe：注視 .3 s → 色+音 1 s → 等 y/n
    present(fix.draw, 0.3)
    probe.fillColor = trial["probe_colour"]
    kb.clearEvents()
    clock.reset()
    present(probe.draw, 1.0, play=trial["probe_sound"])
    keys = kb.getKeys(RESP_KEYS, waitRelease=False)
    while not keys and clock.getTime() < RESP_WINDOW:
        win.flip()
        keys = kb.getKeys(RESP_KEYS, waitRelease=False)
        if kb.getKeys(["escape"]):
            core.quit()
    if keys:
        return keys[0].name, keys[0].rt
    return None, None


def run_block(cal, n, title):
    show(f"{title}\n\n看到一個顏色並聽到一個聲音後：\n跟剛才記住的相同按 [y]，不同按 [n]\n\n按空白鍵開始")
    for i in range(n):
        trial = cal.next_trial()
        key, rt = run_trial(trial)
        r, correct = cal.record(key, rt)
        fb = "沒有作答" if key is None else ("正確" if correct else "錯誤")
        present(lambda: (setattr(msg, "text", fb), msg.draw()), 0.8)
        row = dict(cal.log[-1])
        row["block"] = cal.dim
        rows.append(row)
        save_trial_log()
        for k, v in row.items():                 # 同一列也進 ExperimentHandler
            thisExp.addData(k, v)
        thisExp.nextEntry()
    if METHOD == "lnrm":                                            # 擬合要幾十秒，先把畫面停在提示上
        msg.text = "計算中，請稍候…"
        msg.draw()
        win.flip()
    res = cal.finish()
    print(f"[{cal.dim}] {res['extra']['method']} FA={res['false_alarm']:.2f} alpha={res['alpha']:.2f} "
          f"beta={res['beta']:.2f} H={res['high']:.2f} L={res['low']:.2f} in_range={res['in_range']} {res['warnings']}")
    if not res["in_range"]:
        show(f"注意：{cal.dim} 的 H/L 落在範圍外\n{res['warnings']}\n\n按空白鍵繼續")
    return res


seed = int(subj) if subj.isdigit() else abs(hash(subj)) % 2**32
if METHOD == "lnrm":
    cal_c = LNRMCalibrator("colour", n_per_level=N_PER_LEVEL, p_match=P_MATCH, h_targ=H_TARG, l_targ=L_TARG,
                           link=LINK, seed=seed, **FIT_KW)
    cal_a = LNRMCalibrator("audio", n_per_level=N_PER_LEVEL, p_match=P_MATCH, h_targ=H_TARG, l_targ=L_TARG,
                           link=LINK, seed=seed + 1, **FIT_KW)
    n_c, n_a = cal_c.n_trials, cal_a.n_trials
elif METHOD == "psi":
    cal_c = PsiCalibrator("colour", p_high=P_HIGH, p_low=P_LOW, p_match=P_MATCH, seed=seed)
    cal_a = PsiCalibrator("audio", p_high=P_HIGH, p_low=P_LOW, p_match=P_MATCH, seed=seed + 1)
    n_c, n_a = N_COLOUR, N_AUDIO
else:
    raise ValueError(f"METHOD 必須是 'lnrm' 或 'psi'，拿到 {METHOD!r}")
colour = run_block(cal_c, n_c, "區塊 1：顏色")
audio = run_block(cal_a, n_a, "區塊 2：聲音")
out = f"data/{subj}_calib.json"
save_calibration(out, colour, audio, info=dict(expInfo, date=data.getDateStr(), method=METHOD, n_colour=n_c, n_audio=n_a))
thisExp.saveAsWideText(thisExp.dataFileName + ".csv")
thisExp.saveAsPickle(thisExp.dataFileName)
_plog.flush()
show(f"校準完成。\n\n{out}\n接著執行 make_adaptive_blocks.py 再跑 VAWM_nobox.py\n\n按空白鍵結束")
win.close()
core.quit()
