"""Button- and LED-guided calibration workflow."""

from learning.profile import make_profile, summarize_trial, validate_profile

_TRIALS = (
    ("jazz_hands", 1, (0, 255, 255)),
    ("fist_bump", 2, (255, 80, 0)),
    ("wave", 3, (255, 0, 0)),
    ("rest", 4, (255, 255, 255)),
)
_VALIDATION_TRIALS = (
    ("jazz_hands", 1, (0, 255, 255)),
    ("wave", 3, (255, 0, 0)),
    ("jazz_hands", 1, (0, 255, 255)),
    ("fist_bump", 2, (255, 80, 0)),
    ("jazz_hands", 1, (0, 255, 255)),
    ("rest", 4, (255, 255, 255)),
)
_REPETITIONS = 5
_RECORD_SECONDS = 3.0
_COUNTDOWN_SECONDS = 1.8
_PROMPT_UNIT_SECONDS = 0.36
_PROMPT_GAP_SECONDS = 0.7
_RECORDING_COLOR = (96, 0, 160)
_SUCCESS_COLORS = ((0, 255, 255), (0, 255, 0))
_FAILURE_COLOR = (255, 0, 0)


class CalibrationSession:
    """Collects labeled examples and validates a simple per-user profile."""

    def __init__(self, config, now, button_b_pressed=False):
        self._config = config
        self._button_was_pressed = button_b_pressed
        self._state = "prompt"
        self._state_started = now
        self._completion_next_state = "prompt"
        self._training_index = 0
        self._validation_index = 0
        self._trials = []
        self._validation_data = []
        self._samples = []
        self.profile = None
        self.finished = False
        print("Learning mode: follow the README LED cue key.")

    def update(self, now, acceleration, button_b_pressed):
        pressed_edge = button_b_pressed and not self._button_was_pressed
        self._button_was_pressed = button_b_pressed

        if self._state == "done":
            if self.profile is not None:
                return _SUCCESS_COLORS[int(now * 2) % len(_SUCCESS_COLORS)]
            return _FAILURE_COLOR if int(now * 2) % 2 == 0 else (0, 0, 0)

        if self._state == "trial_done":
            elapsed = now - self._state_started
            if elapsed >= 0.8:
                self._state = self._completion_next_state
                self._state_started = now
                if self._state == "done":
                    return (
                        _SUCCESS_COLORS[0]
                        if self.profile is not None
                        else _FAILURE_COLOR
                    )
                trial = self._current_trial()
                return self._prompt_color(now, trial[1], trial[2])
            pulse = elapsed % 0.4
            return (255, 0, 0) if pulse < 0.2 else (0, 0, 0)

        if self._state == "prompt":
            trial = self._current_trial()
            cue = self._prompt_color(now, trial[1], trial[2])
            if pressed_edge:
                self._state = "countdown"
                self._state_started = now
                return (255, 255, 255)
            return cue

        elapsed = now - self._state_started
        if self._state == "countdown":
            if elapsed >= _COUNTDOWN_SECONDS:
                self._state = "recording"
                self._state_started = now
                self._samples = []
                return _RECORDING_COLOR
            countdown_on = (
                int(elapsed / 0.6) % 2 == 0 and elapsed % 0.6 < 0.3
            )
            return (255, 255, 255) if countdown_on else (0, 0, 0)

        if self._state == "recording":
            self._samples.append(
                (now, acceleration[0], acceleration[1], acceleration[2])
            )
            if elapsed >= _RECORD_SECONDS:
                self._finish_trial()
                self._completion_next_state = (
                    "done" if self.finished else "prompt"
                )
                self._state = "trial_done"
                self._state_started = now
                return (255, 0, 0)
            return _RECORDING_COLOR

        raise RuntimeError("Unknown calibration state: {}".format(self._state))

    def _current_trial(self):
        if self._training_index < len(_TRIALS) * _REPETITIONS:
            return _TRIALS[self._training_index % len(_TRIALS)]
        return _VALIDATION_TRIALS[self._validation_index]

    def _prompt_color(self, now, pulse_count, color):
        pulse_duration = pulse_count * _PROMPT_UNIT_SECONDS
        cycle_duration = 2 * pulse_duration + _PROMPT_GAP_SECONDS
        phase = (now - self._state_started) % cycle_duration
        in_first_prompt = phase < pulse_duration
        in_second_prompt = (
            pulse_duration + _PROMPT_GAP_SECONDS
            <= phase
            < 2 * pulse_duration + _PROMPT_GAP_SECONDS
        )
        pulse_phase = phase % _PROMPT_UNIT_SECONDS
        if (
            (in_first_prompt or in_second_prompt)
            and pulse_phase < _PROMPT_UNIT_SECONDS / 2
        ):
            return color
        return (0, 0, 0)

    def _finish_trial(self):
        if self._training_index < len(_TRIALS) * _REPETITIONS:
            trial_type = _TRIALS[self._training_index % len(_TRIALS)]
            summary = summarize_trial(trial_type[0], self._samples)
            self._trials.append(summary)
            self._print_summary("TRAIN", self._training_index, summary)
            self._training_index += 1
            if self._training_index == len(_TRIALS) * _REPETITIONS:
                self.profile = make_profile(self._trials, self._config)
                if self.profile is None:
                    self._finish(False)
                    return
        else:
            validation_index = self._validation_index
            trial_type = _VALIDATION_TRIALS[validation_index]
            summary = summarize_trial(trial_type[0], self._samples)
            self._validation_data.append(summary)
            self._print_summary("CHECK", validation_index, summary)
            self._validation_index += 1
            if self._validation_index == len(_VALIDATION_TRIALS):
                if not validate_profile(self.profile, self._validation_data):
                    self.profile = None
                self._finish(self.profile is not None)
                return

        self._samples = []

    def _finish(self, succeeded):
        self.finished = True
        self._state = "done"
        if succeeded:
            print(
                "CALIBRATION,passed,axis,{},min_amplitude,{:.1f},min_reversals,{}".format(
                    self.profile["axis"],
                    self.profile["min_amplitude"],
                    self.profile["min_reversals"],
                )
            )
        else:
            print("CALIBRATION,not_separated,previous_profile_kept")

    def _print_summary(self, group, trial_number, summary):
        parts = []
        for axis, name in enumerate(("x", "y", "z")):
            default_threshold_index = int(
                self._config.JAZZ_HANDS_MIN_AMPLITUDE * 2
            ) - 2
            reversals = summary["reversals"][axis][default_threshold_index]
            parts.extend(
                (
                    "{}_amplitude={:.2f}".format(
                        name, summary["amplitudes"][axis]
                    ),
                    "{}_reversals={}".format(name, reversals),
                )
            )
        print(
            "CALIBRATION,{},{},label,{},samples,{},{}".format(
                group,
                trial_number + 1,
                summary["label"],
                summary["sample_count"],
                ",".join(parts),
            )
        )
