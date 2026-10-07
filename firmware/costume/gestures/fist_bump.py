from gestures.base import GestureEvent


class FistBumpDetector:
    """Detects an acceleration spike followed by a sudden stop, any direction.

    State machine: idle -> spiked (waiting for settle) -> fire or timeout back to idle.
    """

    def __init__(self, config):
        self._config = config
        self._state = "idle"
        self._spike_time = 0.0

    def update(self, magnitude, now):
        cfg = self._config

        if self._state == "idle":
            if magnitude >= cfg.FIST_BUMP_PUNCH_THRESHOLD:
                self._state = "spiked"
                self._spike_time = now
            return None

        elapsed = now - self._spike_time
        if elapsed > cfg.FIST_BUMP_WINDOW_S:
            self._state = "idle"
            return None

        low = cfg.RESTING_GRAVITY - cfg.FIST_BUMP_SETTLE_BAND
        high = cfg.RESTING_GRAVITY + cfg.FIST_BUMP_SETTLE_BAND
        if low <= magnitude <= high:
            self._state = "idle"
            return GestureEvent("fist_bump", now)
        return None
