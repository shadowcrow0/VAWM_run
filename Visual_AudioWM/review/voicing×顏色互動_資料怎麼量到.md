# 決策脈絡 — voicing×顏色的互動:現有設計把每一個量從哪裡算出來

**日期** 2026-08-13　**用途** 回答「voicing(b→p)向度與顏色的互動,為什麼現有設計的資料全部量得到?」
**核實對象** `GRTv2.py`(工作檔,branch `claude/adaptive-grt-config-niapay`)、`AGRT.py`。
本檔的每一個試次數與欄位名都標了行號;**沒有一個數字來自轉述**。

---

## 0. 一句話

**四個量全部落在同一份 CSV 的九個欄位上**(`cue_valid` / `relation` / `target_item` /
`cued_item` / `chosen_item` / `outcome` / `err_rel` / `is_practice` / `psi_*`),
差別只在「用哪一批 trial 當分母」:
特徵獨立性用 **valid 的 384 筆**、intrusion 不對稱用 **invalid 的 192 筆(每 relation 64)**、
一致性對比用 **target_item 四格各 96 筆(valid)**、兩維可比性用 **同一批 valid 的 err_rel 邊際**
再掛上適應階段存下的 **`psi_col_beta` / `psi_snd_beta`** 當共變項。

> ⛔ **但先看 §1.5:現行程式碼存不下這些資料。**
> `trials` loop 建立時 `isTrials=False`(`GRTv2.py:1124`、`GRTv2.psyexp:1029`),
> PsychoPy 因此**不會**在迴圈裡產生 `thisExp.nextEntry()`,而 `TrialHandler2.__next__`
> 自己也不呼叫它 —— **600 個試次全部寫進同一個 entry dict,互相覆蓋,存檔時只剩一列。**
> **四個量在設計上全部成立,但這一行不修,一個都拿不到。** 修法見 §1.5 與末節 ⛔ 0。

**核實過程翻出四件與我拿到的轉述不符的事,而且都會改寫解讀**:

0. **⛔ 資料存檔會把 600 個試次壓成一列**(上面那段;證據鏈在 §1.5)。
1. **`cue` routine 在提示標記之後、四選一之前,會把 target 的顏色與聲音實際呈現出來**
   (`GRTv2.py:1611–1614`,probe 畫在 **cue 的位置**(`:1617–1618`))。所以「correct」的定義是
   **報告剛剛看到/聽到的 probe**,不是「回憶那個角落原本是什麼」。
   → 這讓 valid trials 成為一個**乾淨的 4×4 identification confusion matrix**(每刺激 96 次),
   完整 GRT 反而**估得動**;但也讓「記憶」只透過 invalid 的 intrusion 進場。**見 §1.3。**
2. **指導語與計分不一致**:指導語寫 "report which item was there"(`GRTv2.py:406`),
   照做的人在 invalid 試次上一律被記成 intrusion。**見 §3.1,這是最大的一條。**
3. **每維目標正確率不是 80%,是 89.4%**(聯合才是 80%)。
   `GRTv2.py:854` 的註解「每維 sqrt(0.64) = 0.80」與 `AGRT.py:406 + 170` 的實際運算不符,
   後者又開了一次根號。[[決策脈絡_AGRT模型假設]] 與 [[決策脈絡_統計方法]] §1 的表都是對的。**見 §2.4。**

---

## 1. 先核實:資料檔裡實際有什麼

### 1.1 item 編碼(`GRTv2.py:421–426`)

```
colour = i & 1        itemColhex = [C1, C2, C1, C2]     (GRTv2.py:1160)
sound  = (i >> 1) & 1 itemAudi   = [B , B , P , P ]     (GRTv2.py:1159)
REL_NAME = {0:'valid', 1:'colour_only', 2:'sound_only', 3:'both'}   (:426)
```

| item | 顏色 | 聲音 | 慣用名 |
|---|---|---|---|
| 0 | `COLOUR_HEX[0]` = `colour_for(colour_arc_lo)` | `AUDIO_B` | C1B |
| 1 | `COLOUR_HEX[1]` = `colour_for(colour_arc_hi)` | `AUDIO_B` | C2B |
| 2 | `COLOUR_HEX[0]` | `AUDIO_P` | C1P |
| 3 | `COLOUR_HEX[1]` | `AUDIO_P` | C2P |

✅ 轉述無誤。

**C1/C2 哪一端是藍、哪一端是粉?**(推導,非註解)
適應階段的回饋規則是 `_corr_c = int(_r1 == int(_arc > 0))`(`GRTv2.py:923`),
而 `_r1=1` 對應按鍵 `j` = "more pink"(`:914–916`),所以 **arc > 0 = 粉側、arc < 0 = 藍側**。
`AGRT.py:170–171` 回傳的 tuple 第一項用 `+thresh`、第二項用 `1-thresh`,
`erfinv` 的引數在第一項為正 → 第一項 = `α − β√2·(正值)` **低於**界線 α。
所以 `colour_arc_lo < α < colour_arc_hi`,而 α 在適應收斂時應接近錨點(arc=0)。
→ **C1(index 0)通常是藍側、C2(index 1)是粉側。**
⚠️ 這是從公式推的,不是程式碼寫的;個別受試者的 α 若偏離 0 很多,`colour_arc_lo` 可能同號。
**分析時應直接讀 `colour_arc_lo` / `colour_arc_hi` 的實際數值,不要假設符號。**

### 1.2 試次計畫與細格數(`GRTv2.py:428–441, 456–467`)

```python
N_VALID_PER_CELL   = 24   # :428  每個 (target_item × serial_pos)
N_INVALID_PER_CELL = 4    # :429  每個 (target_item × relation × serial_pos)
BLOCK_SIZE         = 144  # :430
```

我把 `:434–441` 的 strata 迴圈原封不動抽出來跑過(本地實測):

```
valid   : target_item(4) × serial_pos(4)                = 16 格 × 24 = 384
invalid : target_item(4) × relation(3) × serial_pos(4)  = 48 格 ×  4 = 192
N_MAIN  = 576         n_blocks = 576 // 144 = 4
practice(:456–465) = 16 valid + 8 invalid = 24
N_TRIALS = 24 + 576 = 600     (:467;TrialHandler2 nReps=N_TRIALS,:1116–1118)
```

**每個分析要用的分母,已算好:**

| 切法 | 每人筆數 |
|---|---|
| valid(main) | **384** |
| invalid(main) | **192** |
| invalid,每個 relation ∈ {1,2,3} | **各 64** |
| 每個 target_item 當靶(main 全部) | **各 144** |
| 每個 target_item 當靶(僅 valid) | **各 96** |
| 每個 (target_item × relation) invalid 細格 | **各 16** |

⚠️ **練習的 24 試次不平衡**:invalid 那 8 筆是 `rng.permutation([1,2,3])[:2]` 每 item 抽兩個
relation(`:461–463`),relation 不等頻,serial_pos 也是隨機抽。
**四個分析一律先 `is_practice == False` 濾掉**(欄位在 `:1577`)。

⚠️ 96 次/刺激這個數字與 [[silbert2012]] 的 200 次/刺激仍差一倍
(卡片裡已標為「AVWM 可對照的已發表基準」)。

### 1.3 ⭐ 一個 trial 實際發生什麼 —— 這一節推翻了我原本的理解

