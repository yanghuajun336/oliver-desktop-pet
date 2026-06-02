"""Geometric calculations and transformations"""
import math
from dataclasses import dataclass
from typing import Tuple

@dataclass
class Point:
    """2D point"""
    x: float
    y: float
    
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Point(self.x * scalar, self.y * scalar)
    
    def distance_to(self, other) -> float:
        """Calculate distance to another point"""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    
    def to_tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)


def rotate_point(point: Point, center: Point, angle: float) -> Point:
    """Rotate a point around a center by angle (in degrees)"""
    angle_rad = math.radians(angle)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    
    px = point.x - center.x
    py = point.y - center.y
    
    new_x = px * cos_a - py * sin_a + center.x
    new_y = px * sin_a + py * cos_a + center.y
    
    return Point(new_x, new_y)


def interpolate_points(p1: Point, p2: Point, t: float) -> Point:
    """Linear interpolation between two points"""
    return Point(
        p1.x + (p2.x - p1.x) * t,
        p1.y + (p2.y - p1.y) * t
    )


def bezier_curve(p0: Point, p1: Point, p2: Point, p3: Point, t: float) -> Point:
    """Cubic Bezier curve interpolation"""
    mt = 1 - t
    mt3 = mt * mt * mt
    t3 = t * t * t
    
    x = mt3 * p0.x + 3 * mt * mt * t * p1.x + 3 * mt * t * t * p2.x + t3 * p3.x
    y = mt3 * p0.y + 3 * mt * mt * t * p1.y + 3 * mt * t * t * p2.y + t3 * p3.y
    
    return Point(x, y)


def get_angle(from_point: Point, to_point: Point) -> float:
    """Get angle from one point to another (in degrees)"""
    dx = to_point.x - from_point.x
    dy = to_point.y - from_point.y
    return math.degrees(math.atan2(dy, dx))
