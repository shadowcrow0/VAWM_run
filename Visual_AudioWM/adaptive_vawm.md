# VAWM 的自適應校準（adaptive SFT）—— 怎麼跑

**這是什麼。** 這份文件說明：在跑 VAWM 主實驗之前，怎麼替每一位受試者量身訂做「顏色差多少」和「子音差多少」，
讓主實驗的「容易題」和「困難題」對每個人一樣難。

**一個比喻。** 像音樂會前的調音。每把琴（每位受試者）鬆緊不一樣；不先調音就直接合奏（直接跑主實驗），
最後聽到的差異是琴的問題還是演奏的問題，分不開。校準就是調音，主實驗才是演出。調音的結果（校到的差距）
會寫進一張表（`data/<subj>_calib.json`），主實驗照那張表出題。

每個決定的理由與生效位置：`DECISIONS.md`。

## 先認識幾個詞

- **salience（顯著度）**：兩個刺激「有多容易分辨」。顏色差得越遠、子音越不像，顯著度越高。
- **H / L**：High / Low salience。H = 容易分（差距大），L = 難分（差距小）。主實驗每一題都要有一個 H 版本和
  一個 L 版本，而且「容易」與「困難」的程度要跨受試者一致——這就是校準要做到的事。
- **ΔE**：兩個顏色在 CIELAB 色彩空間裡的距離，數字越大顏色差越遠。可以把它當顏色的捲尺。
- **foil（干擾音）**：聲音區塊裡，探測時播放的「不是目標、但跟目標子音有點像」的子音。
- **AA 試**：探測跟剛才記住的完全一樣的試次（A 對 A）。正確答案是「相同」。
- **假警報率（false alarm rate, FA）**：AA 試裡，受試者明明看到／聽到一樣的東西，卻按「不同」的比例。
  它告訴我們受試者「亂按不同」的底線在哪。
- **Psi**：一種「每一試都挑最有資訊量的強度」的自適應程序（Kontsevich & Tyler 1999）。像問二十個問題猜數字，
  每次都挑最能縮小範圍的問題。
- **lnrm2**：一種反應時間模型（LNRM）。想像兩個跑者在賽跑，一個代表「答對」、一個代表「答錯」，誰先到終點就
  按哪個鍵。「2」代表刺激強度用二次式（α·u + α₂·u²）影響跑者速度。
- **漂移差（drift separation, z₂ − z₁）**：上面兩個跑者的速度差。差越大，「答對」那個跑者贏得越快越穩，
  反應時間越短、正確率越高。
- **後驗（posterior）**：模型擬合完之後，對每個參數「相信的分布」——不是單一個數字，而是一堆可能值和各自的
  可信程度。從這個分布抽出來的每一筆樣本叫一個 draw。
- **PyMC**：做這種貝氏擬合的 Python 套件。NUTS 是它抽後驗樣本的演算法。
- **DFP（double factorial paradigm，雙因子派典）**：主實驗的設計——顏色 H/L × 聲音 H/L 四格，看反應時間怎麼變。
- **SIC / MIC**：從四格反應時間算出的兩個指標（survival / mean interaction contrast）。曲線的形狀告訴你
  顏色和聲音是「平行處理」還是「序列處理」、是「一個夠就停」還是「兩個都要」。這是整個實驗最後要回答的問題。

## 整體流程

```
   ① VAWM_calibrate.py            區塊 1 校顏色差距、區塊 2 校子音混淆度（作業 = VAWM_nobox 的 study → probe → y/n）
          │                       METHOD = "lnrm"（原始 adaptiveSFT）或 "psi"
          │  data/<subj>_calib.json（ΔE_H、ΔE_L、count_H、count_L、假警報率、α、β）
          ▼
   ② make_adaptive_blocks.py      → stimuli/block1..6.csv（欄位與 practice.csv 完全相同）
          │
          ▼
   ③ VAWM_nobox.py                主實驗照舊（它讀 stimuli/block*.csv）
          │  data/<subj>_VAWM_<date>.csv
          ▼
   ④ python -c "from adaptive_vawm import analyze_vawm; print(analyze_vawm('data/<subj>_VAWM_….csv')['report'])"
                                  SIC / MIC / dominance → 預測架構
```

