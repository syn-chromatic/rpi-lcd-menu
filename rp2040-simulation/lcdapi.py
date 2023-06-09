import time
from wgpio import I2CGPIO


class LCDAPI:
    LCD_CLR = 0x01  # DB0: clear display
    LCD_HOME = 0x02  # DB1: return to home position

    LCD_ENTRY_MODE = 0x04  # DB2: set entry mode
    LCD_ENTRY_INC = 0x02  # --DB1: increment
    LCD_ENTRY_SHIFT = 0x01  # --DB0: shift

    LCD_ON_CTRL = 0x08  # DB3: turn lcd/cursor on
    LCD_ON_DISPLAY = 0x04  # --DB2: turn display on
    LCD_ON_CURSOR = 0x02  # --DB1: turn cursor on
    LCD_ON_BLINK = 0x01  # --DB0: blinking cursor

    LCD_MOVE = 0x10  # DB4: move cursor/display
    LCD_MOVE_DISP = 0x08  # --DB3: move display (0-> move cursor)
    LCD_MOVE_RIGHT = 0x04  # --DB2: move right (0-> left)

    LCD_FUNCTION = 0x20  # DB5: function set

    LCD_FUNCTION_8BIT = 0x10  # --DB4: set 8BIT mode (0->4BIT mode)
    LCD_FUNCTION_2LINES = 0x08  # --DB3: two lines (0->one line)
    LCD_FUNCTION_10DOTS = 0x04  # --DB2: 5x10 font (0->5x7 font)
    LCD_FUNCTION_RESET = 0x30  # See "Initializing by Instruction" section

    LCD_CGRAM = 0x40  # DB6: set CG RAM address
    LCD_DDRAM = 0x80  # DB7: set DD RAM address

    LCD_RS_CMD = 0
    LCD_RS_DATA = 1

    LCD_RW_WRITE = 0
    LCD_RW_READ = 1

    # I2C expander pin configuration
    EN = 0x04  # Enable bit
    RW = 0x02  # Read/Write bit
    RS = 0x01  # Register select bit
    BACKLIGHT = 0x08  # Backlight bit

    def __init__(self, bus: int, address: int, rows: int, columns: int):
        self.rows = rows
        self.columns = columns
        self.gpio = I2CGPIO(bus, address)
        self.cursor_x = 0
        self.cursor_y = 0
        self.implied_newline = False
        self.backlight = True
        self.initialize_display()

    def initialize_display(self):
        self.display_off()
        self.backlight_on()
        self.clear()
        self.initialize_4bit_mode()
        self.set_entry_mode()
        self.hide_cursor()
        self.display_on()

    def initialize_4bit_mode(self):
        self.hal_send_bytes(0x03, mode=0)
        self.hal_pulse_enable(0x03)
        self.hal_sleep_us(4500)

        self.hal_send_bytes(0x03, mode=0)
        self.hal_pulse_enable(0x03)
        self.hal_sleep_us(4500)

        self.hal_send_bytes(0x03, mode=0)
        self.hal_pulse_enable(0x03)
        self.hal_sleep_us(150)

        self.hal_send_bytes(0x02, mode=0)  # Set 4-bit mode
        self.hal_pulse_enable(0x02)
        self.hal_write_command(self.LCD_FUNCTION | self.LCD_FUNCTION_2LINES)

    def set_entry_mode(self):
        self.hal_write_command(self.LCD_ENTRY_MODE | self.LCD_ENTRY_INC)

    def clear(self):
        self.hal_write_command(self.LCD_CLR)
        self.hal_write_command(self.LCD_HOME)
        self.cursor_x = 0
        self.cursor_y = 0

    def show_cursor(self):
        self.hal_write_command(
            self.LCD_ON_CTRL | self.LCD_ON_DISPLAY | self.LCD_ON_CURSOR
        )

    def hide_cursor(self):
        self.hal_write_command(self.LCD_ON_CTRL | self.LCD_ON_DISPLAY)

    def blink_cursor_on(self):
        self.hal_write_command(
            self.LCD_ON_CTRL
            | self.LCD_ON_DISPLAY
            | self.LCD_ON_CURSOR
            | self.LCD_ON_BLINK
        )

    def blink_cursor_off(self):
        self.hal_write_command(
            self.LCD_ON_CTRL | self.LCD_ON_DISPLAY | self.LCD_ON_CURSOR
        )

    def display_on(self):
        self.hal_write_command(self.LCD_ON_CTRL | self.LCD_ON_DISPLAY)

    def display_off(self):
        self.hal_write_command(self.LCD_ON_CTRL)

    def backlight_on(self):
        self.backlight = True
        self.hal_backlight_on()

    def backlight_off(self):
        self.backlight = False
        self.hal_backlight_off()

    def get_backlight_state(self) -> bool:
        return self.backlight

    def move_to(self, cursor_x: int, cursor_y: int):
        self.cursor_x = cursor_x
        self.cursor_y = cursor_y
        addr = cursor_x & 0x3F
        if cursor_y & 1:
            addr += 0x40  # Lines 1 & 3 add 0x40
        if cursor_y & 2:  # Lines 2 & 3 add number of columns
            addr += self.columns
        self.hal_write_command(self.LCD_DDRAM | addr)

    def handle_new_line(self):
        if self.implied_newline:
            self.implied_newline = False
            return
        self.cursor_x = self.columns

    def put_character_code(self, char_code: int):
        if char_code == 10:
            self.handle_new_line()
        else:
            self.hal_write_data(char_code)
            self.cursor_x += 1

        if self.cursor_x >= self.columns:
            self.cursor_x = 0
            self.cursor_y += 1
            self.implied_newline = char_code != 10

        if self.cursor_y >= self.rows:
            self.cursor_y = 0

        self.move_to(self.cursor_x, self.cursor_y)

    def put_character(self, char: str):
        char_code = ord(char)
        self.put_character_code(char_code)

    def put_string(self, string: str):
        for char in string:
            self.put_character(char)

    def put_custom_char(self, location: int, charmap: list[int]) -> None:
        location &= 0x7
        self.hal_write_command(self.LCD_CGRAM | (location << 3))
        self.hal_sleep_us(40)
        for i in range(8):
            self.hal_write_data(charmap[i])
            self.hal_sleep_us(40)
        self.move_to(self.cursor_x, self.cursor_y)

    def hal_backlight_on(self):
        self.BACKLIGHT = 0x08
        self.gpio.write_device([self.BACKLIGHT])

    def hal_backlight_off(self):
        self.BACKLIGHT = 0x00
        self.gpio.write_device([self.BACKLIGHT])

    def hal_write_command(self, cmd):
        self.hal_send_bytes(cmd, mode=0)

    def hal_write_data(self, data):
        self.hal_send_bytes(data, mode=self.RS)

    def hal_send_bytes(self, data: int, mode: int):
        high_bits = mode | (data & 0xF0) | self.BACKLIGHT
        low_bits = mode | ((data << 4) & 0xF0) | self.BACKLIGHT

        # Write high 4-bits
        self.gpio.write_device([high_bits])
        self.hal_pulse_enable(high_bits)

        # Write low 4-bits
        self.gpio.write_device([low_bits])
        self.hal_pulse_enable(low_bits)

    def hal_pulse_enable(self, data):
        self.gpio.write_device([data | self.EN])
        # self.hal_sleep_us(1)
        self.gpio.write_device([data & ~self.EN])
        # self.hal_sleep_us(50)

    @staticmethod
    def hal_sleep_us(microseconds: int):
        time.sleep(microseconds / 1_000_000)

    @staticmethod
    def hal_sleep_ms(milliseconds: int):
        time.sleep(milliseconds / 1_000)
