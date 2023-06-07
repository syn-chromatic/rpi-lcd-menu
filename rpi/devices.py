from options.standards import StaticStd, ListStd, RangeStd
from options.item import MenuItem
from options.utils import MenuCreator
from options.abstracts import OptionABC


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

    def get_submenu(self):
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

    def get_menu(self):
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

    def get_menu(self):
        devices = self.devices_item()
        submenu = AddDeviceMenu(self.columns).get_menu()

        heads: list[OptionABC] = [devices]
        submenus = [submenu]
        menu = MenuCreator(heads, submenus)
        return menu
