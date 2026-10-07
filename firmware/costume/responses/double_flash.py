from responses.base import Response


class DoubleFlash(Response):
    """Double tap response: two cyan flashes across all pixels."""

    def __init__(self, config):
        self._config = config
        self._start = 0.0

    def start(self, now):
        self._start = now

    def update(self, now, pixels):
        cfg = self._config
        elapsed = now - self._start
        total = cfg.RESPONSE_DURATIONS["double_tap"]
        if elapsed >= total:
            for i in range(cfg.NUM_PIXELS):
                pixels[i] = cfg.COLORS["off"]
            return True

        cycle = total / 4.0  # on, off, on, off
        phase = int(elapsed / cycle)
        on = phase in (0, 2)
        color = cfg.COLORS["cyan"] if on else cfg.COLORS["off"]
        for i in range(cfg.NUM_PIXELS):
            pixels[i] = color
        return False
