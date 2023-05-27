import platform
import psutil

from typing import Callable
from abc import ABC, abstractmethod


class MenuItem:
    def __init__(self, string: str, chars: int):
        self.string = string
        self.chars = chars
        self.st_range = 0
        self.is_selected = False

    def get_formatted_item(self):
        if self.is_selected:
            return "> " + self.get_string() + "\n"
        return "x " + self.get_string() + "\n"

    def get_string(self) -> str:
        diff_length = self.get_diff_length()
        max_trim_chars = self.get_max_trim_chars()
        max_chars = self.get_max_chars()
        if len(self.string) > max_chars:
            if diff_length >= max_trim_chars:
                en_range = self.st_range + (self.chars - 4)
                new_string = self.string[self.st_range : en_range]
                new_string += ".."
                return new_string
        return self.string[self.st_range :]

    def get_diff_length(self) -> int:
        len_string = len(self.string)
        return len_string - self.st_range

    def get_max_trim_chars(self) -> int:
        return self.chars - 4

    def get_max_chars(self) -> int:
        return self.chars - 2

    def increment_shift_item(self):
        diff_length = self.get_diff_length()
        max_trim_chars = self.get_max_trim_chars()
        max_chars = self.get_max_chars()
        if len(self.string) > max_chars:
            if diff_length > max_trim_chars and self.is_selected:
                self.st_range += 1
                return
        self.st_range = 0


class MenuOption(ABC):
    def __init__(self):
        self.chars: int
        self.item: MenuItem

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def set_callback(self, callback: Callable):
        pass

    @abstractmethod
    def execute_callback(self):
        pass

    @abstractmethod
    def get_option_name(self) -> str:
        pass


class Option1(MenuOption):
    def __init__(self, chars: int):
        self.chars = chars
        self.item = self.make_menu_item()

    def make_menu_item(self) -> MenuItem:
        name = "Option 1"
        return MenuItem(name, self.chars)

    def update(self):
        self.item.increment_shift_item()

    def set_callback(self, _: Callable):
        pass

    def execute_callback(self):
        pass

    def get_option_name(self) -> str:
        return self.item.get_formatted_item()


class Option2(MenuOption):
    def __init__(self, chars: int):
        self.chars = chars
        self.item = self.make_menu_item()

    def make_menu_item(self) -> MenuItem:
        name = "Option 2"
        return MenuItem(name, self.chars)

    def update(self):
        self.item.increment_shift_item()

    def set_callback(self, _: Callable):
        pass

    def execute_callback(self):
        pass

    def get_option_name(self) -> str:
        return self.item.get_formatted_item()


class Option3(MenuOption):
    def __init__(self, chars: int):
        self.chars = chars
        self.item = self.make_menu_item()

    def make_menu_item(self) -> MenuItem:
        name = "Option 3"
        return MenuItem(name, self.chars)

    def update(self):
        self.item.increment_shift_item()

    def set_callback(self, _: Callable):
        pass

    def execute_callback(self):
        pass

    def get_option_name(self) -> str:
        return self.item.get_formatted_item()


class Option4(MenuOption):
    def __init__(self, chars: int):
        self.chars = chars
        self.item = self.make_menu_item()

    def make_menu_item(self) -> MenuItem:
        name = "Option 4"
        return MenuItem(name, self.chars)

    def update(self):
        self.item.increment_shift_item()

    def set_callback(self, _: Callable):
        pass

    def execute_callback(self):
        pass

    def get_option_name(self) -> str:
        return self.item.get_formatted_item()


class Option5(MenuOption):
    def __init__(self, chars: int):
        self.chars = chars
        self.item = self.make_menu_item()

    def make_menu_item(self) -> MenuItem:
        name = "Option 5 This is a test"
        return MenuItem(name, self.chars)

    def update(self):
        self.item.increment_shift_item()

    def set_callback(self, _: Callable):
        pass

    def execute_callback(self):
        pass

    def get_option_name(self) -> str:
        return self.item.get_formatted_item()


