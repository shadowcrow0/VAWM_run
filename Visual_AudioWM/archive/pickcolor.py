import numpy as np
from skimage import color

def pick_three_colors(L, C, H_start):
    colors = []

    for i in range(3):
        H = H_start + i * 120  # 三個顏色間隔 120°
        H_rad = H * np.pi / 180  # 角度轉弧度
        a = C * np.cos(H_rad)
        b = C * np.sin(H_rad)
        
        lab = np.array([[[L, a, b]]])
        rgb = color.lab2rgb(lab)[0][0]
        rgb_clipped = np.clip(rgb, 0, 1)
        r = int(rgb_clipped[0] * 255)
        g = int(rgb_clipped[1] * 255)
        b_ch = int(rgb_clipped[2] * 255)
        hex_val = '#{:02X}{:02X}{:02X}'.format(r, g, b_ch)
        
        colors.append({
            'H': H,
            'L': L,
            'a': round(a, 2),
            'b': round(b, 2),
            'hex': hex_val
        })
    
    return colors

H_start = np.random.randint(0, 330)  # 隨機起始色相
colors = pick_three_colors(L=70, C=50, H_start=H_start+30)
# 容易（prototype）
easy = pick_three_colors(L=60, C=40, H_start=0)

# 困難（boundary）
hard = pick_three_colors(L=60, C=40, H_start=30)
print(f"H_start = {H_start}°")    
for idx, color_info in enumerate(colors):
    print(f"Color {idx+1}: H={color_info['H']}°, L={color_info['L']}, a={color_info['a']}, b={color_info['b']}, Hex={color_info['hex']}")


