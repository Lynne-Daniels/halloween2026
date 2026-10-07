import board
import busio
import digitalio
import neopixel
import adafruit_lis3dh

from hardware import config as cfg

_REG_CLICKSRC = 0x39
_DOUBLE_CLICK_BIT = 0x20
# On real hardware, double-click alone (CLICK_CFG with only XD/YD/ZD set)
# failed to register reliably - also enabling single-click bits (XS/YS/ZS)
# makes double-tap detection work, so we enable both but only ever act on
# the DCLICK bit in software (see read_double_tap below).
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

    def read_double_tap(self):
        # `.tapped` can't distinguish single vs double here since both are
        # enabled at the chip level, so read the DCLICK bit directly -
        # single-click events are enabled on-chip (needed for reliable
        # double-tap detection) but never surfaced in software.
        if not self._int1.value:
            return False
        raw = self._lis3dh._read_register_byte(_REG_CLICKSRC)
        return bool(raw & _DOUBLE_CLICK_BIT)

    def button_a_pressed(self):
        return self._button_a.value

    def set_status_led(self, on):
        self._status_led.value = on

    def show(self, pixel_buffer):
        for i, color in enumerate(pixel_buffer):
            self.pixels[i] = color
        self.pixels.show()
