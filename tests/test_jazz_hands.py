import math

from gestures.jazz_hands import JazzHandsDetector
from hardware import config as cfg


def _run(detector, samples):
    for now, signal in samples:
        event = detector.update(signal, now)
        if event:
            return event
    return None


def test_detects_oscillation():
    detector = JazzHandsDetector(cfg)
    samples = []
    t = 0.0
    step = 0.02
    amplitude = cfg.JAZZ_HANDS_MIN_AMPLITUDE * 2
    for _ in range(80):
        value = amplitude * math.sin(2 * math.pi * 2.0 * t)  # ~2 Hz oscillation
        samples.append((t, value))
        t += step

    event = _run(detector, samples)
    assert event is not None
    assert event.kind == "jazz_hands"


def test_ignores_small_noise():
    detector = JazzHandsDetector(cfg)
    samples = []
    t = 0.0
    step = 0.02
    for i in range(80):
        value = (cfg.JAZZ_HANDS_MIN_AMPLITUDE * 0.3) * (1 if i % 2 == 0 else -1)
        samples.append((t, value))
        t += step

    assert _run(detector, samples) is None


def test_ignores_steady_signal():
    detector = JazzHandsDetector(cfg)
    samples = [(i * 0.02, cfg.RESTING_GRAVITY) for i in range(80)]

    assert _run(detector, samples) is None
