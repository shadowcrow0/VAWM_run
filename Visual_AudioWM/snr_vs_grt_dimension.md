# SNR 當聽覺難度操弄:為什麼它是難度旋鈕,不是 GRT 維度

這份筆記回答一個很容易被忽略、但一旦忽略就會讓輸出形狀整個錯掉的架構問題:
**用噪音(SNR)調聽覺作業的難度,可不可以直接把 SNR 當成 `AGRTHandler` 裡的
「dimension 2」,跟顏色維度一樣丟給同一套適應式程序?**

答案是不行,但「為什麼不行」需要把 `AGRT.py` 的模型攤開來看才會清楚——這不是
一個工程上的限制,而是 SNR 這個量在 GRT 的意義下,從一開始就不是一個「維度」。
它是難度旋鈕。這篇筆記把這個區別講清楚,並說明它在實務上會造成什麼後果、以及
現有 repo 裡已經怎麼處理(`agrt_setup.py` 給顏色維度、`snr_audio.py` 給聲音維度)。

---

## 1. AGRT 的模型只有一行,先把它攤開來看

`AGRT.py` 裡負責計算「給定刺激 x,回答 r 的機率」的,實際上就是
`agrtPsiObject.__init__` 裡的這一行(133 行):

```python
# With lapse
self._probResponseGivenLambdaX = np.array([0,1]).reshape(2,1,1,1) + np.array([1,-1]).reshape(2,1,1,1) * ((self.delta/2) + (1 - self.delta) * stats.norm.cdf(self._alpha, loc=self._x, scale=self._beta))
```

上面 130–131 行還留著一個註解掉的「無 lapse」版本,可以對照著看,兩者差在有沒有
`delta`(猜測率)這一項。翻成數學:

```
P(r=0 | x) = δ/2 + (1-δ)·Φ((α-x)/β)
P(r=1 | x) = δ/2 + (1-δ)·[1 - Φ((α-x)/β)]
```

對應的生成故事(這正是 SDT 的標準故事):受試者每個 trial 抽一個內在知覺樣本
`ψ ~ N(x, β²)`;`ψ < α` 就回答「低」(r=0),否則回答「高」(r=1);另外有 `δ`
的機率整個亂猜(lapse)。這裡:

- **x**:實驗者這個 trial 提出的**物理刺激值**(也是 `agrtPsiObject.x` 網格裡的一點,86–90 行)。
- **α**:受試者的**主觀決策界線**,是模型要估的隱藏參數(91 行的網格,105–116 行建立的聯合先驗 `P(λ)`)。
- **β**:受試者在這個維度上的**知覺標準差**,同樣是要估的隱藏參數(92 行的網格)。

`update()` 方法(140–158 行)每個 trial 用貝氏更新這個 `P(α,β)` 聯合後驗,並且用
「使下個 trial 的預期熵最小」去選下一個 x(157–158 行,`nextIntensityIndex` /
`nextIntensity`)。`estimateThreshold()`(163–171 行)則是拿目前估到的 α、β,
反解出「要讓正確率達到某個目標值,x 該設在哪裡」,而且**一次給出兩個值**——
這點下一節細講。

再往上一層,`AGRTHandler.__init__`(199–316 行)做的事情是**建立兩個完全獨立的
`agrtPsiObject`**:

```python
self._psi1 = agrtPsiObject(
    dim1range, dim1range, dim1betaRange,
    dim1steps, dim1steps, dim1steps,
    delta=marginalLapse, stepType='lin', prior=prior[0])
...
self._psi2 = agrtPsiObject(
    dim2range, dim2range, dim2betaRange,
    dim2steps, dim2steps, dim2steps,
    delta=marginalLapse, stepType='lin', prior=prior[1])
```

（307–316 行）`addResponse()`(318–347 行)把兩個維度的反應分別餵給 `psi1` 和
`psi2`(346–347 行:`self._psi1.update(result[0])` / `self._psi2.update(result[1])`),
兩者之間完全沒有耦合。也就是說,**AGRT 的「維度」定義,從類別簽名開始就是
「每個維度各自有自己的 x/α/β,各自用同一條 133 行的公式描述一個獨立的雙極判斷」**。
這個假設不是隱含的,是寫死在建構子的參數(`dim1range`, `dim2range`, `dim1steps`,
`dim2steps`)跟兩個獨立 psi 物件裡的。

