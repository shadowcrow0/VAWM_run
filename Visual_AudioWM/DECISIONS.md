# DECISIONS —— 自適應校準的每個決定：決定了什麼、為什麼、在哪裡生效

**這是什麼。** 這份文件記錄校準程式裡每一個「本來可以選別的做法、但我們選了這個」的決定，以及選錯會出什麼事。

**一個比喻。** 像房子的裝修紀錄：牆裡的管線為什麼這樣走、哪面牆是承重牆不能拆。三年後要改東西，先讀這個，
就不會拆錯牆。

三年後回來先讀這個。每條三段：**決定**（選了什麼）、**為什麼**（不這樣選會出什麼事）、**在哪**（程式裡哪一行）。
行號是 2026-10-04 核對過的；行號飄了就用 grep 找那個名字。
更長的推導在 `adaptive_vawm.md`、`adaptiveSFT/decisions_for_author.md`、`adaptiveSFT/issue.md`。

幾個會反覆出現的詞（詳細版在 `adaptive_vawm.md` 開頭）：
**salience** = 刺激有多容易分辨，**H / L** = 容易 / 困難兩個等級；**ΔE** = 顏色距離；**foil** = 探測時播放的
干擾子音；**AA 試** = 探測跟目標一樣的題；**假警報率** = AA 試裡按「不同」的比例；**lnrm2** = 兩個跑者賽跑的
反應時間模型；**漂移差** = 兩個跑者的速度差；**後驗** = 擬合後每個參數的可信分布，抽出來的每一筆叫 draw；
**PyMC** = 做貝氏擬合的 Python 套件；**Psi** = 逐試挑刺激的自適應程序；**SIC / MIC** = 從主實驗四格反應時間
算出的架構指標。

```
   VAWM_calibrate.py ──► data/<subj>_calib.json ──► make_adaptive_blocks.py ──► stimuli/block*.csv ──► VAWM_nobox.py
          │                                                                                                 │
   adaptive_vawm.py（校準邏輯）                                   analyze_vawm()（事後：SIC / MIC → 架構） ◄──┘
          │
   ../adaptiveSFT/adaptivesft/（Psi、lnrm2 擬合、反解、SIC）
```

讀法：上面一排是受試者會經過的四個步驟（校準 → 存檔 → 產生題本 → 主實驗）。`VAWM_calibrate.py` 只負責畫面，
真正的校準邏輯在 `adaptive_vawm.py`，它再去隔壁的 adaptiveSFT 借模型。

## 1. 校準方法：原始 adaptiveSFT（LNRM），不是 Psi
- **決定**：`METHOD = "lnrm"`。固定 6 個強度各 8 試 + 1/3 AA 試，收正確率 + RT，區塊結束擬合 lnrm2，反解漂移差。
- **為什麼**：老闆要的是 Houpt 2018–2019 的方法（RT 也進模型）。選 Psi 就只用對錯、丟掉反應時間，
  跟 Houpt 的做法不一樣，結果不能直接比。Psi 版（只用正確率）保留當備案，不需要 PyMC。
- **在哪**：`VAWM_calibrate.py:73`；`adaptive_vawm.py` 的 `LNRMCalibrator` / `PsiCalibrator`。

## 2. 目標是「漂移差」，不是「正確率」（adaptiveSFT 決定 B）
- **決定**：H / L 由 `2·(α·u + α₂·u²) = H_TARG / L_TARG` 反解，單位是兩個累積器的漂移差 z₂ − z₁。
- **為什麼**：主實驗（SFT）看的是反應時間能不能拉開，而「兩個跑者的速度差」直接決定反應時間；
  瞄準正確率是繞一圈。`decisions_for_author.md` A.6 第 3 點：正確率目標和漂移差目標只差一個 varZ，SFT 要的是 RT 拉得開，
  漂移差直接對應 RT。老闆 2026-10-02 選 B。