用白話說：

1. **調音**（`VAWM_calibrate.py`）：受試者做兩個區塊的作業。區塊 1 找出「這個人要顏色差多少才算容易／困難」，
   區塊 2 找出「子音要多像才算容易／困難」。結果存成一個 json 檔。
2. **印題本**（`make_adaptive_blocks.py`）：拿 json 裡的數字，產生六個 block 的刺激表。格式跟原本手工做的
   `practice.csv` 一模一樣，所以主實驗程式完全不用改。
3. **演出**（`VAWM_nobox.py`）：主實驗照舊跑。
4. **事後分析**（`analyze_vawm`）：算 SIC / MIC，再加 dominance 檢驗（確認 H 真的比 L 快），推出處理架構。

## 兩種校準方法

定案（2026-10-02）：實驗用 `adaptiveSFT/decisions_for_author.md` 的 **B**——LNRM 分支、目標是漂移差（不是正確率）、
ogival 模型照 adaptiveSFT 的重建（½L·inv_logit、L = 10 固定、Normal(0, 2) 先驗）。`LINK` 預設 `"quadratic"`（lnrm2，
原檔、已對 Stan 驗證），`"ogival"` 換成 lnrm2a。Psi 版保留但不是實驗用的。

白話版：我們選了 Houpt 原本的做法（LNRM），而且瞄準的是「兩個跑者的速度差」，不是「答對幾成」。模型的
「強度→速度」關係有兩種寫法：`quadratic`（二次式，原始 Stan 檔還在，Python 版對過答案）和 `ogival`（S 形曲線，
原檔遺失，是照文件重建的）。預設用前者。Psi 是備用方案，留著但不拿來做實驗。

**`LINK` 和 `H_TARG` / `L_TARG` 是綁在一起的。** ogival 的分離上限是 L = 10，目標是「L 的幾分之幾」：Houpt 的
8.0 / 1.3 = 80% / 13%，合理；2.0 / 0.5 = 20% / 5% 落在曲線底部，L 會反解到層級範圍外（測試裡量到 ΔE −19）。
quadratic 沒有上限，2.0 / 0.5 是 power scan 建議的值。所以：`LINK = "quadratic"` 配 2.0 / 0.5，
`LINK = "ogival"` 配 8.0 / 1.3（或自己從 L 的比例算）。

為什麼綁在一起：S 形曲線有天花板（最高 10）。目標 2.0 只是天花板的 20%，落在曲線最平的底部；在那裡反推
「要多大的顏色差」會得到荒謬的答案（負的 ΔE）。二次式沒有天花板，所以 2.0 / 0.5 才合理。換曲線就要換目標值。

| | `METHOD = "lnrm"`（**原始 adaptiveSFT**，預設） | `METHOD = "psi"` |
|---|---|---|
| 強度怎麼選 | 定值刺激法：6 層固定，各 `N_PER_LEVEL`（8）試，打散 | Psi 逐試選熵最小的 x |
| 用到的資料 | 正確率 **+ RT**（「不同」試） | 只有正確率 |
| 模型 | lnrm2（`adaptivesft.models_v2.fit_lnrm_v2`，似然全用 PyMC 內建 `LogNormal` 的 logp/logcdf，PyMC NUTS，區塊結束時擬合 20–40 s） | 累積常態心理計量函數 |
| 目標 | 漂移差 `H_TARG` / `L_TARG`（z₂ − z₁；預設 2.0 / 0.5，Houpt 8.0 / 1.3） | 「答不同」機率 `P_HIGH` / `P_LOW` |
| 反解 | `adaptivesft.salience.find_salience`（`adaptiveSFT_functions.R:229-232` 的公式，只用 α₂ < 0 的 draw） | `salience_levels` |
| 實驗機器要什麼 | **完整 adaptivesft 套件（PyMC）** + PsychoPy 在同一個 Python ≥ 3.10 | 只要 `psi.py`（numpy + scipy） |
| 每區塊試次 | 6 × 8 + 24 AA = 72 | 72（含 1/3 AA） |

