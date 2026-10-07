from responses.base import Response


class SingleFlash(Response):
    """Tap response: one white flash across all pixels."""

    def __init__(self, config):
        self._config = config
        self._start = 0.0

    def start(self, now):
        self._start = now

    def update(self, now, pixels):
        cfg = self._config
        elapsed = now - self._start
        on = elapsed < cfg.RESPONSE_DURATIONS["tap"]
        color = cfg.COLORS["white"] if on else cfg.COLORS["off"]
        for i in range(cfg.NUM_PIXELS):
            pixels[i] = color
        return not on
