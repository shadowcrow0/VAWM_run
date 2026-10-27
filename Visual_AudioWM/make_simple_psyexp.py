"""VAWM.psyexp -> VAWM_simple.psyexp：保留 Builder 的 routine/元件，流程邏輯改成 VAWM_simple.py 的寫法（不用 csv）。"""
import copy
import xml.etree.ElementTree as ET

NL = '&#10;'
SRC, DST = 'archive/VAWM.psyexp', 'VAWM_simple.psyexp'
tree = ET.parse(SRC); root = tree.getroot()
routines = root.find('Routines'); flow = root.find('Flow')
R = {rt.get('name'): rt for rt in routines}


def pget(c): return {p.get('name'): p for p in c}
def comp(rt, name):
    for c in rt:
        if 'name' in pget(c) and pget(c)['name'].get('val') == name: return c
    raise KeyError(name)
def setp(c, name, val, updates=None):
    p = pget(c)[name]; p.set('val', val)
    if updates: p.set('updates', updates)
def setcode(c, field, src): pget(c)[field].set('val', src.strip('\n').replace('\n', NL))
def param(name, val, valType='code', updates='None'):
    e = ET.Element('Param'); e.set('name', name); e.set('val', val); e.set('valType', valType); e.set('updates', updates); return e

# ───────────────────────────── 程式碼：全部寫在 StudyCode 的 Begin Experiment ─────────────────────────────
BE = r'''
# ═══════════ 0. 設定（要改的數字都在這） ═══════════
import os, sys, json, time
import numpy as np
os.chdir(_thisDir)                                   # 刺激檔是相對路徑 stimuli/...
LEVELS_COLOUR = [2.0, 6.0, 12.0, 20.0, 30.0, 45.0]   # 校準用的顏色距離 dE
LEVELS_AUDIO  = [-2.6, -2.1, -1.6, -1.1, -0.7, -0.3] # 校準用的子音不相似度 = -log10(混淆次數+1)
N_PER_LEVEL = 8                                      # 每個強度幾試 -> 48 試「不同」
P_MATCH = 1 / 3                                      # 再加 1/3「相同」試 -> 共 72 試
N_WARMUP = 8                                         # 校準前的暖機試次，有回饋、不進擬合
H_TARG, L_TARG = 2.0, 0.5                            # 漂移差目標：容易 H / 困難 L
FIT_KW = dict(tune=1000, draws=1000, chains=4, nuts_sampler="nutpie")
RT_MIN, RT_MAX = 0.15, 3.0
N_BLOCKS, SETS_PER_BLOCK, N_PRACTICE_SETS = 6, 24, 2
N_CALIB = int(len(LEVELS_COLOUR) * N_PER_LEVEL * (1 + P_MATCH / (1 - P_MATCH)) + 0.5)   # = 72（另一維度 = T，進擬合）
N_FILLER = 24             # 另一維度 H/L 的填充試（答案一定 N、不進擬合）
N_CALIB_TOTAL = N_CALIB + N_FILLER
OTHER_TARGETS_CHANGE = False  # False = nochange：另一維度的靶整區塊固定；True = change：每試重抽靶。兩版另一維度探測都抽 T/H/L
PROV_DE_H, PROV_DE_L = 30.0, 6.0
PROV_COUNT_H, PROV_COUNT_L = 10, 200
FIXED_PAIR = None
FIXED_COLS = {}

# ═══════════ 1. 借來的數學 ═══════════
from adaptive_vawm import (TALKERS, audio_x, count_from_x, delta_e, find_colour_at, foil_for,
                           from_model_units, lab_to_hex, load_confusion, load_full_package, random_target,
                           sound_file, to_model_units)
CONFUSION = load_confusion(); CONSONANTS = sorted(CONFUSION)
rng = np.random.default_rng()
PHASE = None                     # 'calib_colour' / 'calib_audio' / 'practice' / 'main'，由各 intro routine 設定
CALIB = {}                       # 校到的 H / L
calib_log = []                   # 校準每一試
probe_plan = []                  # 這一組接下來的 9 個條件

def two_targets():
    t1 = random_target(rng); t2 = random_target(rng, avoid=[t1])
    s1, s2 = rng.choice(CONSONANTS, 2, replace=False); k1, k2 = rng.choice(TALKERS, 2)
    return t1, t2, str(s1), str(s2), str(k1), str(k2)

def calib_plan(levels):          # (正在校維度的等級, 另一維度等級)：72 試 other=T + 24 填充 other=H/L，打散
    plan = [(x, 'T') for x in levels for _ in range(N_PER_LEVEL)]
    plan += [(None, 'T')] * int(round(len(plan) * P_MATCH / (1 - P_MATCH)))
    plan += [(rng.choice(levels + [None]), lev) for lev in ['H', 'L'] * (N_FILLER // 2)]
    plan = [(None if x is None else float(x), o) for x, o in plan]
    rng.shuffle(plan); return plan

def warmup_plan(levels):         # 暖機：AA 與最容易層級交替（None, 最容易, None, 最容易, ...）
    easiest = levels[-1]
    return [(None, 'T'), (easiest, 'T')] * (N_WARMUP // 2)

def foil_near(cons, count):      # 目標子音的干擾子音裡，混淆次數最接近 count 的
    cands = CONFUSION[cons]
    return cands[int(np.argmin([abs(np.log10(c + 1) - np.log10(count + 1)) for _, c in cands]))][0]

def make_study_set():            # 主實驗的一組：2 目標色各有 H/L 版本、2 目標音各有 H/L 干擾子音
    de_h, de_l = CALIB['colour']['high'], CALIB['colour']['low']
    cnt_h, cnt_l = CALIB['audio']['count_high'], CALIB['audio']['count_low']
    for _ in range(200):
        t1, t2, s1, s2, k1, k2 = two_targets()
        cols = [find_colour_at(t, de, rng) for t in (t1, t2) for de in (de_h, de_l)]
        if all(c is not None for c in cols): break
    else:
        raise RuntimeError("色域內找不到符合 dE_H / dE_L 的顏色")
    h1, l1, h2, l2 = cols
    return dict(color1_target=lab_to_hex(t1), color1_H=lab_to_hex(h1), color1_L=lab_to_hex(l1),
                color2_target=lab_to_hex(t2), color2_H=lab_to_hex(h2), color2_L=lab_to_hex(l2),
                audio1_target_file=sound_file(k1, s1), audio1_H_file=sound_file(k1, foil_near(s1, cnt_h)),
                audio1_L_file=sound_file(k1, foil_near(s1, cnt_l)),
                audio2_target_file=sound_file(k2, s2), audio2_H_file=sound_file(k2, foil_near(s2, cnt_h)),
                audio2_L_file=sound_file(k2, foil_near(s2, cnt_l)))

# 條件編號與名字跟 VAWM_nobox.py 一樣：(名字, 探測色欄位, 探測音欄位)；偶數 = 第 1 個目標、奇數 = 第 2 個
# ⚠ 名字字母順序原版就不一致（HA/LA = 聲音 H/L；AH/AL = 顏色 H/L；HH/LH/HL/LL = 顏色,聲音）；計分只看 AA，看欄位別看名字
COND = {0: ("AA", "color1_target", "audio1_target_file"), 1: ("AA", "color2_target", "audio2_target_file"),
        2: ("HA", "color1_target", "audio1_H_file"),      3: ("HA", "color2_target", "audio2_H_file"),
        4: ("LA", "color1_target", "audio1_L_file"),      5: ("LA", "color2_target", "audio2_L_file"),
        6: ("AH", "color1_H", "audio1_target_file"),      7: ("AH", "color2_H", "audio2_target_file"),
        8: ("HH", "color1_H", "audio1_H_file"),           9: ("HH", "color2_H", "audio2_H_file"),
        10: ("LH", "color1_L", "audio1_H_file"),          11: ("LH", "color2_L", "audio2_H_file"),
        12: ("AL", "color1_L", "audio1_target_file"),     13: ("AL", "color2_L", "audio2_target_file"),
        14: ("HL", "color1_H", "audio1_L_file"),          15: ("HL", "color2_H", "audio2_L_file"),
        16: ("LL", "color1_L", "audio1_L_file"),          17: ("LL", "color2_L", "audio2_L_file")}

def nine_probes():               # 2 AA、1 HA、1 LA、1 AH、1 AL、3 個雙通道，打散
    c = [int(rng.choice([0, 1])) for _ in range(2)]
    c += [int(rng.choice([2, 3])), int(rng.choice([4, 5])), int(rng.choice([6, 7])), int(rng.choice([12, 13]))]
    c += [int(rng.choice([8, 9, 10, 11, 14, 15, 16, 17])) for _ in range(3)]
    rng.shuffle(c); return c

def fit_dim(dim):                # 72 試 -> lnrm2 -> H / L（原始 adaptiveSFT）
    levels = LEVELS_COLOUR if dim == 'colour' else LEVELS_AUDIO
    load_full_package()
    from adaptivesft.models import make_data
    from adaptivesft.models_v2 import fit_lnrm_v2 as fit_lnrm   # PyMC 內建 LogNormal logp/logcdf 版（DECISIONS 14）
    from adaptivesft.salience import find_salience
    use = [r for r in calib_log if r['dim'] == dim and r['other'] == 'T' and not r['is_match'] and r['key'] is not None
           and RT_MIN <= r['rt'] <= RT_MAX]
    data = make_data([to_model_units(dim, r['x']) for r in use], [r['rt'] for r in use], [r['correct'] for r in use])
    trace = fit_lnrm(data, link='quadratic', **FIT_KW)
    res = find_salience(trace, h_targ=H_TARG, l_targ=L_TARG, alpha2_rule='filter')
    high, low = from_model_units(dim, res['high']['intensity']), from_model_units(dim, res['low']['intensity'])
    lo_lim, hi_lim = min(levels), max(levels)
    if not (np.isfinite(high) and np.isfinite(low)):
        print(f"[{dim}] 擬合解不出 H/L，暫用中間層級；要重校"); high, low = levels[-2], levels[1]
    in_range = bool(lo_lim <= low < high <= hi_lim)
    if not in_range:
        print(f"[{dim}] H={high:.2f} L={low:.2f} 超出範圍 [{lo_lim},{hi_lim}]，已夾回；要重校")
        high, low = float(np.clip(high, lo_lim, hi_lim)), float(np.clip(low, lo_lim, hi_lim))
        if low >= high: low = lo_lim
    out = dict(high=float(high), low=float(low), in_range=in_range, n_used=len(use), warnings=list(res['warnings']))
    if dim == 'audio':
        out['count_high'], out['count_low'] = float(count_from_x(high)), float(count_from_x(low))
    print(f"[{dim}] H={out['high']:.2f} L={out['low']:.2f} in_range={in_range} {out['warnings']}")
    return out
'''

