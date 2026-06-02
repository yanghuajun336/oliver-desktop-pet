"""Time and datetime utilities"""
from datetime import datetime
from typing import Tuple


def get_current_time() -> Tuple[int, int, int]:
    """Get current time as (hours, minutes, seconds)"""
    now = datetime.now()
    return (now.hour, now.minute, now.second)


def is_daytime(day_start: int = 6, day_end: int = 18) -> bool:
    """Check if current time is daytime"""
    hour, _, _ = get_current_time()
    return day_start <= hour < day_end


def seconds_to_ms(seconds: float) -> int:
    """Convert seconds to milliseconds"""
    return int(seconds * 1000)


def ms_to_seconds(milliseconds: int) -> float:
    """Convert milliseconds to seconds"""
    return milliseconds / 1000.0
