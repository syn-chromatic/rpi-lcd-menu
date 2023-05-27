import platform
import psutil

from abc import ABC, abstractmethod


class MenuItem:
    def __init__(self, string: str, chars: int):
        self.string = string
        self.chars = chars
        self.st_range = 0
        self.is_selected = False

    def get_string(self) -> str:
        exceed_condition = self.get_exceed_condition()
        if exceed_condition:
            en_range = self.st_range + (self.chars - 4)
            new_string = self.string[self.st_range : en_range]
            new_string += ".."
            return new_string
        return self.string[self.st_range :]

    def get_exceed_condition(self):
        if (len(self.string) - self.st_range) >= (self.chars - 4):
            if len(self.string) > (self.chars - 2):
                return True
        return False

    def increment_shift_item(self):
        exceed_condition = self.get_exceed_condition()
        if exceed_condition and self.is_selected:
            self.st_range += 1
            return
        self.st_range = 0


class MenuOption(ABC):
    def __init__(self, chars: int):
        self.chars = chars
        self.item: MenuItem

    @abstractmethod
    def update(self):
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

    def get_option_name(self) -> str:
        return self.item.get_string()


class Option2(MenuOption):
    def __init__(self, chars: int):
        self.chars = chars
        self.item = self.make_menu_item()

    def make_menu_item(self) -> MenuItem:
        name = "Option 2"
        return MenuItem(name, self.chars)

    def update(self):
        self.item.increment_shift_item()

    def get_option_name(self) -> str:
        return self.item.get_string()


class Option3(MenuOption):
    def __init__(self, chars: int):
        self.chars = chars
        self.item = self.make_menu_item()

    def make_menu_item(self) -> MenuItem:
        name = "Option 3"
        return MenuItem(name, self.chars)

    def update(self):
        self.item.increment_shift_item()

    def get_option_name(self) -> str:
        return self.item.get_string()


class Option4(MenuOption):
    def __init__(self, chars: int):
        self.chars = chars
        self.item = self.make_menu_item()

    def make_menu_item(self) -> MenuItem:
        name = "Option 4"
        return MenuItem(name, self.chars)

    def update(self):
        self.item.increment_shift_item()

    def get_option_name(self) -> str:
        return self.item.get_string()


class Option5(MenuOption):
    def __init__(self, chars: int):
        self.chars = chars
        self.item = self.make_menu_item()

    def make_menu_item(self) -> MenuItem:
        name = "Option 5 This is a test"
        return MenuItem(name, self.chars)

    def update(self):
        self.item.increment_shift_item()

    def get_option_name(self) -> str:
        return self.item.get_string()


class Option6(MenuOption):
    def __init__(self, chars: int):
        self.chars = chars
        self.item = self.make_menu_item()

    def make_menu_item(self) -> MenuItem:
        name = "Option 6"
        return MenuItem(name, self.chars)

    def update(self):
        self.item.increment_shift_item()

    def get_option_name(self) -> str:
        return self.item.get_string()


class SystemInfo(MenuOption):
    def __init__(self, chars: int):
        self.chars = chars
        self.item = self.make_menu_item()

    def make_menu_item(self) -> MenuItem:
        name = "System Info"
        return MenuItem(name, self.chars)

    def update(self):
        self.item.increment_shift_item()

    def get_option_name(self) -> str:
        return self.item.get_string()


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

    def get_option_name(self) -> str:
        return self.item.get_string()


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

    def get_option_name(self) -> str:
        return self.item.get_string()


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

    def get_option_name(self) -> str:
        return self.item.get_string()
