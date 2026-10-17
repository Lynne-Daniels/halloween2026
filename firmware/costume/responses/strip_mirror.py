from responses.base import Response


class StripMirror(Response):
    """Expand an existing pixel response across a longer NeoPixel strip."""

    def __init__(self, response, config):
        self._response = response
        self._source_pixels = [config.COLORS["off"]] * config.NUM_PIXELS

    def start(self, now):
        self._response.start(now)

    def update(self, now, pixels):
        done = self._response.update(now, self._source_pixels)
        source_count = len(self._source_pixels)
        strip_count = len(pixels)
        for i in range(strip_count):
            source_index = i * source_count // strip_count
            pixels[i] = self._source_pixels[source_index]
        return done
