from lcd_api import LCDAPI
from wgpio import GPIOI2C

# PCF8574 pin definitions
MASK_RS = 0x01  # P0
MASK_RW = 0x02  # P1
MASK_E = 0x04  # P2

SHIFT_BACKLIGHT = 3  # P3
SHIFT_DATA = 4  # P4-P7


class I2CLCD(LCDAPI):
    def __init__(self, bus: int, address: int, rows: int, columns: int):
        self.gpio = GPIOI2C(bus, address, 400000)
        self.gpio.write_device([0])
        self.hal_initialize_lcd()
        super().__init__(rows, columns)
        self.hal_command()

    def hal_initialize_lcd(self):
        self.hal_power_up()
        self.hal_reset()
        self.hal_function()

    def hal_power_up(self):
        self.hal_sleep_ms(20)

    def hal_reset(self):
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        self.hal_sleep_ms(5)
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        self.hal_sleep_ms(1)
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        self.hal_sleep_ms(1)

    def hal_function(self):
        self.hal_write_init_nibble(self.LCD_FUNCTION)
        self.hal_sleep_ms(1)

    def hal_command(self):
        cmd = self.LCD_FUNCTION
        if self.rows > 1:
            cmd |= self.LCD_FUNCTION_2LINES
        self.hal_write_command(cmd)

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
            self.hal_sleep_ms(5)

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
