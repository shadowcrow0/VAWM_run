# Constructing the Colour Dimension — Method Summary

**Project** AVWM · adaptive GRT · colour × (auditory) working memory
**Status** The **axis** (coordinate system) is settled and implemented.
The **stimulus levels on it are not** — see §8. All figures below are measured
from `agrt_setup.py` and `agrt_colour_lut.json`, not estimated.
**Date** 2026-08-13

---

## 1. Goal

- Build **one** continuous stimulus dimension for colour that satisfies what an
  adaptive GRT procedure requires of a dimension.
- The adaptive procedure (Psi, as implemented in `AGRT.py`) assumes the dimension is:
  - **continuous** — any real value in range must be renderable
  - **monotone** — moving along the axis moves perception in one direction only
  - **affinely related to the internal scale** — the transducer is assumed linear
  - **symmetric about the range midpoint** — the model places α there
- Requirement: changing position on this axis must change **only colour**, and only
  along **one** perceptual attribute.

---

## 2. Why not RGB / HSV / hue degrees

- **RGB and HSV are device spaces, not perceptual spaces.** Equal steps in either
  produce grossly unequal perceptual steps, and they change lightness and saturation
  as a side effect of changing hue.
- **CIELCh** separates the three attributes we care about:
  - `L*` = lightness
  - `C*` = chroma (saturation)
  - `h` = hue angle
- This separation is what makes a **single-attribute** manipulation expressible at all.

---

## 3. The construction — three decisions

### 3.1 Fix two attributes, vary one

- **`L*` = 55** — held constant.
- **`C*` = 38** — held constant.
- **`h` (hue angle) — the only thing that varies.**
- Consequence: no lightness or saturation cue covaries with position on the axis.
  This is the colour-side analogue of pinning F0/F1 in a speech continuum.

### 3.2 Anchor the axis at h = 303°

- The axis spans **60°**, centred on **h = 303°**.
- ⭐ **303° was chosen specifically to avoid 283°**, which sits on the
  **blue/violet categorical boundary**.
- Rationale: a category boundary inside the axis breaks monotonicity of the
  *decision* even when the *stimulus* is monotone — observers switch naming strategy
  mid-axis, and the psychometric function acquires a step the Psi model cannot fit.
- ⚠️ This was an actual correction during development: the anchor was initially set to
  283°, i.e. exactly the value to avoid.

### 3.3 Coordinate = signed ΔE00 arc length, **not** hue degrees

- ⭐ **This is the single most important decision in the whole construction.**
- Hue angle is **not** perceptually uniform. Measured across the 60° span used here:

  | quantity | value |
  |---|---|
  | ΔE00 per degree, minimum | **0.3598** (at h = 243.00°) |
  | ΔE00 per degree, maximum | **0.5546** (at h = 289.72°) |
  | non-uniformity | **54.1 %** |

- Meaning: **equal steps in degrees produce perceptual steps that differ by a factor
  of 1.541 between the two ends of the axis.**
- If degrees were used as the coordinate, the "linear transducer" assumption would be
  violated by construction, and the Psi estimate of β would be biased by an amount
  that depends on *where on the axis* the staircase happened to converge.
- **Fix:** integrate ΔE00 (CIEDE2000) along the hue arc and use the **signed arc
  length in ΔE00 units** as the stimulus coordinate.
- Verified **strictly monotone** across the full LUT.

---

## 4. Range and the β ceiling

- **Gamut limits the axis asymmetrically.** Usable extent, measured:
  - full arc: **−25.866 … +24.134 ΔE00**
  - usable **symmetric** half-length: **24.1372 ΔE00** (the binding side)
- The adaptive procedure cannot estimate a slope steeper than its range allows.
  With the lapse rate fixed at δ = 0.08:

  ```
  β_max  =  (usable half-range) / 2.3107  =  24.1372 / 2.3107  =  10.4458 ΔE00
  ```

- ⚠️ **The numerator is the HALF-range, not the full range.** This was a real error
  during development — using the full range gave 20.99, a factor-of-2 overestimate of
  what the axis can support.
- Practical reading: if a participant's true σ exceeds ~10.4 ΔE00, the axis is too
  short to measure them and the estimate will be censored, not merely noisy.

---

## 5. Implementation

- `agrt_setup.py` — defines the axis, computes ΔE00 arc length, exports the table.
- `agrt_colour_lut.json` — precomputed lookup table:
  - **5001 points**, step **0.01 ΔE00**, arc **−25.866 … 24.134**
  - **298 distinct hex colours** (8-bit display quantisation is the limiter, not the LUT)
  - 53.9 KB
- Anchor (arc = 0) renders as **`#8B7ABB`**; ±3 ΔE00 give **`#827CBE`** and **`#9477B7`**.
- The experiment reads the LUT directly:

  ```python
  def colour_for(arc):
      if not (_LUT_ARC[0] <= arc <= _LUT_ARC[-1]):
          raise ValueError(...)
      return _LUT_HEX[int(np.abs(_LUT_ARC - arc).argmin())]
  ```

