from tickrate import Tickrate
from lcdwriter import WriterABC
from configurations import LCDConfigABC

from options import OptionABC
from options import StaticOption
from options import MenuItem
from options import MenuCreator
from options import (
    BoolEvent,
    RangeOptionEvent,
    SActionOptionEvent,
    ActionOptionEvent,
    ListOptionEvent,
    ToggleOptionEvent,
    ToggleOption,
)
from options import IntEvent, StrEvent, ActionEvent
from devices import RelayDevice
from options import TimeOption, ListOption


from options import CPUArch, CPUPerc, CPUFreq, CPUCoreCount
from options import MemoryTotal, MemoryFree, MemoryUsed, MemoryPerc

from collections import OrderedDict as OrdDict


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

    def get_submenus(self, heads: list[OptionABC]) -> list[OrdDict]:
        submenus = [OrdDict()] * len(heads)
        return submenus

    def get_menu(self) -> OrdDict[OptionABC, OrdDict]:
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

    def get_backlight_option(self) -> ToggleOptionEvent:
        get_backlight = self.writer.get_backlight_state
        set_backlight = self.writer.set_backlight
        backlight_event = BoolEvent(get_backlight, set_backlight)

        bl_name = "Backlight"
        bl_item = self.get_menu_item()

        option = ToggleOptionEvent(bl_name, bl_item, backlight_event)
        return option

    def get_tick_option(self) -> RangeOptionEvent:
        get_tickrate = self.tickrate.get_tickrate
        set_tickrate = self.tickrate.set_tickrate
        tick_event = IntEvent(get_tickrate, set_tickrate)

        tick_name = "Tickrate"
        tick_item = self.get_menu_item()
        tick_step = 5
        tick_min_range = 0
        tick_max_range = 90

        tick_option = RangeOptionEvent(
            tick_name,
            tick_item,
            tick_event,
            tick_step,
            tick_min_range,
            tick_max_range,
        )
        return tick_option

    def get_time_option(self) -> TimeOption:
        time_name = "Time"
        time_item = self.get_menu_item()
        time_option = TimeOption(time_name, time_item)
        return time_option

    def get_types_option(self) -> ListOption:
        test_name = "Types"
        test_item = self.get_menu_item()
        test_list = ["Example", "Long String Test", "End"]
        types_option = ListOption(test_name, test_item, test_list)
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

    def get_submenus(self, heads: list[OptionABC]) -> list[OrdDict]:
        submenus = [OrdDict()] * len(heads)
        return submenus

    def get_menu(self) -> OrdDict[OptionABC, OrdDict]:
        heads = self.get_heads()
        submenus = self.get_submenus(heads)
        menu = MenuCreator(heads, submenus).create()
        return menu


class DeviceMenu:
    def __init__(self):
        self.gpio_mode = "Input"
        self.pin = 0
        self.type = "Relay"
        self.control = "Manual"

    def set_gpio_mode(self, mode: str):
        self.gpio_mode = mode

    def set_pin(self, pin: int):
        self.pin = pin

    def set_type(self, type: str):
        self.type = type

    def set_control(self, control: str):
        self.control = control

    def get_gpio_mode(self) -> str:
        return self.gpio_mode

    def get_pin(self) -> int:
        return self.pin

    def get_type(self) -> str:
        return self.type

    def get_control(self) -> str:
        return self.control

    def reset(self):
        self.gpio_mode = "Input"
        self.pin = 0
        self.type = "Relay"
        self.control = "Manual"


