from menu.tickrate import Tickrate
from writers.abstracts import WriterABC
from configurations import LCDConfigABC

from options.abstracts import OptionABC
from options.standards import TimeOption, ListOption
from options.standards import ToggleOptionEvent
from options.standards import RangeOptionEvent

from options.item import MenuItem
from options.utils import MenuCreator
from options.events import BoolEvent, IntEvent


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
        backlight_event = BoolEvent(get_backlight, set_backlight) # type: ignore

        bl_name = "Backlight"
        bl_item = self.get_menu_item()

        option = ToggleOptionEvent(bl_name, bl_item, backlight_event)
        return option

    def get_tick_option(self) -> RangeOptionEvent:
        get_tickrate = self.tickrate.get_tickrate
        set_tickrate = self.tickrate.set_tickrate
        tick_event = IntEvent(get_tickrate, set_tickrate) # type: ignore

        tick_name = "Tickrate"
        tick_item = self.get_menu_item()
        tick_step = 5
        tick_min_range = 10
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

    def get_submenus(self, heads: list[OptionABC]) -> list[dict]:
        submenus = [{}] * len(heads)
        return submenus

    def get_menu(self) -> dict[OptionABC, dict]:
        heads = self.get_heads()
        submenus = self.get_submenus(heads)
        menu = MenuCreator(heads, submenus).create()
        return menu
