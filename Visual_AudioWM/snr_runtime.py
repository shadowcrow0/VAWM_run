"""執行期即時產生 SNR 聲音刺激,並逐一記錄。

這一支是 `snr_audio.py` 與實驗腳本之間的薄層。`snr_audio` 負責「怎麼把語音
混進噪音」;這一支負責「實驗跑的時候要什麼就現做什麼,而且做過什麼全部留底」。

為什麼要即時做,不預先備好
--------------------------
SNR 是**連續**的旋鈕 —— 這正是本專案當初選它、而不是選 MBROLA 合成 VOT 的
理由(見 snr_audio.py 的 docstring)。適應式程序每個試次會提出一個任意實數的
刺激等級,預先備好的檔案清單接不住;b/p 連續體只有 9 個檔案,所以 GRTv3_a.py
必須把估計值 `int(round(...))` 硬塞回整數 step,還得補一段「兩點落同一 step
就拉開」的 hack。改成即時混音,那兩段都不需要。

實測每次混音 **約 5 ms**(22050 Hz、968 ms 的段落)。一個試次要 5 個刺激
(study 四個 + probe 一個)= 約 26 ms,發生在 Begin Routine、routine 的第一次
flip 之前。因為所有刺激的 onset 都是**相對於 routine 起點**的,這段延遲會讓
整個 routine 一起後移,相對時序不受影響 —— 只有試次之間的間隔多了 ~26 ms。

順帶消掉一個坑:噪音池版本必須刻意避開「同一試抽到同一個檔案」(池只有 24 個,
撞號機率約 4%),因為兩次呈現位元相同的話,噪音樣本本身就成了可比對的線索。
即時混音每次都抽新種子,這件事自動不會發生。

為什麼回傳檔案路徑,而不是波形陣列
----------------------------------
PsychoPy 的 ptb 後端對「直接餵 numpy 陣列」的取樣率與格式要求跨機器不穩,而
`setSound(路徑)` 是這個 repo 已經在跑、確定可用的那條路。多一次寫檔的成本
(約 1 ms)換掉一整類難重現的音訊問題,划算。

副作用是每個實際播出去的刺激都留在磁碟上 —— 對這個專案反而是好事,double-pass
一致性與反向相關那兩條分析路線本來就需要「當時到底播了什麼」。
一個 600 試的 session 約 3000 個檔、130 MB;不想留就傳 keep_wavs=False。

用法
----
    from snr_runtime import SNRStimulus

    snd = SNRStimulus(outdir=filename + '_snr')      # filename = thisExp.dataFileName

    path = snd.make(-6.0)                             # 即時混一個,回傳 wav 路徑
    audiUR.setSound(path, secs=1.0, hamming=True)

    for row in snd.drain_log():                       # 每一試把紀錄寫進資料檔
        thisExp.addData('snd_' + row['tag'], row['summary'])

自我檢查:
    python snr_runtime.py
"""

import os
import time

import numpy as np

import snr_audio


def _rms(x):
    return float(np.sqrt(np.mean(np.asarray(x, dtype=float) ** 2)))


