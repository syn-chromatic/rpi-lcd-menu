import time

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
        self._rows: int = rows
        self._chars: int = chars
        self._selected: int = 0
        self._options: dict[MenuOption, dict] = options
        self._entries: list[MenuOption] = []

    def _get_options_list(self) -> list[MenuOption]:
        options_list = list(self._options.keys())
        if self._entries:
            options_entry = None
            for entry in self._entries:
                options_entry = self._options[entry]
            if options_entry:
                entry_list = list(options_entry.keys())
                return entry_list
        return options_list

    def _get_option_range(self) -> tuple[int, int]:
        if self._selected < self._rows:
            st_range = 0
            en_range = self._rows
            return st_range, en_range

        st_range = self._selected - (self._rows - 1)
        en_range = st_range + self._rows
        return st_range, en_range

    def _add_entry(self, option: MenuOption):
        if option in self._options:
            if self._options[option]:
                self._entries.append(option)
                self._selected = 0

    def _back_entry(self):
        if self._entries:
            self._entries.pop(-1)


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

    def apply_selection(self):
        options_list = self._get_options_list()
        option = options_list[self._selected]
        self._add_entry(option)

    def back_selection(self):
        self._back_entry()


class MenuHandler:
    def __init__(self):
        self.main_menu = self.get_main_menu()
        self.screen = self.get_screen()
        self.lcd_menu = self.get_lcd_menu()
        self.up_button = self.get_up_button()
        self.down_button = self.get_down_button()
        self.apply_button = self.get_apply_button()

    def get_system_submenu(self) -> dict[MenuOption, dict]:
        cpu_name = CPUName()
        cpu_perc = CPUPerc()
        cpu_freq = CPUFreq()
        system_submenu: dict[MenuOption, dict] = {
            cpu_name: {},
            cpu_perc: {},
            cpu_freq: {},
        }
        return system_submenu

    def get_main_menu(self) -> dict[MenuOption, dict]:
        system_submenu = self.get_system_submenu()

        option_1 = Option1()
        option_2 = Option2()
        option_3 = Option3()
        option_4 = Option4()
        option_5 = Option5()
        option_6 = Option6()
        system_info = SystemInfo()

        main_menu: dict[MenuOption, dict] = {
            option_1: {},
            option_2: {},
            option_3: {},
            option_4: {},
            option_5: {},
            option_6: {},
            system_info: system_submenu,
        }
        return main_menu

    def get_screen(self) -> LCDWriter:
        screen = LCDWriter(LCD_ROWS, LCD_CHARS)
        return screen

    def get_lcd_menu(self) -> LCDMenu:
        lcd_menu = LCDMenu(LCD_ROWS, LCD_CHARS, self.main_menu)
        return lcd_menu

    def get_up_button(self) -> Button:
        up_button = Button(UP_BUTTON_PIN)
        return up_button

    def get_down_button(self) -> Button:
        down_button = Button(DOWN_BUTTON_PIN)
        return down_button

    def get_apply_button(self) -> Button:
        apply_button = Button(APPLY_BUTTON_PIN)
        return apply_button

    def increment_option(self):
        self.lcd_menu.increment_selection()
        string = self.lcd_menu.get_string()
        self.screen.write_with_cursor(string, 0.0)

    def decrement_option(self):
        self.lcd_menu.decrement_selection()
        string = self.lcd_menu.get_string()
        self.screen.write_with_cursor(string, 0.0)

    def apply_option(self):
        self.lcd_menu.apply_selection()
        string = self.lcd_menu.get_string()
        self.screen.write_with_cursor(string, 0.0)

    def update_options(self):
        string = self.lcd_menu.get_string()
        self.screen.write_with_cursor(string, 0.0)

    def loop(self):
        string = self.lcd_menu.get_string()
        self.screen.write_with_cursor(string, 0.0)

        counter = 0
        while True:
            counter += 1
            if self.up_button.is_pressed():
                print("Up Button Pressed")
                self.increment_option()

            if self.down_button.is_pressed():
                print("Down Button Pressed")
                self.decrement_option()

            if self.apply_button.is_pressed():
                print("Apply Button Pressed")
                self.apply_option()

            if counter == 100:
                self.update_options()
                counter = 0

            time.sleep(0.01)


if __name__ == "__main__":
    menu_handler = MenuHandler()
    menu_handler.loop()