> 補充:題目提供的參考行號(133 行公式在「99 行」附近)跟我實際讀到的不一致——
> 99 行其實是一行**註解**(`# ALWAYS use the order for P(r|lambda,x); i.e. [r,a,b,x]`),
> 講的是陣列 reshape 的順序慣例,不是公式本身。公式在 133 行(130–131 行是被
> 註解掉的無 lapse 版本)。以下都以我實際讀到的行號為準,細節見文末的「附註」。

---

## 2. 「雙極維度」是什麼意思——顏色維度為什麼吻合

從第 1 節的公式可以反推:AGRT 能處理的維度,必須滿足**受試者的反應,就是對
「這個物理量本身」的低/高判斷**。也就是說,x 軸上必須存在一個受試者主觀認定的
分界點 α,受試者每個 trial 做的事就是「判斷這次的 x 落在 α 的哪一邊」。滿足這個
條件,AGRT 才有辦法：(a) 把 x 往 α 推近或推遠來操弄難度,(b) 用受試者的
低/高反應去反推 α 跟 β 在哪。

顏色維度完全符合這個故事。`agrt_setup.py` 把色彩維度定義成「以錨點色相為起點、
帶正負號的 CIEDE2000 弧長座標」(該檔 13–16 行),這條弧長座標就是 AGRT 的 x:

- x = 弧長座標(一個實數,`de00_to_hex(arc)` 把它轉成螢幕色票)
- 受試者的反應 = 「這個顏色偏錨點的哪一側」(低/高就是這條弧上的位置判斷)
- α = 受試者自己在色相軸上習得的類別界線(用弧長單位表示)
- β = 受試者在這條色相軸上的知覺標準差

`AGRTHandler.estimateGRTintensities()`(377–406 行)的文件字串寫得很直接:

```python
def estimateGRTintensities(self, overallAccuracy, lambdas=None):
    """Returns a tuple of tuples ((L1,H1),(L2,H2)) providing the low (L)
    and high (H) intensities for each dimension (1,2) based on the overall
    accuracy specified.
    ...
    """
```

（378–380 行 docstring,406 行是實際 `return`）對顏色維度而言,`(L1,H1)` 就是
「兩個要拿來當刺激顯示的顏色弧長座標」——直接對應到螢幕上要畫的兩個顏色。這是
因為 `estimateThreshold()`(163–171 行)算出來的兩個值,本來就是**對稱座落在估到
的 α 兩側**(用 `erfinv` 的奇函數性質可以驗證:171 行的兩個 `erfinv` 引數互為
相反數,所以兩個回傳值到 `lamb[0]`=α 的距離相等、方向相反)。這正是「雙極維度」
這個假設在數學上長出來的形狀:一個 α,兩個對稱刺激點。

---

## 3. SNR 不符合這個假設——三個理由

把 SNR 想像成「dimension 2」丟給 `AGRTHandler`,第一步就要問:**受試者在這條軸上
做的判斷是什麼?** 答案揭穿了三個不吻合的地方。

### 3.1 反應變數是音素類別,不是「吵/乾淨」

`GRTv2.py` 裡受試者對聲音維度的反應,是報告「這是 be 還是 pe」——這是四鍵反應
中對應語音類別的那一半(`itemAudi` 陣列,790 行:
`['stimuli/b3.wav','stimuli/b3.wav', 'stimuli/p3.wav', 'stimuli/p3.wav']`)。
沒有任何一個反應通道是在問「這個 trial 的噪音多不多」。而 133 行公式裡的 `r`
（`self.r = np.array(list(range(2)))`,95 行)必須是「對 x 本身的低/高判斷」——
如果 x 是 SNR,那麼 `r=0`/`r=1` 就得代表「這個 SNR 偏低/偏高」,但實驗根本沒有
收集這種反應。硬套的話,唯一能餵進去的資料是「be/pe 答對了沒」,可是「答對」跟
「判斷這個維度偏哪一側」是兩件不同的事——前者是正確率,後者是類別歸屬,不能
互換。