# study_stage 的 Begin Routine：依 PHASE 產生這一試 / 這一組
STUDY_BR = r'''
if PHASE in ('calib_colour', 'calib_audio', 'warm_colour', 'warm_audio'):
    is_warmup = PHASE.startswith('warm_')
    dim = 'colour' if PHASE.endswith('colour') else 'audio'
    loop = (calibCw if dim == 'colour' else calibAw) if is_warmup else (calibC if dim == 'colour' else calibA)
    if is_warmup and loop.thisN == 0:
        plan = warmup_plan(LEVELS_COLOUR if dim == 'colour' else LEVELS_AUDIO)
        FIXED_PAIR = two_targets()                       # nochange：另一維度整區塊固定的靶（暖機+正式 72 試共用）
        FIXED_COLS = {}                                  # nochange 校聲音：固定靶的 H/L 色只算一次
        if not OTHER_TARGETS_CHANGE and dim == 'audio':
            for wi, tcol in enumerate(FIXED_PAIR[:2]):
                for lev, de in (('H', PROV_DE_H), ('L', PROV_DE_L)):
                    lab = find_colour_at(tcol, de, rng)
                    FIXED_COLS[(wi, lev)] = lab_to_hex(lab if lab is not None else tcol)
    elif not is_warmup and loop.thisN == 0:
        plan = calib_plan(LEVELS_COLOUR if dim == 'colour' else LEVELS_AUDIO)
    x_planned, other = plan[loop.thisN]
    dim_match = x_planned is None                        # 正在校的維度一樣嗎（擬合用）
    is_match = dim_match and other == 'T'                # 受試者的規則：兩個都一樣才 Y
    t1, t2, s1, s2, k1, k2 = two_targets()               # change：每試新的靶
    if not OTHER_TARGETS_CHANGE:
        if dim == 'colour':
            s1, s2, k1, k2 = FIXED_PAIR[2:]
        else:
            t1, t2 = FIXED_PAIR[:2]
    which = int(rng.integers(2))
    target_col, target_snd, talker = [t1, t2][which], [s1, s2][which], [k1, k2][which]
    if dim == 'colour':                                  # 校顏色：顏色走層級，聲音 T 或暫定 H/L
        probe_lab = target_col if dim_match else find_colour_at(target_col, x_planned, rng)
        if probe_lab is None: probe_lab = target_col
        x_actual = delta_e(target_col, probe_lab)
        targetCol = lab_to_hex(probe_lab)
        targetAud = sound_file(talker, target_snd if other == 'T' else foil_near(target_snd, PROV_COUNT_H if other == 'H' else PROV_COUNT_L))
    else:                                                # 校聲音：聲音走層級，顏色 T 或暫定 H/L
        foil, count = (target_snd, 0) if dim_match else foil_for(CONFUSION, target_snd, x_planned)
        x_actual = audio_x(count)
        targetAud = sound_file(talker, foil)
        if other == 'T':
            targetCol = lab_to_hex(target_col)
        elif (which, other) in FIXED_COLS:
            targetCol = FIXED_COLS[(which, other)]
        else:
            lab = find_colour_at(target_col, PROV_DE_H if other == 'H' else PROV_DE_L, rng)
            targetCol = lab_to_hex(lab if lab is not None else target_col)
    color1_target, color2_target = lab_to_hex(t1), lab_to_hex(t2)
    audio1_target_file, audio2_target_file = sound_file(k1, s1), sound_file(k2, s2)
    condition, cond_name = -1, 'AA' if is_match else ('warm' if is_warmup else 'calib')
else:                                                    # practice / main：一組 2 色 2 音 + 9 個探測
    st = make_study_set()
    color1_target, color1_H, color1_L = st['color1_target'], st['color1_H'], st['color1_L']
    color2_target, color2_H, color2_L = st['color2_target'], st['color2_H'], st['color2_L']
    audio1_target_file, audio1_H_file, audio1_L_file = st['audio1_target_file'], st['audio1_H_file'], st['audio1_L_file']
    audio2_target_file, audio2_H_file, audio2_L_file = st['audio2_target_file'], st['audio2_H_file'], st['audio2_L_file']
    probe_plan = nine_probes()
'''

