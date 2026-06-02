"""Mathematical helper functions"""
import math
from typing import Union


def clamp(value: Union[int, float], min_val: Union[int, float], max_val: Union[int, float]) -> Union[int, float]:
    """Clamp value between min and max"""
    return max(min_val, min(max_val, value))


def lerp(start: float, end: float, t: float) -> float:
    """Linear interpolation"""
    return start + (end - start) * t


def normalize(value: float, min_val: float, max_val: float) -> float:
    """Normalize value to 0-1 range"""
    if max_val == min_val:
        return 0
    return (value - min_val) / (max_val - min_val)


def remap(value: float, in_min: float, in_max: float, out_min: float, out_max: float) -> float:
    """Remap value from one range to another"""
    normalized = normalize(value, in_min, in_max)
    return out_min + normalized * (out_max - out_min)


def smooth_step(t: float) -> float:
    """Smoothstep function (Hermite interpolation)"""
    t = clamp(t, 0, 1)
    return t * t * (3 - 2 * t)


def smooth_step_clamped(min_val: float, max_val: float, value: float) -> float:
    """Smoothstep between min and max values"""
    return smooth_step(normalize(value, min_val, max_val))