- ⭐ Deliberate design choice: shipping a **LUT rather than a converter** means
  PsychoPy needs no colour-science dependency at runtime. (Installing one broke the
  local SciPy during development — a numpy upgrade conflicted with the system SciPy.)
- Out-of-range requests **raise** rather than clamp, so a silent gamut clip cannot be
  mistaken for a real stimulus level.

---

## 6. Validation performed

- ✅ Arc length **strictly monotone** over all 5001 points.
- ✅ Usable symmetric half-length **24.1372 ΔE00**, independently recomputed.
- ✅ β ceiling **10.4458 ΔE00** (corrected from an erroneous 20.99).
- ✅ Hue non-uniformity **54.1 %** — the quantity that justifies the ΔE00 coordinate.
- ✅ LUT reproduces the candidate pairs in `bv_candidates_for_advisor.csv`
  (sets 17 and 18) **exactly**.
- ✅ Anchor 303° confirmed clear of the 283° category boundary.

---

## 7. Known limits — state these in the write-up

- **ΔE00 is calibrated on large uniform patches under a reference illuminant.** Our
  stimuli are small (4 × 4 units) and briefly presented. ΔE00 is the best available
  metric, not a guarantee of perceptual uniformity under these conditions.
- **No monitor calibration is assumed.** Hex values are nominal sRGB. Without a
  colorimeter, the realised ΔE00 on the actual display is unverified.
- **298 distinct colours over 50 ΔE00** means the finest realisable step is
  ~0.17 ΔE00. Adaptive requests finer than that silently land on the same hex.
  This is below any plausible discrimination threshold, so it does not bind in
  practice — but it is a hard floor.
- **Category boundaries were avoided, not measured.** The 283° boundary comes from the
  literature, not from a pilot in this lab with these observers.
- **One attribute varying does not guarantee one *perceptual* dimension varying.**
  Physical orthogonality in CIELCh is not the same as perceptual separability; that is
  an empirical question GRT is meant to answer, not an assumption it can be given.

---

## 8. ⚠️ What is NOT settled

The axis is a ruler. Nothing has yet decided **where on the ruler the stimuli sit.**

- **The colour values in the experiment are placeholders.** `GRTv2.psyexp` currently
  has `COLOUR_ARC = [-3.0, +3.0]` with an explicit PLACEHOLDER comment. ±3 ΔE00 was
  not derived from anything.
- **Why this matters:** reported colour-memory SDs run **3–8 ΔE00**. A 6-ΔE00
  separation is comfortable for an observer at the low end and near-indiscriminable
  at the high end. This spread is precisely why an adaptive procedure was planned.
- **The adaptive block that was meant to set these values has not been built.**
  No `dim1range` / `dim1steps` is configured anywhere in the project.
- **The gamut clamp is documented but not enforced.** `arc_range_in_gamut()` exists
  and is the required way to bound adaptive proposals (the blue side leaves sRGB at
  h ≈ 250.3°), but nothing outside `agrt_setup.py`'s self-test calls it.
- **Display quantisation interacts with the unbuilt config:** proposals finer than
  ~0.15 ΔE00 render as the same 8-bit colour, so whether `dim1steps = 100` is
  appropriate depends on the final `dim1range` — which does not exist yet.

Two ways to close this, decided by (not before) the design discussion:
1. **Build the adaptive block** (per-participant staircase on the colour axis) — the
   original plan; still valid in a colour-only design.
2. **Fix the separation from a short pilot** (e.g. constant stimuli at 4–6 levels)
   and drop the adaptive machinery — cheaper, defensible if the DV is the
   between-condition difference rather than the threshold itself.

## 9. Summary for a reader in a hurry

- Colour is manipulated in **CIELCh** with **L\* = 55** and **C\* = 38 fixed**;
  **only hue angle varies**.
- The axis is centred at **h = 303°**, deliberately away from the **283°
  blue/violet category boundary**, and spans **60°**.
- The stimulus coordinate is **signed ΔE00 arc length**, not degrees, because hue is
  **54.1 % non-uniform** across this span — equal angular steps would differ
  perceptually by a factor of 1.541 end to end.
- Usable symmetric half-range is **24.14 ΔE00**, which caps the measurable slope at
  **β ≤ 10.45 ΔE00**.
- Delivered as a **5001-point lookup table** so the experiment carries no colour
  dependency, with out-of-range values raising rather than clamping.
- ⚠️ **Not settled:** the actual stimulus separation (currently a ±3 ΔE00
  placeholder) and the adaptive block meant to determine it — see §8.

---

## Related
- Decision trail (Chinese) — [[決策脈絡_顏色維度]]
- The AGRT model assumptions this axis is built to satisfy — [[決策脈絡_AGRT模型假設]]
- Auditory dimension, by contrast — [[聽覺維度_嘗試與放棄紀錄]]
- Colour-in-WM background — [[colorWM]]
