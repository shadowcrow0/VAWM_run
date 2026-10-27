---
tags: [literature-note, MBROLA, VOT, 語音合成, 工具限制]
citekey: mbrola-cannot-do-vot
---

# MBROLA 為何做不出 VOT 連續體(綜合證據卡)

**DOI / URL** MBROLA README https://github.com/numediart/MBROLA | MaxMBROLA https://zenodo.org/records/39427
**閱讀狀態** **綜合卡**。MBROLA README 與 MaxMBROLA 論文的引句已核實;本地實測由我在此機器上執行。

```bibtex
@inproceedings{dutoit1996mbrola,
  author    = {Dutoit, Thierry and Pagel, Vincent and Pierret, Nicolas and
               Bataille, Fran{\c c}ois and Van der Vrecken, Olivier},
  title     = {The {MBROLA} project: Towards a set of high quality speech synthesizers
               free of use for non-commercial purposes},
  booktitle = {Proc. ICSLP '96}, volume = {3}, pages = {1393--1396}, year = {1996},
  doi       = {10.1109/ICSLP.1996.607874}
}
@inproceedings{dalessandro2005maxmbrola,
  author    = {D'Alessandro, Nicolas and Sebbe, Rapha{\"e}l and Bozkurt, Baris and
               Dutoit, Thierry},
  title     = {{MaxMBROLA}: A {Max/MSP} {MBROLA}-based tool for real-time voice synthesis},
  booktitle = {Proc. EUSIPCO 2005}, year = {2005}
}
```

## 研究問題
AVWM 原本打算用 MBROLA 產生 /b/–/p/ 的 VOT 連續體。這個工具做得到嗎?如果做不到,限制的來源是什麼層次 —— 參數介面、演算法、還是資料庫架構?

## 方法與族群
三條獨立證據 + 本地實測(us1 語者,自寫的 VOT 偵測器,±10 ms 固定偏誤,因此**絕對值不可信、比較性結論可信**)。

## 結果與限制
**1. 架構 —— MBROLA README**
> "Each line contains a phoneme name, a duration (in ms), and a series (possibly none)
> of pitch targets composed of two float numbers each."

控制面只有三個:音素身分、音素時長、F0 目標。VOT 不在其中。

**2. 作者自承次音素限制 —— D'Alessandro et al. (2005)**,Dutoit(MBROLA 創作者)撰:
> "**phoneme duration is the smallest subdivision of time for control.**"

**3. 已發表的明確陳述 —— Vojtech et al. (2019)** *AJSLP* 28, 875-886,
doi 10.1044/2019_AJSLP-MSC18-18-0052:
> "decreasing speech rate using MBROLA 2.00 only stretches the spectral content of the
> sentence in time. Thus, acoustically relevant properties of speech, **such as voice
> onset time, are linearly stretched in time**..."

**4. 文獻計量**:全文檢索 `"VOT continuum"` 的共現次數 —— MBROLA **0**、
Klatt **114**、Praat **200**(OpenAlex / Europe PMC)。唯一同時出現 MBROLA 與 VOT 的
論文([[zuk2013]])用的是 Klatt,MBROLA 只在討論區當「未來可試」。

**5. 本地實測(2026-08)**
- `b` 的 VOT 在時長 8-200 ms 全程固定(49 個請求值只落在 7 個相異結果)
- voicing onset 量化到**一個音高週期**(180 Hz → 5.5 ms;300 Hz → 3.3 ms)
- 請求時長 +1 ms 常讓實測 VOT **下降** —— **非單調,對 Psi 致命**
- 插入 `h` 段的 workaround 無效:VOT 飽和在 ~7 ms
- **`generate_b3_p3_auditory_baseline.py` 的 `duration_diff` 從 5 掃到 50 ms,
  ΔVOT 只從 81 動到 98 ms** —— 原本的難度操弄根本沒有在動 VOT

**限制**:我的 VOT 偵測器有 ~+10 ms 固定偏誤;絕對數值需以 Praat 複核。
「文獻 0 篇」是跨多個索引的檢索結果,非數學證明。

## 可連結脈絡
- 方法學參考文獻對 MBROLA 完全沉默 —— [[winn2020]]
- 唯一的反例其實是反證 —— [[zuk2013]]
- 促成改用 SNR 路線 —— [[snr_audio]]、[[snr_vs_grt_dimension]]

---
標籤note:[[literature-note]] [[speech-perception]] [[AVWM]]

## 回查線索
**我在哪些地方用過「工具的參數介面就是它的能力上界」這個論證?** → 本卡。
**哪些工具我實測過非單調性?** → 本卡(MBROLA);KlattGrid 的兩份研究結論不一致,待實測。
