# Halloween Costume: Gesture-to-Light Firmware

CircuitPython firmware for two Adafruit Circuit Playground Bluefruit boards. Reads the onboard
accelerometer (tap engine + custom motion detectors) and lights up the 10-pixel NeoPixel ring in
response to gestures: double tap, fist bump, and jazz hands.

See [plan.md](plan.md) for the full project plan, BOM, and design decisions.

## Repo layout

```
firmware/
  blink/            # tiny standalone smoke test (verify board/cable/CircuitPython install)
  costume/          # the real project - this is what gets copied onto the board
    code.py         # CircuitPython entry point (must keep this exact filename)
    main.py         # game loop wiring everything together
    hardware/       # the only code that touches board/neopixel/adafruit_lis3dh
    gestures/       # pure-logic gesture detectors (hardware-import-free, desktop-testable)
    responses/      # pure-logic light animations (hardware-import-free, desktop-testable)
tests/              # desktop pytest suite for gestures/ and responses/ logic
```

## Prerequisites

- A code editor - [VS Code](https://code.visualstudio.com/) is what this project was built with.
- **Python 3.10 or newer** on your computer (for running the desktop test suite - this is
  separate from CircuitPython, which runs _on_ the board).
- Locate the CircutPython website (https://circuitpython.org/board/circuitplayground_bluefruit/) and download the UF2 file for
  Adafruit Circuit Playground Bluefruit. Follow those instructions to install on the device. 
- An Adafruit Circuit Playground Bluefruit and a USB cable that carries data (not just power -
  see plan.md's cable troubleshooting notes if `CIRCUITPY` doesn't show up as a drive).

## Setup

### macOS

```bash
python3 --version   # confirm 3.10+; if not, install from https://www.python.org/downloads/macos/
cd halloween2026
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements-dev.txt
pytest               # should show all tests passing, no board needed for this
pip install circup
```

Plug in the board, then install the CircuitPython libraries it needs:

```bash
circup install neopixel adafruit_lis3dh
```

Sync your code to the board (repeat this any time you change a file under `firmware/costume/`):

```bash
rsync -av --exclude '__pycache__' firmware/costume/ /Volumes/CIRCUITPY/
```

### Windows

```powershell
python --version   # confirm 3.10+; if not, install from https://www.python.org/downloads/windows/
cd halloween2026
python -m venv .venv
.venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements-dev.txt
pytest
pip install circup
```

Plug in the board (it will appear as a new drive letter, e.g. `D:\`), then:

```powershell
circup install neopixel adafruit_lis3dh
```

Sync your code to the board (replace `D:` with your board's actual drive letter):

```powershell
robocopy firmware\costume D:\ /E /XD __pycache__
```

#### View serial output in VS Code

The VS Code integrated terminal is a command prompt, not a serial monitor. To see the
board's CircuitPython output:

1. Connect the board to your computer with a USB data cable and make sure it is running
   from its `CIRCUITPY` drive.
2. In VS Code, open **Extensions** by clicking the Extensions icon in the Activity Bar
   or pressing `Ctrl+Shift+X`.
3. Search for **Serial Monitor**. Choose the extension published by **Microsoft**, then
   click **Install**. The first time, VS Code may ask whether you trust the extension;
   confirm to proceed.
4. Open the Command Palette with `Ctrl+Shift+P`, type **Serial Monitor: Focus on Serial
   Monitor View**, and press `Enter`. If that command is not listed, check that the
   extension finished installing.
5. In the Serial Monitor view, select the board's **COM port** and set the baud rate to
   **115200**. If you are unsure which COM port belongs to the board, unplug the board,
   check the available ports, then plug it back in and choose the newly appearing port.
6. Press **Button A** on the board to turn on debug output. The status LED turns on and
   acceleration readings or detected gestures appear in the monitor. Press Button A
   again to turn debug output off.
7. Locate the Start Monitoring button in the Serial Monitor and click Start. 

If the monitor is blank, confirm that the program is running from `CIRCUITPY` with
`code.py` at the drive's root, and that the board's required CircuitPython libraries
are installed. Connect the monitor, then press the board's **Reset** button once to
restart the program and reveal any startup error messages. Close other serial-monitor
applications while using the VS Code monitor, since only one application can use the
board's serial port at a time.

### WSL (Windows Subsystem for Linux)

WSL can run the desktop test suite just fine, but **USB devices (the board's serial port and its
`CIRCUITPY` drive) are not visible inside WSL by default** - WSL2 doesn't pass through USB hardware
automatically. You have two options:

**Option A (simplest): do hardware steps from native Windows, everything else from WSL.**
Use WSL for editing code and running `pytest`. Use a regular Windows PowerShell/Command Prompt
window (not WSL) for `circup` and copying files to the board's drive letter, following the
Windows steps above.

**Option B: share the USB device into WSL** using
[usbipd-win](https://github.com/dorchard/usbipd-win) if you want everything in one WSL terminal.
This is more setup and not necessary for this project - Option A is recommended for new
developers.

Either way, the desktop test suite itself works the same as on native Linux:

```bash
python3 --version   # confirm 3.10+
cd halloween2026
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements-dev.txt
pytest
```

## Everyday workflow

1. Edit files under `firmware/costume/`.
2. Run `pytest` to check the gesture/response logic you changed (no board needed).
3. Sync to the board (`rsync` on macOS/Linux, `robocopy` on Windows - see above).
4. Watch it run: open a serial console to see debug output (press **Button A** on the board to
   toggle debug prints on/off).
5. To test fully wireless/untethered, eject the `CIRCUITPY` drive first, then unplug and move the
   USB cable to a battery pack instead of your computer.

## Troubleshooting

- **No `CIRCUITPY` drive appears**: try a different USB cable (some are power-only, not data) -
  see plan.md's "Notes" section for the full diagnostic steps.
- **Board shows `CPLAYBTBOOT` instead of `CIRCUITPY`**: CircuitPython needs to be (re)installed -
  download the `.uf2` from [circuitpython.org](https://circuitpython.org/board/circuitplayground_bluefruit/)
  and drag it onto `CPLAYBTBOOT`.
- **`pytest` fails with an unrelated-looking import error**: make sure your virtual environment
  (`.venv`) is activated and using a modern Python (3.10+), not an old system Python.
