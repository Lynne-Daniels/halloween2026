import time

from hardware.board_io import BoardIO
from hardware import config as cfg
from gestures.manager import GestureManager
from responses.manager import ResponseManager
from responses.double_flash import DoubleFlash
from responses.rainbow_chase import RainbowChase
from responses.quarter_flash import QuarterFlash
from debug import DebugState


def _jazz_signal(x, y, z):
    # Power connector "down", data connector "up": x is the lateral axis
    # perpendicular to that up/down axis on the wrist. Placeholder pending
    # on-hardware confirmation (see plan.md Further Considerations).
    return x


def run_forever():
    io = BoardIO()
    gestures = GestureManager(cfg)
    responses = ResponseManager(
        cfg,
        {
            "double_tap": lambda: DoubleFlash(cfg),
            "jazz_hands": lambda: RainbowChase(cfg),
            "fist_bump": lambda: QuarterFlash(cfg),
        },
    )
    debug = DebugState(io)
    pixel_buffer = [cfg.COLORS["off"]] * cfg.NUM_PIXELS

    while True:
        now = time.monotonic()
        debug_on = debug.poll(now)

        acceleration = io.read_acceleration()
        double_tap = io.read_double_tap()
        jazz_signal = _jazz_signal(*acceleration)

        event = gestures.update(acceleration, double_tap, jazz_signal, now)
        if event:
            responses.trigger(event.kind, now)
            debug.log("gesture: {} @ {:.3f}".format(event.kind, event.timestamp))
        elif debug_on:
            debug.log("accel: {}".format(acceleration))

        responses.tick(now, pixel_buffer)
        io.show(pixel_buffer)

        time.sleep(cfg.LOOP_SLEEP)
