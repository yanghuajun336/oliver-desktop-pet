"""Character class and state management"""
from enum import Enum
from src.config import CHARACTER, ANIMATION
from src.utils.geometry import Point
from src.utils.time_utils import is_daytime
from src.particles import ParticleManager
import math


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
        self.breathing_offset = 0.0
        self.body_y_offset = 0.0
        self.facial_expression = "neutral"
        self.eye_state = "open"
        self.eye_openness = 1.0
        self.wing_spread_angle = 0.0
        self.wing_flap_offset = 0.0
        self.forward_tilt = 0.0
        self.monocle_offset_y = 0.0
        self.beak_open_height = 8.0
        self.pupil_star_rotation = 0.0
        self.star_pupil_mode = False
        self._blink_timer = 0.0
        self._blink_cooldown = ANIMATION['blink_interval']
        self._is_blinking = False
        self.particle_manager = ParticleManager()
        self.recent_keywords = ["索引", "检索", "归档"]
        
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
        
        # Update particle system
        activity_multiplier = 1.0
        if self.state in (CharacterState.THINKING, CharacterState.FLYING):
            activity_multiplier = 1.8
        elif self.state == CharacterState.SURPRISED:
            activity_multiplier = 1.5
        self.particle_manager.update(delta_time, activity_multiplier)
    
    def update_blink(self, delta_time: float):
        """Update eye blinking animation"""
        self._blink_timer += delta_time
        
        if not self._is_blinking:
            self._blink_cooldown -= delta_time
            if self._blink_cooldown <= 0:
                self._is_blinking = True
                self._blink_timer = 0.0
                self._blink_cooldown = ANIMATION['blink_interval']
        
        if self._is_blinking:
            blink_duration = max(0.01, ANIMATION['blink_duration'])
            blink_t = min(1.0, self._blink_timer / blink_duration)
            
            if blink_t < 0.5:
                self.eye_blink_progress = blink_t * 2.0
            else:
                self.eye_blink_progress = (1.0 - blink_t) * 2.0
            
            if blink_t >= 1.0:
                self._is_blinking = False
                self.eye_blink_progress = 0.0
                self.particle_manager.spawn_blink_sparkles(0.0, -64.0)
        
        self.eye_openness = max(0.05, 1.0 - self.eye_blink_progress)
        self.eye_state = "closed" if self.eye_openness <= 0.2 else "open"
    
    def update_breathing(self, delta_time: float):
        """Update breathing animation"""
        self.breathing_progress = (self.animation_time % ANIMATION['breathing_duration']) / ANIMATION['breathing_duration']
        # Sine wave for smooth breathing
        self.breathing_offset = math.sin(self.breathing_progress * 2 * math.pi) * 2.5
        self.body_y_offset = self.breathing_offset
    
    def update_horn_shake(self, delta_time: float):
        """Update horn shaking animation when thinking"""
        freq = ANIMATION['horn_shake_frequency']
        self.horn_shake_progress = math.sin(self.animation_time * 2 * math.pi * freq) * 3.0
    
    def _update_state_animation(self, delta_time: float):
        """Update animations based on current state"""
        self.forward_tilt = 0.0
        self.monocle_offset_y = 0.0
        self.star_pupil_mode = False
        self.wing_flap_offset = 0.0
        self.beak_open_height = 8.0
        self.pupil_star_rotation += delta_time * 45.0
        
        if self.state == CharacterState.IDLE:
            self.head_tilt = 15.0  # Default tilt to right
            self.wing_spread_angle = 0.0
            self.facial_expression = "neutral"
        elif self.state == CharacterState.THINKING:
            self.head_tilt = 15.0
            self.wing_spread_angle = min(45.0, self.state_time * 120.0)
            self.facial_expression = "thinking"
        elif self.state == CharacterState.CONFUSED:
            self.head_tilt = 30.0
            self.wing_spread_angle = 10.0
            self.monocle_offset_y = 10.0
            self.facial_expression = "confused"
        elif self.state == CharacterState.SURPRISED:
            self.head_tilt = 12.0
            self.wing_spread_angle = 90.0
            self.star_pupil_mode = True
            self.pupil_star_rotation += delta_time * 240.0
            self.facial_expression = "surprised"
        elif self.state == CharacterState.YAWNING:
            self.head_tilt = 10.0
            self.wing_spread_angle = 0.0
            yawn_cycle = max(0.1, ANIMATION['yawn_duration'])
            yawn_progress = min(1.0, self.state_time / yawn_cycle)
            self.beak_open_height = 8.0 + math.sin(yawn_progress * math.pi) * 12.0
            self.facial_expression = "yawning"
        elif self.state == CharacterState.WALKING:
            self.head_tilt = 15.0
            self.wing_spread_angle = 18.0
            flap_freq = 1.0 / max(0.1, 0.3)
            self.wing_flap_offset = math.sin(self.animation_time * 2 * math.pi * flap_freq) * 6.0
            self.facial_expression = "curious"
        elif self.state == CharacterState.FLYING:
            self.head_tilt = 8.0
            self.wing_spread_angle = 45.0
            flap_freq = 1.0 / max(0.05, ANIMATION['wing_flap_speed'])
            self.wing_flap_offset = math.sin(self.animation_time * 2 * math.pi * flap_freq) * 14.0
            self.forward_tilt = 8.0
            self.facial_expression = "focused"
            if int(self.animation_time * 10) % 2 == 0:
                self.particle_manager.spawn_flight_trail(self.recent_keywords)
    
    def set_state(self, new_state: CharacterState):
        """Change character state"""
        self.state = new_state
        self.state_time = 0.0
        if new_state == CharacterState.SURPRISED:
            self.particle_manager.spawn_pulse_wave()
        if new_state == CharacterState.THINKING:
            self.particle_manager.spawn_pulse_wave()
    
    def trigger_knowledge_update(self):
        """Trigger visual pulse when knowledge base updates"""
        self.particle_manager.spawn_pulse_wave()
    
    def get_is_daytime(self) -> bool:
        """Get current daytime status"""
        return is_daytime()