逐 routine 讀 `GRTv2.py`:

```
study   (:1152–1585)   四個 item 各 1.0 s,起始時間 START=[0.3,1.3,2.3,3.3](:1169)
                       quad_content = rng.permutation(4)  (:1179)
                       → 每一試四個 item 全部出現,各佔一個象限
cue     (:1596–1805)   t=0–1 s  Cue 白框畫在 cued_item 的象限   (:1604–1607)
                       t=1–2 s  targetC 色塊 + targetAudi 聲音
                                內容 = itemColhex[target_item] / itemAudi[target_item]  (:1613–1614)
                                位置 = cue 的位置                                        (:1617–1620)
task    (:1817–2206)   四個選項:色塊 + 文字標籤,位置每試重洗(opt_perm,:1842)
                       選項內容 = final_value / TXT              (:1832–1833)
                       按 f/g/h/j,無時限 → 幾乎不會有 noresp
```

**兩個後果:**

**(a) 每一試四個 item 都在場。** `quad_content` 是 0–3 的排列(`:1179`),
所以 study 畫面永遠含 C1B、C2B、C1P、C2P 各一。
→ 一致性對比(§2.3)因此是**同一個畫面內部**「哪一個被考」的對比,
刺激集在兩個水準之間**完全相同**,沒有 set-level 混淆。這是設計上的一個意外優點。
→ 但也表示這個設計**測不到** display-level 的一致性(「全一致畫面 vs 全不一致畫面」),
[[brunetti2017]] 那種操弄在這裡不存在。

**(b) probe 把答案呈現出來了。** `cue_color = itemColhex[target_item]`(`:1613`)。
[[決策脈絡_實驗設計]] 的「被推翻的假設」一節已經記過這是**刻意的衝突設計**
(該檔還警告舊版 `GRTv2.py` 誤寫成 `itemColhex[cue_idx]` —— **現在的工作檔是對的**,已用
`target_item`)。所以正確的讀法是:

```
study:  A 位置放 item X(= cued_item)   B 位置放 item Y(= target_item)
cue:    標記指向 A                      ← 注意力被拉到 A
probe:  畫/播在 A,內容卻是 Y            ← 衝突
task:   報 Y = 刺激驅動勝出(correct);報 X = 注意力捕獲(intrusion)
```

→ **valid trials 上 cued_item == target_item,沒有衝突,整段就是一個標準的 2×2
identification 作業**:刺激 = probe 的四個 item 之一,反應 = 四選一。
每刺激 96 次的混淆矩陣**存在**,[[soto2017]] 說的 2×2 GRT 設計條件在這裡是滿足的。
這也正是 [[決策脈絡_統計方法]] §5 步驟 1「valid trials → 直接擬合 GRT」的前提。

→ **記憶只透過 invalid 的 intrusion 進場。** 「b/p 的記憶表現差異」這個 DV,
在現設計下嚴格說是「b/p 的 **identification** 表現差異(在記憶競爭者在場時)」。
**這個措辭差別要進論文,不能含糊。**

### 1.4 欄位在哪個 End Routine 寫的

| 欄位 | 行號 | 寫入時機 | 內容 |
|---|---|---|---|
| `is_practice` `trial_i` `quad_content` `time_perm` `target_serial` | `:1577–1581` | study End | 練習旗標、四象限內容、序列位置 |
| `studyUR/UL/BL/BR` | `:1582–1585` | study End | `hex\|wav\|t=起始秒` 字串 |
| `cue_valid` `relation` `relation_name` `target_item` `cued_item` `target_quad` `cue_idx` `cue_color` `cue_audi` | `:1795–1803` | cue End | 提示與 probe 的完整規格 |
| `opt_perm` `pressed_key` `chosen_slot` `chosen_item` | `:2187–2190` | task End | 選項排列與反應 |
| `outcome` `err_rel` `err_rel_name` `is_correct` `rt` | `:2191–2195` | task End | 結果分類 |
| `adapt_trial` `adapt_arc` `adapt_step` `adapt_resp_col` `adapt_resp_snd` `adapt_corr_col` `adapt_corr_snd` | `:939–945` | 適應階段每試 | 60 筆 Psi 原始資料 |
| `psi_col_alpha` `psi_col_beta` `psi_snd_alpha` `psi_snd_beta` `colour_arc_lo` `colour_arc_hi` `snd_step_b` `snd_step_p` | `:964–971` | 適應階段結束 | 每人一筆 |

**結果分類的程式碼(`:2171–2185`),原文照抄:**

```python
if chosen_item is None:            outcome = 'noresp'
elif chosen_item == target_item:   outcome = 'correct'
elif chosen_item == cued_item:     outcome = 'intrusion'
else:                              outcome = 'other'

err_rel = None if (chosen_item is None or outcome == 'correct') else (chosen_item ^ target_item)
```

三個必須記住的性質:

- **順序不可換**(`:2171–2172` 的註解自己也標了):valid 試次 `cued_item == target_item`,
  correct 先接走 → **valid 試次的 `outcome` 永遠不會是 `intrusion`**。這是設計保證,不是實測結果。
- **`err_rel` 是 XOR**,所以 `err_rel & 1` = 顏色錯、`err_rel & 2` = 聲音錯。
  correct 與 noresp 都是 `None`(CSV 裡是空字串)。
- **`outcome=='intrusion'` ⟺ `err_rel == relation`**(在 invalid 上)。
  兩個欄位是同一件事的兩種寫法;§2.2 用 `err_rel` 版本,因為它同時給得出基線。

### 1.5 ⛔ CSV 的列結構 —— 現行程式碼存不下試次資料

我原本只想標一句「分析時記得 `psi_*` 自成一列」。核實 PsychoPy 原始碼之後,發現的是別的東西。

**證據鏈(五步,全部逐行核實;PsychoPy `2026.1.1`,與 `GRTv2.py:42` 的 `psychopyVersion` 一致;
安裝路徑 `/mnt/c/Program Files/PsychoPy/Lib/site-packages/psychopy/`)**

| # | 事實 | 出處 |
|---|---|---|
| 1 | CSV 的「一列」= `ExperimentHandler.entries` 的一個元素,而 `entries` **只在 `nextEntry()` 裡成長** | `data/experiment.py:702` `self.entries.append(this)` |
| 2 | `thisExp.addData(...)` 只寫進 `self.thisEntry` 這個 dict,**同名就覆蓋**,永遠不推進列 | `data/experiment.py:300, 310` |
| 3 | `TrialHandler2.__next__` **不呼叫** `nextEntry()`,只呼叫 `exp.updateEntryFromLoop(self)` | `data/trial.py:1101–1103`(全檔唯一呼叫 `nextEntry()` 的地方是 `skipTrials`,`:1293`) |
| 4 | Builder 只在 **`isTrials == True`** 時才在迴圈裡產生 `thisExp.nextEntry()` | `experiment/loops.py:483–487` `# just within the loop advance data line if loop is whole trials` |
| 5 | **本專案的 `trials` loop 是 `isTrials=False`** | `GRTv2.py:1124`;來源 `GRTv2.psyexp:1029` `<Param name="isTrials" ... val="False" .../>` |

