import platform
import psutil

from typing import Callable

from options.abstracts import Option, OptionToggle
from options.item import MenuItem


class Option1(Option):
    def __init__(self, item: MenuItem):
        self.item = item
        self.update_menu_item()

    def update_menu_item(self):
        string = "Option 1"
        self.item.set_string(string)

    def update(self):
        self.item.increment_shift_item()

    def get_string(self) -> str:
        return self.item.get_formatted()


class Option2(Option):
    def __init__(self, item: MenuItem):
        self.item = item
        self.update_menu_item()

    def update_menu_item(self):
        string = "Option 2"
        self.item.set_string(string)

    def update(self):
        self.item.increment_shift_item()

    def get_string(self) -> str:
        return self.item.get_formatted()


class Option3(Option):
    def __init__(self, item: MenuItem):
        self.item = item

        self.update_menu_item()

    def update_menu_item(self):
        string = "Option 3"
        self.item.set_string(string)

    def update(self):
        self.item.increment_shift_item()

    def get_string(self) -> str:
        return self.item.get_formatted()


class Option4(Option):
    def __init__(self, item: MenuItem):
        self.item = item
        self.update_menu_item()

    def update_menu_item(self):
        string = "Option 4"
        self.item.set_string(string)

    def update(self):
        self.item.increment_shift_item()

    def get_string(self) -> str:
        return self.item.get_formatted()


class Option5(Option):
    def __init__(self, item: MenuItem):
        self.item = item
        self.update_menu_item()

    def update_menu_item(self):
        string = "Option 6"
        self.item.set_string(string)

    def update(self):
        self.item.increment_shift_item()

    def get_string(self) -> str:
        return self.item.get_formatted()


class Option6(Option):
    def __init__(self, item: MenuItem):
        self.item = item
        self.update_menu_item()

    def update_menu_item(self):
        string = "Option 6"
        self.item.set_string(string)

    def update(self):
        self.item.increment_shift_item()

    def get_string(self) -> str:
        return self.item.get_formatted()


class SystemInfo(Option):
    def __init__(self, item: MenuItem):
        self.item = item
        self.update_menu_item()

    def update_menu_item(self):
        string = "System Info"
        self.item.set_string(string)

    def update(self):
        self.item.increment_shift_item()

    def get_string(self) -> str:
        return self.item.get_formatted()


class DisplayConfig(Option):
    def __init__(self, item: MenuItem):
        self.item = item
        self.update_menu_item()

    def update_menu_item(self):
        string = "Display Config"
        self.item.set_string(string)

    def update(self):
        self.item.increment_shift_item()

    def get_string(self) -> str:
        return self.item.get_formatted()


class BacklightToggle(OptionToggle):
    def __init__(self, item: MenuItem, callback: Callable, state_callback: Callable):
        self.item = item
        self.callback = callback
        self.state_callback = state_callback
        self.update_menu_item()

    def update_menu_item(self):
        string = "Backlight: {}"
        string = string.format(self.get_backlight_state())
        self.item.set_string(string)

    def get_backlight_state(self) -> str:
        if self.get_state():
            return "ON"
        return "OFF"

    def update(self):
        self.update_menu_item()
        self.item.increment_shift_item()

    def get_string(self) -> str:
        return self.item.get_formatted()

    def get_state(self):
        return self.state_callback()

    def execute_callback(self):
        self.backlight = not self.backlight
        self.callback(self.backlight)


class CPUName(Option):
    def __init__(self, item: MenuItem):
        self.item = item
        self.update_menu_item()

    def update_menu_item(self):
        string = "CPU: {}"
        string = string.format(self.get_cpu_name())
        self.item.set_string(string)

    @staticmethod
    def get_cpu_name() -> str:
        cpu = platform.processor()
        return cpu

    def update(self):
        self.update_menu_item()
        self.item.increment_shift_item()

    def get_string(self) -> str:
        return self.item.get_formatted()


class CPUPerc(Option):
    def __init__(self, item: MenuItem):
        self.item = item
        self.update_menu_item()

    def update_menu_item(self):
        string = "Perc: {}%"
        string = string.format(self.get_cpu_perc())
        self.item.set_string(string)

    @staticmethod
    def get_cpu_perc() -> float:
        perc = psutil.cpu_times_percent().user
        return perc

    def update(self):
        self.update_menu_item()
        self.item.increment_shift_item()

    def get_string(self) -> str:
        return self.item.get_formatted()


class CPUFreq(Option):
    def __init__(self, item: MenuItem):
        self.item = item
        self.update_menu_item()

    def update_menu_item(self):
        string = "Freq: {}Mhz"
        string = string.format(self.get_cpu_freq())
        self.item.set_string(string)

    @staticmethod
    def get_cpu_freq() -> int:
        freq = psutil.cpu_freq().current
        freq = int(freq)
        return freq

    def update(self):
        self.update_menu_item()
        self.item.increment_shift_item()

    def get_string(self) -> str:
        return self.item.get_formatted()