PROBE_BR = r'''
if PHASE in ('practice', 'main'):                        # 校準時 targetCol / targetAud 已在 study_stage 決定
    condition = probe_plan.pop(0)
    cond_name, col_key, snd_key = COND[condition]
    targetCol, targetAud = st[col_key], st[snd_key]
    is_match = (cond_name == 'AA')
'''
PROBE_ER = r'''
key = ResponseBox.keys if ResponseBox.keys not in ('', [], None) else None
rt = ResponseBox.rt if key is not None else None
correct = None if key is None else int(key == ('y' if is_match else 'n'))
thisExp.addData('phase', PHASE); thisExp.addData('condition', condition); thisExp.addData('cond_name', cond_name)
thisExp.addData('targetCol', targetCol); thisExp.addData('targetAud', targetAud)
thisExp.addData('is_match', int(is_match)); thisExp.addData('correct', correct)
if PHASE in ('calib_colour', 'calib_audio', 'warm_colour', 'warm_audio'):
    thisExp.addData('x', x_actual)
    if PHASE in ('calib_colour', 'calib_audio'):          # 暖機不進 calib_log（擬合只用正式試次）
        calib_log.append(dict(dim='colour' if PHASE == 'calib_colour' else 'audio', is_match=dim_match, other=other,
                              x=x_actual, key=key, rt=rt, correct=correct))
resp = 'No response' if key is None else ('Correct' if correct else 'Wrong')
'''
FB_BR = r'''
# resp 已在 probe 的 End Routine 算好（'正確' / '錯誤' / '沒有作答'）
'''
FIT_BR = r'''
dim = 'colour' if PHASE == 'calib_colour' else 'audio'
CALIB[dim] = fit_dim(dim)
with open(os.path.join('data', expInfo['participant'] + '_simple_calib.json'), 'w', encoding='utf-8') as f:
    json.dump(dict(info=dict(participant=expInfo['participant'], method='lnrm', h_targ=H_TARG, l_targ=L_TARG),
                   colour=CALIB.get('colour'), audio=CALIB.get('audio')), f, ensure_ascii=False, indent=2)
continueRoutine = False
'''
REST_BR = r'''
if blocks.thisN == N_BLOCKS - 1:        # 最後一個 block 後不休息
    continueRoutine = False
'''

