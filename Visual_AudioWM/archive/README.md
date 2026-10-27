# archive/ —— 不再執行、但決策文件引用過的歷史檔（2026-10-19 整理）

搬進來的理由分三類，對應 `review/` 與 `DECISIONS.md` 的脈絡：

- **色彩探索叢集**（`colorpool.py`、`generate_colors*.py`、`generate_bv_*.py`、`color_tools.py`、`lc_*.py`、`psychopy_pickcolor.py` 與 `data/`、`figure/`、`stimuli/` 裡它們的輸出）：
  `review/決策脈絡_顏色維度.md` 引用。結論已進 `agrt_setup.py` / `agrt_colour_lut.json`。
- **聽覺維度嘗試叢集**（`GetAudioStim.py`、`generate_b3_p3_auditory_baseline.py`、`adaptive_duration_staircase.py`、
  `generate_speech_stimulus.py`、`psychopy_*_adaptive.py`、`psychopy_integration_example.py`、相關 csv）：
  `review/聽覺維度_嘗試與放棄紀錄.md` 記錄的對象。
- **舊版本**：`VAWM.psyexp`（`VAWM_nobox.py` 的 Builder 原始檔，也是 `make_simple_psyexp.py` 的底稿）、
  `GRTv3_a.py`（CLAUDE.md：GRTv3_ada 的前身）與它用的 `stimuli/box_keys.png`、六張舊 pilot 分析圖。

同一次整理直接刪掉的（零引用或逐 byte 重複，git 歷史裡找得回來）：十支舊 Builder 編譯檔、測試殘渣、
根目錄與 `data/`/`figure/` 重複的 csv/png、誤入版控的 `.pyc`、孤兒音檔。

## 第二輪（2026-10-19）

以現行入口（`SFT_WM_change.py`、`SFT_WM_nochange.py`、`VAWM_simple.psyexp`、`make_simple_psyexp.py`、
`VAWM_calibrate.py`、`make_adaptive_blocks.py`、`VAWM_nobox.py`、`adaptive_vawm.py`、`debug_adaptivesft.py`、
`setup_pymc_coder.bat`、`tests/`、`GRTv3_ada.py`、`GRTv3.py`、`AGRT.py`、`agrt_setup.py`、
`agrt_colour_lut.json`、`snr_audio.py`、`snr_runtime.py`、`generate_trials.py`）為根重新追了一次引用圖，
把還留在現行目錄、但零引用的檔案搬進來（一律 `git mv`，沒有刪除任何東西）：

- **`GRTv3_demo.py`** → `archive/GRTv3_demo.py`：CLAUDE.md 的版本表沒列它，`git grep` 全專案零引用
  （唯一提到它的只有它自己檔內的字串）。
- **根目錄舊 pilot 輸出**（2026-05 那批，`VAWM_simple`/`SFT_WM_*` 這代入口不會再產生這種檔名）：
  `296317_VAWM_2026-05-07_13h49.41.551.log` → `archive/296317_VAWM_2026-05-07_13h49.41.551.log`、
  `595945_VAWM_2026-05-11_11h28.52.013.csv` → `archive/595945_VAWM_2026-05-11_11h28.52.013.csv`、
  `yyc_clean.csv` → `archive/yyc_clean.csv`。
  後兩個跟 `data/` 底下同名檔逐 byte相同（`diff` 確認），兩邊都留著搬過去，沒有互相取代。
- **`data/` 裡 2026-05 的舊輸出與重複檔**：`595945_VAWM_2026-05-11_11h28.52.013.csv`、`clean_yyc.csv`、
  `yyc_clean.csv`、`combined_75.csv`、`combined_75trials.csv`、`conditions.csv`、`test.csv`、`trial.csv`、
  `task.xlsx` → 全部搬到 `archive/data/` 下同名。這些是舊 pilot 的資料輸出，不是程式，目前入口不讀它們。
- **`stimuli/` 裡 2026-04 的舊 pilot 輸出與一個零引用的殘留 csv**：
  `000379_VAWM_2026-04-30_07h05.36.895.csv`、`424167_VAWM_2026-04-30_07h10.24.747.csv`、
  `817499_VAWM_2026-04-30_07h19.17.758.csv` → `archive/stimuli/`；另外 `stimuli/conditions.csv`
  （對應早期 `archive/GetAudioStim.py` 那套舊流程，現在實驗讀的是 `practice.csv`/`block1..6.csv`，
  零引用）也一併搬到 `archive/stimuli/conditions.csv`。注意 `stimuli/b3.wav`、`stimuli/p3.wav` **沒有**搬，
  因為 `GRTv1.psyexp`（保留清單內的檔案）和聽覺維度決策文件仍直接引用這兩個路徑。
- **`figure/`（單數，跟保留的 `figures/` 是不同目錄）整個清空**：`pilot1_cdf.png`、`pilot_den.png`、
  `stu_color_compare.png`、`yyc_cdf.png`、`yyc_color.png`、`yyc_den.png` → `archive/figure/`。
  這是舊 pilot（`pilot1`/`stu`/`yyc`）分析圖，零引用；`adaptivesft/README.md` 和
  `adaptivesft/fit_calibration.py` 裡出現的 `figure/psychometric_S01.png` 只是範例輸出路徑字串，
  跟這批既存檔案無關，不影響搬移。

**沿用保留、沒有搬的候選**（有引用，附引用處）：
- `audio_device.py`：被 `GRTv3.py`、`GRTv3_ada.py`、`SFT_WM_change.py`、`SFT_WM_nochange.py`、
  `VAWM_calibrate.py`、`VAWM_nobox.py`、`VAWM_simple.psyexp`、`debug_adaptivesft.py`、
  `make_simple_psyexp.py` 等現行入口 import。
- `snr_vs_grt_dimension.md`：被 `GRTv3_ada.py`（程式註解引用）、`90_Sources/*.md`、
  `review/決策脈絡_聽覺維度.md` 引用。
- `colorWM.md`：被 `agrt_setup.py`、`adaptivesft/sim_recovery.py`（程式註解引用 HUE_CENTER=303° 的依據）、
  `review/colour_axis_method_EN.md`、`review/決策脈絡_顏色維度.md`、`snr_vs_grt_dimension.md` 引用。
- `文獻卡.md`：被 `review/consonant-pair-choice.md`、`review/natural-vs-synthetic-speech.md` 等多篇
  `review/` 文件引用（雖然沒有程式或 `CLAUDE.md` 引用）。

搬移後重跑過的檢查：`ast.parse` 所有現行 Python 入口、`adaptive_vawm.load_confusion()`、
`make_simple_psyexp.py` 重新產生 `VAWM_simple.psyexp` 後 `git diff` 無差異、`snr_audio._load_speech()`、
以及對每個搬走的檔名在現行入口裡 `git grep` 零命中，全部通過。