- **在哪**：`VAWM_calibrate.py:77`；反解公式 `adaptiveSFT/adaptivesft/salience.py:84`（`adaptiveSFT_functions.R:229-232` 逐字）。

## 3. 目標值 2.0 / 0.5，不是 Houpt 的 8.0 / 1.3
- **決定**：`H_TARG, L_TARG = 2.0, 0.5`（配 `LINK = "quadratic"`）。
- **為什麼**：用 Houpt 的 8.0，模擬受試者需要的顏色差會超出我們能呈現的最大值——校準會告訴你「做不到」。
  `adaptiveSFT/results/power_scan.csv`（a = 3, v = 2 的 DDM 受試者）：8.0 時 H 落在刺激範圍外 10/10；
  2.0 / 0.5 在範圍內，250 試/格時 PAR-OR 9/10、PAR-AND 8/10、COA 7/10。ogival 的 L = 10 上限下 2.0 / 0.5 只是
  曲線的 20% / 5%，反解會掉到範圍外，所以 **換 `LINK = "ogival"` 就要換回 8.0 / 1.3**。
- **在哪**：`VAWM_calibrate.py:77-78`；預設值 `adaptive_vawm.py:99-100`。

## 4. 模型用 lnrm2（quadratic），ogival 是備案
- **決定**：`LINK = "quadratic"`。
- **為什麼**：quadratic 的原始 Stan 檔還在，Python 版算出來的答案跟它對過，所以可以相信；ogival 的原檔遺失，
  現在的版本是照文件猜著重建的，沒有東西可以對。`lnrm2.stan` 是 repo 裡唯一還在的原檔，Python 版對過 Stan（Arc、cmdstanr 2.40.0，五個參數後驗平均差
  ≤ 0.01 SD，`adaptiveSFT/tests/test_lnrm_vs_stan.py`）。ogival 的 `lnrm2a.stan` 已遺失，是重建（½L·inv_logit、L = 10）。
- **在哪**：`VAWM_calibrate.py:78`；`adaptiveSFT/adaptivesft/models.py:118`。

## 5. 反解只用 α₂ < 0 的後驗 draw
- **決定**：`alpha2_rule = "filter"`。
- **為什麼**：反解是解一條開口向下的二次方程式；後驗裡有些 draw 的 α₂ 是正的（開口向上），公式在那些 draw
  會給出負的顏色差，一起平均就把答案拉成負數。WM 資料下約三成 draw 的 α₂ > 0，R 的公式在那些 draw 給負根，全部平均會得到 −49 之類的值
  （`tests/test_adaptive_vawm.py` 第一版就撞到）。中位數與 filter 後的平均一致。`"all_draws"` 是 R 字面。
- **在哪**：`adaptive_vawm.py:415`；規則實作 `adaptiveSFT/adaptivesft/salience.py:96-125`。

## 6. 強度進模型前先縮放
- **決定**：顏色 `u = ΔE / 10`；聲音 `u = x + 2.7`。
- **為什麼**：模型的先驗是為「幾個單位」的強度設計的；ΔE 直接塞到 45，參數會被擠到很小的尺度。聲音軸的數字
  是負的，而反解公式固定取「較小的根」，負數會讓它取錯邊。lnrm2.stan 的先驗是 α ~ N(0, 2)、α₂ ~ N(0, 1)，ΔE 到 45 會讓 α 掉到 0.05 的尺度。聲音 x 是負的
  （−2.66…−0.3），R 的反解公式取「較小根」，x 為負時會取錯根，平移到 ≥ 0 才對。
- **在哪**：`adaptive_vawm.py:101`、`to_model_units` `adaptive_vawm.py:301`。

