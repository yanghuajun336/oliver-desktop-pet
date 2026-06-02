"""Idle visual effects for Oliver."""
from dataclasses import dataclass
import math
import random
from typing import List

from src.config import COLOR_PALETTE


@dataclass
class AmbientParticle:
    """Small orbiting star."""
    angle: float
    radius: float
    speed: float
    size: float
    phase: float
    x: float = 0.0
    y: float = 0.0
    alpha: float = 0.0

    def update(self, delta_time: float):
        self.angle += self.speed * delta_time
        self.x = math.cos(self.angle) * self.radius
        self.y = math.sin(self.angle) * self.radius * 0.75 - 26.0
        self.alpha = 0.45 + 0.35 * (0.5 + 0.5 * math.sin(self.angle * 2.0 + self.phase))


@dataclass
class PulseWave:
    """Soft glow ring."""
    radius: float = 22.0
    lifetime: float = 1.8
    age: float = 0.0
    alpha: float = 0.0

    def update(self, delta_time: float):
        self.age += delta_time
        progress = min(1.0, self.age / self.lifetime)
        self.radius = 22.0 + progress * 38.0
        self.alpha = max(0.0, 0.25 * (1.0 - progress))

    @property
    def alive(self) -> bool:
        return self.age < self.lifetime and self.alpha > 0.0


@dataclass
class StarDust:
    """Twinkling dust particle."""
    x: float
    y: float
    vx: float
    vy: float
    size: float
    lifetime: float
    age: float = 0.0
    alpha: float = 1.0

    def update(self, delta_time: float):
        self.age += delta_time
        self.x += self.vx * delta_time
        self.y += self.vy * delta_time
        progress = min(1.0, self.age / self.lifetime)
        self.alpha = max(0.0, 1.0 - progress)

    @property
    def alive(self) -> bool:
        return self.age < self.lifetime and self.alpha > 0.0


class ParticleSystem:
    """Idle particle controller."""

    def __init__(self):
        count = random.randint(3, 5)
        self.ambient_particles: List[AmbientParticle] = [
            AmbientParticle(
                angle=(2.0 * math.pi / count) * index,
                radius=random.uniform(54.0, 68.0),
                speed=random.uniform(0.55, 0.9),
                size=random.uniform(4.0, 7.0),
                phase=random.uniform(0.0, math.pi),
            )
            for index in range(count)
        ]
        self.pulse_waves: List[PulseWave] = [PulseWave()]
        self.star_dust: List[StarDust] = []
        self._pulse_timer = 0.0
        self._dust_timer = 0.0

    def update(self, delta_time: float, character):
        """Update all idle visual effects."""
        for particle in self.ambient_particles:
            particle.update(delta_time)

        self._pulse_timer += delta_time
        if self._pulse_timer >= 2.6:
            self._pulse_timer = 0.0
            self.pulse_waves.append(PulseWave())

        for pulse in self.pulse_waves:
            pulse.update(delta_time)
        self.pulse_waves = [pulse for pulse in self.pulse_waves if pulse.alive]

        self._dust_timer += delta_time
        if self._dust_timer >= 0.6:
            self._dust_timer = 0.0
            anchor_y = -20.0 + character.body_y_offset
            self.star_dust.append(
                StarDust(
                    x=random.uniform(-18.0, 18.0),
                    y=anchor_y + random.uniform(-10.0, 6.0),
                    vx=random.uniform(-8.0, 8.0),
                    vy=random.uniform(-12.0, -4.0),
                    size=random.uniform(1.5, 3.5),
                    lifetime=random.uniform(0.8, 1.3),
                )
            )

        for dust in self.star_dust:
            dust.update(delta_time)
        self.star_dust = [dust for dust in self.star_dust if dust.alive]

    @property
    def ambient_color(self):
        return COLOR_PALETTE["amber_gold"]
