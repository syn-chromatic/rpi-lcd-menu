from options.abstracts import OptionABC
from options.standards import StaticStd, ToggleStd, TimeStd, ListStd, RangeStd
from options.standards import LinkedRangeStd
from options.customs import CPUArch, CPUPerc, CPUFreq, CPUCoreCount
from options.customs import MemoryTotal, MemoryFree, MemoryUsed, MemoryPerc
from options.item import MenuItem
from options.utils import MenuCreator
from options.states import LinkedStateBool, LinkedStateInt
from menu.tickrate import Tickrate
from writers.abstracts import WriterABC
from configurations import LCDConfigABC


class SystemInfoMenu:
    def __init__(self, lcd_config: LCDConfigABC):
        self.lcd_config = lcd_config

    def get_menu_item(self) -> MenuItem:
        columns = self.lcd_config.lcd_columns
        return MenuItem(columns)

    def get_heads(self) -> list[OptionABC]:
        cpu_arch = CPUArch(self.get_menu_item())
        cpu_perc = CPUPerc(self.get_menu_item())
        cpu_freq = CPUFreq(self.get_menu_item())
        cpu_cores = CPUCoreCount(self.get_menu_item())
        mem_total = MemoryTotal(self.get_menu_item())
        mem_free = MemoryFree(self.get_menu_item())
        mem_used = MemoryUsed(self.get_menu_item())
        mem_perc = MemoryPerc(self.get_menu_item())

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
        return heads

    def get_submenus(self, heads: list[OptionABC]) -> list[dict]:
        submenus = [{}] * len(heads)
        return submenus

    def get_menu(self) -> dict[OptionABC, dict]:
        heads = self.get_heads()
        submenus = self.get_submenus(heads)
        menu = MenuCreator(heads, submenus).create()
        return menu


class ConfigurationMenu:
    def __init__(
        self,
        writer: WriterABC,
        lcd_config: LCDConfigABC,
        tickrate: Tickrate,
    ):
        self.writer = writer
        self.lcd_config = lcd_config
        self.tickrate = tickrate

    def get_menu_item(self) -> MenuItem:
        columns = self.lcd_config.lcd_columns
        return MenuItem(columns)

    def get_backlight_option(self) -> ToggleStd:
        get_backlight_state = self.writer.get_backlight_state
        set_backlight_state = self.writer.set_backlight
        backlight_state = LinkedStateBool(get_backlight_state, set_backlight_state)

        bl_name = "Backlight"
        bl_item = self.get_menu_item()

        option = ToggleStd(bl_name, bl_item, backlight_state)
        return option

    def get_tick_option(self) -> LinkedRangeStd:
        get_tickrate_state = self.tickrate.get_tickrate
        set_tickrate_state = self.tickrate.set_tickrate
        tick_state = LinkedStateInt(get_tickrate_state, set_tickrate_state)

        tick_name = "Tickrate"
        tick_item = self.get_menu_item()
        tick_step = 5
        tick_min_range = 10
        tick_max_range = 90

        tick_option = LinkedRangeStd(
            tick_name,
            tick_item,
            tick_state,
            tick_step,
            tick_min_range,
            tick_max_range,
        )
        return tick_option

    def get_time_option(self) -> TimeStd:
        time_name = "Time"
        time_item = self.get_menu_item()
        time_option = TimeStd(time_name, time_item)
        return time_option

    def get_types_option(self) -> ListStd:
        test_name = "Types"
        test_item = self.get_menu_item()
        test_list = ["Example", "Long String Test", "End"]
        types_option = ListStd(test_name, test_item, test_list)
        return types_option

    def get_heads(self) -> list[OptionABC]:
        backlight_option = self.get_backlight_option()
        tick_option = self.get_tick_option()
        time_option = self.get_time_option()
        types_option = self.get_types_option()

        heads: list[OptionABC] = [
            backlight_option,
            tick_option,
            time_option,
            types_option,
        ]
        return heads

    def get_submenus(self, heads: list[OptionABC]) -> list[dict]:
        submenus = [{}] * len(heads)
        return submenus

    def get_menu(self) -> dict[OptionABC, dict]:
        heads = self.get_heads()
        submenus = self.get_submenus(heads)
        menu = MenuCreator(heads, submenus).create()
        return menu


