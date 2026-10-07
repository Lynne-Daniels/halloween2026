from gestures.tap import TapDetector
from gestures.fist_bump import FistBumpDetector
from gestures.jazz_hands import JazzHandsDetector


class GestureManager:
    """Feeds each sample to all detectors, then applies priority + cooldown
    so at most one gesture event fires per cooldown window."""

    def __init__(self, config):
        self._config = config
        self._tap = TapDetector()
        self._fist_bump = FistBumpDetector(config)
        self._jazz_hands = JazzHandsDetector(config)
        self._cooldown_until = 0.0

    def update(self, acceleration, tap_flags, jazz_signal, now):
        x, y, z = acceleration
        magnitude = (x * x + y * y + z * z) ** 0.5

        # Always run detectors so their internal buffers/state stay current,
        # even while suppressing results during cooldown.
        tap_event = self._tap.update(tap_flags[0], tap_flags[1], now)
        fist_event = self._fist_bump.update(magnitude, now)
        jazz_event = self._jazz_hands.update(jazz_signal, now)

        if now < self._cooldown_until:
            return None

        candidates = {}
        for event in (tap_event, fist_event, jazz_event):
            if event is not None:
                candidates[event.kind] = event

        for kind in self._config.GESTURE_PRIORITY:
            if kind in candidates:
                self._cooldown_until = now + self._config.GESTURE_COOLDOWN_S
                return candidates[kind]
        return None
