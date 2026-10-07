class DebugState:
    """Button A toggles debug mode; solid status LED + serial logging while active."""

    def __init__(self, board_io):
        self._io = board_io
        self._enabled = False
        self._button_was_down = False

    def poll(self, now):
        down = self._io.button_a_pressed()
        if down and not self._button_was_down:
            self._enabled = not self._enabled
            self._io.set_status_led(self._enabled)
        self._button_was_down = down
        return self._enabled

    def log(self, message):
        if self._enabled:
            print(message)
