# CLAUDE.md

## What this repo is

A **PsychoPy** experiment on **audiovisual working memory**, analysed with
**GRT** (General Recognition Theory). The question: when you remember a colour
paired with a speech sound, are the two features stored independently, or does
one interfere with the other?

Each item is a **colour × sound** pair, encoded as 2 bits:

```
item = 0     1     2     3
color  C1    C2    C1    C2      colour = i & 1
sound  S1    S1    S2    S2      sound  = (i >> 1) & 1

so:  target ^ 1 = differs in colour only
     target ^ 2 = differs in sound only
     target ^ 3 = differs in both
```

That XOR trick is used throughout the trial code — `relation` in the data files
is exactly this value.

## One trial

```
study  ~4.3s   four colour+sound items, one per corner, 1s each
               onsets 0.3 / 1.3 / 2.3 / 3.3s, order reshuffled per trial
               all four items appear every trial (one of each)

cue     2.0s   0-1s  empty white frame at one corner
               1-2s  a colour+sound appears inside that frame
               ⚠ the frame sits where cued_item was studied,
                 but the content shown is target_item

task     ---   four options (colour + label), one per corner, reshuffled
               keys:  i = upper left    o = upper right
                      k = lower left    l = lower right

rest     ---   only after practice and after each block; skipped otherwise
```

On **valid** trials (2/3 of them) cued_item == target_item, so there is no
conflict. On **invalid** trials the cue points one way and the probe shows
another; picking the cued item is scored `intrusion`.

**Because the probe displays the answer, valid trials are an identification
task, not a memory task.** Memory only enters through the invalid trials'
intrusions. See `review/voicing×顏色互動_資料怎麼量到.md` §1.3 — that wording
matters for any write-up.

Counts: 24 practice + 576 main (4 blocks × 144) = 600 trials, valid:invalid
held at 2:1 within every block. Practice deliberately uses the same ratio.

## The two experiment scripts

Both are PsychoPy Builder output from `GRTv2.psyexp`, hand-edited afterwards.
**Do not regenerate from Builder** — that would wipe the hand-written sections.

| | `GRTv3.py` | `GRTv3_a.py` | `GRTv3_ada.py` |
|---|---|---|---|
| Sound stimulus | one token `be.wav` (/bi/), always | same | same |
| Two auditory items | **high SNR** vs **low SNR** (+6 / −6 dB, fixed) | ±SNR from AGRT | ±SNR from AGRT |
| What the listener reports | **the consonant: [bi] or [pi]** | "clear / noisy" | **[bi] or [pi]** |
| Colour axis | fixed ±3.0 ΔE00 | calibrated by a 60-trial AGRT phase | same |
| Calibration | — | 60 joint trials, two f/j questions | **72 colour + 72 sound trials of the real task, then 15 practice with feedback** |
| Status | fixed-level design | superseded by `_ada` | current adaptive design |

**The design (`GRTv3.py`).** One syllable is played all session. Noise masks the
voicing cue, so the low-SNR item is often heard as /pi/. The physical difference
between the two auditory items is the noise level; the *reported* difference is
the consonant.

⚠️ Structural ceiling to state in any write-up: with only /bi/ presented, the
low-SNR item can at best drive responses to **chance** (50/50) — it cannot be
reliably heard as /p/ unless noise produces a systematic b→p bias, which has not
been measured here. So the auditory dimension's d′ is capped and the confusion
matrix is asymmetric. The alternative that avoids this is two tokens (be + pe)
at one shared SNR — which is what `snr_audio.py` was actually built for; it
aligns the two tokens' onsets and voiced-segment RMS so that one SNR number
means the same thing for both.

**`GRTv3_ada.py` — the adaptive design.** Both dimensions are calibrated per
participant by the two independent Psi objects in `AGRT.py` (60 trials, one
audiovisual compound per trial). The sound axis is SNR used as a *stand-in for
the b/p (VOT) continuum*, which the program cannot synthesise: high-SNR /bi/
stands for the b end, low-SNR /bi/ for the p end, 0 dB is the nominal category
boundary, and trial-by-trial feedback anchors the listener's b/p criterion
there. Under that design P(report bi) is meant to run from 1 down to 0 across
SNR, which is exactly the shape `AGRT.py:133` models ([δ/2, 1−δ/2]) — so the
earlier objection (a one-token curve that floors at 0.5 and needs a 1-D
`QuestHandler`) no longer applies. The session runs in three blocks, **all of them the real task** (four
study items → cue → four-corner choice), so the calibrated values reflect the
limit under working-memory load, not bare perception: (1) colour calibration
— Psi proposes a signed distance x, the two colours are ±|x|, and all four
squares play the same clear /bi/ (`ADAPT_FIX_SNR`); the chosen option's colour
bit feeds `_psi1`; (2) sound calibration — Psi proposes s, the two levels are
±|s|, all four squares are the anchor colour (`ADAPT_FIX_ARC` = 0); the chosen
option's syllable bit feeds `_psi2`; (3) the estimates go into the main task,
starting with `N_PRACTICE` (15) practice trials. Calibration trials are all
valid; in them two corners are content-identical (the other dimension does not
vary) and either counts as correct — `outcome`/`is_correct` score only the
calibrated dimension there. Calibration and practice frame the correct
option(s) after each answer; the main blocks give no feedback. Trial counts
per calibration block are `N_ADAPT_COL` / `N_ADAPT_SND` (72 each — half of
Glavan's 144, because each calibration trial here is a full ~8-10 s WM trial
rather than a 2 s judgement; the two blocks take roughly 20-25 minutes).

