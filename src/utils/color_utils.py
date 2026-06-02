"""Color manipulation utilities"""
from typing import Tuple
import colorsys

RGB = Tuple[int, int, int]


def hex_to_rgb(hex_color: str) -> RGB:
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb: RGB) -> str:
    """Convert RGB tuple to hex color"""
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))


def interpolate_color(color1: RGB, color2: RGB, t: float) -> RGB:
    """Linear interpolation between two RGB colors"""
    r = int(color1[0] + (color2[0] - color1[0]) * t)
    g = int(color1[1] + (color2[1] - color1[1]) * t)
    b = int(color1[2] + (color2[2] - color1[2]) * t)
    return (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))


def add_brightness(color: RGB, factor: float) -> RGB:
    """Adjust color brightness"""
    h, s, v = colorsys.rgb_to_hsv(color[0]/255, color[1]/255, color[2]/255)
    v = min(1.0, max(0, v * factor))
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return (int(r * 255), int(g * 255), int(b * 255))


def create_gradient(start_color: RGB, end_color: RGB, steps: int = 10) -> list:
    """Create a gradient of colors between two colors"""
    gradient = []
    for i in range(steps):
        t = i / (steps - 1) if steps > 1 else 0
        gradient.append(interpolate_color(start_color, end_color, t))
    return gradient