逐列解釋：

- **強度怎麼選**：lnrm 版像「定值刺激法」——事先訂好 6 個差距，每個差距出 8 題，順序打散。Psi 版則每一題
  都臨時決定出哪個差距（挑「熵最小」= 最能減少不確定性的那個）。
- **用到的資料**：lnrm 版同時看「答對沒」和「花了幾秒」；Psi 版只看答對沒。
- **模型**：lnrm 版在區塊結束時用 PyMC 跑一次擬合，要等 20–40 秒。Psi 版用的是一條 S 形的心理計量函數
  （累積常態），每題即時更新，不用等。
- **目標**：lnrm 版瞄準「速度差」；Psi 版瞄準「答『不同』的機率」。
- **反解**：擬合完得到參數，再反過來問「要多大的差距，速度差才會剛好是目標值」。lnrm 版用 Houpt 的 R 公式，
  而且只用後驗裡 α₂ < 0 的 draw（理由見 `DECISIONS.md` 第 5 條）。
- **實驗機器要什麼**：lnrm 版要在跑實驗的電腦上裝完整的 adaptiveSFT（含 PyMC）；Psi 版只要一個檔案。
- **每區塊試次**：兩種都是 72 試。

兩者共用同一個試次產生器（`make_colour_trial` / `make_audio_trial`），差別只在強度怎麼來、結束時怎麼算。
類別只有兩個：`LNRMCalibrator(dim, …)` 與 `PsiCalibrator(dim, …)`，`dim` 是 `"colour"` 或 `"audio"`；結果是普通 dict。json 的 `colour.p_high` / `p_low` 在 lnrm 下放的是 `H_TARG` / `L_TARG`；`extra.method` 標明方法，
`extra.params` 是 lnrm2 五個參數的後驗平均，`extra.high_median` / `low_median` 是逐 draw 反解的中位數（平均的對照）。

也就是說：一題長什麼樣（兩個顏色、兩個聲音、一個探測）兩種方法完全相同；不同的只是「這題的差距是誰決定的」
和「區塊結束時怎麼算出 H / L」。json 裡 `p_high` / `p_low` 這兩個欄位名字是 Psi 時代留下的；用 lnrm 時裡面放的
其實是漂移差目標。`high_median` / `low_median` 是用另一種方式（中位數）算出的 H / L，拿來跟主結果對照，
兩者差很多就代表擬合有問題。

```
   lnrm：  6 層 × 8 試 ──► (x, correct, rt) ──► fit_lnrm_v2(link="quadratic") ──► {μ, α, α₂, varZ, ψ}
                                                                                    │
                                        ΔE_H, ΔE_L  ◄── 換回物理單位 ◄── 解 2·(α·u + α₂·u²) = H_TARG / L_TARG
```

讀法：左到右，48 題「不同」試的（差距、對錯、秒數）餵進模型，吐出五個參數；再從右到左，解一條二次方程式
找出「速度差剛好等於目標」的差距 u，最後換回 ΔE 或混淆次數。

強度送進模型前縮放：顏色 `u = ΔE / 10`、聲音 `u = x + 2.7`（`x = −log10(count+1)`，平移到 ≥ 0，否則 R 的
反解公式取錯根）。聲音的層級會貼到目標子音可用的 foil，所以實際的 u 是散的（測試裡 29 個不同值），lnrm2 直接
對實際值擬合。

為什麼要縮放：模型的先驗（擬合前對參數的預設想像）是為「幾個單位」的強度設計的。ΔE 可以到 45，直接塞進去
會讓參數擠在很小的尺度。聲音軸的 x 是負數，而 R 公式解二次方程式時固定取「較小的根」，x 為負會取到錯的那一個；
整個往右移 2.7 讓它變正就好。另外聲音這邊，模型想要「差距 −1.6」，但目標子音的 foil 不一定剛好有這個值，
只能貼到最接近的，所以實際出現的差距比 6 個多（測試裡 29 個）。模型對實際值擬合，不受影響。