### 3.2 be 和 pe 的位置是固定的,不是適應程序在搬動的座標

AGRT 整個 `update()` 迴圈(140–158 行)存在的理由,是要去**選下一個 x 該放在
哪**——這只有在 x 可以在一段連續範圍內自由取值時才有意義。顏色維度的 x(弧長
座標)正是這樣,`agrt_setup.py` 的 `arc_range_in_gamut()`(213–219 行)給出的就是
這段可以自由提議的範圍。

but be 跟 pe 不是這樣的量。它們是一個語音連續體上的**兩個固定端點**(自然的
類別典型,不是要被估計、被搬動的座標)。`snr_audio.py` 的設計正是把它們當固定
的:`SPEECH_FILES = {'be': 'be.wav', 'pe': 'pe.wav'}`(35–38 行),而且特別選了
`/i/` 母音版本以避開跟 VOT 共變的額外線索(39–41 行,引用
[[90_Sources/winn2020]] §II.D)。適應程序沒有、也不該去移動 be/pe
本身——它們是任務要問的問題(「這是哪一個類別?」),不是拿來被搜尋的座標。

### 3.3 SNR 動的是有效 β,不是 x

回到 SDT 的生成故事:`agrtPsiObject` 原本(被註解掉的)舊版註解寫得很白
（127 行附近的舊註解):`x == the mean of the perceptual distribution`,
`beta == the sd of the perceptual distribution`。也就是說,在 AGRT 的模型裡,
**x 決定知覺分布的平均數在哪、β 是受試者自己的知覺雜訊(一個要被估計的隱藏
特質,不是實驗者每個 trial 灌進去的量)**。

而 `snr_audio.mix_at_snr(name, snr_db)`(183–208 行)做的事情,是把一段外部的
語音頻譜噪音(speech-shaped noise)混進固定的 be/pe token 裡。這在知覺上做的事
是**提高受試者那個 trial 感受到的有效知覺雜訊**——也就是把 β 往上推,而 be/pe
本身的「知覺平均位置」(它們是哪個類別)完全沒有動。換句話說:SNR 操縱的是
公式裡的**分母**(β),AGRT 的維度機制設計來操縱的是**分子**(x 相對 α 的距離)。
把 SNR 塞進 `dim2range`,等於要求 AGRT 去估計一個「β 軸上的 α」——這在概念上
是自我矛盾的,因為 β 在 AGRT 的模型裡本來就不是一個可以被「判斷高低」的物理量,
它是分布的形狀參數。

---

## 4. 具體後果:硬把 SNR 塞進 `AGRTHandler` 會發生什麼

假設真的寫了 `AGRTHandler(dim1range=color_arc_range, dim2range=(snr_lo_db, snr_hi_db), ...)`。
先不管 3.1–3.3 已經指出反應變數對不上,只看**輸出形狀**這一步,問題最直接:

`estimateGRTintensities()`(377–406 行)回傳的是 `((L1,H1),(L2,H2))`——每個維度
各自一對 (低,高) 刺激值。對 dim2(假想的 SNR 維度),這會給出 **兩個不同的
SNR 值** `L2` 和 `H2`,對稱座落在估到的「SNR 決策界線」`α2` 兩側。但實驗真正
需要的,是**一個** SNR 值,同時、同樣地套用在 be 跟 pe 上——這正是
`mix_at_snr(name, snr_db)` 的簽名所反映的:`snr_db` 是單一個純量,`name` 才是
be/pe 的選擇,兩者互相獨立(183 行)。`snr_audio.py` 裡也刻意把 be、pe 正規化到
相同 RMS(43–44 行:「兩個 token 正規化到相同 RMS,否則同一個 SNR 設定在 be 與
pe 上的實際值會差 0.7 dB」),就是為了讓「一個 SNR 數字」在兩個類別上代表同一件
事。

