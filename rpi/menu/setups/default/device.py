from configurations import LCDConfigABC

from options.abstracts import OptionABC
from options.standards import StaticOption
from options.standards import ToggleOption
from options.standards import (
    RangeOptionEvent,
    SActionOptionEvent,
    ActionOptionEvent,
    ListOptionEvent,
)

from options.item import MenuItem
from options.utils import MenuCreator
from options.events import IntEvent, StrEvent, ActionEvent


class Device:
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


class DeviceInfo:
    def __init__(self, lcd_config: LCDConfigABC, device: Device):
        self.lcd_config = lcd_config
        self.device = device

    def get_menu_item(self) -> MenuItem:
        columns = self.lcd_config.lcd_columns
        return MenuItem(columns)

    def get_info_menu(self) -> dict[OptionABC, dict]:
        _gpio = self.device.get_gpio_mode()
        _pin = self.device.get_pin()
        _type = self.device.get_type()
        _ctrl = self.device.get_control()

        gpio_name = f"GPIO: {_gpio}"
        pin_name = f"Pin: {_pin}"
        type_name = f"Type: {_type}"
        ctrl_name = f"Control: {_ctrl}"

        gpio_option = StaticOption(gpio_name, self.get_menu_item())
        pin_option = StaticOption(pin_name, self.get_menu_item())
        type_option = StaticOption(type_name, self.get_menu_item())
        ctrl_option = StaticOption(ctrl_name, self.get_menu_item())

        heads: list[OptionABC] = [gpio_option, pin_option, type_option, ctrl_option]
        submenus = [{}] * len(heads)
        submenu = MenuCreator(heads, submenus).create()

        control_option = StaticOption("Info", self.get_menu_item())
        heads = [control_option]
        submenus = [submenu]
        menu = MenuCreator(heads, submenus).create()
        return menu


class DeviceControl:
    def __init__(self, lcd_config: LCDConfigABC, device: Device):
        self.lcd_config = lcd_config
        self.device = device

    def get_menu_item(self) -> MenuItem:
        columns = self.lcd_config.lcd_columns
        return MenuItem(columns)

    def get_scheduled_control(self) -> dict[OptionABC, dict]:
        gpio_state = StaticOption("[Add Schedule]", self.get_menu_item())
        heads: list[OptionABC] = [gpio_state]
        submenus = [{}] * len(heads)
        submenu = MenuCreator(heads, submenus).create()

        control_option = StaticOption("Control", self.get_menu_item())
        heads = [control_option]
        submenus = [submenu]
        menu = MenuCreator(heads, submenus).create()
        return menu

    def get_manual_control(self) -> dict[OptionABC, dict]:
        gpio_state = ToggleOption("GPIO", self.get_menu_item())
        heads: list[OptionABC] = [gpio_state]
        submenus = [{}] * len(heads)
        submenu = MenuCreator(heads, submenus).create()

        control_option = StaticOption("Control", self.get_menu_item())
        heads = [control_option]
        submenus = [submenu]
        menu = MenuCreator(heads, submenus).create()
        return menu

    def get_control_menu(self) -> dict[OptionABC, dict]:
        control = self.device.get_control()
        if control == "Manual":
            menu = self.get_manual_control()
            return menu
        menu = self.get_scheduled_control()
        return menu


class AddDeviceMenuBase:
    def __init__(self, lcd_config: LCDConfigABC):
        self._lcd_config = lcd_config
        self._device = Device()
        self._add_device_submenu = {}
        self._menu = self._get_menu()

    def _get_menu_item(self) -> MenuItem:
        columns = self._lcd_config.lcd_columns
        return MenuItem(columns)

    def _set_add_device_submenu(self):
        self._add_device_submenu.clear()
        self._add_device_submenu.update(self._get_add_device_menu())
        self._device.reset()

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
        get_gpio = self._device.get_gpio_mode
        set_gpio = self._device.set_gpio_mode
        event = StrEvent(get_gpio, set_gpio)
        option = ListOptionEvent(name, menu_item, event, item_list)
        return option

    def _get_pin_option(self) -> RangeOptionEvent:
        name = "Pin"
        menu_item = self._get_menu_item()
        get_pin = self._device.get_pin
        set_pin = self._device.set_pin
        event = IntEvent(get_pin, set_pin)
        option = RangeOptionEvent(name, menu_item, event, 1, 0, 40)
        return option

    def _get_type_option(self) -> ListOptionEvent:
        name = "Type"
        item_list = ["Relay", "DHT"]
        menu_item = self._get_menu_item()
        get_type = self._device.get_type
        set_type = self._device.set_type
        event = StrEvent(get_type, set_type)
        option = ListOptionEvent(name, menu_item, event, item_list)
        return option

    def _get_control_option(self) -> ListOptionEvent:
        name = "Ctrl"
        item_list = ["Manual", "Schedule"]
        menu_item = self._get_menu_item()
        get_control = self._device.get_control
        set_control = self._device.set_control
        event = StrEvent(get_control, set_control)
        option = ListOptionEvent(name, menu_item, event, item_list)
        return option

    def _create_new_device(self) -> dict[OptionABC, dict]:
        device_info = DeviceInfo(self._lcd_config, self._device)
        device_control = DeviceControl(self._lcd_config, self._device)

        info_menu = device_info.get_info_menu()
        control_menu = device_control.get_control_menu()
        submenus = {**info_menu, **control_menu}

        pin = self._device.get_pin()
        name = f"Device ({pin})"
        menu_item = self._get_menu_item()
        option = StaticOption(name, menu_item)

        heads: list[OptionABC] = [option]
        submenus = [submenus]
        menu = MenuCreator(heads, submenus).create()

        return menu

    def _add_device_to_menu(self):
        new_device = self._create_new_device()
        self._menu.update(new_device)

    def _get_ok_option(self) -> SActionOptionEvent:
        name = "[Confirm]"
        success_name = "(Added)"
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

    def _get_submenus(self, heads: list[OptionABC]) -> list[dict]:
        submenus = [{}] * len(heads)
        return submenus

    def _get_add_device_menu(self) -> dict[OptionABC, dict]:
        heads = self._get_heads()
        submenus = self._get_submenus(heads)
        menu = MenuCreator(heads, submenus).create()
        return menu

    def _get_menu(self) -> dict[OptionABC, dict]:
        add_device = self._get_add_device_option()
        heads: list[OptionABC] = [add_device]
        submenus = [self._add_device_submenu]
        menu = MenuCreator(heads, submenus).create()
        return menu


class AddDeviceMenu(AddDeviceMenuBase):
    def __init__(self, lcd_config: LCDConfigABC):
        super().__init__(lcd_config)

    def get_menu(self) -> dict[OptionABC, dict]:
        return self._menu
