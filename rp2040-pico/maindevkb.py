import time

from options.abstracts import OptionABC
from menu.coordinator import MenuCoordinator
from writers.console_writer import ConsoleWriter
from controllers.kb_controller import KBController

from configurations import KBCtrlConfigABC, LCDConfigABC
from configurations import KBCtrlConfig, LCD2004Config

from menu.tickrate import Tickrate
from menu.setups.default.main import MainMenu


class MenuHandler:
    def __init__(self, ctrl_config: KBCtrlConfigABC, lcd_config: LCDConfigABC):
        self.tick_rate = Tickrate(40)
        self.ctrl_config = ctrl_config
        self.lcd_config = lcd_config
        self.writer = self.get_console_writer()
        self.main_menu = self.get_main_menu()
        self.menu_coord = self.get_menu_coord()
        self.controller = self.get_kb_controller()

    def get_kb_controller(self) -> KBController:
        controller = KBController(self.ctrl_config)
        controller.register_back_callback(self.back_option) # type: ignore
        controller.register_prev_callback(self.decrement_option) # type: ignore
        controller.register_next_callback(self.increment_option) # type: ignore
        controller.register_apply_callback(self.apply_option) # type: ignore
        return controller

    def get_main_menu(self) -> dict[OptionABC, dict]:
        main_menu = MainMenu(self.writer, self.lcd_config, self.tick_rate)
        menu = main_menu.get_menu()
        return menu

    def get_console_writer(self) -> ConsoleWriter:
        rows = self.lcd_config.lcd_rows
        columns = self.lcd_config.lcd_columns
        writer = ConsoleWriter(rows, columns)
        return writer

    def get_menu_coord(self) -> MenuCoordinator:
        rows = self.lcd_config.lcd_rows
        columns = self.lcd_config.lcd_columns
        menu_coord = MenuCoordinator(rows, columns, self.main_menu)
        return menu_coord

    def increment_option(self):
        self.menu_coord.increment_selection()
        chars = self.menu_coord.get_chars()
        self.writer.write(chars, 0.0)

    def decrement_option(self):
        self.menu_coord.decrement_selection()
        chars = self.menu_coord.get_chars()
        self.writer.write(chars, 0.0)

    def apply_option(self):
        self.menu_coord.apply_selection()
        chars = self.menu_coord.get_chars()
        self.writer.write(chars, 0.0)

    def back_option(self):
        self.menu_coord.back_selection()
        chars = self.menu_coord.get_chars()
        self.writer.write(chars, 0.0)

    def update_options(self):
        chars = self.menu_coord.get_chars()
        self.writer.write(chars, 0.0)

    def loop(self):
        chars = self.menu_coord.get_chars()
        self.writer.write(chars, 0.0)
        counter = 0

        while True:
            counter += 1
            self.controller.check()
            if counter >= self.tick_rate.get_tickrate():
                self.update_options()
                counter = 0

            time.sleep(0.01)


if __name__ == "__main__":
    ctrl_config = KBCtrlConfig()
    lcd_config = LCD2004Config()

    menu_handler = MenuHandler(ctrl_config, lcd_config)
    menu_handler.loop()
