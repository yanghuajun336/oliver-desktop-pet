"""Rendering engine for character drawing"""
from PyQt5.QtGui import (
    QPainter,
    QColor,
    QBrush,
    QPen,
    QLinearGradient,
    QRadialGradient,
    QPainterPath,
    QPolygonF,
)
from PyQt5.QtCore import Qt, QRectF, QPointF
from src.config import COLOR_PALETTE, CHARACTER
from src.character import Character
from src.particles import ParticleType
import math


class Renderer:
    """Handles all drawing operations"""
    
    def __init__(self, widget):
        self.widget = widget
        self.palette = COLOR_PALETTE
    
    def render(self, painter: QPainter, character: Character):
        """Main render function"""
        # Calculate scaling factor based on character screen height
        scale = CHARACTER['screen_height_px'] / 100  # Base unit
        
        # Translate to character position
        painter.save()
        painter.translate(character.position.x, character.position.y)
        painter.scale(character.scale, character.scale)
        painter.rotate(character.forward_tilt)
        
        # Draw character layers (back to front), matching designed render order
        self.draw_particles_background(painter, character, scale)
        self.draw_wings(painter, character, scale, side="left", expanded=False)
        self.draw_body(painter, character, scale)
        self.draw_wings(painter, character, scale, side="right", expanded=False)
        self.draw_belly(painter, character, scale)
        self.draw_wings(painter, character, scale, side="left", expanded=True)
        self.draw_head(painter, character, scale)
        self.draw_cheeks(painter, character, scale)
        self.draw_eyes(painter, character, scale)
        self.draw_eyebrows(painter, character, scale)
        self.draw_beak(painter, character, scale)
        self.draw_horns(painter, character, scale)
        self.draw_accessories(painter, character, scale)
        self.draw_effects(painter, character, scale)
        painter.restore()
    
    def draw_particles_background(self, painter: QPainter, character: Character, scale: float):
        """Draw background particle effects"""
        for particle in character.particle_manager.get_particles(ParticleType.ORBIT_STAR):
            painter.save()
            color = QColor(*particle.color)
            color.setAlphaF(max(0.0, min(1.0, particle.alpha * 0.6)))
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(color))
            s = particle.size * scale
            painter.drawEllipse(QRectF(particle.x * scale - s / 2, particle.y * scale - s / 2, s, s))
            painter.restore()
    
    def draw_body(self, painter: QPainter, character: Character, scale: float):
        """Draw character body"""
        body_width = 60 * scale
        body_height = 80 * scale
        body_top = (0 + character.body_y_offset) * scale
        
        painter.setBrush(QBrush(QColor(*self.palette['starry_blue'])))
        painter.setPen(QPen(QColor(*self.palette['light_gold']), max(1.0, scale * 0.5)))
        painter.drawEllipse(QRectF(-body_width / 2, body_top, body_width, body_height))
    
    def draw_belly(self, painter: QPainter, character: Character, scale: float):
        """Draw body lower belly."""
        belly_width = 60 * scale
        belly_height = 50 * scale
        belly_top = (25 + character.body_y_offset) * scale
        painter.setBrush(QBrush(QColor(*self.palette['ivory_white'])))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QRectF(-belly_width / 2, belly_top, belly_width, belly_height))
    
    def draw_head(self, painter: QPainter, character: Character, scale: float):
        """Draw character head"""
        head_radius = 35 * scale
        head_y = (-60 + character.body_y_offset) * scale
        painter.save()
        painter.translate(0, head_y)
        painter.rotate(character.head_tilt)
        brush = QBrush(QColor(*self.palette['starry_blue']))
        painter.setBrush(brush)
        painter.setPen(QPen(QColor(*self.palette['light_gold']), max(1.0, scale * 0.4)))
        painter.drawEllipse(QRectF(-head_radius, -head_radius, head_radius * 2, head_radius * 2))
        painter.restore()
    
    def draw_cheeks(self, painter: QPainter, character: Character, scale: float):
        """Draw fluffy cheeks."""
        painter.save()
        self._prepare_head_space(painter, character, scale)
        painter.setBrush(QColor(*self.palette['apricot_pink']))
        painter.setPen(Qt.NoPen)
        cheek_w = 16 * scale
        cheek_h = 12 * scale
        painter.drawEllipse(QRectF(-30 * scale - cheek_w / 2, -4 * scale - cheek_h / 2, cheek_w, cheek_h))
        painter.drawEllipse(QRectF(30 * scale - cheek_w / 2, -4 * scale - cheek_h / 2, cheek_w, cheek_h))
        painter.restore()
    
    def draw_eyes(self, painter: QPainter, character: Character, scale: float):
        """Draw character eyes"""
        painter.save()
        self._prepare_head_space(painter, character, scale)
        
        eye_d = 28 * scale
        iris_d = 16 * scale
        pupil_d = 10 * scale
        left_eye = QPointF(-14 * scale, -4 * scale)
        right_eye = QPointF(14 * scale, -4 * scale)
        eye_openness = character.eye_openness
        
        for center in (left_eye, right_eye):
            # silver feather eyeliner
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QPen(QColor(*self.palette['silver_white']), max(2.0, scale)))
            painter.drawEllipse(QRectF(center.x() - eye_d / 2 - scale, center.y() - eye_d / 2 - scale, eye_d + 2 * scale, eye_d + 2 * scale))
            
            # eye white with blink squash
            eye_h = max(2.0, eye_d * eye_openness)
            painter.setBrush(QColor(*self.palette['ivory_white']))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QRectF(center.x() - eye_d / 2, center.y() - eye_h / 2, eye_d, eye_h))
            
            if eye_openness > 0.2:
                iris_h = iris_d * max(0.4, eye_openness)
                painter.setBrush(QColor(*self.palette['amber_gold']))
                painter.drawEllipse(QRectF(center.x() - iris_d / 2, center.y() - iris_h / 2, iris_d, iris_h))
                
                if character.star_pupil_mode:
                    self._draw_star_shape(
                        painter,
                        center,
                        outer_radius=pupil_d * 0.5,
                        inner_radius=pupil_d * 0.22,
                        points=5,
                        fill_color=QColor(0, 0, 0),
                        rotation=character.pupil_star_rotation,
                    )
                else:
                    painter.setBrush(QColor(0, 0, 0))
                    painter.drawEllipse(QRectF(center.x() - pupil_d / 2, center.y() - pupil_d / 2, pupil_d, pupil_d))
                    self._draw_six_point_star(painter, center, radius=3 * scale, line_width=max(1.5, scale))
            else:
                painter.setPen(QPen(QColor(*self.palette['dark_indigo']), max(2.0, scale), Qt.SolidLine, Qt.RoundCap))
                painter.drawLine(QPointF(center.x() - eye_d / 2, center.y()), QPointF(center.x() + eye_d / 2, center.y()))
            
            # lower eyelid smile arc
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QPen(QColor(*self.palette['dark_indigo']), max(1.0, scale * 0.6)))
            arc_rect = QRectF(center.x() - eye_d / 2, center.y() - eye_d / 4, eye_d, eye_d)
            painter.drawArc(arc_rect, 210 * 16, 120 * 16)
        
        painter.restore()
    
    def draw_beak(self, painter: QPainter, character: Character, scale: float):
        """Draw character beak"""
        painter.save()
        self._prepare_head_space(painter, character, scale)
        painter.translate(0, 12 * scale)
        painter.rotate(-3.0)
        
        beak_w = 10 * scale
        beak_h = max(8 * scale, character.beak_open_height * scale)
        points = QPolygonF([
            QPointF(-beak_w / 2, 0),
            QPointF(beak_w / 2, 0),
            QPointF(0, beak_h),
        ])
        painter.setBrush(QColor(*self.palette['tangerine']))
        painter.setPen(Qt.NoPen)
        painter.drawPolygon(points)
        
        # tip highlight
        painter.setBrush(QColor(*self.palette['light_gold']))
        painter.drawEllipse(QRectF(-0.5 * scale, beak_h - 1.5 * scale, 1.5 * scale, 1.5 * scale))
        
        if character.facial_expression == "yawning":
            painter.setBrush(QColor(*self.palette['soft_pink']))
            painter.drawEllipse(QRectF(-2.0 * scale, beak_h - 4.0 * scale, 4.0 * scale, 2.0 * scale))
        painter.restore()
    
    def draw_wings(self, painter: QPainter, character: Character, scale: float, side: str, expanded: bool):
        """Draw character wings"""
        spread = max(0.0, min(90.0, character.wing_spread_angle))
        wing_w = 40 * scale
        wing_h = 70 * scale
        root_x = (-30 if side == "left" else 30) * scale
        root_y = (34 + character.body_y_offset) * scale
        direction = -1 if side == "left" else 1
        
        if expanded and spread <= 1.0:
            return
        
        painter.save()
        painter.translate(root_x, root_y)
        base_angle = direction * (18 if not expanded else spread * 0.5) + character.wing_flap_offset * direction
        painter.rotate(base_angle)
        
        path = QPainterPath()
        path.moveTo(0, 0)
        path.lineTo(direction * wing_w * 0.4, -wing_h * 0.25)
        path.lineTo(direction * wing_w, wing_h * 0.25)
        path.lineTo(direction * wing_w * 0.2, wing_h * 0.6)
        path.closeSubpath()
        
        if expanded:
            gradient = QLinearGradient(0, 0, direction * wing_w, wing_h * 0.6)
            gradient.setColorAt(0.0, QColor(*self.palette['starry_blue']))
            gradient.setColorAt(0.55, QColor(*self.palette['purple_gradient']))
            gradient.setColorAt(1.0, QColor(*self.palette['pink_gradient']))
            painter.setBrush(QBrush(gradient))
        else:
            painter.setBrush(QColor(*self.palette['starry_blue']))
        
        painter.setPen(QPen(QColor(*self.palette['light_gold']), max(1.0, scale * 0.5)))
        painter.drawPath(path)
        painter.restore()
    
    def draw_eyebrows(self, painter: QPainter, character: Character, scale: float):
        """Draw expressive eyebrow feathers."""
        painter.save()
        self._prepare_head_space(painter, character, scale)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(*self.palette['dark_indigo']), max(1.5, scale * 0.8), Qt.SolidLine, Qt.RoundCap))
        
        left_base_x = -14 * scale
        right_base_x = 14 * scale
        y = -20 * scale
        if character.facial_expression == "curious":
            left_offset, right_offset = -2 * scale, 2 * scale
        elif character.facial_expression == "thinking":
            left_base_x += 5 * scale
            right_base_x -= 5 * scale
            left_offset = right_offset = 0
        elif character.facial_expression == "confused":
            left_offset = right_offset = 3 * scale
        else:
            left_offset = right_offset = 0
        
        for i in range(3):
            dx = i * 2 * scale
            painter.drawLine(QPointF(left_base_x - dx, y + left_offset), QPointF(left_base_x - dx - 5 * scale, y - 4 * scale + left_offset))
            painter.drawLine(QPointF(right_base_x + dx, y + right_offset), QPointF(right_base_x + dx + 5 * scale, y - 4 * scale + right_offset))
        painter.restore()
    
    def draw_horns(self, painter: QPainter, character: Character, scale: float):
        """Draw animated horn feathers."""
        painter.save()
        self._prepare_head_space(painter, character, scale)
        spacing = 4 * scale
        length = 50 * scale
        base_y = -30 * scale
        
        for side in ("left", "right"):
            direction = -1 if side == "left" else 1
            base_x = direction * 14 * scale
            for i in range(6):
                start = QPointF(base_x + direction * i * spacing, base_y)
                angle_base = -75 if side == "left" else -105
                angle = angle_base + direction * i * 5
                if character.facial_expression == "thinking":
                    angle += character.horn_shake_progress * (1 if i % 2 == 0 else -1)
                elif character.facial_expression == "confused":
                    angle += 25
                elif character.facial_expression == "surprised":
                    angle = -90 + direction * (i - 2) * 3
                else:
                    angle += 3
                
                rad = math.radians(angle)
                end = QPointF(start.x() + math.cos(rad) * length, start.y() + math.sin(rad) * length)
                gradient = QLinearGradient(start, end)
                gradient.setColorAt(0.0, QColor(*self.palette['starry_blue']))
                gradient.setColorAt(1.0, QColor(*self.palette['light_gold']))
                painter.setPen(QPen(QBrush(gradient), max(1.5, scale * 0.8), Qt.SolidLine, Qt.RoundCap))
                if character.facial_expression == "confused":
                    ctrl = QPointF((start.x() + end.x()) / 2, (start.y() + end.y()) / 2 + 10 * scale)
                    path = QPainterPath(start)
                    path.quadTo(ctrl, end)
                    painter.drawPath(path)
                else:
                    painter.drawLine(start, end)
        painter.restore()
    
    def draw_accessories(self, painter: QPainter, character: Character, scale: float):
        """Draw character accessories (hat, glasses, scarf, etc.)"""
        self._draw_hat(painter, character, scale)
        self._draw_monocle(painter, character, scale)
        self._draw_scarf(painter, character, scale)
        self._draw_badge(painter, character, scale)
        self._draw_shoes(painter, character, scale)
    
    def draw_effects(self, painter: QPainter, character: Character, scale: float):
        """Draw visual effects (glow, particles, etc.)"""
        for particle in character.particle_manager.get_particles():
            if particle.kind == ParticleType.ORBIT_STAR:
                continue
            
            painter.save()
            color = QColor(*particle.color)
            color.setAlphaF(max(0.0, min(1.0, particle.alpha)))
            if particle.kind == ParticleType.PULSE_WAVE:
                painter.setBrush(Qt.NoBrush)
                painter.setPen(QPen(color, max(1.0, scale)))
                radius = particle.size * scale
                painter.drawEllipse(QRectF(-radius, -radius, radius * 2, radius * 2))
            else:
                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(color))
                s = particle.size * scale
                painter.drawEllipse(QRectF(particle.x * scale - s / 2, particle.y * scale - s / 2, s, s))
                if particle.kind == ParticleType.FLIGHT_TRAIL and particle.text:
                    painter.setPen(QPen(color, max(1.0, scale * 0.4)))
                    painter.drawText(QPointF((particle.x - 8) * scale, (particle.y - 4) * scale), particle.text)
            painter.restore()
    
    def _prepare_head_space(self, painter: QPainter, character: Character, scale: float):
        head_y = (-60 + character.body_y_offset) * scale
        painter.translate(0, head_y)
        painter.rotate(character.head_tilt)
    
    def _draw_six_point_star(self, painter: QPainter, center: QPointF, radius: float, line_width: float):
        painter.setPen(QPen(QColor(255, 255, 255), line_width))
        for offset in (0.0, 60.0, -60.0):
            r = math.radians(offset)
            dx = math.cos(r) * radius
            dy = math.sin(r) * radius
            painter.drawLine(QPointF(center.x() - dx, center.y() - dy), QPointF(center.x() + dx, center.y() + dy))
    
    def _draw_star_shape(
        self,
        painter: QPainter,
        center: QPointF,
        outer_radius: float,
        inner_radius: float,
        points: int,
        fill_color: QColor,
        rotation: float = 0.0,
    ):
        star = QPolygonF()
        for i in range(points * 2):
            angle = math.radians(rotation + i * 180.0 / points - 90.0)
            radius = outer_radius if i % 2 == 0 else inner_radius
            star.append(QPointF(center.x() + math.cos(angle) * radius, center.y() + math.sin(angle) * radius))
        painter.setPen(Qt.NoPen)
        painter.setBrush(fill_color)
        painter.drawPolygon(star)
    
    def _draw_hat(self, painter: QPainter, character: Character, scale: float):
        painter.save()
        self._prepare_head_space(painter, character, scale)
        painter.translate(0, -38 * scale)
        painter.rotate(-5)
        
        brown = QColor(101, 67, 33)
        painter.setBrush(brown)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QRectF(-22.5 * scale, -10 * scale, 45 * scale, 20 * scale))
        painter.setPen(QPen(brown, max(2.0, scale)))
        painter.drawArc(QRectF(-25 * scale, -2 * scale, 50 * scale, 10 * scale), 200 * 16, 140 * 16)
        
        tassel_start = QPointF(0, 0)
        tassel_end = QPointF(0, 50 * scale)
        painter.setPen(QPen(QColor(*self.palette['light_gold']), max(1.0, scale * 0.5)))
        painter.drawLine(tassel_start, tassel_end)
        painter.setBrush(QColor(200, 20, 40))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QRectF(tassel_end.x() - 1.5 * scale, tassel_end.y() - 1.5 * scale, 3 * scale, 3 * scale))
        
        glow = QRadialGradient(tassel_end, 6 * scale)
        glow.setColorAt(0.0, QColor(255, 80, 80, 180))
        glow.setColorAt(1.0, QColor(255, 80, 80, 0))
        painter.setBrush(QBrush(glow))
        painter.drawEllipse(QRectF(tassel_end.x() - 6 * scale, tassel_end.y() - 6 * scale, 12 * scale, 12 * scale))
        painter.restore()
    
    def _draw_monocle(self, painter: QPainter, character: Character, scale: float):
        painter.save()
        self._prepare_head_space(painter, character, scale)
        painter.translate(16 * scale, -4 * scale + character.monocle_offset_y * scale)
        painter.rotate(-15)
        
        copper = QColor(184, 115, 51)
        lens = QColor(135, 206, 235, 128)
        diameter = 26 * scale
        painter.setBrush(lens)
        painter.setPen(QPen(copper, max(2.0, scale * 1.5)))
        painter.drawEllipse(QRectF(-diameter / 2, -diameter / 2, diameter, diameter))
        
        painter.setPen(QPen(copper, max(1.0, scale * 0.5)))
        for i in range(5):
            x = -8 * scale + i * 4 * scale
            painter.drawLine(QPointF(x, -10 * scale), QPointF(x + 1.5 * scale, -8.5 * scale))
        painter.drawLine(QPointF(diameter / 2, 0), QPointF(24 * scale, 8 * scale))
        painter.restore()
    
    def _draw_scarf(self, painter: QPainter, character: Character, scale: float):
        painter.save()
        scarf = QColor(47, 79, 127)
        silver = QColor(*self.palette['silver_white'])
        y = (-20 + character.body_y_offset) * scale
        painter.setBrush(scarf)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(QRectF(-22 * scale, y, 44 * scale, 12 * scale), 5 * scale, 5 * scale)
        painter.drawRoundedRect(QRectF(10 * scale, (2 + character.body_y_offset) * scale, 12 * scale, 26 * scale), 3 * scale, 3 * scale)
        
        # tree symbol
        painter.setPen(QPen(silver, max(1.0, scale * 0.5)))
        trunk_x = 16 * scale
        trunk_y = (8 + character.body_y_offset) * scale
        painter.drawLine(QPointF(trunk_x, trunk_y), QPointF(trunk_x, trunk_y + 8 * scale))
        painter.drawLine(QPointF(trunk_x, trunk_y + 2 * scale), QPointF(trunk_x - 3 * scale, trunk_y + 5 * scale))
        painter.drawLine(QPointF(trunk_x, trunk_y + 2 * scale), QPointF(trunk_x + 3 * scale, trunk_y + 5 * scale))
        for i, ch in enumerate(["★", "☆", "◆", "○", "▲"]):
            painter.drawText(QPointF((12 + i * 2) * scale, (22 + character.body_y_offset) * scale), ch)
        painter.restore()
    
    def _draw_badge(self, painter: QPainter, character: Character, scale: float):
        painter.save()
        center = QPointF(-30 * scale, (30 + character.body_y_offset) * scale)
        painter.setBrush(QColor(205, 127, 50))
        painter.setPen(QPen(QColor(*self.palette['light_gold']), max(1.0, scale * 0.5)))
        painter.drawEllipse(QRectF(center.x() - 10 * scale, center.y() - 10 * scale, 20 * scale, 20 * scale))
        
        painter.setPen(QPen(QColor(*self.palette['dark_indigo']), max(1.0, scale * 0.5)))
        painter.drawLine(QPointF(center.x() - 5 * scale, center.y()), QPointF(center.x() + 5 * scale, center.y()))
        painter.drawLine(QPointF(center.x(), center.y() - 4 * scale), QPointF(center.x(), center.y() + 4 * scale))
        feather = QPainterPath(QPointF(center.x() + 3 * scale, center.y() - 3 * scale))
        feather.quadTo(QPointF(center.x() + 9 * scale, center.y()), QPointF(center.x() + 3 * scale, center.y() + 5 * scale))
        painter.drawPath(feather)
        painter.restore()
    
    def _draw_shoes(self, painter: QPainter, character: Character, scale: float):
        painter.save()
        shoe_color = QColor(62, 39, 35)
        lace_color = QColor(*self.palette['light_gold'])
        y = (80 + character.body_y_offset) * scale
        for x in (-12, 12):
            painter.setBrush(shoe_color)
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(QRectF((x - 10) * scale, y, 20 * scale, 8 * scale), 3 * scale, 3 * scale)
            painter.setPen(QPen(lace_color, max(1.0, scale * 0.4)))
            painter.drawLine(QPointF((x - 4) * scale, (y + 2 * scale)), QPointF((x + 4) * scale, (y + 6 * scale)))
            painter.drawLine(QPointF((x + 4) * scale, (y + 2 * scale)), QPointF((x - 4) * scale, (y + 6 * scale)))
            for idx in range(3):
                sy = y + (6 + idx) * scale
                painter.drawLine(QPointF((x - 8) * scale, sy), QPointF((x + 8) * scale, sy))
        painter.restore()
