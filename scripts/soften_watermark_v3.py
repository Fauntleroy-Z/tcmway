"""
TCM Way 漫画水印淡化脚本 v3
============================
对7张 -new.png 漫画图的右下角AI字幕/水印区域进行淡化处理。

策略：
1. 检测右下角异常纯色块区域
2. 采样上方和左方的正常背景色
3. 创建从边缘向中心的透明度渐变遮罩
4. 将背景色以低不透明度混合覆盖，实现自然淡化
5. 高斯模糊边缘消除硬边界

输出: -soft.png 版本文件
"""

from PIL import Image, ImageDraw, ImageFilter
import os
import math

IMG_DIR = r'C:\Users\Administrator\tcmway-blog\images'

# 每张图的处理参数 (基于目视诊断 + 数据分析)
# (文件名, 右侧比例, 底部比例, 融合强度0-255)
COMICS = [
    ('comic-01-exhaustion-new.png',   0.30, 0.18, 180),
    ('comic-01-why-share-new.png',     0.35, 0.20, 200),
    ('comic-03-qi-new.png',            0.28, 0.16, 170),
    ('comic-04-traffic-jam-new.png',   0.25, 0.18, 190),
    ('comic-05-body-clock-new.png',    0.27, 0.15, 180),
    ('comic-06-dampness-new.png',      0.22, 0.12, 160),
    ('comic-06-spleen-new.png',        0.25, 0.18, 185),
    # ── #07-#10 (added 2026-05-29) ──
    ('comic-07-six-signs-new.png',          0.30, 0.18, 190),
    ('comic-08-cold-hands-new.png',          0.28, 0.18, 180),
    ('comic-09-six-layer-defense-new.png',   0.28, 0.18, 185),
    ('comic-10-stop-feeding-new.png',        0.30, 0.18, 190),
]


def get_edge_color(img, x_start, y_start, sample_width=20):
    """采样目标区域上边缘和左边缘的颜色作为融合基准"""
    top_colors = []
    left_colors = []
    
    # 上边缘采样（区域内顶部几行）
    for x in range(x_start, min(x_start + sample_width, img.width)):
        for dy in range(8):
            y = y_start + dy
            if y < img.height:
                px = img.getpixel((x, y))
                if len(px) >= 4 and px[3] > 128:
                    top_colors.append(px[:3])
                    break
    
    # 左边缘采样（区域内左侧几列）
    for y in range(y_start, min(y_start + sample_width, img.height)):
        for dx in range(8):
            x = x_start + dx
            if x < img.width:
                px = img.getpixel((x, y))
                if len(px) >= 4 and px[3] > 128:
                    left_colors.append(px[:3])
                    break
    
    # 合并计算平均基准色
    all_edge = top_colors + left_colors
    if not all_edge:
        return (240, 230, 210)  # fallback 米白色
    
    avg = tuple(sum(c) // len(all_edge) for c in zip(*all_edge))
    return avg


def create_fade_mask(width, height, feather_radius=30):
    """创建从边缘向中心淡入的渐变遮罩（边缘透明，中心不透明）"""
    mask = Image.new('L', (width, height), 0)
    
    for y in range(height):
        for x in range(width):
            # 计算到最近边缘的距离
            dist_to_top = y
            dist_to_bottom = height - 1 - y
            dist_to_left = x
            dist_to_right = width - 1 - x
            dist = min(dist_to_top, dist_to_bottom, dist_to_left, dist_to_right)
            
            # 羽化过渡
            if dist >= feather_radius:
                opacity = 255
            else:
                opacity = int(255 * (dist / feather_radius) ** 1.5)
            
            mask.putpixel((x, y), opacity)
    
    # 用高斯模糊让过渡更自然
    mask = mask.filter(ImageFilter.GaussianBlur(radius=feather_radius // 2))
    return mask


def process_comic(fname, right_ratio, bottom_ratio, blend_strength):
    """处理单张漫画图片"""
    src_path = os.path.join(IMG_DIR, fname)
    base_name = fname.replace('-new.png', '')
    out_path = os.path.join(IMG_DIR, f'{base_name}-soft.png')
    
    print(f"\n{'='*60}")
    print(f"Processing: {fname}")
    
    img = Image.open(src_path).convert('RGBA')
    w, h = img.size
    
    # 计算处理区域
    x_start = int(w * (1 - right_ratio))
    y_start = int(h * (1 - bottom_ratio))
    region_w = w - x_start
    region_h = h - y_start
    
    print(f"  Size: {w}x{h}, Region: ({x_start},{y_start},{w},{h}) [{region_w}x{region_h}]")
    
    # 采样边缘颜色作为融合基准
    base_color = get_edge_color(img, x_start, y_start)
    print(f"  Base edge color: RGB{base_color}")
    
    # 提取右下角区域
    region = img.crop((x_start, y_start, w, h))
    
    # 创建渐变遮罩
    feather = max(15, min(region_w, region_h) // 5)
    fade_mask = create_fade_mask(region_w, region_h, feather_radius=feather)
    
    # 创建覆盖层（使用基准色的柔和版本）
    overlay = Image.new('RGBA', (region_w, region_h), (*base_color, blend_strength))
    
    # 将覆盖层用渐变遮罩应用到区域上
    # 遮罩控制覆盖层的透明度分布
    faded_overlay = Image.composite(overlay, Image.new('RGBA', (region_w, region_h), (0, 0, 0, 0)), fade_mask)
    
    # 将淡化后的覆盖层与原图区域混合
    # 使用 alpha compositing: overlay 渐变融入原区域
    blended = Image.alpha_composite(region, faded_overlay)
    
    # 整体轻微模糊整个处理区域使融合更自然
    blended = blended.filter(ImageFilter.GaussianBlur(radius=1.5))
    
    # 将处理后的区域贴回原图
    img.paste(blended, (x_start, y_start))
    
    # 转回RGB保存为PNG（保持质量）
    rgb_img = Image.new('RGB', img.size, (255, 255, 255))
    rgb_img.paste(img, mask=img.split()[3])  # 用alpha通道作为mask
    
    rgb_img.save(out_path, 'PNG', optimize=True)
    file_size = os.path.getsize(out_path)
    print(f"  -> Saved: {out_path}")
    print(f"     Size: {file_size / 1024:.1f} KB")
    
    return out_path


def main():
    print("=" * 60)
    print("TCM Way Comic Watermark Softener v3")
    print("Strategy: Edge-color gradient fade with feather blending")
    print("=" * 60)
    
    results = []
    for fname, rp, bp, strength in COMICS:
        try:
            out = process_comic(fname, rp, bp, strength)
            results.append((fname, 'OK', out))
        except Exception as e:
            results.append((f'ERROR: {e}', None))
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for fname, status, out in results:
        icon = "✅" if status == "OK" else "❌"
        print(f"  {icon} {fname}: {status}")


if __name__ == '__main__':
    main()