**結論**:`GRTv2.py` 裡 `thisExp.nextEntry()` 只出現在 `:840, 946, 972, 1111`(全部在
`trials` 迴圈**之外**:Intro、適應階段每試、適應階段結束、instruction_normal)。
迴圈內部沒有,`TrialHandler2` 也不補。
→ **600 個主試次的 `is_practice` / `relation` / `target_item` / `outcome` / `err_rel` …
全部寫進同一個 dict,一路互相覆蓋。存檔時 `getAllEntries()` 把這個孤兒 entry 補上,
所以整個主實驗在 CSV 裡是「一列」,內容是最後一個試次的值。**

⚠️ 這是**逐行讀原始碼**推出來的,**沒有實跑驗證**(PsychoPy 裝在 Windows 側,本機跑不動)。
**但它是可以 30 秒證偽的**:跑 10 個試次,看 CSV 有幾列。

📌 **兩條修法(擇一)**

1. **從 Builder 修(建議,因為 `GRTv2.py` 是 `GRTv2.psyexp` 編譯後手改的)**:
   把 `trials` loop 的 `isTrials` 勾成 True(`GRTv2.psyexp:1029` 的 `val="False"` → `"True"`),重新編譯。
   ⚠️ 重新編譯會沖掉手改的部分,要重做 patch。
2. **直接在 `GRTv2.py` 補一行**:在 `for thisTrial in trials:`(`:1133`)迴圈的最後 ——
   `:2389` `trials.status = STARTED` 之後、`:2390` `# completed N_TRIALS repeats` 之前 ——
   以迴圈本體的縮排(8 空格)加一行 `thisExp.nextEntry()`。
   **同時要把 `GRTv2.psyexp:1029` 的 `isTrials` 也改掉**,否則下一次重編譯這行又會不見。

**修好之後,CSV 的列結構應該是:**

- 指導語/Intro 若干列(`:840, 1111`)
- 適應階段 60 列(`:946`)
- `psi_*` 八個欄位**自成一列**(`:972`),整份檔案只有這一列有值
  → 分析時要先 `ffill` / `groupby(participant).max()` 廣播到全部試次列
- 主試次 **600 列**,每列含 §1.4 前五組欄位

📌 **pilot 拿到第一份 CSV 的第一件事:數列數。** 期望 ≈ 60 + 1 + 600 + 少數指導語列。

---

## 2. 四個量得到的互動

### 2.1 特徵獨立性:綁定丟失 vs 獨立漂移

**用哪些欄位** `is_practice`、`cue_valid`、`err_rel`、`outcome`
**用哪些 trial** `is_practice == False & cue_valid == 1` → **每人 384 筆**
**為什麼只用 valid** invalid 試次上 intrusion 會把質量全部灌進 `err_rel == relation` 那一格
([[決策脈絡_統計方法]] §3:10% intrusion 就能偽造出 ρ=0.5 的訊號),
所以 invalid **不能**與 valid 合併算獨立性。這一點是該檔的核心發現,直接套用。

**怎麼算**

把每一筆 valid 試次攤成一個 2×2 表:

```
c = 1 if (err_rel & 1) else 0      # 顏色錯
s = 1 if (err_rel & 2) else 0      # 聲音錯      (correct → err_rel 為空 → c=s=0)

           s=0        s=1
   c=0    n00        n01      n00 = correct 數
   c=1    n10        n11      n11 = err_rel==3 的數
```

兩個等價的統計量:

```
超額     Δ = P(err_rel = 3) − P(err_rel ∈ {1,3}) · P(err_rel ∈ {2,3})
對數勝算比 logOR = log( n00·n11 / (n01·n10) )
```

**虛無/對立假設**

| | 心理機制 |
|---|---|
| Δ = 0(logOR = 0) | **獨立漂移**:顏色與聲音在工作記憶裡各自獨立地退化/被誤讀,兩個特徵同時錯只是巧合 |
| Δ > 0(logOR > 0) | **綁定丟失**:整個物件一起丟,錯就兩個特徵一起錯 —— GRT 的 perceptual independence 違反在工作記憶側的對應物 |
| Δ < 0 | **互斥式的資源競爭**:一個特徵保住的代價是另一個被犧牲(顧此失彼) |

**最小配方(pseudo-code)**

```python
d = df[(~df.is_practice) & (df.cue_valid == 1) & (df.outcome != 'noresp')]
e = d.err_rel.fillna(0).astype(int)
c, s = (e & 1) > 0, (e & 2) > 0
n00, n01, n10, n11 = ((~c)&(~s)).sum(), ((~c)&s).sum(), (c&(~s)).sum(), (c&s).sum()
logOR = log((n00 + .5)*(n11 + .5) / ((n01 + .5)*(n10 + .5)))     # Haldane 修正
# 群體層次: 每人一個 logOR -> 單樣本 t / bootstrap
# 或直接 GLMM: glmer(colour_err ~ sound_err + (sound_err | subject), family = binomial)
```

#### ⚠️ 兩個必須誠實處理的污染

**(a) 目標側 vs 提示側的錯誤來源混合 —— valid 上不成問題,但另一個混合躲不掉。**

valid 試次沒有第二個 item 可以被誤報成「提示側」,所以 [[決策脈絡_統計方法]] §3 那種污染
在這裡是**乾淨的**。**但有另一個混合:**因為 study 畫面上四個 item 全在場(§1.3a),
而四個選項就是這四個 item(`:1832–1833`),所以任何一次錯誤在資料上都無法區分

- **特徵層次的誤讀**(probe 的顏色被讀成另一個色),與
- **位置→物件的交換**(把另一個象限的 item 報出來)。

`err_rel` 只告訴你「錯掉的反應與 target 差在哪幾個特徵」,**不告訴你錯誤發生在哪個階段**。
→ 現設計**無法**把 swap error 從 feature error 裡拆出來。
可拆的前提是選項裡放**未出現過的 lure**(現在沒有),或另外量位置報告。
**這一條要寫進 Limitation,不能靠分析救。**

**(b) 猜測會憑空製造「綁定」訊號 —— 而且很大。**

四選一,一次純亂猜對 1/4、三個錯選項各 1/4。若受試者以機率 g 亂猜、
其餘 (1−g) 走真正獨立的記憶歷程(每維錯誤率 a):

```
P(cell) = g/4 + (1−g)·[獨立模型的 cell]
```

本地算了一張表(真值:完全獨立,記憶側每維錯 8%):

| g | 觀察到的聯合正確率 | 觀察到的 logOR |
|---|---|---|
| 0.00 | 0.846 | **0.000** |
| 0.05 | 0.817 | **+0.804** |
| 0.10 | 0.787 | **+1.067** |
| 0.20 | 0.727 | **+1.218** |

**5% 的亂猜就足以在真值為零時造出 logOR ≈ +0.8。**
這與 [[決策脈絡_統計方法]] §3 的 intrusion 現象是**同一型的模型誤設**:
混合模型裡多出來的那一塊質量,在只有「相關」這個參數的模型裡無處可去。

**怎麼辦(三選一,誠實度遞減):**

1. **敏感度分析(建議)**:反解「要多少 g 才能單靠猜測解釋掉觀察到的 logOR」。
   把 ĝ 與該受試者的實際正確率一起看 —— 上表顯示 g 每增加 0.05,聯合正確率就掉約 0.03,
   所以正確率高的人不可能有大的 g。若 break-even 的 ĝ 與觀察到的正確率互相矛盾,
   綁定結論站得住;若 ĝ 落在正確率容許的範圍內,**不宣稱**。
   ```python
   from scipy.optimize import brentq
   f = lambda g: model_logOR(g, a_hat(g)) - logOR_obs   # a_hat: 讓邊際錯誤率吻合的解
   g_break = brentq(f, 1e-6, 0.99)
   ```
