from gestures.manager import GestureManager
from hardware import config as cfg


def test_double_tap_fires():
    manager = GestureManager(cfg)
    event = manager.update((0, 0, cfg.RESTING_GRAVITY), True, 0.0, 0.0)
    assert event is not None
    assert event.kind == "double_tap"


def test_cooldown_blocks_immediate_retrigger():
    manager = GestureManager(cfg)
    now = 0.0
    first = manager.update((0, 0, cfg.RESTING_GRAVITY), True, 0.0, now)
    assert first is not None
    assert first.kind == "double_tap"

    now += 0.05  # well inside the cooldown window
    second = manager.update((0, 0, cfg.RESTING_GRAVITY), True, 0.0, now)
    assert second is None

    now += cfg.GESTURE_COOLDOWN_S + 0.1
    third = manager.update((0, 0, cfg.RESTING_GRAVITY), True, 0.0, now)
    assert third is not None
    assert third.kind == "double_tap"


def test_idle_signal_produces_no_event():
    manager = GestureManager(cfg)
    event = manager.update((0, 0, cfg.RESTING_GRAVITY), False, 0.0, 0.0)
    assert event is None


def test_button_b_triggers_jazz_hands_on_press():
    manager = GestureManager(cfg)
    event = manager.update(
        (0, 0, cfg.RESTING_GRAVITY), False, 0.0, 0.0, button_b_pressed=True
    )

    assert event is not None
    assert event.kind == "jazz_hands"


def test_button_b_triggers_only_once_while_held():
    manager = GestureManager(cfg)
    first = manager.update(
        (0, 0, cfg.RESTING_GRAVITY), False, 0.0, 0.0, button_b_pressed=True
    )
    second = manager.update(
        (0, 0, cfg.RESTING_GRAVITY),
        False,
        0.0,
        cfg.GESTURE_COOLDOWN_S + 0.1,
        button_b_pressed=True,
    )

    assert first is not None
    assert first.kind == "jazz_hands"
    assert second is None