如果照著 AGRT 的輸出去用「L2 這個 SNR 給其中一類、H2 這個 SNR 給另一類」,
等於是讓噪音量跟音素身分系統性地共變——這正好摧毀了 GRT 想要檢驗的東西:
「顏色維度」跟「聲音維度」的知覺可分離性,前提是兩個維度的物理操弄互相獨立。
一旦聲音維度的噪音量取決於是 be 還是 pe,聲音維度自己內部就先有了一個混淆
來源,遑論拿去跟顏色維度做交叉分析。

下表整理這個形狀不吻合:

| | 顏色維度(`agrt_setup.py` 弧長座標) | 假想中的「SNR 維度」 |
|---|---|---|
| 受試者在這條軸上做的判斷 | 「這個色相偏界線哪一側」——low/high 就是這條軸本身的位置判斷 | 「這是 be 還是 pe」——類別判斷,跟 SNR 無關 |
| 餵給 `agrtPsiObject` 的 x 代表什麼 | 弧長座標,直接是被判斷的量 | SNR dB,但沒人被要求判斷 SNR |
| α(決策界線)有沒有心理實體 | 有——受試者主觀的顏色類別邊界 | 沒有——be/pe 本身不存在一個「SNR 界線」 |
| β 在模型裡的角色 | 待估的受試者知覺標準差(隱藏特質) | 這正是 SNR 實際在操縱的東西,不該同時當 x |
| `estimateGRTintensities` 回傳的 `(L,H)` 該怎麼用 | 兩個要顯示的顏色刺激,直接可用 | 兩個 SNR 值——但實驗只需要**一個**,同時套用在 be、pe 上 |

---

## 5. 為什麼 GRT 的分析本身完全不受影響

上面講的都是「AGRT 這個**適應式引擎**不能吃 SNR」,但這不代表 SNR 不能拿來
操縱聽覺難度,也不代表最後的 GRT 分析(4×4 混淆矩陣上的知覺可分離性/決策
可分離性檢定)會出問題。原因是:GRT 的分析只看最終的**刺激—反應聯合分布**,
不在意難度是用哪個物理參數調出來的。

用第 3.3 節的語言講:AGRT 的做法(把顏色刺激往類別界線推近)跟 SNR 的做法
(把噪音加大),在 SDT 的意義下都是在**降低 d′**——前者是縮小分子(訊號間距),
後者是放大分母(知覺雜訊)。單看最後測到的正確率/混淆矩陣,這兩種操弄產生的
反應機率結構是同一種形狀(這正是古典 SDT 裡「只有 d′ 可被辨識,Δ 跟 σ 個別
的值不行」的老問題)。GRT 的複合辨識邏輯要的正是這個層次的資料——一個 2×2
（顏色兩階 × 聲音兩階)的刺激—反應矩陣——它不需要知道聲音那一階的難度是用
VOT 連續體、共振峰合成器,還是噪音調出來的。

[[90_Sources/winn2013]] 是這條路在文獻上的直接前例:用遮蔽噪音
（masking noise)操縱塞音濁化(voicing)辨識難度,是已發表的既有手段。但這篇
也帶了一個要寫進限制的警告:噪音改變的不只是整體難度,還會改變 VOT 與 F0
兩條線索的**相對權重**——也就是說,不同 SNR 下受試者可能在用不同的線索組合
做判斷。這對 GRT 的知覺可分離性解釋是個複雜性:如果「聲音維度」內部的線索
權重本身隨難度漂移,那麼跨難度層級比較知覺可分離性時,要留意這不是一個
「純粹只變 d′、其他都不變」的操弄。這點在本專案原本討論顏色維度可分離性時
（`colorWM.md` 引用 Ashby & Townsend 1986 的複合辨識架構)已經在用同一套邏輯,
這裡只是把同樣的警覺套用到聲音維度上。

---

## 6. 解法:兩個維度用兩套不同的適應機制

既然顏色維度符合「雙極維度」假設、聲音維度的難度來自「動 β 而非動 x」,最直接
的解法就是**別用同一套引擎**:

- **顏色**:繼續用 `AGRTHandler`(或行為等價的 PsychoPy `PsiHandler`)跑在
  `agrt_setup.py` 的 ΔE00 弧長座標上,回傳 `(L, H)` 兩個顏色弧長座標,直接對應
  兩個要顯示的顏色刺激。