class MainMenu:
    def __init__(
        self,
        writer: WriterABC,
        lcd_config: LCDConfigABC,
        tickrate: Tickrate,
    ):
        self.writer = writer
        self.lcd_config = lcd_config
        self.tickrate = tickrate

    def get_menu_item(self) -> MenuItem:
        columns = self.lcd_config.lcd_columns
        return MenuItem(columns)

    def get_heads(self) -> list[OptionABC]:
        option_1 = StaticStd("Option 1", self.get_menu_item())
        option_2 = StaticStd("Option 2", self.get_menu_item())
        option_3 = StaticStd("Option 3", self.get_menu_item())
        option_4 = StaticStd("Option 4", self.get_menu_item())
        option_5 = StaticStd("Option 5", self.get_menu_item())
        config = StaticStd("Configuration", self.get_menu_item())
        system_info = StaticStd("System Info", self.get_menu_item())

        heads: list[OptionABC] = [
            option_1,
            option_2,
            option_3,
            option_4,
            option_5,
            config,
            system_info,
        ]
        return heads

    def get_submenus(self) -> list[dict]:
        config_menu = ConfigurationMenu(
            self.writer,
            self.lcd_config,
            self.tickrate,
        )
        system_menu = SystemInfoMenu(self.lcd_config)

        submenus: list[dict] = [
            {},
            {},
            {},
            {},
            {},
            config_menu.get_menu(),
            system_menu.get_menu(),
        ]
        return submenus

    def get_menu(self) -> dict[OptionABC, dict]:
        heads = self.get_heads()
        submenus = self.get_submenus()
        menu = MenuCreator(heads, submenus).create()
        return menu


class AddDeviceMenu:
    def __init__(self, columns: int):
        self.columns = columns

    def add_device_item(self) -> StaticStd:
        name = "Add Device.."
        menu_item = MenuItem(self.columns)
        option = StaticStd(name, menu_item)
        return option

    def gpio_selection_item(self) -> ListStd:
        name = "GPIO"
        item_list = ["Input", "Output"]
        menu_item = MenuItem(self.columns)
        option = ListStd(name, menu_item, item_list)
        return option

    def pin_selection_item(self) -> RangeStd:
        name = "Pin"
        menu_item = MenuItem(self.columns)
        option = RangeStd(name, menu_item, 1, 0, 40)
        return option

    def type_selection_item(self) -> ListStd:
        name = "Type"
        item_list = ["Relay", "DHT"]
        menu_item = MenuItem(self.columns)
        option = ListStd(name, menu_item, item_list)
        return option

    def control_selection_item(self) -> ListStd:
        name = "Ctrl"
        item_list = ["Manual", "Schedule"]
        menu_item = MenuItem(self.columns)
        option = ListStd(name, menu_item, item_list)
        return option

    def get_submenu(self) -> dict[OptionABC, dict]:
        gpio_select = self.gpio_selection_item()
        pin_select = self.pin_selection_item()
        type_select = self.type_selection_item()
        control_select = self.control_selection_item()

        heads = [
            gpio_select,
            pin_select,
            type_select,
            control_select,
        ]
        submenus = [{}] * len(heads)
        menu = MenuCreator(heads, submenus).create()
        return menu

    def get_menu(self) -> dict[OptionABC, dict]:
        add_device = self.add_device_item()
        submenu = self.get_submenu()

        heads: list[OptionABC] = [add_device]
        submenus = [submenu]
        menu = MenuCreator(heads, submenus).create()
        return menu


class DevicesMenu:
    def __init__(self, columns: int):
        self.columns = columns

    def devices_item(self) -> StaticStd:
        name = "Devices"
        menu_item = MenuItem(self.columns)
        option = StaticStd(name, menu_item)
        return option

    def get_menu(self) -> MenuCreator:
        devices = self.devices_item()
        submenu = AddDeviceMenu(self.columns).get_menu()

        heads: list[OptionABC] = [devices]
        submenus = [submenu]
        menu = MenuCreator(heads, submenus)
        return menu