2. **混合模型直接估 g**:需要一個 g 的識別來源。現設計**沒有**乾淨的錨
   (適應階段估的是知覺 lapse `LAPSE=0.08`(`:855`)→ 邊際 lapse
   `1 − √(1−0.08) = 0.0408`(`AGRT.py:288`),那是**知覺階段**的 lapse,
   不等於作業階段的猜測率)。⚠️ **把它當 g 用是外推,我不建議,但它可以當 g 的下界。**
3. **不修正、只報 logOR**。⛔ 不建議 —— 上表顯示這等於把猜測率當成綁定證據。

**每人精度(本地算)**:384 筆 valid、聯合正確率 0.80、真值獨立 →
四格期望次數 (307, 36, 36, 4),**單人 SE(logOR) ≈ 0.54**,完全被「兩個都錯」那一格的
4 次觀察綁死。正確率掉到 0.65 時 SE 降到 0.33。
→ **這個量必須在群體層次做(GLMM 或 per-subject logOR 的 t 檢定),單人估計沒有解釋力。**
順帶一提:這也是 [[決策脈絡_統計方法]] §3 末尾「訊號在低正確率時反而更強」的同一個現象。

---

### 2.2 Intrusion 的 relation 不對稱:哪個特徵先被搶走

**用哪些欄位** `cue_valid`、`relation`、`err_rel`(或等價的 `outcome`)、`is_practice`
**用哪些 trial** `is_practice == False & cue_valid == 0` → **每人 192 筆,每個 relation 各 64 筆**
(§1.2 的算術:4 item × 4 serial × 4 重複 = 64)

**怎麼算 —— 一定要扣基線**

`outcome == 'intrusion'` 的原始比率**不能直接比**:即使完全沒有注意力捕獲,
一個亂錯的人也會有 1/3 的機率剛好選到 cued_item。而且三個錯誤選項的**混淆度本來就不同**
(只差顏色的那個比兩個都差的那個容易被誤選)。

[[決策脈絡_統計方法]] §3 已經給出正確的估計式,直接引用:

$$\hat{\pi}_r \;=\; P(\texttt{err\_rel}=r \mid \texttt{relation}=r)\;-\;P(\texttt{err\_rel}=r \mid \texttt{relation}\neq r)$$

分子分母:被減項 **64 筆**,減項 **128 筆**(另外兩個 relation)。
`relation` 是隨機指派、**不改變任何刺激**,所以減項就是「同一個 err_rel 格子在沒有提示拉力時
自然會有多少質量」—— 顏色/聲音的混淆度基線被完全相消。

**虛無/對立假設**

| | 心理機制 |
|---|---|
| π̂₁ = π̂₂ = π̂₃ | **物件式捕獲**:空間提示搶的是整個綁好的物件,與特徵無關 |
| π̂₁ > π̂₂ | **顏色先被搶走**:視覺空間提示對視覺特徵的拉力較大(模態一致) |
| π̂₂ > π̂₁ | **聲音先被搶走**:語音碼與空間位置的綁定較弱,較容易被重新指派 |
| π̂₃ ≈ π̂₁·π̂₂ | **特徵各自獨立被捕獲**:兩個特徵一起被搶只是兩件獨立事件同時發生 |
| π̂₃ ≫ π̂₁·π̂₂ | **整體捕獲**:被搶就整包搶 —— 與 §2.1 的綁定結論可以互相印證 |

⭐ **最後兩列是 §2.1 的獨立性檢定在「提示側」的版本。**
兩邊都測到綁定 → 綁定是表徵層次的;只有提示側測到 → 綁定是注意力選擇層次的。
**這是現設計最值錢的一組對比,而且兩邊用的是不同批 trial,不互相污染。**

**最小配方**

```python
d = df[(~df.is_practice) & (df.cue_valid == 0) & (df.outcome != 'noresp')]
d['e'] = d.err_rel.fillna(0).astype(int)
pi = {}
for r in (1, 2, 3):
    hit  = (d.loc[d.relation == r, 'e'] == r).mean()          # n = 64
    base = (d.loc[d.relation != r, 'e'] == r).mean()          # n = 128
    pi[r] = hit - base
# 群體: 每人一組 (pi1, pi2, pi3) -> repeated-measures ANOVA / 對比 pi1-pi2
# 或 GLMM: glmer(chose_cued ~ relation + (relation | subject), family = binomial)
```

**每人精度(本地算)**:π 真值 0.10 → SE(π̂) ≈ 0.046;π 真值 0.20 → SE ≈ 0.061。
兩個 relation 之差的 SE 約 0.053–0.071。
→ **單人只能看到 15 個百分點以上的不對稱。** 群體 n=30 時可偵測到約 1–1.3 個百分點。
⚠️ [[決策脈絡_統計方法]] §3 報的「估到 ±0.004」是**模擬全體**的精度,不是單人精度,
引用時不要混用。

**另一個可選基線**:也可以拿 valid 的 384 筆去估 `P(err_rel = r)` 當基線,樣本更大。
⚠️ 代價是 valid 與 invalid 的整體難度不同(probe 與記憶不衝突 vs 衝突),
基線會平移。**建議兩種都算,當作 robustness check;主分析用 relation≠r 的版本。**

---

### 2.3 一致性對比(跨感官對應):(C1B+C2P) vs (C2B+C1P)

**用哪些欄位** `target_item`、`is_correct`(或 `outcome`)、`cue_valid`、`is_practice`
**用哪些 trial** 主分析 `cue_valid == 1` → **每個 target_item 各 96 筆**;
穩健性檢查可加上 invalid(每 item 144 筆),但 invalid 上的正確率被 intrusion 壓低,
且壓低幅度依 relation 而異 → **不要混算**。

**怎麼算 —— 這就是一個 2×2 交互作用**

```
tgt_col = target_item & 1          # 0 = C1, 1 = C2
tgt_snd = (target_item >> 1) & 1   # 0 = B , 1 = P

一致性對比 C = ½[acc(item0) + acc(item3)] − ½[acc(item1) + acc(item2)]
           = 顏色 × 聲音 的交互作用對比,權重 (+1, −1, −1, +1)
```

同一個平衡計畫還免費給出兩個**正交**的主效果:

- **`tgt_snd` 主效果 = 使用者的 DV(1)**:acc(item0,1) − acc(item2,3) = **b vs p 的表現差**
- **`tgt_col` 主效果**:acc(item0,2) − acc(item1,3) = C1 vs C2 的表現差

三個對比正交,因為四格 trial 數完全相等(§1.2 核實:各 96)。

**⭐ 這個對比的設計乾淨度,比我預期的高**(§1.3a 的推論):
因為 `quad_content` 是排列,**每一試四個 item 全部在場**,四個選項也永遠是這四個 item。
→ 一致性的兩個水準**共用完全相同的刺激集、相同的畫面、相同的選項**,
差別只有「哪一個被 probe」。刺激層次的混淆在對比中相消。
→ 但相對地,它**測不到** display-level 的一致性效果([[brunetti2017]] 那型),
因為每個畫面都同時含兩個「一致」與兩個「不一致」的連言。

