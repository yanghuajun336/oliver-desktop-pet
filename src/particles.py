"""Particle system for Oliver visual effects."""
from dataclasses import dataclass, field
from enum import Enum
import math
import random
from typing import Dict, List, Optional, Tuple

from src.config import COLOR_PALETTE, PARTICLES


class ParticleType(Enum):
    """Supported particle types."""
    ORBIT_STAR = "orbit_star"
    BLINK_SPARKLE = "blink_sparkle"
    PULSE_WAVE = "pulse_wave"
    FLIGHT_TRAIL = "flight_trail"


@dataclass
class Particle:
    """Single particle unit."""
    kind: ParticleType
    x: float
    y: float
    size: float
    color: Tuple[int, int, int]
    alpha: float
    lifetime: float
    vx: float = 0.0
    vy: float = 0.0
    age: float = 0.0
    data: Dict[str, float] = field(default_factory=dict)
    text: str = ""

    def update(self, delta_time: float, activity_multiplier: float = 1.0):
        """Update particle behavior."""
        self.age += delta_time
        
        if self.kind == ParticleType.ORBIT_STAR:
            angle = self.data.get("angle", 0.0)
            speed = self.data.get("speed", 1.0) * activity_multiplier
            radius = self.data.get("radius", 40.0)
            angle += speed * delta_time
            self.data["angle"] = angle
            self.x = math.cos(angle) * radius
            self.y = math.sin(angle) * radius
            self.alpha = 0.45 + 0.15 * (1.0 + math.sin(angle * 2.0))
            return
        
        self.x += self.vx * delta_time
        self.y += self.vy * delta_time
        
        if self.lifetime > 0:
            life_progress = min(1.0, self.age / self.lifetime)
            self.alpha = max(0.0, 1.0 - life_progress)
        
        if self.kind == ParticleType.PULSE_WAVE:
            self.size = self.data.get("start_radius", 0.0) + self.data.get("radius_speed", 130.0) * self.age
        elif self.kind == ParticleType.FLIGHT_TRAIL:
            self.size = max(0.5, self.size * 0.98)

    def is_alive(self) -> bool:
        """Whether particle should still be rendered."""
        if self.kind == ParticleType.ORBIT_STAR:
            return True
        return self.age < self.lifetime and self.alpha > 0


class ParticleManager:
    """Manages all visual particles."""

    def __init__(self):
        self.particles: List[Particle] = []
        self._trail_spawn_accumulator = 0.0
        self._spawn_orbit_particles()

    def _spawn_orbit_particles(self):
        count = random.randint(3, 5)
        for i in range(count):
            angle = (2 * math.pi / count) * i
            self.particles.append(
                Particle(
                    kind=ParticleType.ORBIT_STAR,
                    x=math.cos(angle) * PARTICLES['ambient_star_radius'],
                    y=math.sin(angle) * PARTICLES['ambient_star_radius'],
                    size=PARTICLES['ambient_star_size'],
                    color=COLOR_PALETTE['amber_gold'],
                    alpha=0.6,
                    lifetime=-1.0,
                    data={
                        "angle": angle,
                        "radius": float(PARTICLES['ambient_star_radius']),
                        "speed": 1.2,
                    },
                )
            )

    def update(self, delta_time: float, activity_multiplier: float = 1.0):
        """Update all particles."""
        for particle in self.particles:
            particle.update(delta_time, activity_multiplier)
        self.particles = [p for p in self.particles if p.is_alive()]

    def spawn_blink_sparkles(self, x: float, y: float):
        """Spawn blink sparkles under eyes."""
        for _ in range(random.randint(3, 5)):
            self.particles.append(
                Particle(
                    kind=ParticleType.BLINK_SPARKLE,
                    x=x + random.uniform(-10, 10),
                    y=y + random.uniform(-2, 2),
                    size=random.uniform(1.0, 2.0),
                    color=COLOR_PALETTE['light_gold'],
                    alpha=1.0,
                    lifetime=0.5,
                    vx=random.uniform(-8, 8),
                    vy=random.uniform(18, 30),
                )
            )

    def spawn_pulse_wave(self):
        """Spawn a knowledge update pulse."""
        self.particles.append(
            Particle(
                kind=ParticleType.PULSE_WAVE,
                x=0.0,
                y=0.0,
                size=0.0,
                color=COLOR_PALETTE['starry_blue'],
                alpha=0.5,
                lifetime=0.6,
                data={
                    "start_radius": 0.0,
                    "radius_speed": 133.0,
                },
            )
        )

    def spawn_flight_trail(self, keywords: Optional[List[str]] = None):
        """Spawn flight stardust trail."""
        self._trail_spawn_accumulator += 1.0
        if self._trail_spawn_accumulator < 2.0:
            return
        self._trail_spawn_accumulator = 0.0
        
        text = ""
        if keywords:
            text = random.choice(keywords[-3:])
        
        self.particles.append(
            Particle(
                kind=ParticleType.FLIGHT_TRAIL,
                x=random.uniform(-35, -20),
                y=random.uniform(-8, 8),
                size=random.uniform(3.0, 5.0),
                color=COLOR_PALETTE['light_gold'],
                alpha=0.8,
                lifetime=0.7,
                vx=random.uniform(-16, -8),
                vy=random.uniform(-2, 2),
                text=text,
            )
        )

    def get_particles(self, kind: Optional[ParticleType] = None) -> List[Particle]:
        """Get particles by type or return all."""
        if kind is None:
            return self.particles
        return [p for p in self.particles if p.kind == kind]