# 音訊輸出裝置交給 audio_pick.py（列裝置、實際試開、優先耳機；換新電腦先跑 python audio_pick.py）。
# Builder 從 Coder 執行時 sys.argv 沒有參數，所以指定裝置用 `python audio_pick.py --set "名稱"` 或環境變數 VAWM_AUDIO_DEVICE。
PICKER = ("# 音訊輸出裝置：見 audio_pick.py\n"
          "import sys\n"
          "from audio_pick import setup_from_argv\n"
          "AUDIO = setup_from_argv(sys.argv)\n")

# ───────────────────────────── 改 study_stage ─────────────────────────────
st = R['study_stage']; sc = comp(st, 'StudyCode')
setcode(sc, 'Before Experiment', PICKER); setcode(sc, 'Begin Experiment', BE); setcode(sc, 'Begin Routine', STUDY_BR)

# ───────────────────────────── 改 probe：Cedrus -> 鍵盤 y/n ─────────────────────────────
pr = R['probe']; pc = comp(pr, 'ProbeCode')
setcode(pc, 'Before Experiment', ''); setcode(pc, 'Begin Routine', PROBE_BR); setcode(pc, 'End Routine', PROBE_ER)
old_box = comp(pr, 'ResponseBox'); pr.remove(old_box)
kb = copy.deepcopy(comp(R['studyintro'], 'confirm'))
kb.set('name', 'ResponseBox'); setp(kb, 'name', 'ResponseBox')
setp(kb, 'allowedKeys', "'y','n'"); setp(kb, 'startVal', '.3'); setp(kb, 'stopVal', '3.0')
setp(kb, 'forceEndRoutine', 'True'); setp(kb, 'store', 'last key')
pr.append(kb)

