import os
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtWidgets import QApplication, QWidget

from src.character import Character
from src.config import SPRITES_DIR
from src.renderer import Renderer


class IdleVisualTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_character_exposes_idle_visual_attributes(self):
        character = Character()
        character.update(1.0 / 60.0)

        self.assertEqual(character.facial_expression, "idle")
        self.assertIn("hat", character.accessory_visibility)
        self.assertGreater(character.breathing_amplitude, 0.0)
        self.assertGreaterEqual(character.ambient_glow_intensity, 0.0)

        head_transform = character.get_component_transform("head")
        self.assertEqual(set(head_transform.keys()), {"position", "rotation", "scale", "opacity"})
        self.assertAlmostEqual(head_transform["rotation"], 15.0)

    def test_renderer_loads_svg_and_renders_idle_frame(self):
        renderer = Renderer(QWidget())
        body = renderer.load_svg(SPRITES_DIR / "oliver_body.svg")
        self.assertFalse(body.isNull())

        image = QImage(320, 320, QImage.Format_ARGB32_Premultiplied)
        image.fill(0)
        painter = QPainter(image)
        character = Character()
        character.position = type("PointLike", (), {"x": 160, "y": 150})()
        renderer.draw_oliver_idle(painter, character, 2.0)
        painter.end()

        non_empty_pixels = 0
        for x in range(0, image.width(), 16):
            for y in range(0, image.height(), 16):
                if image.pixelColor(x, y).alpha() > 0:
                    non_empty_pixels += 1
        self.assertGreater(non_empty_pixels, 10)


if __name__ == "__main__":
    unittest.main()