## 7. 強度層級
- **決定**：顏色 ΔE [2, 6, 12, 20, 30, 45]；聲音 x [−2.6, −2.1, −1.6, −1.1, −0.7, −0.3]。
- **為什麼**：層級要蓋住受試者可能落的範圍，否則校出來的 H 或 L 會掉在我們沒測過的地方。現有手工 csv 的 L 在 ΔE 20–30、H 在 25–50，層級要蓋住它們；最低 2 是因為模擬受試者的 L 反解到 3。
  聲音層級是整個混淆表的範圍，每試貼到目標子音實際有的 foil（`foil_for`）。
- **在哪**：`adaptive_vawm.py:97-98`、`adaptive_vawm.py:212`。

## 8. 兩個軸的定義
- **決定**：顏色 = CIELAB 歐氏距離（ΔE76）；聲音 = −log10(混淆次數 + 1)，次數少 = 好分 = H。
- **為什麼**：校準量出來的數字要能直接填進主實驗的題本。用現有題本同樣的單位，主實驗程式一行都不用改；
  換單位就要改 `VAWM_nobox.py`。與現有 `block*.csv` 的 `*_deltaE` 和 `*_count` 同單位，`VAWM_nobox.py` 不用改。
  ΔE76 是 `colorpool.py:9-10` 的定義（不是 ΔE00）；混淆表是 `generate_trials.py` 的 Miller & Nicely 1955。
- **在哪**：`adaptive_vawm.py` 的 `delta_e`、`audio_x`。

## 9. AA 試佔 1/3，用來估假警報率
- **決定**：`P_MATCH = 1/3`；AA 試不進模型，只算「答不同」的比例當 FA。
- **為什麼**：在「相同／不同」作業裡，受試者就算什麼都沒看出來也會有一定比例按「不同」，曲線的底不是 0；
  沒有 AA 試就量不到這個底線，也看不出受試者有沒有亂按。yes/no 作業的心理計量函數下漸近線不是 0，Psi 版要 FA 當 lower；lnrm 版拿它檢查受試者有沒有亂按。
  不到 5 筆 AA 試就用 `floor_guess = 0.10`。
- **在哪**：`VAWM_calibrate.py:74`；`false_alarm_rate` `adaptive_vawm.py:293`。

## 10. 校準試次的作業 = 主實驗的作業
- **決定**：校準試次完整跑 study（兩色兩音）→ probe → y/n，不是單純的辨別作業。
- **為什麼**：用單純的「兩個顏色比一比」校出來的差距，拿到要記東西的主實驗會變得太難——校到的值要反映工作記憶負荷下的極限，不是裸知覺。代價是每試 ~8 s，所以每區塊只 72 試。
- **在哪**：`VAWM_calibrate.py` 的 `run_trial`；`make_colour_trial` / `make_audio_trial`。

## 11. 實驗機器需要 PyMC；分析在 Arc
- **決定**：lnrm 版在實驗中即時擬合，所以實驗機器要 Python ≥ 3.10 + PsychoPy + adaptiveSFT 同一環境。
- **為什麼**：校完才能出主實驗的題本，所以擬合一定要在受試者還坐在那裡的時候做完。擬合 20–40 s，受試者等得起；分開兩次跑受試者要回來兩趟。Arc 沒螢幕沒聲卡只能跑測試與分析。
  Arc 上那個 `psychopy-env` 是 Python 3.6，裝不了 adaptiveSFT，別用。
- **在哪**：`adaptive_vawm.md` 的「一次性」；鎖定的套件版本在 `adaptiveSFT/requirements-lock.txt`。

## 12. 順手修的 bug：練習回饋永遠 Incorrect
- **決定**：鍵盤的 `'y'` / `'n'` 對到 `rule.csv` 的 Cedrus 代碼 `'4'` / `'3'`。
- **為什麼**：答案表是為 Cedrus 按鍵盒寫的，鍵盤送來的是字母，兩邊對不上，練習階段不管怎麼按都說你錯。`rule.csv` 的 `ResponseBox` 欄是 Cedrus 按鍵碼，鍵盤版收到的是字母，查表永遠失敗。主實驗不算 Acc，不受影響。
- **在哪**：`VAWM_nobox.py:2132`。

