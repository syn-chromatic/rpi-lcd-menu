import lgpio as gp

from time import sleep
from typing import Literal

from rpi_i2c_lcd import I2cLcd


UP_BUTTON_PIN = 5
DOWN_BUTTON_PIN = 6


class I2CScreenBase:
    def __init__(self, chars: int, rows: int):
        self._chars = chars
        self._rows = rows
        self._cur_row = 0
        self._row_states = [0] * rows
        self._lcd = self._get_lcd()
        self._row_data = []

    def _get_lcd(self):
        lcd = I2cLcd(1, 0x27, self._rows, self._chars)
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


class I2CScreen(I2CScreenBase):
    def __init__(self, chars: int, rows: int):
        super().__init__(chars, rows)

    def write_with_cursor(self, string: str, hold_time: float):
        self._write_with_cursor(string, hold_time)


class Button:
    def __init__(self, bcm_pin: int):
        self.bcm_pin = bcm_pin
        self.handle = self.register_pin()
        self.state = 0
        self.p_state = 1

    def register_pin(self):
        handle = gp.gpiochip_open(0)
        gp.gpio_claim_input(handle, self.bcm_pin)
        return handle

    def get_state(self) -> Literal[0, 1]:
        self.state = gp.gpio_read(self.handle, self.bcm_pin)
        return self.state

    def is_pressed(self) -> bool:
        state = self.get_state()
        bool_state = False
        if self.p_state == 0 and state == 1:
            bool_state = True
        self.p_state = state
        return bool_state

    def __del__(self):
        if hasattr(self, "hanlde"):
            gp.gpiochip_close(self.handle)


screen = I2CScreen(16, 2)

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
    if selected < 2:
        option_st_range = 0
        option_en_range = 2

    else:
        option_st_range = selected - 1
        option_en_range = option_st_range + 2

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


up_button = Button(UP_BUTTON_PIN)
down_button = Button(DOWN_BUTTON_PIN)


while True:
    if up_button.is_pressed():
        print("Up Button Pressed")
        selected = decrement_selection(options, selected)
        string = get_string(options, selected)
        screen.write_with_cursor(string, 0.0)

    if down_button.is_pressed():
        print("Down Button Pressed")
        selected = increment_selection(options, selected)
        string = get_string(options, selected)
        screen.write_with_cursor(string, 0.0)

    sleep(0.01)
