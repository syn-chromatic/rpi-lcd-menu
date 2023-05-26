from time import sleep

from lcd import LCDWriter
from button import Button


UP_BUTTON_PIN = 5
DOWN_BUTTON_PIN = 6
LCD_ROWS = 2
LCD_CHARS = 16


class LCDMenuBase:
    def __init__(self, rows: int, chars: int):
        self._rows = rows
        self._chars = chars
        self._selected = 0

    def _get_option_range(self) -> tuple[int, int]:
        if self._selected < self._rows:
            st_range = 0
            en_range = self._rows
            return st_range, en_range

        st_range = self._selected - self._rows - 1
        en_range = st_range + self._rows
        return st_range, en_range


class LCDMenu(LCDMenuBase):
    def __init__(self, rows: int, chars: int):
        super().__init__(rows, chars)

    def increment_selection(self, options: list[str]):
        if self._selected < len(options) - 1:
            self.selected += 1
            return
        self.selected = 0

    def decrement_selection(self, options: list[str]):
        if self.selected > 0:
            self.selected -= 1
            return
        self.selected = len(options) - 1

    def get_string(self, options: list[str]) -> str:
        st_range, en_range = self._get_option_range()

        string = ""
        for idx in range(st_range, en_range):
            option = options[idx]
            if idx == self.selected:
                string += "> " + option + "\n"
                continue
            string += "x " + option + "\n"
        return string


options = [
    "Option 1",
    "Option 2",
    "Option 3",
    "Option 4",
    "Option 5",
    "Option 6",
    "System Info",
]


screen = LCDWriter(LCD_ROWS, LCD_CHARS)
menu = LCDMenu(LCD_ROWS, LCD_CHARS)

string = menu.get_string(options)
screen.write_with_cursor(string, 0.0)

up_button = Button(UP_BUTTON_PIN)
down_button = Button(DOWN_BUTTON_PIN)


while True:
    if up_button.is_pressed():
        print("Up Button Pressed")
        menu.decrement_selection(options)
        string = menu.get_string(options)
        screen.write_with_cursor(string, 0.0)

    if down_button.is_pressed():
        print("Down Button Pressed")
        menu.increment_selection(options)
        string = menu.get_string(options)
        screen.write_with_cursor(string, 0.0)

    sleep(0.01)