class DeviceInfoMenu:
    def __init__(self, lcd_config: LCDConfigABC, device_menu: DeviceMenu):
        self.lcd_config = lcd_config
        self.device_menu = device_menu

    def get_menu_item(self) -> MenuItem:
        columns = self.lcd_config.lcd_columns
        return MenuItem(columns)

    def get_info_menu(self) -> OrdDict[OptionABC, OrdDict]:
        _gpio = self.device_menu.get_gpio_mode()
        _pin = self.device_menu.get_pin()
        _type = self.device_menu.get_type()
        _ctrl = self.device_menu.get_control()

        gpio_name = f"GPIO: {_gpio}"
        pin_name = f"Pin: {_pin}"
        type_name = f"Type: {_type}"
        ctrl_name = f"Control: {_ctrl}"

        gpio_option = StaticOption(gpio_name, self.get_menu_item())
        pin_option = StaticOption(pin_name, self.get_menu_item())
        type_option = StaticOption(type_name, self.get_menu_item())
        ctrl_option = StaticOption(ctrl_name, self.get_menu_item())

        heads: list[OptionABC] = [gpio_option, pin_option, type_option, ctrl_option]
        submenus = [OrdDict()] * len(heads)
        submenu = MenuCreator(heads, submenus).create()

        control_option = StaticOption("Info", self.get_menu_item())
        heads = [control_option]
        submenus = [submenu]
        menu = MenuCreator(heads, submenus).create()
        return menu


class DeviceControlMenu:
    def __init__(self, lcd_config: LCDConfigABC, device_menu: DeviceMenu):
        self.lcd_config = lcd_config
        self.device_menu = device_menu
        self.devices = []

    def get_menu_item(self) -> MenuItem:
        columns = self.lcd_config.lcd_columns
        return MenuItem(columns)

    def get_scheduled_control(self) -> OrdDict[OptionABC, OrdDict]:
        gpio_state = StaticOption("[Add Schedule]", self.get_menu_item())
        heads: list[OptionABC] = [gpio_state]
        submenus = [OrdDict()] * len(heads)
        submenu = MenuCreator(heads, submenus).create()

        control_option = StaticOption("Control", self.get_menu_item())
        heads = [control_option]
        submenus = [submenu]
        menu = MenuCreator(heads, submenus).create()
        return menu

    def get_manual_control(self) -> OrdDict[OptionABC, OrdDict]:
        pin = self.device_menu.pin
        relay = RelayDevice(pin)
        self.devices.append(relay)
        event = BoolEvent(relay.get_state, relay.set_state)
        gpio_state = ToggleOptionEvent("GPIO", self.get_menu_item(), event)
        # gpio_state = ToggleOption("GPIO", self.get_menu_item())
        heads: list[OptionABC] = [gpio_state]
        submenus = [OrdDict()] * len(heads)
        submenu = MenuCreator(heads, submenus).create()

        control_option = StaticOption("Control", self.get_menu_item())
        heads = [control_option]
        submenus = [submenu]
        menu = MenuCreator(heads, submenus).create()
        return menu

    def get_control_menu(self) -> OrdDict[OptionABC, OrdDict]:
        control = self.device_menu.get_control()
        if control == "Manual":
            menu = self.get_manual_control()
            return menu
        menu = self.get_scheduled_control()
        return menu


