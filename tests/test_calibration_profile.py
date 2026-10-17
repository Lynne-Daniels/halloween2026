import math

from hardware import config as cfg
from learning.profile import make_profile, summarize_trial, validate_profile
from learning.profile_store import load_profile, save_profile
from learning.session import CalibrationSession


def _capture(label, axis, frequency, amplitude, start=0.0):
    samples = []
    step = 0.01
    for index in range(150):
        now = start + index * step
        value = amplitude * math.sin(2 * math.pi * frequency * now)
        acceleration = [0.0, 0.0, 0.0]
        acceleration[axis] = value
        samples.append((now, acceleration[0], acceleration[1], acceleration[2]))
    return summarize_trial(label, samples)


def _training_examples():
    trials = []
    for repetition in range(5):
        trials.extend(
            (
                _capture("jazz_hands", 1, 2.0, 5.0, repetition * 0.03),
                _capture("fist_bump", 0, 0.4, 7.0),
                _capture("wave", 0, 0.5, 7.0),
                _capture("rest", 0, 0.0, 0.0),
            )
        )
    return trials


def test_calibration_selects_separable_axis_and_thresholds():
    profile = make_profile(_training_examples(), cfg)

    assert profile is not None
    assert profile["axis"] == 1
    assert profile["min_amplitude"] >= 1.0
    assert profile["min_reversals"] >= cfg.JAZZ_HANDS_MIN_REVERSALS


def test_calibration_rejects_non_separable_examples():
    trials = []
    for _ in range(5):
        trials.extend(
            (
                _capture("jazz_hands", 0, 1.0, 5.0),
                _capture("fist_bump", 0, 1.0, 5.0),
                _capture("wave", 0, 1.0, 5.0),
                _capture("rest", 0, 0.0, 0.0),
            )
        )

    assert make_profile(trials, cfg) is None


def test_profile_validation_accepts_new_separated_examples():
    profile = make_profile(_training_examples(), cfg)
    validation = [
        _capture("jazz_hands", 1, 2.0, 5.0, index * 0.03)
        for index in range(3)
    ]
    validation.extend(
        (
            _capture("wave", 0, 0.5, 7.0),
            _capture("fist_bump", 0, 0.4, 7.0),
            _capture("rest", 0, 0.0, 0.0),
        )
    )

    assert validate_profile(profile, validation)


def test_profile_store_round_trips_and_rejects_corruption():
    nvm = bytearray([0xFF] * 16)
    profile = {"axis": 1, "min_amplitude": 3.5, "min_reversals": 5}

    save_profile(nvm, profile)
    assert load_profile(nvm) == profile

    nvm[4] ^= 1
    assert load_profile(nvm) is None


def test_guided_session_completes_training_and_validation():
    session = CalibrationSession(cfg, 0.0)
    now = 0.0
    training = ("jazz_hands", "fist_bump", "wave", "rest") * 5
    validation = ("jazz_hands", "wave", "jazz_hands", "fist_bump", "jazz_hands", "rest")

    for label in training + validation:
        session.update(now, (0.0, 0.0, 0.0), True)
        now += 0.01
        session.update(now, (0.0, 0.0, 0.0), False)

        for index in range(181):
            now += 0.01
            acceleration = _gesture_sample(label, now)
            session.update(now, acceleration, False)

        for _ in range(301):
            now += 0.01
            acceleration = _gesture_sample(label, now)
            session.update(now, acceleration, False)

        for _ in range(81):
            now += 0.01
            session.update(now, (0.0, 0.0, 0.0), False)

    assert session.finished
    assert session.profile is not None


def _gesture_sample(label, now):
    if label == "jazz_hands":
        return (0.0, 5.0 * math.sin(2 * math.pi * 2.0 * now), 0.0)
    if label == "fist_bump":
        return (7.0 * math.sin(2 * math.pi * 0.4 * now), 0.0, 0.0)
    if label == "wave":
        return (7.0 * math.sin(2 * math.pi * 0.5 * now), 0.0, 0.0)
    return (0.0, 0.0, 0.0)
