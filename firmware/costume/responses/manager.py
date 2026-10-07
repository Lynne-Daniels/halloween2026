class ResponseManager:
    """Holds at most one active Response; a new trigger replaces it."""

    def __init__(self, config, factories):
        """factories: dict kind -> zero-arg callable returning a fresh Response."""
        self._config = config
        self._factories = factories
        self._active = None

    def trigger(self, kind, now):
        factory = self._factories.get(kind)
        if factory is None:
            return
        self._active = factory()
        self._active.start(now)

    def tick(self, now, pixels):
        if self._active is None:
            return
        done = self._active.update(now, pixels)
        if done:
            self._active = None
