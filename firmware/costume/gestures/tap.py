from gestures.base import GestureEvent


class TapDetector:
    """Converts hardware single/double tap flags into gesture events.

    Double tap is checked first since the LIS3DH's single-click flag may
    also be set alongside a double-click event.
    """

    def update(self, single, double, now):
        if double:
            return GestureEvent("double_tap", now)
        if single:
            return GestureEvent("tap", now)
        return None
