import time

from typing import Optional

from lcd import LCDWriter
from button import Button

from options.abstracts import Option, OptionToggle, OptionRange, OptionTimeHM
from options.item import MenuItem
from options.configurations import CPUName, CPUPerc, CPUFreq
from options.bases import StaticBase, RangeBase, ToggleBase, TimeBase


UP_BUTTON_PIN = 5
DOWN_BUTTON_PIN = 6
APPLY_BUTTON_PIN = 4
BACK_BUTTON_PIN = 27
LCD_ROWS = 2
LCD_CHARS = 16


class LCDMenuBase:
    def __init__(self, rows: int, chars: int, options: dict[Option, dict]):
        self._rows: int = rows
        self._chars: int = chars
        self._selected: int = 0
        self._options: dict[Option, dict] = options
        self._entries: list[tuple[int, Option]] = []

    def _get_options_list(self) -> list[Option]:
        if self._entries:
            _, entry_option = self._entries[0]
            option = self._options[entry_option]
            for _, entry_option in self._entries:
                option = self._options[entry_option]
            entry_list = list(option.keys())
            return entry_list
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

    def _add_entry(self, option: Option):
        if option in self._options:
            if self._options[option]:
                entry_idx = self._selected
                self._entries.append((entry_idx, option))
                self._selected = 0

    def _back_entry(self):
        if self._entries:
            entry_idx, _ = self._entries.pop(-1)
            self._selected = entry_idx

    def _get_option(self, options_list: list[Option], idx: int) -> Optional[Option]:
        if len(options_list) > idx:
            return options_list[idx]


class LCDMenu(LCDMenuBase):
    def __init__(self, rows: int, chars: int, options: dict[Option, dict]):
        super().__init__(rows, chars, options)

    def increment_selection(self):
        options_list = self._get_options_list()
        option = options_list[self._selected]

        if isinstance(option, (OptionRange, OptionTimeHM)):
            if option.get_hold_state():
                option.increment()
                option.update()
                return

        if self._selected < len(options_list) - 1:
            self._selected += 1
            return
        self._selected = 0

    def decrement_selection(self):
        options_list = self._get_options_list()
        option = options_list[self._selected]

        if isinstance(option, (OptionRange, OptionTimeHM)):
            if option.get_hold_state():
                option.decrement()
                option.update()
                return

        if self._selected > 0:
            self._selected -= 1
            return
        self._selected = len(options_list) - 1

    def update_selection(
        self, options_list: list[Option], st_range: int, en_range: int
    ):
        for idx in range(st_range, en_range):
            option = self._get_option(options_list, idx)
            if not option:
                continue

            if idx == self._selected:
                option.item.is_selected = True
                continue
            option.item.is_selected = False

    def get_string(self) -> str:
        st_range, en_range = self._get_option_range()
        options_list = self._get_options_list()
        self.update_selection(options_list, st_range, en_range)

        string = ""
        string_lines = 0
        for idx in range(st_range, en_range):
            option = self._get_option(options_list, idx)
            if option:
                option_name = option.get_string()
                option.update()
                option.update_shift()
                string += option_name
                string_lines += 1
        if string_lines == 1:
            string += " " * self._chars
        return string

    def apply_selection(self):
        options_list = self._get_options_list()
        option = options_list[self._selected]
        self._add_entry(option)
        if isinstance(option, OptionToggle):
            option.execute_callback()
            option.update()

        if isinstance(option, (OptionRange, OptionTimeHM)):
            option.advance_state()
            option.update()

    def back_selection(self):
        options_list = self._get_options_list()
        option = options_list[self._selected]
        if isinstance(option, (OptionRange, OptionTimeHM)):
            if option.get_hold_state():
                option.back_state()
                option.update()
                return

        self._back_entry()


