from hardware import config as cfg
from responses.double_flash import DoubleFlash
from responses.strip_mirror import StripMirror


def test_strip_mirror_expands_double_flash_across_60_pixels():
    response = StripMirror(DoubleFlash(cfg), cfg)
    pixels = [cfg.COLORS["off"]] * cfg.STRIP_NUM_PIXELS
    response.start(0.0)

    assert response.update(0.0, pixels) is False
    assert pixels == [cfg.COLORS["cyan"]] * cfg.STRIP_NUM_PIXELS

    assert response.update(0.15, pixels) is False
    assert pixels == [cfg.COLORS["off"]] * cfg.STRIP_NUM_PIXELS

    assert response.update(cfg.RESPONSE_DURATIONS["double_tap"], pixels) is True
    assert pixels == [cfg.COLORS["off"]] * cfg.STRIP_NUM_PIXELS