**虛無/對立假設 —— 而且方向不能由文獻決定**

[[voicing與顏色的跨感官對應]] §4 的結論(該檔標為「我的推論,信心中高」)是:

> 在等明度等彩度只動色相的設計下,這個對比**文獻傾向預測趨近零**。
> 理由是 voicing 與顏色之間唯一有實證基礎的通道是**明度**,而 AVWM 把明度固定在 L\*=55、
> C\*=38 只動色相角([[決策脈絡_顏色維度]]);而純色相在等明度等彩度下,
> 連最穩固的 pitch/loudness 對應都幾乎測不到([[anikin-johansson2019]]、[[spence2011]])。

因此這個對比在現設計裡有**兩個角色,擇一但要事前寫定**
([[聽覺維度_嘗試與放棄紀錄]] §6.5 已把這兩條列為要與老闆確認的事項):

| | 讀法 | 對應的假設 |
|---|---|---|
| (a) **設計乾淨性的控制** | C ≈ 0 是**預期結果**,證明四個連言之間沒有配對偏袒 → §2.2 的 intrusion 比較不被「某些配對天生好記」污染 | H₀ 成立即為設計通過 |
| (b) **若非零則是新發現** | 知覺路徑已被設計關閉(明度固定),所以任何非零效應**只能**走語意路徑(voiced ↔ 邪惡/負面,[[kawahara-kumagai2019]] z=5.87) | H₁ 成立即為可發表 |

⚠️ **哪一對算「一致」,文獻給不出方向。** [[voicing與顏色的跨感官對應]] §2.4 查證的結論是
**沒有任何研究測過藍-紫色相範圍(AVWM 錨點 303°)的聲音對應**,
連 [[anikin-johansson2019]] 唯一測到的微弱 hue 效應(pitch↔blue)都在藍-黃軸。
→ **檢定必須雙尾,而且「C1B+C2P 是一致的那一組」這個標籤是任意的、只用來定義對比方向。**
論文裡不能寫成「我們預測 voiced 配較暗的顏色」—— 那個方向在色相軸上沒有文獻依據。

**最小配方**

```python
d = df[(~df.is_practice) & (df.cue_valid == 1) & (df.outcome != 'noresp')]
d['col'] = d.target_item & 1
d['snd'] = (d.target_item >> 1) & 1
# 每人四格正確率
acc = d.groupby(['subject','target_item']).is_correct.mean().unstack()
C   = 0.5*(acc[0] + acc[3]) - 0.5*(acc[1] + acc[2])     # 一致性交互作用
D1  = 0.5*(acc[0] + acc[1]) - 0.5*(acc[2] + acc[3])     # DV(1): b vs p
# GLMM 版(建議,保留 trial 層次):
# glmer(is_correct ~ col * snd + (col * snd | subject), family = binomial)
#   交互作用項 col:snd 即 C;snd 主效果即 DV(1)
```

**每人精度(本地算)**:每格 96 筆、p ≈ 0.8 → **SE(C) ≈ 0.041**(p=0.7 時 0.047)。
n=30 且無受試者間變異時群體 SE ≈ 0.008 → 可偵測約 1.6 個百分點的一致性效果。
**⚠️ 但「趨近零」的預測要靠等價檢定(TOST)而不是 p > .05 才能宣稱**,
等價界要事前定(例如 ±0.02),否則 (a) 這條讀法拿不出證據。

---

### 2.4 兩維校準後的可比性

**用哪些欄位** `psi_col_alpha` `psi_col_beta` `psi_snd_alpha` `psi_snd_beta`
`colour_arc_lo` `colour_arc_hi` `snd_step_b` `snd_step_p`(`:964–971`,每人一列)
+ `adapt_*` 60 筆原始資料(`:939–945`)
+ valid 試次的 `err_rel` 邊際

**校準做了什麼(逐行核實)**

```
GRTv2.py:851  from AGRT import AGRTHandler          # 官方 handler
GRTv2.py:853  N_ADAPT     = 60                      # 一個 handler,每試同時更新兩條 Psi
GRTv2.py:854  OVERALL_ACC = 0.64
GRTv2.py:855  LAPSE       = 0.08
GRTv2.py:893  AGRTHandler(nTrials=60, lapse=.08, dim1range=[-24.13, +24.13], dim2range=[1,9], ...)
GRTv2.py:950  estimateGRTintensities(0.64, lams) -> ((c_lo,c_hi),(s_lo,s_hi))
GRTv2.py:960–962  覆寫 COLOUR_ARC / COLOUR_HEX / AUDIO_B / AUDIO_P
```

⚠️ **`:854` 的註解是錯的。** 它寫「目標整體正確率 -> 每維 sqrt(0.64) = 0.80」,但:

```
AGRT.py:406   estimateGRTintensities 把 np.sqrt(overallAccuracy) 傳給 estimateThreshold
AGRT.py:170   estimateThreshold 內部 又 取一次 np.sqrt(thresh)
→ 每維目標比例 = 0.64^(1/4) = 0.8944      聯合 = 0.8944² = 0.8000
```

本地驗算:`0.64**0.25 = 0.894427`,平方 = `0.80`。
與 [[決策脈絡_AGRT模型假設]]「❌ overallAccuracy 填多少就得到多少」一節、
以及 [[決策脈絡_統計方法]] §1 的表(`0.6400 | 單維 0.894 | 聯合 0.800`)完全吻合。
→ **正確說法是「兩維各校到 89.4%、聯合 80%」,不是「每維 80%」。**
📌 **待辦:`GRTv2.py:854` 的註解應該修掉,否則下一個讀 code 的人會再被誤導一次。**

**為什麼這讓兩個 DV 可比**

`psi_*_beta` 就是測量模型裡的知覺雜訊 SD(`AGRT.py:133`:`scale=self._beta`,
推導見 [[決策脈絡_AGRT模型假設]])。適應階段把**兩維的刺激間距各自撐到相同的
心理物理表現水準**(89.4%),意思是:

> 主實驗開始時,「一步 b→p」與「一階 ΔE00 色相差」在知覺上是**等難的**。

→ 因此「b/p 之間的表現差異」若不為零,**不能**再用「聲音本來就比較難分」來解釋 ——
知覺可辨度已經被等化掉了。剩下的差異落在**知覺之後**(編碼、維持、反應選擇)。

**怎麼算**

```
維度不對稱 A = P(err_rel ∈ {2,3}) − P(err_rel ∈ {1,3})     # 聲音錯 − 顏色錯,valid 384 筆
```

| | 心理機制 |
|---|---|
| A = 0 | 兩維在知覺等化後,記憶/反應階段也對稱 |
| A > 0 | **語音碼比顏色碼脆弱**:等知覺可辨度下,voicing 資訊先流失 |
| A < 0 | 顏色碼先流失 |

**共變項用法**

