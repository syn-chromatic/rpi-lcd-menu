from menu.tickrate import Tickrate
from writers.abstracts import WriterABC
from configurations import LCDConfigABC

from options.abstracts import OptionABC
from options.standards import StaticOption
from options.item import MenuItem
from options.utils import MenuCreator

from menu.setups.default.device import AddDeviceMenu
from menu.setups.default.config import ConfigurationMenu
from menu.setups.default.system import SystemInfoMenu


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

    def get_submenus(self) -> list[dict]:
        devices_menu = AddDeviceMenu(self.lcd_config)
        config_menu = ConfigurationMenu(
            self.writer,
            self.lcd_config,
            self.tickrate,
        )
        system_menu = SystemInfoMenu(self.lcd_config)

        submenus: list[dict] = [
            devices_menu.get_menu(),
            config_menu.get_menu(),
            system_menu.get_menu(),
        ]
        return submenus

    def get_menu(self) -> dict[OptionABC, dict]:
        heads = self.get_heads()
        submenus = self.get_submenus()
        menu = MenuCreator(heads, submenus).create()
        return menu
