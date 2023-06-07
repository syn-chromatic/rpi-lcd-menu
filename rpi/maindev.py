import time
from typing import Optional

from options.abstracts import OptionABC
from options.item import MenuItem
from options.configurations import CPUArch, CPUPerc, CPUFreq, CPUCoreCount
from options.configurations import MemoryTotal, MemoryUsed, MemoryFree, MemoryPerc
from options.states import LinkedStateBool, LinkedStateInt
from options.standards import StaticStd, LinkedRangeStd, ToggleStd, TimeStd, ListStd
from options.utils import MenuCreator

from character.abstracts import CharABC
from character.chars import SpaceChar

from writers.console_writer import ConsoleWriter
from controllers.kb_controller import KBController

from devices import AddDeviceMenu


PREV_BUTTON_KEY = ord("2")
NEXT_BUTTON_KEY = ord("3")
APPLY_BUTTON_KEY = ord("4")
BACK_BUTTON_KEY = ord("1")
LCD_ROWS = 4
LCD_CHARS = 20


class LCDMenuBase:
    def __init__(self, rows: int, columns: int, options: dict[OptionABC, dict]):
        self._rows: int = rows
        self._columns: int = columns
        self._selected: int = 0
        self._options: dict[OptionABC, dict] = options
        self._entries: list[tuple[int, OptionABC]] = []
        self._initiate_options(self._options)

    def _initiate_options(self, options: dict[OptionABC, dict]):
        for option in options.keys():
            option_item = option.get_item()
            option_item.set_selected(True)
            return

    def _get_options(self) -> dict[OptionABC, dict]:
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

    def _get_option(
        self, options_list: list[OptionABC], idx: int
    ) -> Optional[OptionABC]:
        if len(options_list) > idx:
            return options_list[idx]


class LCDMenu(LCDMenuBase):
    def __init__(self, rows: int, columns: int, options: dict[OptionABC, dict]):
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
        self.controller = self.get_kb_controller()

    def get_kb_controller(self) -> KBController:
        controller = KBController(
            BACK_BUTTON_KEY,
            PREV_BUTTON_KEY,
            NEXT_BUTTON_KEY,
            APPLY_BUTTON_KEY,
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
        return self.screen.get_backlight_state()

    def get_system_submenu(self) -> dict[OptionABC, dict]:
        cpu_arch = CPUArch(MenuItem(LCD_CHARS))
        cpu_perc = CPUPerc(MenuItem(LCD_CHARS))
        cpu_freq = CPUFreq(MenuItem(LCD_CHARS))
        cpu_cores = CPUCoreCount(MenuItem(LCD_CHARS))
        mem_total = MemoryTotal(MenuItem(LCD_CHARS))
        mem_free = MemoryFree(MenuItem(LCD_CHARS))
        mem_used = MemoryUsed(MenuItem(LCD_CHARS))
        mem_perc = MemoryPerc(MenuItem(LCD_CHARS))

        heads = [
            cpu_arch,
            cpu_perc,
            cpu_freq,
            cpu_cores,
            mem_total,
            mem_free,
            mem_used,
            mem_perc,
        ]

        submenus = [{}] * len(heads)
        menu = MenuCreator(heads, submenus).create()
        return menu

    def get_display_submenu(self) -> dict[OptionABC, dict]:
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

        tick_rate = LinkedRangeStd(
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

        test_name = "Types"
        test_item = MenuItem(LCD_CHARS)
        test_list = ["Example", "Long String Test", "End"]
        option_list = ListStd(test_name, test_item, test_list)

        heads: list[OptionABC] = [
            backlight_toggle,
            tick_rate,
            time_option,
            option_list,
        ]

        submenus: list[dict] = [{}] * len(heads)

        menu = MenuCreator(heads, submenus).create()
        return menu

    def get_test_submenus(self) -> dict[OptionABC, dict]:
        option_test1 = StaticStd("Option Test1", MenuItem(LCD_CHARS))
        option_test2 = StaticStd("Option Test2", MenuItem(LCD_CHARS))
        option_test3 = StaticStd("Option Test3", MenuItem(LCD_CHARS))
        option_test = StaticStd("Option Test", MenuItem(LCD_CHARS))

        heads_lvl2: list[OptionABC] = [
            option_test1,
            option_test2,
            option_test3,
        ]
        submenus_lvl2: list[dict] = [{}] * 3
        heads_lvl1: list[OptionABC] = [option_test]
        submenus_lvl1: list[dict] = [MenuCreator(heads_lvl2, submenus_lvl2).create()]
        menu = MenuCreator(heads_lvl1, submenus_lvl1).create()
        return menu

    def get_main_menu(self) -> dict[OptionABC, dict]:
        option_1 = StaticStd("Option 1", MenuItem(LCD_CHARS))
        option_2 = StaticStd("Option 2", MenuItem(LCD_CHARS))
        option_3 = StaticStd("Option 3", MenuItem(LCD_CHARS))
        option_4 = StaticStd("Option 4", MenuItem(LCD_CHARS))
        option_5 = StaticStd("Option 5", MenuItem(LCD_CHARS))
        rolling_test = StaticStd("Testing rolling option", MenuItem(LCD_CHARS))
        devices = StaticStd("Devices", MenuItem(LCD_CHARS))
        config = StaticStd("Configuration", MenuItem(LCD_CHARS))
        system_info = StaticStd("System Info", MenuItem(LCD_CHARS))

        heads: list[OptionABC] = [
            option_1,
            option_2,
            option_3,
            option_4,
            option_5,
            rolling_test,
            devices,
            config,
            system_info,
        ]

        submenus: list[dict] = [
            {},
            {},
            {},
            {},
            {},
            self.get_test_submenus(),
            AddDeviceMenu(LCD_CHARS).get_menu(),
            self.get_display_submenu(),
            self.get_system_submenu(),
        ]
        menu = MenuCreator(heads, submenus).create()

        return menu

    def get_screen(self) -> ConsoleWriter:
        screen = ConsoleWriter(LCD_ROWS, LCD_CHARS)
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

            time.sleep(0.01)


if __name__ == "__main__":
    menu_handler = MenuHandler()
    menu_handler.loop()
