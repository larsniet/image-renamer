#!/usr/bin/env python3
"""
Script to generate an icon for the Image Renamer application.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size=256, bg_color=(13, 99, 156), fg_color=(255, 255, 255)):
    """Create a simple icon for the application."""
    img = Image.new('RGB', (size, size), color=bg_color)
    d = ImageDraw.Draw(img)
    
    # Draw a simple camera shape
    padding = size // 5
    body_width = size - (2 * padding)
    body_height = body_width * 2 // 3
    
    # Camera body
    d.rectangle(
        [(padding, padding + size//10), 
         (padding + body_width, padding + size//10 + body_height)],
        fill=fg_color
    )
    
    # Camera lens
    lens_center = (size // 2, padding + size//10 + body_height // 2)
    lens_radius = body_height // 3
    d.ellipse(
        [(lens_center[0] - lens_radius, lens_center[1] - lens_radius),
         (lens_center[0] + lens_radius, lens_center[1] + lens_radius)],
        fill=bg_color
    )
    
    # Flash
    flash_width = body_width // 4
    d.rectangle(
        [(padding + body_width - flash_width, padding),
         (padding + body_width, padding + size//10)],
        fill=fg_color
    )
    
    # Add calendar icon to represent date
    calendar_width = body_width // 2
    calendar_height = calendar_width * 3 // 4
    calendar_x = padding + (body_width - calendar_width) // 2
    calendar_y = padding + size//10 + body_height + padding // 2
    
    # Calendar base
    d.rectangle(
        [(calendar_x, calendar_y),
         (calendar_x + calendar_width, calendar_y + calendar_height)],
        fill=fg_color
    )
    
    # Calendar lines
    line_spacing = calendar_height // 4
    for i in range(1, 4):
        y = calendar_y + (i * line_spacing)
        d.line(
            [(calendar_x, y), (calendar_x + calendar_width, y)],
            fill=bg_color, width=2
        )
    
    # Save as PNG and ICO
    img.save('resources/icon.png')
    
    # Convert to ICO format for Windows
    img_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img.save('resources/icon.ico', sizes=img_sizes)
    
    print(f"Icons created at: resources/icon.png and resources/icon.ico")

if __name__ == "__main__":
    create_icon() 