```python
psi = df.groupby('subject')[['psi_col_alpha','psi_col_beta',
                             'psi_snd_alpha','psi_snd_beta',
                             'colour_arc_lo','colour_arc_hi',
                             'snd_step_b','snd_step_p']].max()      # 每人一列
psi['beta_ratio']   = psi.psi_snd_beta / psi.psi_col_beta           # 兩維知覺雜訊比
psi['col_sep_dE00'] = psi.colour_arc_hi - psi.colour_arc_lo         # 實際色差(ΔE00)
psi['snd_sep_step'] = psi.snd_step_p    - psi.snd_step_b            # 實際步階距
# glmer(is_correct ~ col*snd + scale(beta_ratio) + (col*snd | subject), family = binomial)
# 或把 A、C、pi_r 當 outcome,對 beta_ratio 做受試者層次回歸
```

`α` 是決策界線位置 —— 對顏色而言是「受試者自己的藍/粉分界落在色相軸哪裡」。
`α` 明顯偏離 0 的人,`colour_arc_lo/hi` 會不對稱於錨點,他的兩個顏色**不是**對稱地
跨過類別邊界。[[決策脈絡_顏色維度]] 選 303° 就是為了離 283° 藍/紫邊界有 20° 餘裕;
**`psi_col_alpha` 可以直接檢查這個餘裕在每個人身上是否真的成立**,這是意外的紅利。

#### ⚠️ 三個會把「可比性」打折的東西(全部由程式碼核實)

**(a) 反應階段兩維不對稱 —— 這條最嚴重。**
選項的內容是 `final_value`(**色塊**)+ `TXT = ["[bɛ]","[bɛ]","[pɛ]","[pɛ]"]`(**文字標籤**),
`GRTv2.py:1832–1833`。所以:

- **顏色**:測驗時螢幕上同時出現 C1 與 C2 的**實際色塊** → 受試者做的是**有參照的比對**
- **聲音**:測驗時只有 `[bɛ]`/`[pɛ]` 兩個**文字標籤**,沒有任何聲音重播 → **絕對類別判斷**

而適應階段量的是**兩維都做絕對類別判斷**(`f = more blue / j = more pink`;
`f = like 'b' / j = like 'p'`,`GRTv2.py:914–919`)。
→ **校準等化的是「絕對分類」的難度,但主實驗只有聲音維度仍是絕對分類,顏色維度變成有參照的比對。**
有參照比對比絕對分類容易 → **顏色維度在主實驗會比校準時更容易,聲音不會。**
**結論:89.4% 的等化在反應階段被打破了,A > 0 有一部分可能只是這個。**
📌 pilot 必查:valid 正確率是否顯著高於 0.80;以及 `err_rel` 的顏色/聲音邊際是否嚴重偏斜。