# ───────────────────────────── 改 feedback ─────────────────────────────
fb = R['feedback']; setcode(comp(fb, 'code'), 'Begin Routine', FB_BR); setcode(comp(fb, 'code'), 'End Routine', '')

# ───────────────────────────── intro routines：設 PHASE + 文字 ─────────────────────────────
def add_code(rt, name, begin_routine):
    cc = ET.Element('CodeComponent'); cc.set('name', name)
    for n, v, t in [('Before Experiment','','extendedCode'), ('Before JS Experiment','','extendedCode'),
                    ('Begin Experiment','','extendedCode'), ('Begin JS Experiment','','extendedCode'),
                    ('Begin Routine', begin_routine.strip('\n').replace('\n', NL),'extendedCode'),
                    ('Begin JS Routine','','extendedCode'), ('Code Type','Py','str'),
                    ('Each Frame','','extendedCode'), ('Each JS Frame','','extendedCode'),
                    ('End Experiment','','extendedCode'), ('End JS Experiment','','extendedCode'),
                    ('End Routine','','extendedCode'), ('End JS Routine','','extendedCode'),
                    ('disabled','False','bool'), ('name',name,'code')]:
        cc.append(param(n, v, t))
    rt.insert(1, cc)

def clone_routine(src_name, new_name, text, code):
    rt = copy.deepcopy(R[src_name]); rt.set('name', new_name)
    for c in rt:
        pn = pget(c)
        if 'name' in pn:
            old = pn['name'].get('val'); new = f"{old}_{new_name}"
            if c.tag == 'RoutineSettingsComponent': new = new_name
            pn['name'].set('val', new); c.set('name', new)
            if c.tag == 'TextComponent': pn['text'].set('val', text.replace('\n', NL)); pn['stopVal'].set('val', '')
    add_code(rt, f'code_{new_name}', code); routines.append(rt); R[new_name] = rt; return rt