class SNRStimulus:
    """即時混音器 + 產生紀錄。

    Parameters
    ----------
    outdir : str
        wav 的輸出目錄,不存在就建立。建議用 `thisExp.dataFileName + '_snr'`,
        這樣刺激檔跟資料檔放在一起、命名對得起來。
    token : str
        `snr_audio.SPEECH_FILES` 裡的鍵。預設 'be'(= /bi/)。
    keep_wavs : bool
        False 的話,每次 make() 之前先刪掉上一批檔案,磁碟只留最近 keep_last 個。
        紀錄裡的種子仍可位元重建,所以刪掉不會失去資訊 —— 只是要重建才拿得回來。
    keep_last : int
        keep_wavs=False 時磁碟上保留幾個最近的檔案。不能太小:PsychoPy 可能在
        routine 結束後才真正放開檔案,刪到還在用的檔會出錯。預設 32 ≈ 6 個試次。
    """

    def __init__(self, outdir, token='be', keep_wavs=True, keep_last=32):
        if token not in snr_audio.speech_names():
            raise KeyError(f"未知的 token:{token!r};"
                           f"可用的是 {snr_audio.speech_names()}")
        self.outdir = outdir
        self.token = token
        self.keep_wavs = bool(keep_wavs)
        self.keep_last = int(keep_last)
        os.makedirs(self.outdir, exist_ok=True)

        self.n_made = 0          # 累計產生數,也是檔名的流水號
        self._log = []           # 還沒被 drain_log() 取走的紀錄
        self._written = []       # 磁碟上還留著的檔案(keep_wavs=False 時用來輪替)
        self._t_total = 0.0      # 累計耗時,用來事後確認沒有拖慢流程

        # 先把語音載進來、把 LTAS 算好,免得第一個試次比其他試次慢一大截。
        snr_audio._load_speech()
        snr_audio.speech_shaped_noise(1024, np.random.default_rng(0))

    # ────────────────────────────────────────────────────────────
    # 主要介面
    # ────────────────────────────────────────────────────────────

    def make(self, snr_db, tag=None, seed=None):
        """即時混一個刺激,寫成 wav,回傳路徑。

        Parameters
        ----------
        snr_db : float
            任意實數 dB。混音器的解析度是 0.001 dB,不需要對齊到任何格點。
        tag : str or None
            這個刺激在試次裡的角色(例如 'UR'、'probe'、'adapt')。只進紀錄,
            不影響音訊;留 None 就用流水號。
        seed : int or None
            指定噪音種子以重建某個舊刺激。正常實驗留 None —— 每次都要新的
            噪音樣本(running noise;frozen noise 會被受試者學起來)。
        """
        t0 = time.perf_counter()
        snr_db = float(snr_db)
        if seed is None:
            seed = snr_audio.new_seed()
        seed = int(seed)

        # 用 mix_components 而不是 mix_at_snr:兩個成分分開拿得到,就能量出
        # **這一個檔案**真正做出來的 SNR,而不是另外混一次去估。
        sr, sp, nz, lead = snr_audio.mix_components(
            self.token, snr_db, np.random.default_rng(seed))
        tail = int(round(snr_audio.NOISE_TAIL_MS * sr / 1000.0))
        seg = slice(lead, len(sp) - tail)
        realised = 20.0 * np.log10(_rms(sp[seg]) / _rms(nz[seg]))

        self.n_made += 1
        name = f"{self.n_made:05d}_{'na' if tag is None else tag}_{snr_db:+.2f}dB.wav"
        path = os.path.join(self.outdir, name)
        # write_wav 回傳縮放量:>0 表示峰值超過上限被壓下來過。等比縮放不會改變
        # SNR,但會改變呈現音量,所以還是記下來 —— 正常設定下不該發生。
        scale = snr_audio.write_wav(path, sr, sp + nz)

        dt = time.perf_counter() - t0
        self._t_total += dt
        self._log.append({
            'n': self.n_made,
            'tag': tag if tag is not None else str(self.n_made),
            'snr_db': snr_db,
            'realised_db': float(realised),
            'seed': seed,
            'token': self.token,
            'path': path,
            'peak_scale': float(scale),
            'ms': dt * 1000.0,
            'summary': f"{self.token}|{snr_db:+.2f}dB|seed={seed}|{name}",
        })

        self._written.append(path)
        if not self.keep_wavs:
            self._prune()
        return path

    def make_many(self, snr_db_list, tags=None):
        """一次做好幾個,回傳路徑 list。順序與輸入一致。

        同一個 dB 出現兩次也沒關係:每次都抽新種子,兩個檔案的噪音必然不同。
        """
        tags = [None] * len(snr_db_list) if tags is None else list(tags)
        if len(tags) != len(snr_db_list):
            raise ValueError("tags 的長度要跟 snr_db_list 一樣")
        return [self.make(db, tag=t) for db, t in zip(snr_db_list, tags)]

    def drain_log(self):
        """取走並清空還沒讀過的紀錄。每個試次結束時呼叫一次,寫進資料檔。"""
        rows, self._log = self._log, []
        return rows

    def stats(self):
        """累計統計,實驗結束時印出來確認即時混音沒有拖慢流程。"""
        return {
            'n_made': self.n_made,
            'total_s': self._t_total,
            'mean_ms': (self._t_total / self.n_made * 1000.0) if self.n_made else 0.0,
            'outdir': self.outdir,
            'on_disk': len(self._written),
        }

    # ────────────────────────────────────────────────────────────
    # 內部
    # ────────────────────────────────────────────────────────────

    def _prune(self):
        """只在 keep_wavs=False 時用:刪掉超出 keep_last 的舊檔。

        刪不掉就算了(Windows 上 PsychoPy 可能還握著檔案)—— 這是省磁碟的
        最佳努力,不是正確性的一環。
        """
        while len(self._written) > self.keep_last:
            old = self._written.pop(0)
            try:
                os.remove(old)
            except OSError:
                pass

    @staticmethod
    def rebuild(seed, snr_db, token='be'):
        """從紀錄裡的 (seed, snr_db) 位元重建某個刺激,回傳 (sr, waveform)。

        double-pass 一致性(同一段噪音重播,看反應一不一致 -> 分離知覺雜訊與
        決策雜訊)與反向相關(哪些頻譜時間區域驅動了反應)這兩條分析靠它。
        """
        return snr_audio.mix_at_snr(token, float(snr_db),
                                    np.random.default_rng(int(seed)))


