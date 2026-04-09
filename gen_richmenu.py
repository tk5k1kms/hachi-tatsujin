from PIL import Image, ImageDraw, ImageFont
import os, math

W, H = 2500, 843
panel_w = W // 3

# Create RGBA image for gradient support
img = Image.new('RGBA', (W, H))
draw = ImageDraw.Draw(img)

# Gradient backgrounds for each panel
def draw_gradient(draw, x0, y0, x1, y1, color_top, color_bot):
    for y in range(y0, y1):
        ratio = (y - y0) / (y1 - y0)
        r = int(color_top[0] + (color_bot[0] - color_top[0]) * ratio)
        g = int(color_top[1] + (color_bot[1] - color_top[1]) * ratio)
        b = int(color_top[2] + (color_bot[2] - color_top[2]) * ratio)
        draw.line([(x0, y), (x1, y)], fill=(r, g, b, 255))

# Panel 1: Navy gradient
draw_gradient(draw, 0, 0, panel_w, H, (20, 60, 110), (15, 40, 80))
# Panel 2: Green gradient
draw_gradient(draw, panel_w, 0, panel_w * 2, H, (10, 210, 95), (6, 170, 70))
# Panel 3: Orange gradient
draw_gradient(draw, panel_w * 2, 0, W, H, (255, 120, 55), (230, 90, 40))

# Separator lines
for i in range(1, 3):
    x = i * panel_w
    draw.line([(x, 0), (x, H)], fill=(255, 255, 255, 60), width=4)

# Load fonts
font_paths = [
    "C:/Windows/Fonts/meiryob.ttc",  # Meiryo Bold
    "C:/Windows/Fonts/meiryo.ttc",
    "C:/Windows/Fonts/YuGothB.ttc",
    "C:/Windows/Fonts/msgothic.ttc",
]
font_label = None
font_sub = None
font_icon = None
for fp in font_paths:
    if os.path.exists(fp):
        try:
            font_label = ImageFont.truetype(fp, 88)
            font_sub = ImageFont.truetype(fp, 46)
            font_icon = ImageFont.truetype(fp, 110)
            print(f"Using font: {fp}")
            break
        except:
            continue

if font_label is None:
    font_label = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_icon = ImageFont.load_default()

# --- Draw icons using shapes ---

def draw_yen_icon(draw, cx, cy, r):
    """Draw a yen sign using lines"""
    white = (255, 255, 255, 255)
    lw = 8
    # Y shape top
    draw.line([(cx - 50, cy - 55), (cx, cy - 5)], fill=white, width=lw)
    draw.line([(cx + 50, cy - 55), (cx, cy - 5)], fill=white, width=lw)
    # Vertical line down
    draw.line([(cx, cy - 5), (cx, cy + 55)], fill=white, width=lw)
    # Two horizontal bars
    draw.line([(cx - 35, cy + 5), (cx + 35, cy + 5)], fill=white, width=lw)
    draw.line([(cx - 35, cy + 25), (cx + 35, cy + 25)], fill=white, width=lw)

def draw_chat_icon(draw, cx, cy, r):
    """Draw a chat bubble using polygon"""
    white = (255, 255, 255, 255)
    # Rounded rectangle approximation for chat bubble
    bx, by, bw, bh = cx - 55, cy - 45, 110, 70
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=15, fill=white)
    # Chat tail (triangle)
    draw.polygon([(cx - 15, by + bh), (cx + 10, by + bh), (cx - 20, by + bh + 25)], fill=white)
    # Three dots inside
    dot_r = 7
    dot_y = cy - 10
    for dx in [-25, 0, 25]:
        ddx = cx + dx
        draw.ellipse([ddx - dot_r, dot_y - dot_r, ddx + dot_r, dot_y + dot_r],
                      fill=(6, 199, 85, 255))

def draw_phone_icon(draw, cx, cy, r):
    """Draw a phone handset using shapes"""
    white = (255, 255, 255, 255)
    # Simple phone shape using ellipses and lines
    # Handset body (rotated rectangle approximation)
    lw = 10
    # Arc-like handset
    draw.arc([cx - 45, cy - 50, cx + 45, cy + 50], start=210, end=330, fill=white, width=lw)
    # Earpiece (top)
    draw.rounded_rectangle([cx - 50, cy - 55, cx - 15, cy - 25], radius=8, fill=white)
    # Mouthpiece (bottom)
    draw.rounded_rectangle([cx + 15, cy + 25, cx + 50, cy + 55], radius=8, fill=white)

panels = [
    {"draw_icon": draw_yen_icon, "label": "料金を見る", "sub": "基本料金4,400円〜"},
    {"draw_icon": draw_chat_icon, "label": "見積り依頼", "sub": "LINE割引2,000円OFF"},
    {"draw_icon": draw_phone_icon, "label": "電話する", "sub": "24時間対応"},
]

for i, p in enumerate(panels):
    cx = i * panel_w + panel_w // 2
    icon_cy = 230

    # Outer circle ring
    r_outer = 90
    draw.ellipse(
        [cx - r_outer, icon_cy - r_outer, cx + r_outer, icon_cy + r_outer],
        fill=None,
        outline=(255, 255, 255, 160),
        width=4
    )

    # Draw the icon shape
    p["draw_icon"](draw, cx, icon_cy, r_outer)

    # Label text
    label_y = 400
    bbox = draw.textbbox((0, 0), p["label"], font=font_label)
    lw = bbox[2] - bbox[0]
    draw.text((cx - lw // 2, label_y), p["label"], fill="white", font=font_label)

    # Decorative line under label
    line_y = label_y + 110
    line_hw = 80
    draw.line([(cx - line_hw, line_y), (cx + line_hw, line_y)], fill=(255, 255, 255, 120), width=3)

    # Sub text
    sub_y = line_y + 24
    bbox = draw.textbbox((0, 0), p["sub"], font=font_sub)
    sw2 = bbox[2] - bbox[0]
    draw.text((cx - sw2 // 2, sub_y), p["sub"], fill=(255, 255, 255, 220), font=font_sub)

# Convert to RGB for PNG save (LINE requires no alpha)
img_rgb = img.convert('RGB')
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "richmenu.png")
img_rgb.save(output_path, "PNG", quality=95)
print(f"Saved to {output_path} ({os.path.getsize(output_path) // 1024} KB)")