- **聲音**:用**一維**的 `QuestHandler`(或 `PsiHandler` 的單維度用法)跑在
  SNR dB 這條軸上,目標是某個正確率(例如 0.75),回傳**一個** SNR 值;這個值
  透過 `snr_audio.mix_at_snr(name, snr_db)` 同時套用在該 trial 出現的 be 或
  pe token 上——`name` 由 trial 設計決定要放哪個音素,`snr_db` 由適應程序決定
  這個 trial 有多難,兩者互相獨立,不會像 AGRT 硬套那樣把兩者綁死。

這樣做**比原本更簡單**,不需要 `RunAdaptiveGRTExperiment`(517–532 行)那套把
`RunAdaptiveBlock` 的輸出直接接給 `RunGRTBlock` 的耦合機制——因為聲音維度根本
不需要跟顏色維度共用同一個聯合熵最小化迴圈,兩條適應程序本來就該各自獨立收斂。
`adaptivesft/fit_calibration.py` 的欄位設計已經隱含了這個方向:它的
`intensity` 欄位註解直接寫「顏色用 ΔE00,聽覺用 SNR dB」(該檔 11 行),把兩者
都當成單純的純量強度——這跟這裡建議的「聲音維度只需要一個純量、不需要雙極
結構」是一致的。

示意骨架(非可直接執行的完整程式,只標出兩套機制怎麼分工):

```python
from AGRT import AGRTHandler
from psychopy.data import QuestHandler   # 或 PsiHandler,視要不要要似然權重
import agrt_setup
import snr_audio

# --- 顏色維度:雙極,AGRT ---
color_agrt = AGRTHandler(
    nTrials=nColorTrials,
    dim1range=agrt_setup.arc_range_in_gamut(),
    dim2range=agrt_setup.arc_range_in_gamut(),  # 若顏色本身就是唯一維度,
                                                 # 可改用單維度版本;這裡沿用
                                                 # 既有二維介面示意即可
)
for arc_x, arc_y in color_agrt:
    hex_low  = agrt_setup.de00_to_hex(arc_x)
    ...
    color_agrt.addResponse((resp_low_high_1, resp_low_high_2))
color_L, color_H = color_agrt.estimateGRTintensities(overallAccuracy=0.75)[0]

# --- 聲音維度:純量難度旋鈕,QuestHandler ---
snr_quest = QuestHandler(
    startVal=-6.0, startValSd=6.0,
    pThreshold=0.75,
    nTrials=nSoundTrials,
    minVal=-30.0, maxVal=10.0,
)
for this_snr in snr_quest:
    token = 'be' if trial_is_be else 'pe'
    sr, y = snr_audio.mix_at_snr(token, snr_db=this_snr)
    correct = play_and_get_response(sr, y, token)   # 答對/答錯,不是低/高判斷
    snr_quest.addResponse(correct)
final_snr_db = snr_quest.mean()   # 單一個 SNR 值,套用在 be 跟 pe 上都一樣
```

`color_agrt` 的輸出是「兩個顏色」,`snr_quest` 的輸出是「一個 SNR」——形狀跟
各自維度真正需要的東西完全對上,不用再繞路把 SNR 硬塞進一個假想的雙極結構
裡。

---

## 7. 補充觀察:dB 已經是對數尺度,不需要先做座標變換

`agrt_setup.py` 之所以要把「色相角度」轉換成「ΔE00 弧長」,是因為 CIELAB 的
色相角本身**不是**知覺均勻的座標——該檔自己的檢查報告指出,目前設定下色相軸
一端跟另一端,同樣一度所值的知覺距離,落差大約 54%(該檔 9–11 行的說明,對應
`validate()` 印出的「色相非均勻性」區塊)。這正是 AGRT 的假設 (b)(知覺標準差
在整個範圍上是同一個常數)會被默默違反的地方——如果不做這個弧長變換,同樣的
β 網格在色相軸的兩端其實代表完全不同的知覺雜訊量。