## 13. GRTv3_ada：study 後加 0.3 s 視聽遮蔽
- **決定**：`MASK_DUR = 0.3`，視覺 = 四角亮度像素噪音，聽覺 = 語音形狀噪音（0 dB SNR 的噪音位準）。
- **為什麼**：老闆要求。遮蔽會讓作業變難，所以加了之後之前沒遮蔽時量到的校準值不能沿用，要重校；亮度噪音遮不遮得掉色度記憶是開放問題。
- **在哪**：`GRTv3_ada.py` 的 `MASK_*` 參數區與 `mask` routine。

## 14. 擬合改走 `fit_lnrm_v2`：似然用 PyMC 內建的 `LogNormal`
- **決定**：校準（`LNRMCalibrator.finish`、`SFT_WM_*` 的 `fit_calibration`）呼叫 `adaptivesft.models_v2.fit_lnrm_v2`，不再是 `models.fit_lnrm`。
- **為什麼**：v1 的 lognormal 密度與存活函數是手寫的；v2 用 `pm.logp(pm.LogNormal.dist(...))` 和 `pm.logcdf(...)` 拼出賽跑似然，再包進 `pm.CustomDist`，比較好對照教科書、也比較好讓後人（和老闆）檢查。兩版 logp 差 < 1e−7，後驗與 Stan 一致（`scripts/proof_pymc_lognormal.py`）；回傳格式相同，`find_salience` 不用改。PyMC 本身沒有「lognormal race」分布，所以 race 仍然要自己組。
- **在哪**：`adaptive_vawm.py` 的 `finish`；`SFT_WM_change.py` / `SFT_WM_nochange.py` / `make_simple_psyexp.py` 的 `fit_calibration`；模型在 `adaptiveSFT/adaptivesft/models_v2.py:36-37`。

## 還沒決定的
- adaptiveSFT 決定 A（DDM 的 `a` 是邊界距離還是分離）：只影響 DDM 模擬與 power scan 的數字，不影響實驗程式。
- 聲音 lnrm 的層級貼到 foil 後 u 是散的（測試裡 29 個不同值），擬合沒問題，但「層級」這個概念在聲音軸上是近似。

## 三年後要改東西，從哪裡下手
| 想改 | 先跑 | 再改 |
|---|---|---|
| 目標值、層級、試次數 | `pytest tests/test_adaptive_vawm.py -k lnrm` | `VAWM_calibrate.py` 最上面的參數 |
| 一試長什麼樣 | `-k psi_colour`、`-k psi_audio` | `make_colour_trial` / `make_audio_trial` |
| block csv 的欄位 | `-k write_blocks` | `write_blocks`、`CSV_COLUMNS` |
| 分析（SIC / MIC） | `-k dfp_analysis` | `vawm_to_dfp_rows`、`adaptiveSFT/adaptivesft/sic.py` |
| 擬合模型本身 | `adaptiveSFT: pytest tests/test_models.py tests/test_lnrm_vs_stan.py` | `adaptiveSFT/adaptivesft/models.py` |

表的讀法：「先跑」那一欄是改之前要先確認會過的測試（改完再跑一次，過了才算改好）；「再改」是要動的地方。

## 所以你要做什麼
1. 不要動的：第 2、3、4 條綁在一起（模型曲線 ↔ 目標值）。改一個就要改另一個。
2. 想改任何數字：先讀對應那一條的「為什麼」，再照最後那張表先跑測試、再改、再跑測試。
3. 改了遮蔽（第 13 條）或作業形式（第 10 條）之後，之前校過的受試者要重校。
4. 行號對不上時，用 grep 搜「在哪」裡的名字（例如 `grep -n alpha2_rule adaptive_vawm.py`），不要猜。
5. 「還沒決定的」兩條如果有一天要定案，加成第 14、15 條，格式照舊。
