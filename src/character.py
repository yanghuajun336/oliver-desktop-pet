"""Character class and state management"""
from enum import Enum
from typing import Optional
from src.config import CHARACTER, ANIMATION
from src.utils.geometry import Point
from src.utils.time_utils import is_daytime


class CharacterState(Enum):
    """Character states"""
    IDLE = "idle"                          # 待机
    THINKING = "thinking"                  # 思考
    SURPRISED = "surprised"                # 惊喜
    CONFUSED = "confused"                  # 困惑
    WALKING = "walking"                    # 行走/闲逛
    YAWNING = "yawning"                    # 打哈欠
    FLYING = "flying"                      # 飞行


class Character:
    """Oliver character"""
    
    def __init__(self):
        self.state = CharacterState.IDLE
        self.position = Point(100, 100)
        self.scale = 1.0
        self.rotation = 0.0
        self.head_tilt = 0.0
        self.wing_spread = 0.0
        self.eye_blink_progress = 0.0
        self.breathing_progress = 0.0
        self.horn_shake_progress = 0.0
        self.animation_time = 0.0
        self.state_time = 0.0
        self.is_daytime = is_daytime()
        self.last_activity_time = 0.0
        
    def update(self, delta_time: float):
        """Update character state and animations"""
        self.animation_time += delta_time
        self.state_time += delta_time
        self.last_activity_time += delta_time
        
        # Update eye blinking
        self.update_blink(delta_time)
        
        # Update breathing
        self.update_breathing(delta_time)
        
        # Update horn shake (when thinking)
        if self.state == CharacterState.THINKING:
            self.update_horn_shake(delta_time)
        
        # State-specific updates
        self._update_state_animation(delta_time)
    
    def update_blink(self, delta_time: float):
        """Update eye blinking animation"""
        # Simplified blinking logic
        pass
    
    def update_breathing(self, delta_time: float):
        """Update breathing animation"""
        import math
        self.breathing_progress = (self.animation_time % ANIMATION['breathing_duration']) / ANIMATION['breathing_duration']
        # Sine wave for smooth breathing
        self.breathing_offset = math.sin(self.breathing_progress * 2 * math.pi) * 2
    
    def update_horn_shake(self, delta_time: float):
        """Update horn shaking animation when thinking"""
        import math
        freq = ANIMATION['horn_shake_frequency']
        self.horn_shake_progress = math.sin(self.animation_time * 2 * math.pi * freq) * 0.5
    
    def _update_state_animation(self, delta_time: float):
        """Update animations based on current state"""
        if self.state == CharacterState.IDLE:
            self.head_tilt = 15.0  # Default tilt to right
        elif self.state == CharacterState.THINKING:
            self.head_tilt = 15.0
        elif self.state == CharacterState.CONFUSED:
            self.head_tilt = 30.0
    
    def set_state(self, new_state: CharacterState):
        """Change character state"""
        self.state = new_state
        self.state_time = 0.0
    
    def get_is_daytime(self) -> bool:
        """Get current daytime status"""
        return is_daytime()
