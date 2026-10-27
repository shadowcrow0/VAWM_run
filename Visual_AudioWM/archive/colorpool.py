import numpy as np
import csv
from skimage import color as skcolor

# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------

def delta_e(c1, c2):
    return float(np.sqrt(np.sum((np.array(c1) - np.array(c2)) ** 2)))

def is_in_gamut(L, a, b):
    rgb = skcolor.lab2rgb(np.array([[[L, a, b]]]))[0][0]
    return bool(np.all(rgb >= 0) and np.all(rgb <= 1))

def lab_to_hex(lab):
    L, a, b = lab
    rgb = skcolor.lab2rgb(np.array([[[L, a, b]]]))[0][0]
    r, g, b_ch = [int(x * 255) for x in np.clip(rgb, 0, 1)]
    return '#{:02X}{:02X}{:02X}'.format(r, g, b_ch)

def random_lab():
    L     = np.random.uniform(40, 60)
    C     = np.random.uniform(40, 60)
    H_rad = np.random.uniform(0, 2 * np.pi)
    return np.array([L, C * np.cos(H_rad), C * np.sin(H_rad)])

def find_color(target, de_min, de_max, max_tries=2000):
    for _ in range(max_tries):
        direction = np.random.randn(3)
        direction = direction / np.linalg.norm(direction)
        candidate = target + direction * np.random.uniform(de_min, de_max)
        L, a, b = candidate
        if is_in_gamut(L, a, b) and de_min < delta_e(target, candidate) < de_max:
            return candidate
    return None

# ------------------------------------------------------------
# Generate 155 color trials: 2 targets each with H (ΔE ≥ 25), L (ΔE ≥ 20)
# Within trial: target1 vs target2 ΔE ≥ 20
# Between trials: consecutive targets ΔE ≥ 30
# H vs L within same target: ΔE ≥ 15
# No duplicate colors across all trials
# ------------------------------------------------------------

color_pool = []
prev_targets = []  # 記錄上一組的 targets
used_hex = set()   # 記錄已使用的 hex 顏色

while len(color_pool) < 155:

    # target1: random valid color, 且與前一組距離 > 30
    t1 = None
    for _ in range(500):
        c = random_lab()
        if not is_in_gamut(*c):
            continue
        # 檢查與前一組所有 targets 的距離
        if prev_targets and any(delta_e(c, pt) < 30 for pt in prev_targets):
            continue
        t1 = c
        break
    if t1 is None:
        continue

    # H1 and L1 for target1
    h1 = find_color(t1, 25, 50)
    if h1 is None:
        continue
    l1 = find_color(t1, 20, 30)
    if l1 is None:
        continue
    # H1 vs L1 must be > 15
    if delta_e(h1, l1) < 15:
        continue

    # target2: different from t1 (ΔE > 20), 且與前一組距離 > 30
    t2 = None
    for _ in range(500):
        c = random_lab()
        if not is_in_gamut(*c):
            continue
        if delta_e(t1, c) < 20:
            continue
        if prev_targets and any(delta_e(c, pt) < 30 for pt in prev_targets):
            continue
        t2 = c
        break
    if t2 is None:
        continue

    # H2 and L2 for target2
    h2 = find_color(t2, 25, 50)
    if h2 is None:
        continue
    l2 = find_color(t2, 20, 30)
    if l2 is None:
        continue
    # H2 vs L2 must be > 15
    if delta_e(h2, l2) < 15:
        continue

    # compute actual delta E values
    de_h1, de_l1 = delta_e(t1, h1), delta_e(t1, l1)
    de_h2, de_l2 = delta_e(t2, h2), delta_e(t2, l2)
    de_hl1, de_hl2 = delta_e(h1, l1), delta_e(h2, l2)

    # check for duplicate hex colors
    hex_colors = [lab_to_hex(t1), lab_to_hex(h1), lab_to_hex(l1),
                  lab_to_hex(t2), lab_to_hex(h2), lab_to_hex(l2)]
    if any(h in used_hex for h in hex_colors):
        continue
    # also check within this trial for duplicates
    if len(set(hex_colors)) != 6:
        continue

    # all conditions met, add to pool
    used_hex.update(hex_colors)
    color_pool.append({
        'trial': len(color_pool) + 1,
        'color1_target': lab_to_hex(t1),
        'color1_H': lab_to_hex(h1),
        'color1_L': lab_to_hex(l1),
        'color1_H_deltaE': round(de_h1, 2),
        'color1_L_deltaE': round(de_l1, 2),
        'color1_HL_deltaE': round(de_hl1, 2),
        'color2_target': lab_to_hex(t2),
        'color2_H': lab_to_hex(h2),
        'color2_L': lab_to_hex(l2),
        'color2_H_deltaE': round(de_h2, 2),
        'color2_L_deltaE': round(de_l2, 2),
        'color2_HL_deltaE': round(de_hl2, 2),
    })

    # 更新 prev_targets 給下一組檢查
    prev_targets = [t1, t2]

    print(f"Trial {len(color_pool):3d}/155  H1={de_h1:.1f} L1={de_l1:.1f} HL1={de_hl1:.1f}  H2={de_h2:.1f} L2={de_l2:.1f} HL2={de_hl2:.1f}")

# ------------------------------------------------------------
# Save to CSV
# ------------------------------------------------------------

csv_path = "stimuli/color_155trials.csv"
with open(csv_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=color_pool[0].keys())
    writer.writeheader()
    writer.writerows(color_pool)

print(f"\nDone. Saved to {csv_path}")
