import time
import microcontroller

from hardware.board_io import BoardIO
from hardware import config as cfg
from gestures.manager import GestureManager
from responses.manager import ResponseManager
from responses.double_flash import DoubleFlash
from responses.rainbow_chase import RainbowChase
from responses.quarter_flash import QuarterFlash
from responses.strip_mirror import StripMirror
from debug import DebugState
from learning.profile_store import load_profile, save_profile
from learning.session import CalibrationSession


def _jazz_signal(acceleration, profile):
    axis = profile["axis"] if profile is not None else 0
    return acceleration[axis]


def run_forever():
    io = BoardIO()
    debug = DebugState(io)
    learning_mode = None
    learner = None
    learning_result_handled = False
    profile = None

    response_factories = {
        "double_tap": lambda: DoubleFlash(cfg),
        "jazz_hands": lambda: RainbowChase(cfg),
        "fist_bump": lambda: QuarterFlash(cfg),
    }
    pixel_buffer = [cfg.COLORS["off"]] * cfg.NUM_PIXELS
    strip_buffer = [cfg.COLORS["off"]] * cfg.STRIP_NUM_PIXELS

    while True:
        now = time.monotonic()
        selected_learning_mode = io.learning_mode_selected()
        if selected_learning_mode != learning_mode:
            learning_mode = selected_learning_mode
            if learning_mode:
                learner = CalibrationSession(
                    cfg, now, io.button_b_pressed()
                )
                learning_result_handled = False
                print("Slide switch: learning mode.")
            else:
                learner = None
                profile = load_profile(microcontroller.nvm)
                gestures = GestureManager(cfg, profile)
                responses = ResponseManager(cfg, response_factories)
                strip_responses = ResponseManager(
                    cfg,
                    {
                        kind: (
                            lambda factory=factory: StripMirror(factory(), cfg)
                        )
                        for kind, factory in response_factories.items()
                    },
                )
                pixel_buffer = [cfg.COLORS["off"]] * cfg.NUM_PIXELS
                strip_buffer = [cfg.COLORS["off"]] * cfg.STRIP_NUM_PIXELS
                print(
                    "Slide switch: operation mode. Jazz-hands profile: {}.".format(
                        "loaded" if profile is not None else "default"
                    )
                )

        acceleration = io.read_acceleration()
        if learning_mode:
            color = learner.update(now, acceleration, io.button_b_pressed())
            io.show_learning_cue(color)
            if learner.finished and not learning_result_handled:
                if learner.profile is not None:
                    save_profile(microcontroller.nvm, learner.profile)
                    print("Calibration profile saved to board NVM.")
                learning_result_handled = True
        else:
            debug_on = debug.poll(now)
            double_tap = io.read_double_tap()
            button_b_pressed = io.button_b_pressed()
            jazz_signal = _jazz_signal(acceleration, profile)

            event = gestures.update(
                acceleration,
                double_tap,
                jazz_signal,
                now,
                button_b_pressed=button_b_pressed,
            )
            if event:
                responses.trigger(event.kind, now)
                strip_responses.trigger(event.kind, now)
                debug.log(
                    "gesture: {} @ {:.3f}".format(event.kind, event.timestamp)
                )
            elif debug_on:
                debug.log("accel: {}".format(acceleration))

            responses.tick(now, pixel_buffer)
            strip_responses.tick(now, strip_buffer)
            io.show(pixel_buffer)
            io.show_strip(strip_buffer)

        time.sleep(cfg.LOOP_SLEEP)