INTRO_TXT = ("{title}\n\nOn each trial you will first see two coloured squares and hear two speech sounds. "
             "Try to remember them.\nThen one colour will appear together with one sound.\n\n"
             "If the colour AND the sound are both the same as before, press Y.\nIf anything is different, press N.\n"
             "{extra}\n\nPress the space bar to begin.")
clone_routine('practice_intro', 'calibC_intro', 'Part 1 of 3: colour calibration (96 trials)\n\nOn each trial you will first see two coloured squares and hear two speech sounds. Try to remember them. Then one colour will appear together with one sound.\n\nDid this colour AND this sound both appear a moment ago?\n   Y = yes, both of them did.      N = no, at least one of them is different.\n\nFirst, 8 practice trials with feedback. Then 96 trials without feedback.\n\nPress the space bar to begin.', "PHASE = 'warm_colour'")
clone_routine('practice_intro', 'calibA_intro', 'Part 2 of 3: sound calibration (96 trials)\n\nOn each trial you will first see two coloured squares and hear two speech sounds. Try to remember them. Then one colour will appear together with one sound.\n\nDid this colour AND this sound both appear a moment ago?\n   Y = yes, both of them did.      N = no, at least one of them is different.\n\nFirst, 8 practice trials with feedback. Then 96 trials without feedback.\n\nPress the space bar to begin.', "PHASE = 'warm_audio'")
PRACTICE_DONE_TXT = 'Practice done. From now on there is no feedback.\n\nPress the space bar to continue.'
clone_routine('practice_intro', 'calibCw_done', PRACTICE_DONE_TXT, "PHASE = 'calib_colour'")
clone_routine('practice_intro', 'calibAw_done', PRACTICE_DONE_TXT, "PHASE = 'calib_audio'")
clone_routine('practice_intro', 'fit_msg', 'Calculating... this takes about a minute. Please wait.', "")
setp(comp(R['fit_msg'], 'key_resp_2_fit_msg'), 'stopVal', '0.5'); setp(comp(R['fit_msg'], 'key_resp_2_fit_msg'), 'forceEndRoutine', 'False')
setp(comp(R['fit_msg'], 'prac_intro_fit_msg'), 'stopVal', '0.5')
fitr = ET.Element('Routine'); fitr.set('name', 'fit')
rs = copy.deepcopy(R['feedback'].find('RoutineSettingsComponent')); rs.set('name', 'fit'); setp(rs, 'name', 'fit'); fitr.append(rs)
add_code(fitr, 'code_fit', FIT_BR); routines.append(fitr); R['fit'] = fitr
# 既有 intro 文字 + PHASE
setp(comp(R['practice_intro'], 'prac_intro'), 'text', INTRO_TXT.format(title='Part 3 of 3: the main task. First, a short practice.', extra='After each pair you will answer nine questions in a row. Feedback is shown during practice only.').replace('\n', NL)); setp(comp(R['practice_intro'], 'prac_intro'), 'stopVal', '')
add_code(R['practice_intro'], 'code_practice_intro', "PHASE = 'practice'")
setp(comp(R['SFT_start'], 'text'), 'text', INTRO_TXT.format(title='Main task', extra='Same rules as the practice. There is no feedback from now on. Answer as accurately as you can; speed is not important.').replace('\n', NL)); setp(comp(R['SFT_start'], 'text'), 'stopVal', '')
add_code(R['SFT_start'], 'code_SFT_start', "PHASE = 'main'")
add_code(R['rest'], 'code_rest', REST_BR)
# studyintro 的舊 device 設定拿掉
setcode(comp(R['studyintro'], 'code_2'), 'Begin Experiment', '')