SNR 用 dB 表示的話,不需要這一步預先的座標變換。dB 本身的定義就是訊號/噪音
振幅比的對數(`20·log10(比值)`),也就是說它已經是一個比例尺度,同樣的 dB
間距,原則上對應同樣量級的知覺間距,跨操作範圍相對穩定——這跟「音長」通常
需要先取 log(Weber's law 意義下的等比而非等差知覺)、色相角需要換成 ΔE00
弧長,是同一類問題,但 dB 已經在定義上滿足了。`snr_audio.py` 的檔案開頭
docstring 把這點寫在第 10–12 行:「dB 本身已經是對數尺度。音長維度要先取
log、色相角要換成 ΔE00 弧長,才能滿足『等物理間距 ≈ 等知覺間距』與『知覺
標準差跨範圍固定』這兩個假設;dB 不需要任何變換就已經滿足。」

這裡要提醒的是:「dB 已經是等知覺間距」是一個合理的**工作假設**,不是保證——
尤其接近心理測量函數的地板/天花板時,dB-線性未必仍然成立。`agrt_setup.py`
自己的作法是不空口白話,而是用 `validate()` 把非均勻性**量出來**印出報告
(492–497 行那段)。如果之後要對聲音維度的難度旋鈕做同等嚴謹的檢查,建議比照
辦理:用真實的 be/pe-in-noise 校準資料(例如透過 `adaptivesft.fit_calibration`
擬合心理測量函數),實際檢查在使用的 SNR 範圍內,正確率對 dB 的斜率是否大致
穩定,而不是只憑 dB 的定義就假定它成立。

---

## 小結

| | 顏色維度 | 聲音維度(SNR) |
|---|---|---|
| 受試者的反應 | 對色相位置的低/高判斷 | 對音素類別(be/pe)的判斷 |
| 難度操弄的對象 | x(刺激相對決策界線 α 的距離) | 有效 β(知覺雜訊,經由外加噪音) |
| 是否存在受試者主觀的「界線」 | 有(顏色類別邊界) | 沒有(be/pe 是固定端點,不是連續體上待估的邊界) |
| 適合的適應機制 | `AGRTHandler` / 雙極 `PsiHandler`(在 ΔE00 弧長軸上) | 一維 `QuestHandler` / `PsiHandler`(在 SNR dB 軸上) |
| 該機制的輸出形狀 | `(L, H)` 兩個顏色刺激 | 單一個 SNR 值 |
| 座標是否需要預先變換 | 需要(色相角 → ΔE00 弧長,見 `agrt_setup.py`) | 原則上不需要(dB 已是對數/比例尺度),但建議仍做實測驗證 |
| 對後端 GRT 分析(4×4 混淆矩陣)的影響 | 兩種難度操弄產生的都是「降低 d′」,GRT 分析本身不區分難度旋鈕的物理來源 | 同左 |

一句話總結:**SNR 是難度旋鈕,不是 GRT 意義下的維度**——因為 GRT/AGRT 的
「維度」定義要求受試者直接對那個物理量做低/高判斷,而聽覺這一路的判斷對象是
音素類別本身;SNR 動的是知覺雜訊(β),不是刺激位置(x)。把它硬塞進
`AGRTHandler`,不只反應變數對不上,連 `estimateGRTintensities` 的輸出形狀
`((L1,H1),(L2,H2))` 都會產生實驗用不上的兩個 SNR 值。分開處理(顏色用 AGRT、
聲音用一維 Quest/Psi)不只在概念上正確,實作上也更簡單。

---

## 參考文獻(APA 7th,均已在 `90_Sources/` 建卡查證)

Winn, M. B. (2020). Manipulation of voice onset time in speech stimuli: A tutorial and
flexible Praat script. *The Journal of the Acoustical Society of America*, 147(2),
852–866. https://doi.org/10.1121/10.0000692

Winn, M. B., Chatterjee, M., & Idsardi, W. J. (2013). The roles of voice onset time and
F0 in stop consonant voicing perception: Effects of masking noise and low-pass
filtering. *Journal of Speech, Language, and Hearing Research*, 56(4), 1097–1107.
https://doi.org/10.1044/1092-4388(2012/12-0086)
