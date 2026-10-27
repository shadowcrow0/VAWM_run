---
tags: [literature-note, Klatt, 語音合成, VOT, 參數化合成]
citekey: klatt1980
---

# Klatt (1980) — 串聯/並聯共振峰合成器

**DOI / URL** https://doi.org/10.1121/1.383940
**閱讀狀態** ⚠️ **未讀原文**。依二手引用與 Praat KlattGrid 文件。

```bibtex
@article{klatt1980software,
  author  = {Klatt, Dennis H.},
  title   = {Software for a cascade/parallel formant synthesizer},
  journal = {The Journal of the Acoustical Society of America},
  volume  = {67}, number = {3}, pages = {971--995}, year = {1980}
}
```

## 研究問題
如何用參數化的來源-濾波器模型合成語音,使每個聲學參數都能獨立設定?

## 方法與族群
合成器規格與軟體。非實證研究。

## 結果與限制
**對 AVWM 的關鍵性質**:VOT 是**定義性參數**(嗓音振幅開始上升的時刻相對於 burst),
不是副作用。這與 [[mbrola-cannot-do-vot]] 的 diphone 架構形成對比。

**現代實作**:Praat KlattGrid(Weenink 2009, Interspeech, 2059-2062),tier-based、
**連續時間**參數化。可經 `parselmouth` 從 Python 驅動。

**使用實例**:Fox, Leonard, Sjerps & Chang (2020) *eLife* 9, e53051,
doi 10.7554/eLife.53051:
> "Stimuli were generated with a parallel/cascade Klatt-synthesizer KLSYN88a... all
> stimulus parameters were identical across stimuli, with the exception of the time at
> which the amplitude of voicing began to increase (in 10 ms steps from 0 ms to 50 ms
> after burst onset)."

**⚠️ 未解的實測衝突**:兩份獨立的 subagent 研究對 KlattGrid 的時間解析度結論**不一致** ——
一份測到 voicing onset 量化到約一個音高週期(80 Hz 時誤差達 4.04 ms),另一份測到
差分解析度為單一取樣點(0.023 ms),僅有可校正的固定 +0.3 ms 偏移。兩者量測方法不同。
**若要走 KlattGrid 路線,必須先自行實測釐清。**

**限制**:未讀原文;上述使用實例與 KlattGrid 性質均為二手。

## 可連結脈絡
- 與 diphone 架構的對比 —— [[mbrola-cannot-do-vot]]
- 唯一的 MBROLA/VOT 論文其實用它 —— [[zuk2013]]
- 若 SNR 路線失敗時的備案 —— [[snr_vs_grt_dimension]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**我在哪些工具上遇過「兩份獨立測量結論不一致」?** → 本卡(KlattGrid 時間解析度)。
**哪些工具能把 VOT 當成可設定參數而非湧現結果?** → 本卡;VocalTractLab 則是湧現的。
