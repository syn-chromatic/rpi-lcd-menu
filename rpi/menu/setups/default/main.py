from menu.tickrate import Tickrate
from writers.abstracts import WriterABC
from configurations import LCDConfigABC

from options.abstracts import OptionABC
from options.standards import StaticOption
from options.item import MenuItem
from options.utils import MenuCreator

from menu.setups.default.config import ConfigurationMenu
from menu.setups.default.system import SystemInfoMenu

# For interchangeable compatibility with MicroPython
from collections import OrderedDict as OrdDict


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
        config = StaticOption("Configuration", self.get_menu_item())
        system_info = StaticOption("System Info", self.get_menu_item())

        heads: list[OptionABC] = [
            config,
            system_info,
        ]
        return heads

    def get_submenus(self) -> list[OrdDict]:
        config_menu = ConfigurationMenu(
            self.writer,
            self.lcd_config,
            self.tickrate,
        )
        system_menu = SystemInfoMenu(self.lcd_config)

        submenus: list[OrdDict] = [
            config_menu.get_menu(),
            system_menu.get_menu(),
        ]
        return submenus

    def get_menu(self) -> OrdDict[OptionABC, OrdDict]:
        heads = self.get_heads()
        submenus = self.get_submenus()
        menu = MenuCreator(heads, submenus).create()
        return menu
