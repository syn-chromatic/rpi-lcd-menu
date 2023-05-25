from machine import I2C, Pin
from time import sleep
from pico_i2c_lcd import I2cLcd


class I2CScreenBase:
    def __init__(self, chars: int, rows: int):
        self._chars = chars
        self._rows = rows
        self._cur_row = 0
        self._row_states = [0] * rows
        self._i2c = self._get_i2c()
        self._i2c_address = self._get_i2c_address()
        self._lcd = self._get_lcd()
        self._row_data = []

    def _get_i2c(self):
        i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
        return i2c

    def _get_i2c_address(self):
        i2c_address = self._i2c.scan()[0]
        return i2c_address

    def _get_lcd(self):
        i2c = self._i2c
        i2c_address = self._i2c_address
        chars = self._chars
        rows = self._rows
        lcd = I2cLcd(i2c, i2c_address, rows, chars)
        return lcd

    def _increment_row(self):
        if self._cur_row < self._rows - 1:
            self._cur_row += 1
            return
        self._cur_row = 0

    def _set_row_state(self, string: str):
        self._row_states[self._cur_row] = len(string)

    def _get_row_fill(self, string: str) -> str:
        row_state = self._row_states[self._cur_row]
        fill = row_state - len(string)
        if fill > 0:
            char_fill = " " * fill
            return char_fill
        return ""

    def _insert_row_data(self, string: str):
        if len(self._row_data) - 1 < self._cur_row:
            self._row_data.insert(self._cur_row, string)
            return
        self._row_data[self._cur_row] = string

    def _get_string_changes(
        self, string: str, row_data: str
    ) -> list[tuple[str, int, int]]:
        changes = []
        max_idx = len(row_data) - 1
        for idx in range(len(string)):
            char1 = string[idx]
            if idx <= max_idx:
                char2 = row_data[idx]
                if char1 != char2:
                    changes.append((char1, idx, self._cur_row))
                continue
            changes.append((char1, idx, self._cur_row))
        return changes

    def _put_str(self, string: str):
        if len(self._row_data) - 1 < self._cur_row:
            self._lcd.move_to(0, self._cur_row)
            self._insert_row_data(string)
            row_fill = self._get_row_fill(string)
            self._lcd.putstr(string)
            self._lcd.putstr(row_fill)
            self._lcd.move_to(len(string), self._cur_row)
            self._set_row_state(string)
            self._increment_row()
            return
        row_data = self._row_data[self._cur_row]
        changes = self._get_string_changes(string, row_data)

        for char, idx, row in changes:
            self._lcd.move_to(idx, row)
            self._lcd.putstr(char)
        row_fill = self._get_row_fill(string)
        self._lcd.putstr(row_fill)
        self._lcd.move_to(len(string), self._cur_row)
        self._insert_row_data(string)
        self._set_row_state(string)
        self._increment_row()

    def _seg_string(self, string: str) -> list[str]:
        string = string.strip()
        lines = string.split("\n")
        segments = []
        for line in lines:
            words = line.split(" ")
            segment = ""
            for word in words:
                if len(segment) + len(word) > 20:
                    segments.append(segment.strip())
                    segment = word + " "
                else:
                    segment += word + " "
            segments.append(segment.strip())
        return segments

    def _write_with_cursor(self, string: str, hold_time: float):
        self._lcd.blink_cursor_on()
        segments = self._seg_string(string)
        for segment in segments:
            self._put_str(segment)
        sleep(hold_time)
        self._lcd.blink_cursor_off()

    def _write_address(self):
        string = "I2C Address: {}"
        string = string.format(self._i2c_address)
        self._write_with_cursor(string, 2)


class I2CScreen(I2CScreenBase):
    def __init__(self, chars: int, rows: int):
        super().__init__(chars, rows)

    def write_with_cursor(self, string: str, hold_time: float):
        self._write_with_cursor(string, hold_time)


screen = I2CScreen(20, 4)

selected = 0
options = [
    "Option 1",
    "Option 2",
    "Option 3",
    "Option 4",
    "Option 5",
    "Option 6",
    "System Info",
]


def get_string(options: list[str], selected: int):
    if selected < 3:
        option_st_range = 0
        option_en_range = 4

    else:
        option_st_range = selected - 3
        option_en_range = option_st_range + 4

    string = ""

    for idx in range(option_st_range, option_en_range):
        option = options[idx]
        if idx == selected:
            string += "> " + option + "\n"
            continue
        string += "x " + option + "\n"
    return string


string = get_string(options, selected)
screen.write_with_cursor(string, 0.0)


def increment_selection(options: list[str], selected: int):
    if selected < len(options) - 1:
        selected += 1
        return selected
    return 0


def decrement_selection(options: list[str], selected: int):
    if selected > 0:
        selected -= 1
        return selected
    return len(options) - 1


up_button = Pin(10, Pin.IN, Pin.PULL_UP)
down_button = Pin(11, Pin.IN, Pin.PULL_UP)

state = 0

while True:
    if up_button.value() == 0:
        if state == 0:
            selected = decrement_selection(options, selected)
            string = get_string(options, selected)
            screen.write_with_cursor(string, 0.0)
            while up_button.value() == 0:
                state = 1
        else:
            while up_button.value() == 0:
                state = 0

    if down_button.value() == 0:
        if state == 0:
            selected = increment_selection(options, selected)
            string = get_string(options, selected)
            screen.write_with_cursor(string, 0.0)
            while down_button.value() == 0:
                state = 1
        else:
            while down_button.value() == 0:
                state = 0