## 一次性

這一節講「哪台電腦要裝什麼」。只需要做一次。

```
   實驗機器（PsychoPy）                                  分析機器（Arc 或任何有 Python ≥ 3.10 的地方）
   ─────────────────────────────────────────────         ──────────────────────────────────────────
   ① VAWM_calibrate.py  ② make_adaptive_blocks           ④ analyze_vawm、adaptiveSFT 的 pytest
   ③ VAWM_nobox.py
   lnrm：Python ≥ 3.10 + psychopy + adaptiveSFT 同一環境   pip install -e <adaptiveSFT 路徑>
   psi ：只要 adaptiveSFT/adaptivesft/psi.py（numpy+scipy）
         clone 在隔壁或設 ADAPTIVESFT_PATH，不用裝
```

實驗機器（lnrm）建環境，Windows / macOS 都一樣（Arc 不行：沒螢幕沒聲卡，`psychopy-env` 又是 Python 3.6）：

```bash
conda create -n vawm python=3.10
conda activate vawm
pip install psychopy                                         # 2023.2+ 支援 3.10
git clone https://github.com/shadowcrow0/adaptiveSFT.git     # 放在 Visual_AudioWM 隔壁，或任何地方
pip install -e ../adaptiveSFT                               # 帶 PyMC、numba
python -c "import psychopy, pymc; print(psychopy.__version__, pymc.__version__)"
python VAWM_calibrate.py
```

這六行在做什麼：開一個乾淨的 Python 3.10 環境（像開一個新抽屜，不跟別的東西混）、裝 PsychoPy、把 adaptiveSFT
下載到旁邊、裝進去、確認兩個套件都叫得到、然後開始校準。Arc（實驗室的計算伺服器）沒有螢幕也沒有聲卡，
不能跑實驗；它上面現成的 `psychopy-env` 是 Python 3.6，太舊，裝不了 adaptiveSFT。

**PsychoPy 獨立版（Windows，就是 Coder 用的那個 Python）直接裝，不用 conda（2026-10-19 實測）：**
獨立版的 `site-packages` 在 Program Files、不可寫。**而且 Coder 啟動腳本時，psychopy 會把 `PYTHONUSERBASE` 指到 `%APPDATA%\psychopy3\packages`**（`psychopy/__init__.py:78`），所以一般 `pip --user` 裝到的 `%APPDATA%\Python\…` Coder 看不到——要先把 `PYTHONUSERBASE` 設成同一個目錄再 `--user` 裝，不用管理員：

```bat
set PYTHONUSERBASE=%APPDATA%\psychopy3\packages
"C:\Program Files\PsychoPy\python.exe" -m pip install --user pymc numba arviz nutpie
"C:\Program Files\PsychoPy\python.exe" -m pip install --user --no-deps -e "C:\...\adaptiveSFT"
"C:\Program Files\PsychoPy\python.exe" -c "import pymc, nutpie, adaptivesft; print(pymc.__version__)"
```
（或直接執行 repo 裡的 `setup_pymc_coder.bat`。）pip 不會動到獨立版的 numpy 2.2.6 / scipy 1.14.1，PsychoPy 不受影響；
要還原就 `pip uninstall`。裝完 Coder 直接跑 `VAWM_calibrate.py`，`METHOD = "lnrm"` 不用改。

**為什麼要 nutpie**：Windows 上沒有 g++，PyTensor 會退回純 Python 執行（啟動時印 `g++ not detected`），
PyMC 預設 NUTS 連 200/200/1 chain 的縮短擬合都要 5 分鐘，正式的 1000/1000/4 要 20 分鐘以上，受試者等不了。
`nutpie`（Rust 版 NUTS，用 numba 編譯 logp，有 win-64 wheel）同一台機器正式設定 **69 s**，α/α₂ 回復與預設採樣器一致、
零 divergence。`fit_lnrm_v2(**sample_kwargs)` 會把 `nuts_sampler="nutpie"` 原樣傳給 `pm.sample`，所以只要 `FIT_KW` 加這一個鍵
（`VAWM_calibrate.py` 已加）。conda-forge 路線（`conda create -n vawm -c conda-forge python=3.10 pymc` 會附編譯器）也行，
但 Coder 就得從那個環境用 `python -m psychopy.app.psychopyApp` 啟動。