class Option6(MenuOption):
    def __init__(self, chars: int):
        self.chars = chars
        self.item = self.make_menu_item()

    def make_menu_item(self) -> MenuItem:
        name = "Option 6"
        return MenuItem(name, self.chars)

    def update(self):
        self.item.increment_shift_item()

    def set_callback(self, _: Callable):
        pass

    def execute_callback(self):
        pass

    def get_option_name(self) -> str:
        return self.item.get_formatted_item()


class SystemInfo(MenuOption):
    def __init__(self, chars: int):
        self.chars = chars
        self.item = self.make_menu_item()

    def make_menu_item(self) -> MenuItem:
        name = "System Info"
        return MenuItem(name, self.chars)

    def update(self):
        self.item.increment_shift_item()

    def set_callback(self, _: Callable):
        pass

    def execute_callback(self):
        pass

    def get_option_name(self) -> str:
        return self.item.get_formatted_item()


class BacklightToggle(MenuOption):
    def __init__(self, chars: int):
        self.chars = chars
        self.item = self.make_menu_item()
        self.backlight = False

    def get_backlight_state(self) -> str:
        if self.backlight:
            return "ON"
        return "OFF"

    def make_menu_item(self) -> MenuItem:
        name = "Backlight: {}"
        backlight_state = self.get_backlight_state()
        name = name.format(backlight_state)
        return MenuItem(name, self.chars)

    def update(self):
        self.item.increment_shift_item()

    def set_callback(self, callback: Callable):
        self.callback = callback

    def execute_callback(self):
        self.backlight = not self.backlight
        self.callback(self.backlight)

    def get_option_name(self) -> str:
        return self.item.get_formatted_item()


class CPUName(MenuOption):
    def __init__(self, chars: int):
        self.chars = chars
        self.item = self.make_menu_item()

    def make_menu_item(self) -> MenuItem:
        name = self.make_menu_name()
        return MenuItem(name, self.chars)

    def make_menu_name(self) -> str:
        cpu = self.get_cpu_name()
        string = "CPU: {}"
        string = string.format(cpu)
        return string

    @staticmethod
    def get_cpu_name() -> str:
        cpu = platform.processor()
        return cpu

    def update(self):
        self.item = self.make_menu_item()
        self.item.increment_shift_item()

    def set_callback(self, _: Callable):
        pass

    def execute_callback(self):
        pass

    def get_option_name(self) -> str:
        return self.item.get_formatted_item()


class CPUPerc(MenuOption):
    def __init__(self, chars: int):
        self.chars = chars
        self.item = self.make_menu_item()

    def make_menu_item(self) -> MenuItem:
        name = self.make_menu_name()
        return MenuItem(name, self.chars)

    def make_menu_name(self) -> str:
        perc = self.get_cpu_perc()
        string = "Perc: {}%"
        string = string.format(perc)
        return string

    @staticmethod
    def get_cpu_perc() -> float:
        perc = psutil.cpu_times_percent().user
        return perc

    def update(self):
        self.item = self.make_menu_item()
        self.item.increment_shift_item()

    def set_callback(self, _: Callable):
        pass

    def execute_callback(self):
        pass

    def get_option_name(self) -> str:
        return self.item.get_formatted_item()


class CPUFreq(MenuOption):
    def __init__(self, chars: int):
        self.chars = chars
        self.item = self.make_menu_item()

    def make_menu_item(self) -> MenuItem:
        name = self.make_menu_name()
        return MenuItem(name, self.chars)

    def make_menu_name(self) -> str:
        freq = self.get_cpu_freq()
        string = "Freq: {}Mhz"
        string = string.format(freq)
        return string

    @staticmethod
    def get_cpu_freq() -> int:
        freq = psutil.cpu_freq().current
        freq = int(freq)
        return freq

    def update(self):
        self.item = self.make_menu_item()
        self.item.increment_shift_item()

    def set_callback(self, _: Callable):
        pass

    def execute_callback(self):
        pass

    def get_option_name(self) -> str:
        return self.item.get_formatted_item()
