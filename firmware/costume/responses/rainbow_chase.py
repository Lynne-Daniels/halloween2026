from responses.base import Response


def _wheel(pos):
    """Classic NeoPixel rainbow helper: pos 0-255 -> an (r, g, b) color."""
    pos = pos % 256
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    pos -= 170
    return (0, pos * 3, 255 - pos * 3)


class RainbowChase(Response):
    """Jazz hands response: a single rainbow pixel races around the ring."""

    def __init__(self, config):
        self._config = config
        self._start = 0.0

    def start(self, now):
        self._start = now

    def update(self, now, pixels):
        cfg = self._config
        elapsed = now - self._start
        total = cfg.RESPONSE_DURATIONS["jazz_hands"]
        if elapsed >= total:
            for i in range(cfg.NUM_PIXELS):
                pixels[i] = cfg.COLORS["off"]
            return True

        position = int(elapsed * cfg.JAZZ_HANDS_CHASE_SPEED) % cfg.NUM_PIXELS
        for i in range(cfg.NUM_PIXELS):
            pixels[i] = _wheel(int(elapsed * 60)) if i == position else cfg.COLORS["off"]
        return False
