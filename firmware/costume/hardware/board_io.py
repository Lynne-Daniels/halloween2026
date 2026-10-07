import board
import busio
import digitalio
import neopixel
import adafruit_lis3dh

from hardware import config as cfg

_REG_CLICKSRC = 0x39
_SINGLE_CLICK_BIT = 0x10
_DOUBLE_CLICK_BIT = 0x20
# Enables single AND double click detection on all axes at once. The
# driver's built-in set_tap(tap=1) / set_tap(tap=2) modes only support one
# mode at a time, so we pass a custom CLICK_CFG value instead: bits
# XS,YS,ZS (single, 0x15) OR'd with XD,YD,ZD (double, 0x2A) = 0x3F.
_CLICK_CFG_SINGLE_AND_DOUBLE = 0x3F


class BoardIO:
    """Only module that imports board/busio/neopixel/adafruit_lis3dh/digitalio."""

    def __init__(self):
        self.pixels = neopixel.NeoPixel(board.NEOPIXEL, cfg.NUM_PIXELS, auto_write=False)

        i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
        self._int1 = digitalio.DigitalInOut(board.ACCELEROMETER_INTERRUPT)
        self._lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19, int1=self._int1)
        self._lis3dh.range = adafruit_lis3dh.RANGE_4_G
        self._lis3dh.set_tap(
            2,
            cfg.TAP_CLICK_THRESHOLD,
            time_limit=cfg.TAP_TIME_LIMIT,
            time_latency=cfg.TAP_TIME_LATENCY,
            time_window=cfg.TAP_TIME_WINDOW,
            click_cfg=_CLICK_CFG_SINGLE_AND_DOUBLE,
        )

        self._button_a = digitalio.DigitalInOut(board.BUTTON_A)
        self._button_a.switch_to_input(pull=digitalio.Pull.DOWN)

        self._status_led = digitalio.DigitalInOut(board.LED)
        self._status_led.direction = digitalio.Direction.OUTPUT

    def read_acceleration(self):
        return self._lis3dh.acceleration

    def read_tap_flags(self):
        # `.tapped` only reports "an interrupt latched", not which kind, so
        # we read the CLICK_SRC register bits directly to tell single vs
        # double apart (SCLICK=bit4, DCLICK=bit5). Uses a private driver
        # method since the public API has no equivalent - verify against
        # the installed adafruit_lis3dh version if this ever breaks.
        if not self._int1.value:
            return False, False
        raw = self._lis3dh._read_register_byte(_REG_CLICKSRC)
        single = bool(raw & _SINGLE_CLICK_BIT)
        double = bool(raw & _DOUBLE_CLICK_BIT)
        return single, double

    def button_a_pressed(self):
        return self._button_a.value

    def set_status_led(self, on):
        self._status_led.value = on

    def show(self, pixel_buffer):
        for i, color in enumerate(pixel_buffer):
            self.pixels[i] = color
        self.pixels.show()
