from gestures.base import GestureEvent


class TapDetector:
    """Converts the hardware double-tap flag into a gesture event."""

    def update(self, double, now):
        if double:
            return GestureEvent("double_tap", now)
        return None
