from gestures.base import GestureEvent


class JazzHandsDetector:
    """Detects a sustained back-and-forth oscillation via zero-crossing counting.

    Takes a single pre-selected "signal" value per sample (whichever axis or
    combination is most sensitive to the wrist-twisting motion - see
    main.py's `_jazz_signal` for the current axis choice, which is a
    placeholder pending on-hardware confirmation per plan.md).
    """

    def __init__(self, config):
        self._config = config
        self._samples = []  # list of (timestamp, signal)

    def update(self, signal, now):
        cfg = self._config
        self._samples.append((now, signal))
        cutoff = now - cfg.JAZZ_HANDS_WINDOW_S
        while self._samples and self._samples[0][0] < cutoff:
            self._samples.pop(0)

        if len(self._samples) < 4:
            return None

        values = [sample[1] for sample in self._samples]
        mean = sum(values) / len(values)

        reversals = 0
        prev_sign = None
        for value in values:
            deviation = value - mean
            if abs(deviation) < cfg.JAZZ_HANDS_MIN_AMPLITUDE:
                continue
            sign = 1 if deviation > 0 else -1
            if prev_sign is not None and sign != prev_sign:
                reversals += 1
            prev_sign = sign

        if reversals >= cfg.JAZZ_HANDS_MIN_REVERSALS:
            self._samples = []
            return GestureEvent("jazz_hands", now)
        return None
