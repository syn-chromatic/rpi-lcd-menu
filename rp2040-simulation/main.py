import gc
import time
from collections import OrderedDict as OrdDict

from options import OptionABC
from options import MenuItem
from options import MachineName, CPUFreq, MemoryUsed, MemoryFree
from options import DHTTemperature, DHTHumidity
from options import StaticStd, RangeStd, ToggleStd, TimeStd
from options import LinkedStateBool, LinkedStateInt
from options import MenuCreator

from character import CharABC
from character import SpaceChar

from lcd_writer import LCDWriter
from controller import Controller


PREV_BUTTON_PIN = 6
NEXT_BUTTON_PIN = 5
APPLY_BUTTON_PIN = 4
BACK_BUTTON_PIN = 27
LCD_ROWS = 4
LCD_CHARS = 20


class LCDMenuBase:
    def __init__(self, rows: int, columns: int, options: OrdDict[OptionABC, OrdDict]):
        self._rows: int = rows
        self._columns: int = columns
        self._selected: int = 0
        self._options: OrdDict[OptionABC, OrdDict] = options
        self._entries: list[tuple[int, OptionABC]] = []
        self._initiate_options(self._options)

    def _initiate_options(self, options: OrdDict[OptionABC, OrdDict]):
        for option in options.keys():
            option_item = option.get_item()
            option_item.set_selected(True)
            return

    def _get_options(self) -> OrdDict[OptionABC, OrdDict]:
        options = self._options
        for _, entry_option in self._entries:
            if entry_option in options:
                options = options[entry_option]
        return options

    def _get_options_list(self) -> list[OptionABC]:
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

    def _set_option_selected(self, option: OptionABC):
        option_item = option.get_item()
        option_item.set_selected(True)

    def _set_option_deselected(self, option: OptionABC):
        option_item = option.get_item()
        option_item.set_selected(False)
        option_item.reset()

    def _add_entry(self, option: OptionABC):
        options = self._get_options()
        if option in options:
            new_options = options[option]
            if new_options:
                entry_idx = self._selected
                self._entries.append((entry_idx, option))
                self._selected = 0
                option.get_item().reset()
                self._initiate_options(new_options)
                return
        option.apply()

    def _back_entry(self, option: OptionABC):
        if self._entries:
            entry_idx, _ = self._entries.pop(-1)
            self._selected = entry_idx

            option.get_item().set_selected(False)
            option.get_item().reset()

    def _get_option(self, options_list: list[OptionABC], idx: int):
        if len(options_list) > idx:
            return options_list[idx]