**(b) `[bɛ]` / `[pɛ]` 的母音與刺激不符。**
刺激是 `stimuli/kutlu_mcmurray_2024/cv/beachpeach{1..9}_cv.wav`(`:856`),
即 beach/peach 剪成 CV → 母音是 **/i/**([[聽覺維度_嘗試與放棄紀錄]] §5.1、[[osf-kutlu-mcmurray-continua]])。
但標籤寫的是 **[bɛ] / [pɛ]**(ɛ 母音)—— 這是舊 `be.wav`/`pe.wav` 素材的殘留。
指導語也沒有解釋這套記號怎麼念。
📌 **建議改成 `[bi]` / `[pi]`(或直接寫 "b" / "p"),並在指導語裡示範一次。**

**(c) 89.4% 是模型預測值,不是量到的正確率。**
`estimateThreshold` 回傳的是「在估到的 (α, β) 下,理論上會給出該比例的刺激強度」。
適應程序本身的正確率**不能**當驗證(Psi 刻意把取樣集中在界線附近)。
→ **要驗證,只能用主實驗 valid 的實際表現去反推**,或加一段固定刺激的檢核 block。
[[聽覺維度_嘗試與放棄紀錄]] §6.1 已經提過類似的檢查點(端點採樣不足,建議 pilot 每端點加 10 次)。

---

## 3. 量不到的

### 3.1 ⛔ 最大的一條:指導語與計分不一致

```
指導語(GRTv2.py:406,逐字):
  "A marker will then point to one of the corners.
   Your task is to report which item was there."

計分(GRTv2.py:2175–2178):
  correct   = chosen_item == target_item     # = probe 呈現的內容
  intrusion = chosen_item == cued_item       # = 標記所指角落原本的 item
```

在 invalid 試次上,**照指導語做的人報 cued_item → 被記成 intrusion**;
報 probe 內容的人 → 被記成 correct。而主實驗**全程沒有逐試回饋**
(回饋只存在於適應階段,`:923–935`),練習結束只給一個總分(`:2225–2233`),
所以受試者**沒有任何管道學到哪種策略被算對**。

→ 現狀下,`intrusion` 這個量**混合了兩件事**:
(i) 注意力被提示捕獲(設計意圖),與
(ii) 受試者忠實執行了指導語。
**兩者在資料上完全不可分。**

⚠️ **這會直接改變 §2.2 的解讀,但不會讓 §2.2 失效**:
`relation` 是**隨機指派、不改變刺激**的,所以無論受試者採哪種策略,
π̂₁ vs π̂₂ vs π̂₃ 的**不對稱**仍然只能來自「哪個特徵較容易被從提示側取來」。
換句話說 **§2.2 的相對比較是安全的,絕對水準的解釋不安全。**

📌 **要收掉這一條,只需要改指導語**(說明「標記之後會出現一個顏色與聲音,請報告**那一個**」),
或反過來把計分改成 `correct = cued_item`(那會變成另一個實驗)。
**這是設計層次的決定,不是分析能救的,建議列為與老闆討論的第一項。**

### 3.2 完整 GRT 的 PS / PI / DS 參數擬合 —— 比我預期的樂觀

我原本要寫「4AFC 認記作業不是 identification confusion 設計」,**核實後這句話是錯的**:

valid 試次上,刺激 = probe 呈現的四個 item 之一、反應 = 四選一,
每刺激 **96 次**,構成一個標準的 **4×4 identification confusion matrix**。
[[soto2017]] 明文說「2×2 是領域主流設計,只需呈現四個刺激、量四個反應」,
本設計滿足這個條件。這也是 [[決策脈絡_統計方法]] §5 步驟 1 一直預設的做法。

**所以缺的不是設計型態,是三件別的事:**

| 缺什麼 | 為什麼 | 出處 |
|---|---|---|
| **試次數** | 96/刺激 vs [[silbert2012]] 的 200/刺激。且 89.4%×89.4% 的目標讓 12 個非對角格總共只分到 20% 的 384 筆 ≈ 77 次,單格平均約 6 次 | [[決策脈絡_統計方法]] §2「天花板比地板危險」 |
| **猜測不在模型裡** | §2.1(b) 的表:5% 亂猜 → logOR +0.8。GRT 沒有「受試者亂猜」這個參數,質量只能被推到 ρ 上 | 同型論證見 [[決策脈絡_統計方法]] §3 |
| **變異來源不可分離** | GRT 明文承認知覺雜訊與決策雜訊**只有和可估**;刺激變異是同一個和裡的第三項 | [[ashby-wenger-handbook]] |

**invalid 側**照 [[決策脈絡_統計方法]] §5 的流程(先用平衡的 relation 估 π、扣除、再擬合)
理論上可行,還原公式該檔已給:`M_grt[t, t^rel] = (M_obs[t, t^rel] − π/3) / (1 − π)`。
⚠️ 但那個還原是在**該檔自己的模擬**裡驗證的,**沒有在真實資料上驗證過**;
而且 §3.1 的策略混合會讓 π 的意義改變(π 不再是純粹的「捕獲率」)。

⚠️ **無母數檢定(marginal response invariance 這一類)適不適用,我不確定,也不編。**
`90_Sources/` 目前**沒有**任何一張卡片討論 MRI/MSI 的定義或適用條件
(逐檔 grep 過 `ashby-wenger-handbook`、`soto2017`、`silbert2012/2014/2018`、
`soto2015/2017`、`silbert-hawkins2016`、`kingston2008`、`ashby2000`,全部沒有)。
**要用它就得先建卡**(Kadlec & Townsend 一系),本檔按引用紀律不引入無卡文獻。
📌 待辦:若決定走無母數路線,先補卡再寫。

### 3.3 知覺錯誤 vs 記憶錯誤的定位

適應階段把每維校到 89.4%(§2.4),意思是 **valid 的 20% 聯合錯誤裡有一大塊是知覺的**,
而且那一塊**照設計就該存在**([[soto2017]]:GRT 在結構上就需要誤差)。

哪些對比會被它污染、哪些不會:

| 量 | 知覺成分的影響 | 為什麼 |
|---|---|---|
| §2.1 特徵獨立性(logOR) | ⛔ **會被污染** | 知覺階段本身就可能有 PI 違反(ρ ≠ 0)。valid 上「綁定丟失」與「知覺相關」在資料上同型,分不開 |
| §2.2 intrusion 不對稱(π̂) | ✅ **不會** | 減項與被減項用**同一批刺激、同一個難度**,`relation` 只換提示指向。知覺成分兩邊完全相同,相減即消 |
| §2.3 一致性對比(C) | ⚠️ **部分** | 四格刺激不同(四個連言),知覺可辨度可能本來就不等。但四格 trial 數相等、每試四個 item 全在場,主效果吸收掉大部分;交互作用受影響較小 |
| §2.4 維度不對稱(A) | ⛔ **會被污染** | 這正是校準要處理的,而校準在反應階段被 §2.4(a) 破壞了 |
| valid vs invalid 條件差(DV 2) | ✅ **不會** | 同一批刺激、同一個受試者,條件間相減。[[q1範圍聲明_素材]] §5 就是靠這一點 |

**一句話規則:條件間相減(π̂、DV 2)乾淨;跨刺激或跨維度的絕對比較(logOR、A)不乾淨。**

### 3.4 現設計拆不出來的

- **swap error vs feature error**(§2.1a):選項就是畫面上那四個 item,沒有 lure。
- **編碼階段 vs 維持階段**:study 的四個 item 是**依序**出現(START = 0.3/1.3/2.3/3.3,`:1169`),
  `target_serial` 有記錄(`:1581`)且完全平衡(每個 serial_pos × item 各 24 valid),
  所以**序列位置效果量得到**;但那是保留時間的代理,不是編碼/維持的直接分離。
- **display-level 的跨感官一致性**(§2.3):每個畫面必然同時含兩個一致與兩個不一致的連言。
- **顏色的「哪一端」與 voicing 的方向對應**:文獻給不出方向([[voicing與顏色的跨感官對應]] §2.4),
  只能雙尾。

---

## 4. q = 1:所有結論的天花板

聲音維度是 Kutlu & McMurray beachpeach 連續體:**一位語者、一對端點錄音**,
9 個步階是**同一條連續體上的點,不是 9 個獨立樣本**([[osf-kutlu-mcmurray-continua]];
[[q1範圍聲明_素材]] §1)。顏色維度同理 —— 一個錨點(303°)、一條色相弧。

依 [[clark1973]] pp. 352–354 的判準(「單一個案法只適用於對單一個案成立的假設」):

| 主張 | 撐得起? |
|---|---|
| 「**用這對刺激時**,invalid cue 使 intrusion 上升,且顏色/聲音不對稱」(§2.2) | ✅ |
| 「**用這對刺激時**,特徵一起丟失/獨立漂移」(§2.1) | ✅ |
| 「**用這對刺激時**,一致性對比不顯著」(§2.3,配 TOST) | ✅ |
| 「/b/–/p/ **這個類別**的語音表徵與顏色有關」 | ⛔ 集中趨勢假設 |
| 「**voicing 這個特徵**在工作記憶裡比顏色脆弱」(§2.4 的 A) | ⛔ 同上,而且外推更遠 |

⚠️ **§2.4 的 A(維度不對稱)是四個量裡外推最遠的一個** —— 它天然被讀成「voicing vs 顏色」的
特徵層次主張,但資料只支持「這個 b/p 連續體的這兩步 vs 這條色相弧的這兩點」。
**寫作時這一個特別需要範圍聲明擋住自動外推**([[q1範圍聲明_素材]] §3 的「中間地帶」)。
檢力天花板的數字(8 個刺激 → 檢力上限 ~.50,要 .80 需約 16 個刺激)見 [[westfall2014]]。

---

## 可連結脈絡

- 試次計畫與隨機化的原始決策 —— [[決策脈絡_實驗設計]]
- intrusion 污染 GRT、π̂ 的估計式與還原公式 —— [[決策脈絡_統計方法]] §3、§5
- `psi_*_beta` 是什麼、目標正確率的雙重開根號 —— [[決策脈絡_AGRT模型假設]]
- 顏色軸座標系(L\*55/C\*38/錨點 303°/ΔE00 弧長) —— [[決策脈絡_顏色維度]]
- 聲音刺激的來源與四條放棄的路 —— [[聽覺維度_嘗試與放棄紀錄]]、[[決策脈絡_聽覺維度]]
- §2.3 一致性對比預測趨近零的完整推論 —— [[voicing與顏色的跨感官對應]] §4
- q=1 範圍聲明的素材與逐字引句 —— [[q1範圍聲明_素材]]、[[clark1973]]
- GRT 需要誤差、2×2 是主流設計 —— [[soto2017]];語音 GRT 的試次數基準 —— [[silbert2012]]
- 變異來源只有「和」可估 —— [[ashby-wenger-handbook]]
- 色相在等明度等彩度下幾乎不承載聲學對應 —— [[anikin-johansson2019]]、[[spence2011]]
- voiced ↔「暗屬性」的語意證據(非知覺明度)—— [[kawahara-kumagai2019]]
- 跨感官一致性促進 WM 的方法學先例 —— [[brunetti2017]]
- 個體差異當共變項的 GRT 前例 —— [[soto2015]]

## 回查線索

**⛔ 現在跑下去拿得到資料嗎?**
→ **拿不到。** `trials` loop 是 `isTrials=False`(`GRTv2.py:1124` / `GRTv2.psyexp:1029`),
PsychoPy 因此不在迴圈裡產生 `thisExp.nextEntry()`,`TrialHandler2.__next__` 也不呼叫它
→ **600 個試次覆蓋成一列**。修法見 §1.5。逐行讀原始碼推出,未實跑。

**四個量分別從哪裡算出來?**
→ ①特徵獨立性:valid 384 筆,`err_rel` 攤成 2×2 的 logOR;
②intrusion 不對稱:invalid 每 relation 64 筆,π̂ᵣ = P(err_rel=r|relation=r) − P(err_rel=r|relation≠r);
③一致性:valid 每 target_item 96 筆,權重 (+1,−1,−1,+1) 的交互作用;
④維度可比性:同一批 valid 的 `err_rel` 邊際差,共變項用 `psi_*_beta`。

**為什麼特徵獨立性只能用 valid?**
→ invalid 上 intrusion 會把質量全灌進 `err_rel == relation` 那一格,
[[決策脈絡_統計方法]] §3 實測 10% intrusion 就能偽造出 ρ=0.5 的訊號。

**intrusion 率為什麼不能直接比?**
→ 亂錯的人也有 1/3 機率選到 cued_item,而且三個錯選項的混淆度本來就不等。
必須用 `relation ≠ r` 當基線相減 —— `relation` 隨機指派且不改變刺激,基線因此乾淨。

**猜測會怎麼影響 §2.1?**
→ **會憑空製造綁定訊號。** 本地算:真值完全獨立、5% 亂猜 → logOR ≈ +0.80;10% → +1.07。
必須做 break-even 的 ĝ 敏感度分析,不能只報 logOR。

**「兩維都校到 80%」對嗎?**
→ **不對,是每維 89.4%、聯合 80%。** `GRTv2.py:854` 的註解寫錯了;
`AGRT.py:406` 傳 `sqrt(0.64)` 進去、`AGRT.py:170` 內部又開一次根號 → `0.64^(1/4) = 0.8944`。
[[決策脈絡_AGRT模型假設]] 與 [[決策脈絡_統計方法]] §1 的表是對的。

**一致性對比若不顯著,算失敗嗎?**
→ 不算。[[voicing與顏色的跨感官對應]] §4 的預測就是趨近零(等明度設計把明度通道堵死了),
零結果是**設計乾淨性的證據**;若非零則是**語意路徑**的新發現。但要宣稱「零」需 TOST,不能靠 p > .05。

**完整 GRT 擬得動嗎?**
→ **valid 側擬得動**(4×4 混淆矩陣,每刺激 96 次)。缺的是試次數(vs [[silbert2012]] 的 200)、
猜測不在模型裡、以及變異來源本來就只有和可估([[ashby-wenger-handbook]])。

---

## ⚠️ 量不到 / 不確定的

**⛔ 0. 目前「一個都量不到」—— 因為存檔會把 600 個試次壓成一列**

`trials` loop 是 `isTrials=False`(`GRTv2.py:1124` / `GRTv2.psyexp:1029`)→
Builder 不產生迴圈內的 `thisExp.nextEntry()`(`experiment/loops.py:483–487`)→
`TrialHandler2.__next__` 也不呼叫它(`data/trial.py:1101–1103`)→
`addData` 只覆蓋 `thisEntry`(`data/experiment.py:300`)→
`entries` 只在 `nextEntry()` 成長(`data/experiment.py:702`)。
**證據鏈與兩條修法見 §1.5。這一條的優先序高於本檔其他所有內容。**
⚠️ 逐行讀原始碼推出,未實跑;跑 10 個試次數 CSV 列數即可證偽。

**確定量不到(設計層次,分析救不了)**

1. **注意力捕獲 vs 遵照指導語**(§3.1):指導語 `:406` 說報「那個角落原本是什麼」,
   計分 `:2175–2178` 卻以 probe 內容為正確。無逐試回饋 → 受試者學不到。
   **π̂ 的絕對水準因此不可解釋,但相對不對稱(π̂₁ vs π̂₂ vs π̂₃)仍安全。**
   📌 **建議列為與老闆討論的第一項。**
2. **swap error vs feature error**(§2.1a):選項只有畫面上那四個 item,沒有 lure。
3. **display-level 的跨感官一致性**(§2.3):每個畫面必含兩一致 + 兩不一致。
4. **編碼 vs 維持階段的分離**:只有 `target_serial` 這個代理。
5. **一致性對比的方向**:文獻查不到藍-紫色相範圍的任何聲音對應
   ([[voicing與顏色的跨感官對應]] §2.4),只能雙尾。

**量得到但會被污染(§3.3 的表)**

6. **§2.1 的 logOR** 同時吃到「知覺相關」與「記憶綁定」,valid 上分不開;
   而且 **5% 亂猜就造出 logOR ≈ +0.8**。
7. **§2.4 的 A(維度不對稱)**:反應階段兩維不對稱(顏色有參照色塊、聲音只有文字標籤,
   `:1832–1833`)—— 適應階段量的卻是兩維都做絕對分類。**89.4% 的等化在反應階段被打破。**

**程式碼層次的待辦(核實時發現,依優先序)**

7.5 ⛔ **`isTrials=False` → 資料存不下**(上面的 0;`GRTv2.py:1124` / `GRTv2.psyexp:1029`)。**先修這個。**

8. 📌 `GRTv2.py:854` 註解「每維 sqrt(0.64) = 0.80」**應改為「每維 0.894、聯合 0.80」**。
9. 📌 `GRTv2.py:1833` 的 `TXT = ["[bɛ]","[pɛ]"]` 與刺激母音不符
   (beach/peach → /i/)。**建議改 `[bi]`/`[pi]` 並在指導語示範。**
10. 📌 [[決策脈絡_實驗設計]] 記的是「576 分 12 個 block × 48」,
    **現行程式是 `BLOCK_SIZE = 144` → 4 個 block**(`:430`,指導語 `:406` 也寫 four blocks)。
    該檔需要更新。
11. 📌 [[聽覺維度_嘗試與放棄紀錄]] §6.1/§6.2 寫「45 trial 的聲音 Psi」「兩條 staircase」
    「`OVERALL_ACC_SND`」,**現行程式是單一 `AGRTHandler`、60 trial、視聽複合刺激、
    每試同時作兩個判斷**(`:853, 893, 898–919`),沒有 `OVERALL_ACC_SND` 這個常數。
    該檔的 §6 需要更新。

**不確定(標記,不編)**

12. **無母數 GRT 檢定(marginal response invariance 一類)適不適用 —— 我不確定。**
    `90_Sources/` 沒有任何一張卡片討論它的定義或適用條件(已逐檔 grep 九張 GRT 相關卡)。
    要用就得先建卡,本檔按引用紀律不引入無卡文獻。
13. **§1.5 的結論未實跑驗證**:PsychoPy 裝在 Windows 側(`/mnt/c/Program Files/PsychoPy/`,
    版本 `2026.1.1`,與 `GRTv2.py:42` 一致),原始碼逐行讀過,但沒有實際跑一次看 CSV。
    **跑 10 個試次數列數即可確認或推翻。**
14. **`colour_arc_lo` 是不是一定在藍側**(§1.1):從 `AGRT.py:170–171` 推得
    `colour_arc_lo < α < colour_arc_hi`,但 α 偏離錨點很多的受試者可能兩值同號。
    **分析時直接讀數值,不要假設符號。**
15. **valid 的實際正確率會不會遠高於 0.80**:因為顏色維度在測驗時有參照色塊(§2.4a)。
    **這是 pilot 的第一個檢查點**,也決定 §3.2 的「非對角格每格約 6 次」會不會更糟。
16. **[[決策脈絡_統計方法]] §5 的 intrusion 還原公式**只在該檔自己的模擬裡驗證過,
    未在真實資料上驗證;且 §3.1 的策略混合會改變 π 的意義。

---
標籤note:[[決策脈絡_索引]] [[GRT]] [[AVWM]]