# ───────────────────────────── Flow 與 loops ─────────────────────────────
tmpl = next(e for e in flow if e.tag == 'LoopInitiator' and e.get('name') == 'inner')
def loop_pair(name, nreps, is_trials):
    li = copy.deepcopy(tmpl); li.set('name', name)
    for p in li:
        if p.get('name') == 'name': p.set('val', name)
        if p.get('name') == 'nReps': p.set('val', nreps)
        if p.get('name') == 'isTrials': p.set('val', 'True' if is_trials else 'False')
        if p.get('name') == 'loopType': p.set('val', 'sequential')
        if p.get('name') == 'conditionsFile': p.set('val', '')
    lt = ET.Element('LoopTerminator'); lt.set('name', name); return li, lt
def rnode(n): e = ET.Element('Routine'); e.set('name', n); return e

for e in list(flow): flow.remove(e)
cC, cCt = loop_pair('calibC', 'N_CALIB_TOTAL', True); cA, cAt = loop_pair('calibA', 'N_CALIB_TOTAL', True)
cCw, cCwt = loop_pair('calibCw', 'N_WARMUP', True); cAw, cAwt = loop_pair('calibAw', 'N_WARMUP', True)
pr_, prt = loop_pair('practice', 'N_PRACTICE_SETS', False); pin, pint = loop_pair('pinner', '9', True)
bl, blt = loop_pair('blocks', 'N_BLOCKS', False); se, set_ = loop_pair('sets', 'SETS_PER_BLOCK', False); inn, innt = loop_pair('inner', '9', True)
for e in [rnode('studyintro'),
          rnode('calibC_intro'), cCw, rnode('study_stage'), rnode('probe'), rnode('feedback'), cCwt, rnode('calibCw_done'),
          cC, rnode('study_stage'), rnode('probe'), cCt, rnode('fit_msg'), rnode('fit'),
          rnode('calibA_intro'), cAw, rnode('study_stage'), rnode('probe'), rnode('feedback'), cAwt, rnode('calibAw_done'),
          cA, rnode('study_stage'), rnode('probe'), cAt, rnode('fit_msg'), rnode('fit'),
          rnode('practice_intro'), pr_, rnode('study_stage'), pin, rnode('probe'), rnode('feedback'), pint, prt,
          rnode('SFT_start'), bl, se, rnode('study_stage'), inn, rnode('probe'), innt, set_, rnode('rest'), blt,
          rnode('End')]:
    flow.append(e)

# 刪掉不再用的 routines（沒有）；寫檔
JS={'Before JS Experiment','Begin JS Experiment','Begin JS Routine','Each JS Frame','End JS Routine','End JS Experiment'}
for rt in routines:
    for c in rt:
        if c.tag=='CodeComponent':
            pn=pget(c); pn['Code Type'].set('val','Py')
            for f in JS:
                if f in pn: pn[f].set('val','')
tree.write(DST, encoding='utf-8', xml_declaration=True)
print('wrote', DST)