`adaptive_vawm.py` 直接按檔案載入 `psi.py`（`load_psi_module`），不執行套件的 `__init__.py`，所以 PsychoPy
standalone 的 Python（沒有 PyMC）也能跑 psi 版校準。`METHOD = "lnrm"` 與分析端 `analyze_vawm` 才載完整套件
（`load_full_package`）。

注意：本 repo 自己有一個舊的 `adaptivesft/`（PyMC LNRM 版）會遮住裝好的套件，`adaptive_vawm.py` 會自動繞過。

白話：如果只用 Psi 版，連裝都不用裝，程式會自己去隔壁資料夾抓那一個檔案。另外這個 repo 裡有個同名的舊資料夾
會「搶名字」，程式已經會自動避開，不用手動刪。

## 校準的設計

| | 顏色（區塊 1） | 聲音（區塊 2） |
|---|---|---|
| 軸 x | 探測色與目標色的 CIELAB 距離（`colorpool.py` 的 `delta_e`，與 csv 的 `*_deltaE` 同單位），2–50 | −log10(混淆次數 + 1)（`generate_trials.py` 的 Miller & Nicely 表），Psi 提的值貼到目標子音可用的 foil |
| 每試 | 兩個目標色 + 兩個目標音，探測 = 其中一個目標的顏色 ± x 與它自己的聲音 | 探測 = 目標色 + 目標子音的 foil（同 talker） |
| AA 試 | 1/3（探測 = 目標），估假警報率當心理計量函數的下漸近線 | 同 |
| 模型 | `P(答「不同」\| x) = FA + (1 − FA − lapse)·Φ((x − α)/β)`，Psi 逐試選熵最小的 x | 同 |
| 輸出 | ΔE_H、ΔE_L（目標「答不同」機率 .90 / .75，可改） | count_H、count_L |
| 試次 | 72 | 72 |

H = 高 salience = 容易分：顏色 ΔE 大、子音混淆次數少（同 csv 現有的 `audio1_H_count = 1`、`L_count = 91`）。

逐列解釋：

- **軸 x**：顏色的「差多少」用 ΔE 量。聲音的「差多少」用 Miller & Nicely（1955）的混淆表：兩個子音被聽錯的
  次數越多就越像。取 −log10(次數 + 1) 讓「次數少 = 數字大 = 好分」。
- **每試**：一題就是主實驗的一題——先記兩個顏色、兩個聲音，再看一個探測，答「相同／不同」。顏色區塊只動顏色
  （探測色 = 某個目標色往外推 x），聲音照播原本的；聲音區塊只動聲音（換成 foil，同一個說話者），顏色照原本的。
- **AA 試**：每三題有一題探測跟目標完全一樣。這些題不用來擬合，只用來算假警報率。
- **模型**（Psi 版）：答「不同」的機率從底線 FA 一路升到接近 1，中間是一條 S 形曲線；α 是曲線的中點，β 是
  它有多陡。
- **輸出**：顏色區塊給兩個 ΔE，聲音區塊給兩個混淆次數。
- **試次**：各 72。

## 參數（`VAWM_calibrate.py` 最上面）

`METHOD`；lnrm：`N_PER_LEVEL`（8）、`H_TARG` / `L_TARG`（2.0 / 0.5）、`FIT_KW`（NUTS 1000/1000/4 鏈）、層級
`LEVELS_COLOUR`（ΔE 2–45）/ `LEVELS_AUDIO` 在 `adaptive_vawm.py`；psi：`N_COLOUR` / `N_AUDIO`（72）、
`P_HIGH` / `P_LOW`（.90 / .75）、Psi 網格在 `PsiCalibrator.__init__`；共用 `P_MATCH`（1/3）。
漂移差目標怎麼選見 `adaptiveSFT/results/power_scan.csv` 與 `p6_results.md`：8.0 / 1.3 在 a = 3、v = 2 下 H 超出
範圍，2.0 / 0.5 在範圍內且 SIC 判對率最好。

