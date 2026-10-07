class GestureEvent:
    """Plain event object (no dataclasses - not reliably available on CircuitPython)."""

    def __init__(self, kind, timestamp):
        self.kind = kind
        self.timestamp = timestamp

    def __repr__(self):
        return "GestureEvent(kind={}, timestamp={})".format(self.kind, self.timestamp)
