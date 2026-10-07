from gestures.fist_bump import FistBumpDetector
from hardware import config as cfg


def _run(detector, samples):
    for now, magnitude in samples:
        event = detector.update(magnitude, now)
        if event:
            return event
    return None


def test_detects_clean_fist_bump():
    detector = FistBumpDetector(cfg)
    samples = []
    t = 0.0
    step = 0.01
    for _ in range(10):
        samples.append((t, cfg.RESTING_GRAVITY))
        t += step
    samples.append((t, cfg.FIST_BUMP_PUNCH_THRESHOLD + 10))
    t += step
    samples.append((t, cfg.RESTING_GRAVITY))

    event = _run(detector, samples)
    assert event is not None
    assert event.kind == "fist_bump"


def test_ignores_idle_noise():
    detector = FistBumpDetector(cfg)
    samples = []
    t = 0.0
    step = 0.01
    for i in range(50):
        samples.append((t, cfg.RESTING_GRAVITY + (0.2 if i % 2 else -0.2)))
        t += step

    assert _run(detector, samples) is None


def test_spike_without_settle_times_out():
    detector = FistBumpDetector(cfg)
    samples = [(0.0, cfg.RESTING_GRAVITY), (0.01, cfg.FIST_BUMP_PUNCH_THRESHOLD + 10)]
    # Stay spiked (never settling) well past the detection window.
    t = 0.01
    for _ in range(50):
        t += 0.05
        samples.append((t, cfg.FIST_BUMP_PUNCH_THRESHOLD + 10))

    assert _run(detector, samples) is None
