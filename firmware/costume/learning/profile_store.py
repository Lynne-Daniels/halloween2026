"""Persistence for the tiny calibration profile in CircuitPython NVM."""

from learning.profile import PROFILE_MAGIC, PROFILE_SIZE


def load_profile(nvm):
    if len(nvm) < PROFILE_SIZE:
        raise RuntimeError("Board NVM is too small for the gesture profile")

    record = bytes(nvm[:PROFILE_SIZE])
    if record[:2] != bytes(PROFILE_MAGIC):
        return None

    axis, amplitude_half_steps, min_reversals, checksum = record[2:]
    expected_checksum = (
        sum(PROFILE_MAGIC) + axis + amplitude_half_steps + min_reversals
    ) & 0xFF
    if checksum != expected_checksum:
        return None
    if axis > 2 or not 2 <= amplitude_half_steps <= 16 or min_reversals < 4:
        return None

    return {
        "axis": axis,
        "min_amplitude": amplitude_half_steps * 0.5,
        "min_reversals": min_reversals,
    }


def save_profile(nvm, profile):
    if len(nvm) < PROFILE_SIZE:
        raise RuntimeError("Board NVM is too small for the gesture profile")

    axis = profile["axis"]
    amplitude_half_steps = int(profile["min_amplitude"] * 2)
    min_reversals = profile["min_reversals"]
    if not 0 <= axis <= 2:
        raise ValueError("Invalid calibrated accelerometer axis")
    if not 2 <= amplitude_half_steps <= 16:
        raise ValueError("Invalid calibrated amplitude threshold")
    if not 4 <= min_reversals <= 255:
        raise ValueError("Invalid calibrated reversal threshold")

    checksum = (
        sum(PROFILE_MAGIC) + axis + amplitude_half_steps + min_reversals
    ) & 0xFF
    nvm[0:2] = b"\x00\x00"
    nvm[2:PROFILE_SIZE] = bytes(
        (axis, amplitude_half_steps, min_reversals, checksum)
    )
    nvm[0:2] = bytes(PROFILE_MAGIC)
