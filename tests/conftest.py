import sys
from pathlib import Path

# Gesture/response logic lives under firmware/costume/ with no hardware
# imports, so it can be imported directly here without a board attached.
FIRMWARE_ROOT = Path(__file__).resolve().parent.parent / "firmware" / "costume"
sys.path.insert(0, str(FIRMWARE_ROOT))