class LCDMenu(LCDMenuBase):
    def __init__(self, rows: int, columns: int, options: OrdDict[OptionABC, OrdDict]):
        super().__init__(rows, columns, options)

    def get_increment_select(self, select: int, options_list: list[OptionABC]) -> int:
        if select < len(options_list) - 1:
            select += 1
            return select
        select = 0
        return select

    def get_decrement_select(self, select: int, options_list: list[OptionABC]) -> int:
        if select > 0:
            select -= 1
            return select
        select = len(options_list) - 1
        return select

    def increment_selection(self):
        options_list = self._get_options_list()
        cur_select = self._selected
        cur_option = options_list[cur_select]

        if cur_option.get_hold_state():
            cur_option.next()
            return

        new_select = self.get_increment_select(cur_select, options_list)
        new_option = options_list[new_select]

        self._set_option_deselected(cur_option)
        self._set_option_selected(new_option)
        self._selected = new_select

    def decrement_selection(self):
        options_list = self._get_options_list()
        cur_select = self._selected
        cur_option = options_list[cur_select]

        if cur_option.get_hold_state():
            cur_option.prev()
            return

        new_select = self.get_decrement_select(cur_select, options_list)
        new_option = options_list[new_select]

        self._set_option_deselected(cur_option)
        self._set_option_selected(new_option)
        self._selected = new_select

    def get_chars(self) -> list[list[CharABC]]:
        st_range, en_range = self._get_option_range()
        options_list = self._get_options_list()

        chars: list[list[CharABC]] = []
        added_rows = 0
        for idx in range(st_range, en_range):
            option = self._get_option(options_list, idx)
            if option:
                option_name = option.get_char_array()
                option.update()
                option.update_shift()
                chars.append(option_name)
                added_rows += 1

        for _ in range(self._rows - added_rows):
            row_spaces: list[CharABC] = [SpaceChar()] * self._columns
            chars.append(row_spaces)

        return chars

    def apply_selection(self):
        options_list = self._get_options_list()
        option = options_list[self._selected]
        self._add_entry(option)
        return

    def back_selection(self):
        options_list = self._get_options_list()
        option = options_list[self._selected]

        if option.get_hold_state():
            option.back()
            return

        self._back_entry(option)


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

    def get_system_submenu(self) -> OrdDict[OptionABC, OrdDict]:
        machine_name = MachineName(MenuItem(LCD_CHARS))
        cpu_freq = CPUFreq(MenuItem(LCD_CHARS))
        used_mem = MemoryUsed(MenuItem(LCD_CHARS))
        free_mem = MemoryFree(MenuItem(LCD_CHARS))

        heads = [
            machine_name,
            cpu_freq,
            used_mem,
            free_mem,
        ]

        submenus = [OrdDict()] * 4
        menu = MenuCreator(heads, submenus).create()
        return menu

    def get_display_submenu(self) -> OrdDict[OptionABC, OrdDict]:
        bl_state_callback = self.get_state_callback
        bl_assign_callback = self.backlight_callback
        backlight_state = LinkedStateBool(bl_state_callback, bl_assign_callback)

        bl_name = "Backlight"
        bl_item = MenuItem(LCD_CHARS)

        backlight_toggle = ToggleStd(bl_name, bl_item, backlight_state)

        tick_state_callback = self.get_tick_rate
        tick_assign_callback = self.set_tick_rate
        tick_state = LinkedStateInt(tick_state_callback, tick_assign_callback)

        tick_name = "Tickrate"
        tick_item = MenuItem(LCD_CHARS)
        tick_step = 5
        tick_min_range = 10
        tick_max_range = 90

        tick_rate = RangeStd(
            tick_name,
            tick_item,
            tick_state,
            tick_step,
            tick_min_range,
            tick_max_range,
        )

        time_name = "Time"
        time_item = MenuItem(LCD_CHARS)
        time_option = TimeStd(time_name, time_item)

        heads: list[OptionABC] = [
            backlight_toggle,
            tick_rate,
            time_option,
        ]

        submenus: list[OrdDict] = [OrdDict()] * 3

        menu = MenuCreator(heads, submenus).create()
        return menu

    def get_sensors_submenu(self) -> OrdDict[OptionABC, OrdDict]:
        dht_temp = DHTTemperature(MenuItem(LCD_CHARS))
        dht_humidity = DHTHumidity(MenuItem(LCD_CHARS))

        dht = StaticStd("DHT22", MenuItem(LCD_CHARS))

        heads_lvl2: list[OptionABC] = [dht_temp, dht_humidity]
        submenus_lvl2: list[OrdDict] = [OrdDict(), OrdDict()]

        heads_lvl1: list[OptionABC] = [dht]
        submenus_lvl1: list[OrdDict] = [MenuCreator(heads_lvl2, submenus_lvl2).create()]

        menu = MenuCreator(heads_lvl1, submenus_lvl1).create()
        return menu

    def get_main_menu(self) -> OrdDict[OptionABC, OrdDict]:
        sensors = StaticStd("Sensors", MenuItem(LCD_CHARS))
        config = StaticStd("Configuration", MenuItem(LCD_CHARS))
        system_info = StaticStd("System Info", MenuItem(LCD_CHARS))

        heads: list[OptionABC] = [
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
        chars = self.lcd_menu.get_chars()
        self.screen.write(chars, 0.0)

    def decrement_option(self):
        self.lcd_menu.decrement_selection()
        chars = self.lcd_menu.get_chars()
        self.screen.write(chars, 0.0)

    def apply_option(self):
        self.lcd_menu.apply_selection()
        chars = self.lcd_menu.get_chars()
        self.screen.write(chars, 0.0)

    def back_option(self):
        self.lcd_menu.back_selection()
        chars = self.lcd_menu.get_chars()
        self.screen.write(chars, 0.0)

    def update_options(self):
        chars = self.lcd_menu.get_chars()
        self.screen.write(chars, 0.0)

    def loop(self):
        chars = self.lcd_menu.get_chars()
        self.screen.write(chars, 0.0)
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
