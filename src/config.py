"""Configuration management for Oliver Desktop Pet"""
import os
from pathlib import Path

# ============================================================================
# COLOR PALETTE - 配色方案
# ============================================================================
COLOR_PALETTE = {
    # Primary colors - 主要颜色
    'starry_blue': (43, 58, 103),           # #2B3A67 - 星夜蓝
    'ivory_white': (255, 248, 231),         # #FFF8E7 - 奶白色
    'apricot_pink': (247, 197, 160),        # #F7C5A0 - 浅杏色
    'amber_gold': (212, 160, 23),           # #D4A017 - 琥珀金色
    'tangerine': (232, 137, 12),            # #E8890C - 蜜柑色
    'light_gold': (240, 214, 138),          # #F0D68A - 淡金色
    'dark_indigo': (26, 45, 77),            # #1A2D4D - 深靛蓝
    'purple_gradient': (155, 89, 182),      # #9B59B6 - 紫色渐变
    'pink_gradient': (232, 148, 158),       # #E8949E - 粉红渐变
    'silver_white': (220, 220, 230),        # 银白色
    'soft_pink': (255, 200, 200),           # 柔和粉色（舌头）
}

# ============================================================================
# CHARACTER DIMENSIONS - 角色尺寸
# ============================================================================
CHARACTER = {
    'screen_height_px': 200,                # 屏幕显示高度（像素）
    'head_ratio': 0.6,                      # 头部占比
    'body_ratio': 0.4,                      # 身体占比
    'eye_diameter_ratio': 0.25,             # 眼睛直径占头部比例
    'pupil_ratio': 0.4,                     # 瞳孔占眼睛比例
    'horn_length': 50,                      # 角羽长度（px）
    'wing_spread_angle': 45,                # 翅膀展开角度（度）
}

# ============================================================================
# ANIMATION TIMINGS - 动画时间参数
# ============================================================================
ANIMATION = {
    'fps': 60,                              # 目标帧率
    'default_duration': 1.0,                # 默认动画时长（秒）
    'blink_interval': 4.0,                  # 眨眼间隔（秒）
    'blink_duration': 0.15,                 # 眨眼时长（秒）
    'breathing_duration': 2.0,              # 呼吸动作时长（秒）
    'think_head_tilt': 15,                  # 思考时头部倾斜角度（度）
    'confused_head_tilt': 30,               # 困惑时头部倾斜角度（度）
    'yawn_duration': 1.2,                   # 打哈欠时长（秒）
    'spin_duration': 1.0,                   # 旋转一圈时长（秒）
    'wing_flap_speed': 0.1,                 # 翅膀扑动速度（秒/次）
    'horn_shake_frequency': 8,              # 角羽震动频率（Hz）
}

# ============================================================================
# PARTICLE SYSTEM - 粒子系统
# ============================================================================
PARTICLES = {
    'ambient_star_count': 5,                # 环绕星光粒子数量
    'ambient_star_radius': 40,              # 环绕半径（px）
    'ambient_star_speed': 0.5,              # 环绕速度（px/帧）
    'ambient_star_size': 3,                 # 粒子大小（px）
    'stardust_trail_opacity': 0.7,          # 星尘尾迹透明度
    'ripple_max_radius': 60,                # 涟漪最大半径（px）
    'ripple_duration': 0.8,                 # 涟漪持续时间（秒）
}

# ============================================================================
# TIME SYSTEM - 时间系统
# ============================================================================
TIME_SYSTEM = {
    'day_start': 6,                         # 白天开始时间（小时）
    'day_end': 18,                          # 白天结束时间（小时）
    'night_activity_boost': 1.5,            # 夜间活跃度提升倍数
    'day_activity': 0.7,                    # 白天活跃度
    'yawn_interval_day': 45,                # 白天打哈欠间隔（秒）
}

# ============================================================================
# WINDOW PROPERTIES - 窗口属性
# ============================================================================
WINDOW = {
    'width': 250,                           # 窗口宽度（px）
    'height': 300,                          # 窗口高度（px）
    'always_on_top': True,                  # 始终置顶
    'frameless': True,                      # 无边框
    'transparent_background': True,         # 透明背景
    'dock_edge_distance': 20,               # 停靠边缘距离（px）
}

# ============================================================================
# AUDIO SETTINGS - 音频设置
# ============================================================================
AUDIO = {
    'enabled': True,                        # 音效启用
    'volume': 0.7,                          # 音量（0-1）
    'blink_sound': 'assets/sounds/blink.wav',
    'think_sound': 'assets/sounds/think.wav',
    'surprise_sound': 'assets/sounds/surprise.wav',
    'confused_sound': 'assets/sounds/confused.wav',
    'yawn_sound': 'assets/sounds/yawn.wav',
}

# ============================================================================
# PATHS - 文件路径
# ============================================================================
BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / 'assets'
SPRITES_DIR = ASSETS_DIR / 'sprites'
SOUNDS_DIR = ASSETS_DIR / 'sounds'
FONTS_DIR = ASSETS_DIR / 'fonts'

# Create asset directories if they don't exist
for directory in [ASSETS_DIR, SPRITES_DIR, SOUNDS_DIR, FONTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# ============================================================================
# EASING FUNCTIONS - 缓动函数
# ============================================================================
def ease_in_out_quad(t):
    """二次方缓动（快速开始和结束，中间缓慢）"""
    if t < 0.5:
        return 2 * t * t
    else:
        return -1 + (4 - 2 * t) * t

def ease_out_bounce(t):
    """弹跳缓动（结尾弹跳）"""
    if t < 0.36363:
        return 7.5625 * t * t
    elif t < 0.72727:
        t -= 0.545454
        return 7.5625 * t * t + 0.75
    elif t < 0.909091:
        t -= 0.818182
        return 7.5625 * t * t + 0.9375
    else:
        t -= 0.954545
        return 7.5625 * t * t + 0.984375

def ease_in_out_elastic(t):
    """弹性缓动"""
    if t < 0.5:
        return 0.5 * (2 ** (20 * t - 10) * (t - 0.1) * (2 * 3.14159) / 3)
    else:
        return 1 - 0.5 * (2 ** (-20 * t + 10) * ((t - 0.9) * 2 * 3.14159) / 3)

def linear(t):
    """线性缓动"""
    return t

EASING_FUNCTIONS = {
    'linear': linear,
    'ease_in_out_quad': ease_in_out_quad,
    'ease_out_bounce': ease_out_bounce,
    'ease_in_out_elastic': ease_in_out_elastic,
}
