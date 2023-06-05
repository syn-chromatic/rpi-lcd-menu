import gc
import time
from collections import OrderedDict as OrdDict

from options import Option, OptionToggle, OptionRange, OptionTimeHM
from options import MenuItem
from options import MachineName, CPUFreq, UsedMemory, FreeMemory
from options import DHTTemperature, DHTHumidity
from options import StaticBase, RangeBase, ToggleBase, TimeBase
from options import MenuCreator
from lcd_writer import LCDWriter
from controller import Controller


PREV_BUTTON_PIN = 6
NEXT_BUTTON_PIN = 5
APPLY_BUTTON_PIN = 4
BACK_BUTTON_PIN = 27
LCD_ROWS = 4
LCD_CHARS = 20


class LCDMenuBase:
    def __init__(self, rows: int, columns: int, options: OrdDict[Option, OrdDict]):
        self._rows: int = rows
        self._columns: int = columns
        self._selected: int = 0
        self._options: OrdDict[Option, OrdDict] = options
        self._entries: list[tuple[int, Option]] = []

    def _get_options(self) -> OrdDict[Option, OrdDict]:
        options = self._options
        for _, entry_option in self._entries:
            if entry_option in options:
                options = options[entry_option]
        return options

    def _get_options_list(self) -> list[Option]:
        options = self._get_options()
        return list(options)

    def _get_option_range(self) -> tuple[int, int]:
        if self._selected < self._rows:
            st_range = 0
            en_range = self._rows
            return st_range, en_range

        st_range = self._selected - (self._rows - 1)
        en_range = st_range + self._rows
        return st_range, en_range

    def _add_entry(self, option: Option):
        options = self._get_options()
        if option in options:
            if options[option]:
                option.item.reset()
                entry_idx = self._selected
                self._entries.append((entry_idx, option))
                self._selected = 0

    def _back_entry(self):
        if self._entries:
            entry_idx, entry_option = self._entries.pop(-1)
            self._selected = entry_idx

    def _get_option(self, options_list: list[Option], idx: int):
        if len(options_list) > idx:
            return options_list[idx]


class LCDMenu(LCDMenuBase):
    def __init__(self, rows: int, columns: int, options: OrdDict[Option, OrdDict]):
        super().__init__(rows, columns, options)

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
                option.item.set_selected(True)
                continue
            option.item.set_selected(False)

    def ensure_complete_string(self, string: str, string_lines: int):
        if string_lines < self._rows:
            for _ in range(self._rows - string_lines):
                string += " " * self._columns + "\n"
        return string

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

        string = self.ensure_complete_string(string, string_lines)
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

        option.item.set_selected(False)
        option.item.reset()
        self._back_entry()


class MenuHandler:
    def __init__(self):
        self.tick_rate = 40
        self.screen = self.get_screen()
        self.main_menu = self.get_main_menu()
        self.lcd_menu = self.get_lcd_menu()
        self.controller = self.get_controller()

    def get_controller(self) -> Controller:
        controller = Controller(
            BACK_BUTTON_PIN,
            PREV_BUTTON_PIN,
            NEXT_BUTTON_PIN,
            APPLY_BUTTON_PIN,
        )

        controller.register_back_callback(self.back_option)
        controller.register_prev_callback(self.decrement_option)
        controller.register_next_callback(self.increment_option)
        controller.register_apply_callback(self.apply_option)
        return controller

    def set_tick_rate(self, tick_rate: int):
        self.tick_rate = tick_rate

    def get_tick_rate(self):
        return self.tick_rate

    def backlight_callback(self, backlight_state: bool):
        self.screen.set_backlight(backlight_state)

    def get_state_callback(self) -> bool:
        return self.screen._lcd.backlight

    def get_system_submenu(self) -> OrdDict[Option, OrdDict]:
        machine_name = MachineName(MenuItem(LCD_CHARS))
        cpu_freq = CPUFreq(MenuItem(LCD_CHARS))
        used_mem = UsedMemory(MenuItem(LCD_CHARS))
        free_mem = FreeMemory(MenuItem(LCD_CHARS))

        heads = [
            machine_name,
            cpu_freq,
            used_mem,
            free_mem,
        ]

        submenus = [OrdDict()] * 4
        menu = MenuCreator(heads, submenus).create()
        return menu

    def get_display_submenu(self) -> OrdDict[Option, OrdDict]:
        backlight_toggle = ToggleBase(
            "Backlight",
            MenuItem(LCD_CHARS),
            self.backlight_callback,
            self.get_state_callback,
        )
        tick_rate = RangeBase(
            "Tickrate",
            MenuItem(LCD_CHARS),
            10,
            90,
            5,
            self.set_tick_rate,
            self.get_tick_rate,
        )

        time_option = TimeBase("Time", MenuItem(LCD_CHARS))

        heads: list[Option] = [
            backlight_toggle,
            tick_rate,
            time_option,
        ]

        submenus: list[OrdDict] = [OrdDict()] * 3

        menu = MenuCreator(heads, submenus).create()
        return menu

    def get_sensors_submenu(self) -> OrdDict[Option, OrdDict]:
        dht_temp = DHTTemperature(MenuItem(LCD_CHARS))
        dht_humidity = DHTHumidity(MenuItem(LCD_CHARS))

        dht = StaticBase("DHT22", MenuItem(LCD_CHARS))

        heads_lvl2: list[Option] = [dht_temp, dht_humidity]
        submenus_lvl2: list[OrdDict] = [OrdDict(), OrdDict()]

        heads_lvl1: list[Option] = [dht]
        submenus_lvl1: list[OrdDict] = [MenuCreator(heads_lvl2, submenus_lvl2).create()]

        menu = MenuCreator(heads_lvl1, submenus_lvl1).create()
        return menu

    def get_main_menu(self) -> OrdDict[Option, OrdDict]:
        sensors = StaticBase("Sensors", MenuItem(LCD_CHARS))
        config = StaticBase("Configuration", MenuItem(LCD_CHARS))
        system_info = StaticBase("System Info", MenuItem(LCD_CHARS))

        heads: list[Option] = [
            sensors,
            config,
            system_info,
        ]

        submenus: list[OrdDict] = [
            self.get_sensors_submenu(),
            self.get_display_submenu(),
            self.get_system_submenu(),
        ]
        menu = MenuCreator(heads, submenus).create()
        return menu

    def get_screen(self) -> LCDWriter:
        screen = LCDWriter(LCD_ROWS, LCD_CHARS)
        return screen

    def get_lcd_menu(self) -> LCDMenu:
        lcd_menu = LCDMenu(LCD_ROWS, LCD_CHARS, self.main_menu)
        return lcd_menu

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
            self.controller.check()
            if counter >= self.tick_rate:
                self.update_options()
                counter = 0
                gc.collect()

            time.sleep(0.01)


def print_button_layout():
    buttons = "|  Back  |  Prev  |  Next  |  Apply  |"
    line = "-" * len(buttons)
    print("Button Layout:", line, buttons, line, sep="\n")


if __name__ == "__main__":
    print_button_layout()
    menu_handler = MenuHandler()
    menu_handler.loop()