白話：所有可以調的數字都在 `VAWM_calibrate.py` 開頭那一小段，改那裡就好，不用進到程式深處。`FIT_KW` 的
「1000/1000/4 鏈」是 PyMC 抽樣的設定：先暖身 1000 步、再正式抽 1000 筆、四條鏈平行跑；電腦慢可以改成 2 條鏈。
目標值 2.0 / 0.5 不是拍腦袋：用模擬受試者掃過一遍（power scan），Houpt 的 8.0 會要求「超出我們能出的最大顏色差」，
2.0 / 0.5 做得到，而且事後 SIC 判斷架構的正確率最高。

## 驗證

`tests/test_adaptive_vawm.py`（10 個）：Psi 版模擬受試者跑完兩個區塊回復 α/β/FA；audio 的 foil 一定是該子音表裡的；
產生的 block csv 欄位 = `practice.csv`、ΔE 在 ±0.5、H 的 count ≤ L 的；VAWM 格式的輸出 → 判對 ParallelOR；
lnrm 版（quadratic 兩個維度 + ogival 一個）用賽跑模型生成的受試者回復 α/α₂ 或 slope/midpoint，H/L 對上閉式反解。
要 PyMC 的四個（分析、三個 lnrm）沒有 PyMC 就自動 skip；其餘六個只要 numpy + scipy。
PsychoPy 的 `VAWM_calibrate.py` 在這個容器裡只做過 `py_compile`。

白話：測試用「假的受試者」（電腦模擬、已知真實答案）跑一遍校準，確認程式能把真實答案找回來；再確認產生的
題本格式正確、H 真的比 L 容易；最後拿一份假的主實驗資料跑分析，確認它判得出正確的架構。真正的 PsychoPy 畫面
在這個開發環境裡沒跑過（沒螢幕沒聲卡），只確認過程式碼沒有語法錯誤——所以第一次在實驗機器上跑時要有人盯著。

## 順便修的 bug

`VAWM_nobox.py` 練習回饋：`rule.csv` 的 `ResponseBox` 欄是 Cedrus 按鍵碼 3/4，鍵盤版收到 `'y'`/`'n'`，查表永遠失敗，
練習階段每一試都顯示 Incorrect。已改成 `{'y': '4', 'n': '3'}` 對照。主實驗六個 block 不算 Acc（離線算），不受影響。

白話：練習階段的答案表是為 Cedrus 按鍵盒寫的（按鍵編號 3、4），改用鍵盤後收到的是字母 y、n，對不上，所以
不管怎麼按都說你錯。現在加了一張對照表。主實驗的對錯是事後離線算的，沒有被這個 bug 影響過。

## 所以你要做什麼

1. 在實驗機器上照「一次性」那六行指令建好環境（只做一次）。
2. 每位受試者：先跑 `python VAWM_calibrate.py`（兩個區塊，各 72 試，每個區塊結束要等 20–40 秒擬合），
   再跑 `make_adaptive_blocks.py`，再照舊跑 `VAWM_nobox.py`。
3. 校準結束畫面若出現「H/L 落在範圍外」的警告，不要直接進主實驗；先看 `data/<subj>_calib.json` 的 `warnings`。
4. 想改目標值、試次數、層級：只改 `VAWM_calibrate.py` 最上面的參數，改完先跑 `pytest tests/test_adaptive_vawm.py`。
   記得 `LINK` 換 `"ogival"` 就要把目標換回 8.0 / 1.3。
5. 資料收完，在任何有 Python ≥ 3.10 的機器上跑第 ④ 步的 `analyze_vawm`，看 SIC / MIC 的報告。
