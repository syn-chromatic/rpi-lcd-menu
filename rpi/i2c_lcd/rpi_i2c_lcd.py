import time
import lgpio as gp

from lcd_api import LcdApi

# PCF8574 pin definitions
MASK_RS = 0x01  # P0
MASK_RW = 0x02  # P1
MASK_E = 0x04  # P2

SHIFT_BACKLIGHT = 3  # P3
SHIFT_DATA = 4  # P4-P7


class I2cLcd(LcdApi):
    def __init__(self, i2c_bus, i2c_addr, rows, chars):
        self.handle = gp.i2c_open(i2c_bus, i2c_addr)
        gp.i2c_write_device(self.handle, [0])
        time.sleep(0.020)  # Allow LCD time to powerup
        # Send reset 3 times
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        time.sleep(0.005)
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        time.sleep(0.001)
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        time.sleep(0.001)
        # Put LCD into 4-bit mode
        self.hal_write_init_nibble(self.LCD_FUNCTION)
        time.sleep(0.001)
        LcdApi.__init__(self, rows, chars)
        cmd = self.LCD_FUNCTION
        if rows > 1:
            cmd |= self.LCD_FUNCTION_2LINES
        self.hal_write_command(cmd)

    def hal_write_init_nibble(self, nibble):
        byte = ((nibble >> 4) & 0x0F) << SHIFT_DATA
        gp.i2c_write_device(self.handle, [byte | MASK_E])
        gp.i2c_write_device(self.handle, [byte])

    def hal_backlight_on(self):
        gp.i2c_write_device(self.handle, [1 << SHIFT_BACKLIGHT])

    def hal_backlight_off(self):
        gp.i2c_write_device(self.handle, [0])

    def hal_write_command(self, cmd):
        byte = (self.backlight << SHIFT_BACKLIGHT) | (((cmd >> 4) & 0x0F) << SHIFT_DATA)
        gp.i2c_write_device(self.handle, [byte | MASK_E])
        gp.i2c_write_device(self.handle, [byte])
        byte = (self.backlight << SHIFT_BACKLIGHT) | ((cmd & 0x0F) << SHIFT_DATA)
        gp.i2c_write_device(self.handle, [byte | MASK_E])
        gp.i2c_write_device(self.handle, [byte])
        if cmd <= 3:
            time.sleep(0.005)

    def hal_write_data(self, data):
        byte = (
            MASK_RS
            | (self.backlight << SHIFT_BACKLIGHT)
            | (((data >> 4) & 0x0F) << SHIFT_DATA)
        )
        gp.i2c_write_device(self.handle, [byte | MASK_E])
        gp.i2c_write_device(self.handle, [byte])
        byte = (
            MASK_RS
            | (self.backlight << SHIFT_BACKLIGHT)
            | ((data & 0x0F) << SHIFT_DATA)
        )
        gp.i2c_write_device(self.handle, [byte | MASK_E])
        gp.i2c_write_device(self.handle, [byte])