# ──────────────────────────────────────────────────────────────
# 自我檢查
# ──────────────────────────────────────────────────────────────

def validate(outdir=None, cleanup=True):
    import shutil
    import tempfile
    tmp = outdir or tempfile.mkdtemp(prefix='snr_runtime_')
    print("=" * 70)
    print("snr_runtime —— 即時聲音刺激產生器檢查")
    print("=" * 70)

    snd = SNRStimulus(outdir=tmp)

    print("\n-- 任意實數 SNR,量回來的誤差 ------------------------------")
    worst = 0.0
    for db in (+6.0, -6.0, 0.0, -12.5, -3.333, 9.87654):
        snd.make(db, tag='chk')
        r = snd._log[-1]
        err = abs(r['realised_db'] - db)
        worst = max(worst, err)
        print(f"  要求 {db:+9.4f} dB -> 實際 {r['realised_db']:+9.4f} dB   "
              f"誤差 {err:.1e}   峰值縮放 {r['peak_scale']:.3f}")
    print(f"  最大誤差 {worst:.2e} dB —— {'通過' if worst < 1e-6 else '不通過 ✗'}")

    print("\n-- running noise:同一個 dB 連做兩次應為不同噪音 ------------")
    a, b = snd.make(-6.0, tag='r1'), snd.make(-6.0, tag='r2')
    rows = snd._log[-2:]
    ya = SNRStimulus.rebuild(rows[0]['seed'], rows[0]['snr_db'])[1]
    yb = SNRStimulus.rebuild(rows[1]['seed'], rows[1]['snr_db'])[1]
    diff = float(np.abs(ya - yb).max())
    print(f"  種子 {rows[0]['seed'] % 10**8} vs {rows[1]['seed'] % 10**8}")
    print(f"  波形最大差異 {diff:.4f} —— {'不同(正確)' if diff > 1e-6 else '相同 ✗'}")

    print("\n-- 種子可位元重建 ------------------------------------------")
    r = rows[0]
    y1 = SNRStimulus.rebuild(r['seed'], r['snr_db'])[1]
    y2 = SNRStimulus.rebuild(r['seed'], r['snr_db'])[1]
    print(f"  同種子重建兩次的最大差異 {float(np.abs(y1 - y2).max()):.2e} —— "
          f"{'完全相同(正確)' if np.array_equal(y1, y2) else '不同 ✗'}")

    print("\n-- 兩級的呈現音量必須一致(否則響度會變成第二條線索)--------")
    for db in (+6.0, -6.0):
        y = SNRStimulus.rebuild(snr_audio.new_seed(), db)[1]
        print(f"  {db:+5.1f} dB: RMS={_rms(y):.4f}  峰值={np.abs(y).max():.3f}")

    print("\n-- 速度(一個試次 = study 四個 + probe 一個)-----------------")
    t0 = time.perf_counter()
    snd.make_many([6.0, 6.0, -6.0, -6.0], tags=['UR', 'UL', 'BL', 'BR'])
    snd.make(-6.0, tag='probe')
    dt = (time.perf_counter() - t0) * 1000
    print(f"  五個刺激共 {dt:.1f} ms")
    print(f"  600 個試次外推 {dt * 600 / 1000:.1f} s,攤在整場實驗裡")

    print("\n-- 紀錄的樣子 ----------------------------------------------")
    snd.drain_log()
    snd.make(-6.0, tag='UR')
    for k, v in snd._log[-1].items():
        print(f"  {k:12s} {v}")

    s = snd.stats()
    print(f"\n累計 {s['n_made']} 個刺激,平均 {s['mean_ms']:.1f} ms/個")
    print("=" * 70)
    if cleanup and outdir is None:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    validate()