class AddDeviceMenuBase:
    def __init__(self, lcd_config: LCDConfigABC):
        self._lcd_config = lcd_config
        self._device_menu = DeviceMenu()
        self._add_device_submenu = OrdDict()
        self._menu = self._get_menu()

    def _get_menu_item(self) -> MenuItem:
        columns = self._lcd_config.lcd_columns
        return MenuItem(columns)

    def _set_add_device_submenu(self):
        self._add_device_submenu.clear()
        self._add_device_submenu.update(self._get_add_device_menu())
        self._device_menu.reset()

    def _get_add_device_option(self) -> ActionOptionEvent:
        name = "[Add Device]"
        menu_item = self._get_menu_item()
        event = ActionEvent(self._set_add_device_submenu)
        option = ActionOptionEvent(name, menu_item, event)
        return option

    def _get_gpio_mode_option(self) -> ListOptionEvent:
        name = "GPIO"
        item_list = ["Input", "Output"]
        menu_item = self._get_menu_item()
        get_gpio = self._device_menu.get_gpio_mode
        set_gpio = self._device_menu.set_gpio_mode
        event = StrEvent(get_gpio, set_gpio)
        option = ListOptionEvent(name, menu_item, event, item_list)
        return option

    def _get_pin_option(self) -> RangeOptionEvent:
        name = "Pin"
        menu_item = self._get_menu_item()
        get_pin = self._device_menu.get_pin
        set_pin = self._device_menu.set_pin
        event = IntEvent(get_pin, set_pin)
        option = RangeOptionEvent(name, menu_item, event, 1, 0, 40)
        return option

    def _get_type_option(self) -> ListOptionEvent:
        name = "Type"
        item_list = ["Relay", "DHT"]
        menu_item = self._get_menu_item()
        get_type = self._device_menu.get_type
        set_type = self._device_menu.set_type
        event = StrEvent(get_type, set_type)
        option = ListOptionEvent(name, menu_item, event, item_list)
        return option

    def _get_control_option(self) -> ListOptionEvent:
        name = "Ctrl"
        item_list = ["Manual", "Schedule"]
        menu_item = self._get_menu_item()
        get_control = self._device_menu.get_control
        set_control = self._device_menu.set_control
        event = StrEvent(get_control, set_control)
        option = ListOptionEvent(name, menu_item, event, item_list)
        return option

    def _delete_device(self, device_option: OptionABC):
        self._menu.pop(device_option)

    def _create_new_device(self) -> OrdDict[OptionABC, OrdDict]:
        pin = self._device_menu.get_pin()
        name = f"Device ({pin})"
        menu_item = self._get_menu_item()
        option = StaticOption(name, menu_item)

        device_info = DeviceInfoMenu(self._lcd_config, self._device_menu)
        device_control = DeviceControlMenu(self._lcd_config, self._device_menu)

        info_menu = device_info.get_info_menu()
        control_menu = device_control.get_control_menu()
        submenus = OrdDict(list(info_menu.items()) + list(control_menu.items()))

        heads: list[OptionABC] = [option]
        submenus = [submenus]
        menu = MenuCreator(heads, submenus).create()

        return menu

    def _add_device_to_menu(self):
        new_device = self._create_new_device()
        self._menu.update(new_device)

    def _get_ok_option(self) -> SActionOptionEvent:
        name = "[Confirm]"
        success_name = "[Added]"
        menu_item = self._get_menu_item()
        event = ActionEvent(self._add_device_to_menu)
        option = SActionOptionEvent(name, success_name, menu_item, event)
        return option

    def _get_heads(self) -> list[OptionABC]:
        gpio_option = self._get_gpio_mode_option()
        pin_option = self._get_pin_option()
        type_option = self._get_type_option()
        ctrl_option = self._get_control_option()
        ok_option = self._get_ok_option()

        heads = [
            gpio_option,
            pin_option,
            type_option,
            ctrl_option,
            ok_option,
        ]
        return heads

    def _get_submenus(self, heads: list[OptionABC]) -> list[OrdDict]:
        submenus = [OrdDict()] * len(heads)
        return submenus

    def _get_add_device_menu(self) -> OrdDict[OptionABC, OrdDict]:
        heads = self._get_heads()
        submenus = self._get_submenus(heads)
        menu = MenuCreator(heads, submenus).create()
        return menu

    def _get_menu(self) -> OrdDict[OptionABC, OrdDict]:
        add_device = self._get_add_device_option()
        heads: list[OptionABC] = [add_device]
        submenus = [self._add_device_submenu]
        menu = MenuCreator(heads, submenus).create()
        return menu


class AddDeviceMenu(AddDeviceMenuBase):
    def __init__(self, lcd_config: LCDConfigABC):
        super().__init__(lcd_config)

    def get_menu(self) -> OrdDict[OptionABC, OrdDict]:
        return self._menu


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
        devices = StaticOption("Devices", self.get_menu_item())
        config = StaticOption("Configuration", self.get_menu_item())
        system_info = StaticOption("System Info", self.get_menu_item())

        heads: list[OptionABC] = [
            devices,
            config,
            system_info,
        ]
        return heads

    def get_submenus(self) -> list[OrdDict]:
        devices_menu = AddDeviceMenu(self.lcd_config)
        config_menu = ConfigurationMenu(
            self.writer,
            self.lcd_config,
            self.tickrate,
        )
        system_menu = SystemInfoMenu(self.lcd_config)

        submenus: list[OrdDict] = [
            devices_menu.get_menu(),
            config_menu.get_menu(),
            system_menu.get_menu(),
        ]
        return submenus

    def get_menu(self) -> OrdDict[OptionABC, OrdDict]:
        heads = self.get_heads()
        submenus = self.get_submenus()
        menu = MenuCreator(heads, submenus).create()
        return menu
