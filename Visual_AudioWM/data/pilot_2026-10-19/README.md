# 2026-10-19 真人試跑資料

本資料夾收的是 2026-10-19 當天兩次真人（非機器人）試跑留下的原始檔。檔名前綴標明來源腳本：

- `SFTWM_nochange_` —— 來自 `SFT_WM_nochange.py`
- `VAWMcalib_` —— 來自 `VAWM_calibrate.py`

兩次試跑的參與者編號（`subj`）都是空字串，所以原始檔名以 `_` 開頭（例如 `_SFT_WM_...`、`_calib_trials.csv`），前綴直接加在原檔名前面，因此看起來會有雙底線（`SFTWM_nochange__...`、`VAWMcalib__calib_trials.csv`），這是正常的，不是打字錯誤。

## 檔案清單

### `VAWMcalib__calib_trials.csv` — 03:23，VAWM_calibrate.py，4 試

最早的一次試跑，只跑了 4 個試次（顏色+聲音同時校準的 adaptive 試次）。用 `python3` 讀出來：

- 試次數：4
- RT 範圍：約 14.10–36.94 秒

這個 RT 範圍明顯是壞的：當時 `event.Keyboard` 回報的 rt 是相對於鍵盤物件建立時的時間，而不是相對於每個探測刺激出現的時間（`clock.reset()` 動到的是另一個 `core.Clock`，鍵盤的 rt 時鐘沒被重置），所以記錄下來的 RT 其實是「距離程式開始算起」的秒數，不是真正的反應時間。這個 bug 已經在 commit `cd8c55a`（Measure reaction time from probe onset, not from program start）修好：三支手寫腳本（`VAWM_calibrate.py` 與兩個 `SFT_WM_*.py`）現在都用 `clock=clock` 建立 `Keyboard`，讓既有的 per-probe `clock.reset()` 真正成為 RT 的起點。

因為 RT 是壞的，這份資料不能用來擬合心理測量函數，只能當作「流程跑得動」的證據。

### `SFTWM_nochange__SFT_WM_2026-10-19_20h04.38.000.csv` / `.psydat` / `.log` — 20:04 起，SFT_WM_nochange.py

這是 PsychoPy ExperimentHandler 存的標準格式（csv 為主要資料，psydat / log 是對應的二進位與逐行時間戳記錄），已經包含上面提到的 RT bug 修復。用 `python3` 讀 csv：

- 試次數：72（全部是 `dim == colour`，即顏色校準）
- 有效 RT（非空）試次數：65／72
- RT 範圍：約 0.7877–2.8685 秒 —— 數值正常，落在合理反應時間區間內

### `SFTWM_nochange__simple_calib_trials.csv` — 20:12

同一次試跑、同一支腳本（`SFT_WM_nochange.py`）另外寫出的「簡化版」逐試 csv，內容與上面 PsychoPy 標準 csv 的顏色校準部分一致（同樣 72 試、65 個有效 RT、RT 範圍約 0.7877–2.8685 秒）。

## 這次試跑跑到哪裡

20:04 這次試跑完成了「Part 1：顏色校準」（72 試，上面兩個檔記錄的就是這些試次）。接著程式顯示「Part 2 of 3: sound calibration (72 trials)」的指導語，受試者在指導語畫面按了 `escape`，程式照設計結束執行。

因此：

- 沒有進行聲音校準（Part 2）
- 沒有進行主實驗（Part 3）
- 沒有產生 `_simple_calib.json`（腳本在校準完成、擬合出 H/L 後才會寫這個檔；因為流程在那之前就被 escape 中斷，這個檔案不存在）

## 小結

| 檔案 | 腳本 | 時間 | 試次數 | RT 狀態 |
|---|---|---|---|---|
| `VAWMcalib__calib_trials.csv` | VAWM_calibrate.py | 03:23 | 4 | 壞（鍵盤時鐘 bug，commit cd8c55a 修復前） |
| `SFTWM_nochange__SFT_WM_2026-10-19_20h04.38.000.*` | SFT_WM_nochange.py | 20:04 | 72（顏色校準） | 正常（約 0.79–2.87 s） |
| `SFTWM_nochange__simple_calib_trials.csv` | SFT_WM_nochange.py | 20:12 | 72（顏色校準，同一次試跑） | 正常（約 0.79–2.87 s） |