Two things the code cannot settle: (1) whether low SNR really pushes /bi/
toward /pi/ on this token has **not been piloted** — if it does not, the
estimated sound α/β reflect the learned feedback rule, not perception; and
(2) turning `SND_FEEDBACK` off removes the anchor and the curve may floor at
0.5 again, breaking the model.

⛔ `GRTv3_a.py` asks "clear or noisy" and is kept only as the predecessor.

⚠️ The ±6 dB levels in `GRTv3.py` are **placeholders**, not measured. The low
level needs to be low enough to actually push /bi/ toward /pi/, and that
threshold has not been piloted on this token.

## Supporting modules

```
AGRT.py            Psi adaptive procedure (Kontsevich & Tyler 1999),
                   GRT variant by Glavan 2022. GPL, third-party.
                   Locally patched for a removed scipy API.
                   Two independent Psi objects, one per dimension.

agrt_setup.py      builds the perceptually-uniform colour axis (ΔE00 arc
   +               length, not CIELAB hue angle — hue degrees are not
agrt_colour_lut    perceptually uniform, which would silently break AGRT's
   .json           constant-variance assumption).
                   ⚠ Needs `colour-science`, which PsychoPy's bundled Python
                     does NOT have. So the LUT is generated OFFLINE and the
                     experiment only does a numpy table lookup at runtime.
                     To change the colour gamut, re-run export_lut().

snr_audio.py       mixes speech into speech-shaped noise at an exact SNR.
                   Aligns onset + voiced-segment RMS across tokens, fixes
                   output level so loudness is not a cue, logs the noise
                   seed so any sample can be rebuilt bit-for-bit.

snr_runtime.py     the thin layer between snr_audio and the experiment:
                   mixes a stimulus ON DEMAND at any real dB (~3 ms each),
                   writes a wav, and logs dB + noise seed for every one.
                   Fresh seed per call, so running noise is automatic.
                   `SNRStimulus.rebuild(seed, db)` reconstructs any
                   stimulus that was actually presented.
                   Run `python snr_runtime.py` for its self-check.

audio_device.py    resolves the output device BY NAME, never by index
                   (indices shift between machines and across replugging).
```

## Gotchas that have already bitten

- **`thisExp.nextEntry()` is written by hand** at the end of the trial loop.
  The loop's handler is built with `isTrials=False`, so PsychoPy does not
  emit it. Without that line all 600 trials overwrite one row and the saved
  file has a single line of data.
- **`GRTv3.py` requires headphones** (`require_headphones=True`) and errors
  out if none are found. Over speakers the delivered SNR is not the
  configured SNR, so the data is worthless.
- **`dim2steps` in `AGRTHandler` sets three grids at once** — the stimulus
  grid, the α grid and the β grid. It is 9 for the b/p continuum because only
  9 audio files exist, which leaves α and β on a 9-point search grid too.
- **PsychoPy is not installed in the dev container.** Scripts can be
  `py_compile`d and the pure-numpy modules can be exercised, but nothing
  visual or audio-related can be run here. Say so rather than implying a
  script was executed.

## Open design question

The instructions say *"report which item was there"* but scoring credits the
**probe's** content. On invalid trials a participant following the instructions
literally is recorded as `intrusion`, and there is no trial-by-trial feedback
to teach them otherwise. Relative comparisons across `relation` levels survive
this; absolute rates do not. Fixing it means changing the instruction wording
or the scoring — a design decision for the researcher, not a cleanup.

## `review/`

Chinese-language decision and audit notes: why the auditory dimension went
duration → VOT → SNR, why this consonant pair, statistical plan, what was tried
and abandoned. `決策脈絡_索引.md` is the index.

These are **dated records**. They cite line numbers against the older
`GRTv2.py` / `GRTv2_demo.py` filenames — that is intentional, not staleness to
fix.

## Response style

**Be concise.** Lead with the answer. Cut preamble, restatements of the
question, and closing summaries of what was just said. Length should track the
complexity of the question, not the effort spent on it.

Keep what is load-bearing: caveats that change a decision, what was verified
versus assumed, and the numbers behind a claim. Trim commentary, not evidence.

**Use ASCII to visualize content when explaining concepts.** When something has
structure — a timeline, a data flow, a grid, a state change, a before/after —
draw it instead of describing it in prose. Label the boxes, keep it under ~15
lines, put it in a fenced block so the alignment survives. Skip it when there
is no structure to show (a yes/no answer, a single number).

## Conventions

- Comments and docs in this repo are written in Chinese; match that.
- Comments explain **why**, especially where a simpler-looking approach was
  tried and failed. Keep that reasoning when editing nearby code.
- Generated per-participant stimuli (`data/*_snr/`, ~130 MB per session) are
  gitignored — they are rebuildable from the dB + seed logged in each trial's
  `snd_*` columns.
