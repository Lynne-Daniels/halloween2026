# Tunable constants for gesture detection and light responses.
# All values here are starting points; expect to retune against the real
# board/wearer in Phase F (see plan.md).

# --- Main loop ---
LOOP_SLEEP = 0.01  # ~100 Hz poll rate

# --- Gesture conflict resolution ---
GESTURE_PRIORITY = ("double_tap", "fist_bump", "jazz_hands")
GESTURE_COOLDOWN_S = 0.5  # lockout after any trigger, prevents double-firing

# --- Hardware tap engine (LIS3DH), double-tap only ---
TAP_CLICK_THRESHOLD = 80  # LIS3DH register units (0-127); retune on hardware
TAP_TIME_LIMIT = 10
TAP_TIME_LATENCY = 20
TAP_TIME_WINDOW = 255

# --- Fist bump: acceleration spike then sudden stop, any direction ---
RESTING_GRAVITY = 9.8  # m/s^2, ~1g when the board is still
FIST_BUMP_PUNCH_THRESHOLD = 20.0  # m/s^2 magnitude indicating a punch spike
FIST_BUMP_WINDOW_S = 0.4  # max time allowed between spike and settle
FIST_BUMP_SETTLE_BAND = 2.0  # +/- m/s^2 around RESTING_GRAVITY counts as "stopped"

# --- Jazz hands: oscillation / zero-crossing counter ---
JAZZ_HANDS_WINDOW_S = 1.5  # rolling window of samples considered
JAZZ_HANDS_MIN_REVERSALS = 4  # sign changes required within the window
JAZZ_HANDS_MIN_AMPLITUDE = 3.0  # m/s^2 deviation from mean to count as a reversal

# --- NeoPixel ring ---
NUM_PIXELS = 10
COLORS = {
    "cyan": (0, 255, 255),
    "orange": (255, 80, 0),
    "red": (255, 0, 0),
    "off": (0, 0, 0),
}
# Placeholder opposite-arc groups for fist bump; confirm against the physical
# ring layout in Phase F and adjust here.
FIST_BUMP_ARC_A = (0, 1)
FIST_BUMP_ARC_B = (5, 6)
JAZZ_HANDS_CHASE_SPEED = 6.0  # pixels per second

RESPONSE_DURATIONS = {
    "double_tap": 0.6,
    "jazz_hands": 2.5,
    "fist_bump": 1.2,
}
