#!/usr/bin/env python3
"""
Create a minimalist Silicon Valley style icon for PPT Compressor
Inspired by OpenAI's clean design aesthetic
"""

from PIL import Image, ImageDraw, ImageFont
import math

def create_icon():
    # Icon size for macOS (1024x1024 for best quality)
    size = 1024

    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Modern color palette - gradient from blue to purple (like OpenAI)
    bg_color = (16, 16, 28)  # Dark background
    accent_color_1 = (99, 102, 241)  # Indigo
    accent_color_2 = (139, 92, 246)  # Purple

    # Draw rounded square background with gradient effect
    corner_radius = 180

    # Create gradient background
    for i in range(size):
        t = i / size
        r = int(accent_color_1[0] + (accent_color_2[0] - accent_color_1[0]) * t)
        g = int(accent_color_1[1] + (accent_color_2[1] - accent_color_1[1]) * t)
        b = int(accent_color_1[2] + (accent_color_2[2] - accent_color_1[2]) * t)
        draw.line([(0, i), (size, i)], fill=(r, g, b, 255))

    # Create a mask for rounded corners
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle(
        [(0, 0), (size, size)],
        radius=corner_radius,
        fill=255
    )

    # Apply mask to create rounded corners
    output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    output.paste(img, (0, 0), mask)

    # Draw the minimalist compression icon
    draw = ImageDraw.Draw(output)

    # Center position
    center_x, center_y = size // 2, size // 2

    # Draw two overlapping rectangles to represent document compression
    # Left rectangle (original document)
    left_rect_width = 220
    left_rect_height = 320
    left_x = center_x - 180
    left_y = center_y - left_rect_height // 2

    # Draw left document with shadow effect
    shadow_offset = 8
    draw.rounded_rectangle(
        [(left_x + shadow_offset, left_y + shadow_offset),
         (left_x + left_rect_width + shadow_offset, left_y + left_rect_height + shadow_offset)],
        radius=20,
        fill=(0, 0, 0, 60)
    )
    draw.rounded_rectangle(
        [(left_x, left_y), (left_x + left_rect_width, left_y + left_rect_height)],
        radius=20,
        fill=(255, 255, 255, 255),
        outline=(255, 255, 255, 100),
        width=3
    )

    # Draw lines inside left document
    line_y_start = left_y + 60
    for i in range(5):
        y = line_y_start + i * 45
        draw.rounded_rectangle(
            [(left_x + 30, y), (left_x + left_rect_width - 30, y + 15)],
            radius=7,
            fill=(200, 200, 255, 180)
        )

    # Arrow pointing right (compression arrow)
    arrow_x = center_x + 10
    arrow_y = center_y
    arrow_width = 120
    arrow_head_width = 40

    # Arrow shaft
    draw.rounded_rectangle(
        [(arrow_x - arrow_width // 2, arrow_y - 15),
         (arrow_x + arrow_width // 2, arrow_y + 15)],
        radius=8,
        fill=(255, 255, 255, 255)
    )

    # Arrow head (triangle)
    arrow_head = [
        (arrow_x + arrow_width // 2, arrow_y),
        (arrow_x + arrow_width // 2 - arrow_head_width, arrow_y - arrow_head_width),
        (arrow_x + arrow_width // 2 - arrow_head_width, arrow_y + arrow_head_width)
    ]
    draw.polygon(arrow_head, fill=(255, 255, 255, 255))

    # Right rectangle (compressed document - smaller)
    right_rect_width = 160
    right_rect_height = 240
    right_x = center_x + 180
    right_y = center_y - right_rect_height // 2

    # Draw right document with shadow
    draw.rounded_rectangle(
        [(right_x + shadow_offset, right_y + shadow_offset),
         (right_x + right_rect_width + shadow_offset, right_y + right_rect_height + shadow_offset)],
        radius=20,
        fill=(0, 0, 0, 60)
    )
    draw.rounded_rectangle(
        [(right_x, right_y), (right_x + right_rect_width, right_y + right_rect_height)],
        radius=20,
        fill=(255, 255, 255, 255),
        outline=(255, 255, 255, 100),
        width=3
    )

    # Draw lines inside right document (fewer and smaller)
    line_y_start = right_y + 50
    for i in range(3):
        y = line_y_start + i * 50
        draw.rounded_rectangle(
            [(right_x + 25, y), (right_x + right_rect_width - 25, y + 12)],
            radius=6,
            fill=(200, 255, 200, 180)
        )

    # Draw a subtle "ZIP" indicator on compressed document
    draw.ellipse(
        [(right_x + right_rect_width - 55, right_y + 15),
         (right_x + right_rect_width - 15, right_y + 55)],
        fill=(100, 255, 150, 255)
    )

    # Save the icon in multiple sizes
    output.save('/Users/whitney/Downloads/PPT-compressor/icon_1024.png', 'PNG')
    print("✓ Created icon_1024.png (1024x1024)")

    # Create standard macOS icon sizes
    sizes = [512, 256, 128, 64, 32, 16]
    for s in sizes:
        resized = output.resize((s, s), Image.Resampling.LANCZOS)
        resized.save(f'/Users/whitney/Downloads/PPT-compressor/icon_{s}.png', 'PNG')
        print(f"✓ Created icon_{s}.png ({s}x{s})")

    print("\n✓ All icons created successfully!")
    print("Main icon: icon_1024.png")

if __name__ == '__main__':
    create_icon()