class MenuHandler:
    def __init__(self):
        self.tick_rate = 80
        self.screen = self.get_screen()
        self.main_menu = self.get_main_menu()
        self.lcd_menu = self.get_lcd_menu()
        self.up_button = self.get_up_button()
        self.down_button = self.get_down_button()
        self.apply_button = self.get_apply_button()
        self.back_button = self.get_back_button()

    def get_system_submenu(self) -> dict[Option, dict]:
        cpu_name = CPUName(MenuItem(LCD_CHARS))
        cpu_perc = CPUPerc(MenuItem(LCD_CHARS))
        cpu_freq = CPUFreq(MenuItem(LCD_CHARS))
        system_submenu: dict[Option, dict] = {
            cpu_name: {},
            cpu_perc: {},
            cpu_freq: {},
        }
        return system_submenu

    def set_tick_rate(self, tick_rate: int):
        self.tick_rate = tick_rate

    def get_tick_rate(self):
        return self.tick_rate

    def get_display_submenu(self) -> dict[Option, dict]:
        callback = self.backlight_callback
        state_callback = self.get_state_callback
        backlight_item = MenuItem(LCD_CHARS)

        backlight_toggle = ToggleBase(
            "Backlight", backlight_item, callback, state_callback
        )

        assign_callback = self.set_tick_rate
        state_callback = self.get_tick_rate
        tick_item = MenuItem(LCD_CHARS)

        tick_rate = RangeBase(
            "Tickrate", tick_item, 10, 90, 5, assign_callback, state_callback
        )

        time_item = MenuItem(LCD_CHARS)
        time_option = TimeBase("Time", time_item)

        display_submenu: dict[Option, dict] = {
            backlight_toggle: {},
            tick_rate: {},
            time_option: {},
        }
        return display_submenu

    def backlight_callback(self, backlight_state: bool):
        self.screen.set_backlight(backlight_state)

    def get_state_callback(self) -> bool:
        return self.screen._lcd.backlight

    def get_main_menu(self) -> dict[Option, dict]:
        system_submenu = self.get_system_submenu()
        display_submenu = self.get_display_submenu()

        rolling_text = "Testing rolling option"

        option_1 = StaticBase("Option 1", MenuItem(LCD_CHARS))
        option_2 = StaticBase("Option 2", MenuItem(LCD_CHARS))
        option_3 = StaticBase("Option 3", MenuItem(LCD_CHARS))
        option_4 = StaticBase("Option 4", MenuItem(LCD_CHARS))
        option_5 = StaticBase("Option 5", MenuItem(LCD_CHARS))
        rolling = StaticBase(rolling_text, MenuItem(LCD_CHARS))
        option_test = StaticBase("Option Test", MenuItem(LCD_CHARS))
        option_submenu = {option_test: {}}

        display_config = StaticBase("Display Config", MenuItem(LCD_CHARS))
        system_info = StaticBase("System Info", MenuItem(LCD_CHARS))

        main_menu: dict[Option, dict] = {
            option_1: {},
            option_2: {},
            option_3: {},
            option_4: {},
            option_5: {},
            rolling: option_submenu,
            display_config: display_submenu,
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

    def get_back_button(self) -> Button:
        back_button = Button(BACK_BUTTON_PIN)
        return back_button

    def increment_option(self):
        self.lcd_menu.increment_selection()
        string = self.lcd_menu.get_string()
        self.screen.write(string, 0.0)

    def decrement_option(self):
        self.lcd_menu.decrement_selection()
        string = self.lcd_menu.get_string()
        self.screen.write(string, 0.0)

    def apply_option(self):
        self.lcd_menu.apply_selection()
        string = self.lcd_menu.get_string()
        self.screen.write(string, 0.0)

    def back_option(self):
        self.lcd_menu.back_selection()
        string = self.lcd_menu.get_string()
        self.screen.write(string, 0.0)

    def update_options(self):
        string = self.lcd_menu.get_string()
        self.screen.write(string, 0.0)

    def loop(self):
        string = self.lcd_menu.get_string()
        self.screen.write(string, 0.0)

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

            if self.back_button.is_pressed():
                print("Back Button Pressed")
                self.back_option()

            if counter >= self.tick_rate:
                self.update_options()
                counter = 0
            time.sleep(0.01)


if __name__ == "__main__":
    menu_handler = MenuHandler()
    menu_handler.loop()
