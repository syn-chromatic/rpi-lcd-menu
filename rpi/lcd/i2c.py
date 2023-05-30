import time

from lcd.api import LCDAPI
from x_gpio import GPIOI2C

# PCF8574 pin definitions
MASK_RS = 0x01  # P0
MASK_RW = 0x02  # P1
MASK_E = 0x04  # P2

SHIFT_BACKLIGHT = 3  # P3
SHIFT_DATA = 4  # P4-P7


class I2CLCD(LCDAPI):
    def __init__(self, i2c_bus: int, i2c_addr: int, rows: int, chars: int):
        self.gpio = GPIOI2C(i2c_bus, i2c_addr)
        self.gpio.write_device([0])
        self.hal_initialize_lcd()

        super().__init__(rows, chars)

        cmd = self.LCD_FUNCTION
        if rows > 1:
            cmd |= self.LCD_FUNCTION_2LINES
        self.hal_write_command(cmd)

    def hal_initialize_lcd(self):
        self.hal_power_up()
        self.hal_reset()
        self.hal_function()

    def hal_power_up(self):
        time.sleep(0.020)

    def hal_reset(self):
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        time.sleep(0.005)
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        time.sleep(0.001)
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        time.sleep(0.001)

    def hal_function(self):
        self.hal_write_init_nibble(self.LCD_FUNCTION)
        time.sleep(0.001)

    def hal_write_init_nibble(self, nibble):
        "Put LCD into 4-bit mode."
        byte = ((nibble >> 4) & 0x0F) << SHIFT_DATA
        self.gpio.write_device([byte | MASK_E])
        self.gpio.write_device([byte])

    def hal_backlight_on(self):
        self.gpio.write_device([1 << SHIFT_BACKLIGHT])

    def hal_backlight_off(self):
        self.gpio.write_device([0])

    def hal_write_command(self, cmd):
        byte = (self.backlight << SHIFT_BACKLIGHT) | (((cmd >> 4) & 0x0F) << SHIFT_DATA)
        self.gpio.write_device([byte | MASK_E])
        self.gpio.write_device([byte])
        byte = (self.backlight << SHIFT_BACKLIGHT) | ((cmd & 0x0F) << SHIFT_DATA)
        self.gpio.write_device([byte | MASK_E])
        self.gpio.write_device([byte])
        if cmd <= 3:
            time.sleep(0.005)

    def hal_write_data(self, data):
        byte = (
            MASK_RS
            | (self.backlight << SHIFT_BACKLIGHT)
            | (((data >> 4) & 0x0F) << SHIFT_DATA)
        )

        self.gpio.write_device([byte | MASK_E])
        self.gpio.write_device([byte])
        byte = (
            MASK_RS
            | (self.backlight << SHIFT_BACKLIGHT)
            | ((data & 0x0F) << SHIFT_DATA)
        )
        self.gpio.write_device([byte | MASK_E])
        self.gpio.write_device([byte])
