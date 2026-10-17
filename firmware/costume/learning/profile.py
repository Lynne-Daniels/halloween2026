"""Small, non-ML calibration profiles for the jazz-hands detector."""

AMPLITUDE_CANDIDATES = tuple(index * 0.5 for index in range(2, 17))
PROFILE_MAGIC = (0x4A, 0x48)
PROFILE_SIZE = 6


def summarize_trial(label, samples):
    """Summarize one capture without retaining its full sample buffer."""
    axes = [[], [], []]
    for sample in samples:
        for axis in range(3):
            axes[axis].append(sample[axis + 1])

    amplitudes = []
    threshold_counts = []
    for values in axes:
        if not values:
            amplitudes.append(0.0)
            threshold_counts.append(tuple(0 for _ in AMPLITUDE_CANDIDATES))
            continue

        mean = sum(values) / len(values)
        deviations = [value - mean for value in values]
        amplitudes.append((max(values) - min(values)) / 2.0)
        counts = []
        for threshold in AMPLITUDE_CANDIDATES:
            reversals = 0
            previous_sign = None
            for deviation in deviations:
                if abs(deviation) < threshold:
                    continue
                sign = 1 if deviation > 0 else -1
                if previous_sign is not None and sign != previous_sign:
                    reversals += 1
                previous_sign = sign
            counts.append(reversals)
        threshold_counts.append(tuple(counts))

    return {
        "label": label,
        "sample_count": len(samples),
        "amplitudes": tuple(amplitudes),
        "reversals": tuple(threshold_counts),
    }


def make_profile(trials, config):
    """Choose settings only when all training examples cleanly separate."""
    expected_labels = ("jazz_hands", "fist_bump", "wave", "rest")
    counts = dict((label, 0) for label in expected_labels)
    for trial in trials:
        if trial["label"] in counts:
            counts[trial["label"]] += 1
    if any(counts[label] != 5 for label in expected_labels):
        return None

    positive = [trial for trial in trials if trial["label"] == "jazz_hands"]
    negative = [trial for trial in trials if trial["label"] != "jazz_hands"]
    candidates = []
    for axis in range(3):
        for threshold_index, threshold in enumerate(AMPLITUDE_CANDIDATES):
            positive_min = min(
                trial["reversals"][axis][threshold_index] for trial in positive
            )
            negative_max = max(
                trial["reversals"][axis][threshold_index] for trial in negative
            )
            if (
                positive_min >= config.JAZZ_HANDS_MIN_REVERSALS
                and positive_min > negative_max
            ):
                separation = positive_min - negative_max
                candidates.append(
                    (
                        separation,
                        positive_min,
                        -abs(threshold - config.JAZZ_HANDS_MIN_AMPLITUDE),
                        -axis,
                        axis,
                        threshold,
                        max(config.JAZZ_HANDS_MIN_REVERSALS, negative_max + 1),
                    )
                )

    if not candidates:
        return None

    best = max(candidates)
    return {
        "axis": best[4],
        "min_amplitude": best[5],
        "min_reversals": best[6],
    }


def validate_profile(profile, validation_trials):
    """Require at least two of three positives and no false-positive controls."""
    positives = [
        trial for trial in validation_trials if trial["label"] == "jazz_hands"
    ]
    negatives = [
        trial for trial in validation_trials if trial["label"] != "jazz_hands"
    ]
    if len(positives) != 3 or len(negatives) != 3:
        return False

    threshold_index = None
    for index, threshold in enumerate(AMPLITUDE_CANDIDATES):
        if threshold == profile["min_amplitude"]:
            threshold_index = index
            break
    if threshold_index is None:
        return False

    def detected(trial):
        axis = profile["axis"]
        amplitude_ok = trial["amplitudes"][axis] >= profile["min_amplitude"]
        reversals_ok = (
            trial["reversals"][axis][threshold_index]
            >= profile["min_reversals"]
        )
        return amplitude_ok and reversals_ok

    return sum(1 for trial in positives if detected(trial)) >= 2 and not any(
        detected(trial) for trial in negatives
    )
