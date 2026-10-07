class Response:
    """Non-blocking animation interface.

    `update` writes RGB tuples into `pixels` (a list-like buffer of length
    config.NUM_PIXELS) and returns True once the animation is finished.
    """

    def start(self, now):
        raise NotImplementedError

    def update(self, now, pixels):
        raise NotImplementedError
