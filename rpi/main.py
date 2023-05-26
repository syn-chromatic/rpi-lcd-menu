from time import sleep

from lcd import LCDWriter
from button import Button
from options import (
    MenuOption,
    Option1,
    Option2,
    Option3,
    Option4,
    Option5,
    Option6,
    SystemInfo,
    CPUName,
    CPUPerc,
    CPUFreq,
)


UP_BUTTON_PIN = 5
DOWN_BUTTON_PIN = 6
APPLY_BUTTON_PIN = 4
LCD_ROWS = 2
LCD_CHARS = 16


class LCDMenuBase:
    def __init__(self, rows: int, chars: int, options: dict[MenuOption, dict]):
        self._rows = rows
        self._chars = chars
        self._selected = 0
        self._options = options

    def _get_options_list(self) -> list[MenuOption]:
        options_list = list(self._options.keys())
        return options_list

    def _get_option_range(self) -> tuple[int, int]:
        if self._selected < self._rows:
            st_range = 0
            en_range = self._rows
            return st_range, en_range

        st_range = self._selected - (self._rows - 1)
        en_range = st_range + self._rows
        return st_range, en_range


class LCDMenu(LCDMenuBase):
    def __init__(self, rows: int, chars: int, options: dict[MenuOption, dict]):
        super().__init__(rows, chars, options)

    def increment_selection(self):
        if self._selected < len(self._options) - 1:
            self._selected += 1
            return
        self._selected = 0

    def decrement_selection(self):
        if self._selected > 0:
            self._selected -= 1
            return
        self._selected = len(self._options) - 1

    def get_string(self) -> str:
        st_range, en_range = self._get_option_range()
        options_list = self._get_options_list()

        string = ""
        for idx in range(st_range, en_range):
            option = options_list[idx]
            option.update()
            option_name = option.get_option_name()
            if idx == self._selected:
                string += "> " + option_name + "\n"
                continue
            string += "x " + option_name + "\n"
        return string

    def enter_option(self):
        options_list = self._get_options_list()
        option_str = options_list[self._selected]
        options = self._options[option_str]
        if options:
            self._options = options
            self._selected = 0


option_1 = Option1()
option_2 = Option2()
option_3 = Option3()
option_4 = Option4()
option_5 = Option5()
option_6 = Option6()
system_info = SystemInfo()
cpu_name = CPUName()
cpu_perc = CPUPerc()
cpu_freq = CPUFreq()


system_menu: dict[MenuOption, dict] = {
    cpu_name: {},
    cpu_perc: {},
    cpu_freq: {},
}

main_menu: dict[MenuOption, dict] = {
    option_1: {},
    option_2: {},
    option_3: {},
    option_4: {},
    option_5: {},
    option_6: {},
    system_info: system_menu,
}


screen = LCDWriter(LCD_ROWS, LCD_CHARS)
menu = LCDMenu(LCD_ROWS, LCD_CHARS, main_menu)

string = menu.get_string()
screen.write_with_cursor(string, 0.0)

up_button = Button(UP_BUTTON_PIN)
down_button = Button(DOWN_BUTTON_PIN)
apply_button = Button(APPLY_BUTTON_PIN)

counter = 0
while True:
    counter += 1
    if up_button.is_pressed():
        print("Up Button Pressed")
        menu.decrement_selection()
        string = menu.get_string()
        screen.write_with_cursor(string, 0.0)

    if down_button.is_pressed():
        print("Down Button Pressed")
        menu.increment_selection()
        string = menu.get_string()
        screen.write_with_cursor(string, 0.0)

    if apply_button.is_pressed():
        print("Apply Button Pressed")
        menu.enter_option()
        string = menu.get_string()
        screen.write_with_cursor(string, 0.0)

    if counter == 100:
        string = menu.get_string()
        screen.write_with_cursor(string, 0.0)
        counter = 0

    sleep(0.01)
