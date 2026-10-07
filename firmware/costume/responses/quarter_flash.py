from responses.base import Response


class QuarterFlash(Response):
    """Fist bump response: opposite arcs (orange / red) blink together 3x."""

    def __init__(self, config):
        self._config = config
        self._start = 0.0

    def start(self, now):
        self._start = now

    def update(self, now, pixels):
        cfg = self._config
        elapsed = now - self._start
        total = cfg.RESPONSE_DURATIONS["fist_bump"]
        if elapsed >= total:
            for i in range(cfg.NUM_PIXELS):
                pixels[i] = cfg.COLORS["off"]
            return True

        blinks = 3
        cycle = total / (blinks * 2)  # on, off per blink
        phase = int(elapsed / cycle)
        on = (phase % 2) == 0

        for i in range(cfg.NUM_PIXELS):
            pixels[i] = cfg.COLORS["off"]
        if on:
            for i in cfg.FIST_BUMP_ARC_A:
                pixels[i] = cfg.COLORS["orange"]
            for i in cfg.FIST_BUMP_ARC_B:
                pixels[i] = cfg.COLORS["red"]
        return False
