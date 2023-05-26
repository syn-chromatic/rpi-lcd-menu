import platform
import psutil

from abc import ABC, abstractmethod


class MenuOption(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def get_option_name(self) -> str:
        pass


class Option1(MenuOption):
    def __init__(self):
        self.name = "Option 1"

    def update(self):
        pass

    def get_option_name(self) -> str:
        return self.name


class Option2(MenuOption):
    def __init__(self):
        self.name = "Option 2"

    def update(self):
        pass

    def get_option_name(self) -> str:
        return self.name


class Option3(MenuOption):
    def __init__(self):
        self.name = "Option 3"

    def update(self):
        pass

    def get_option_name(self) -> str:
        return self.name


class Option4(MenuOption):
    def __init__(self):
        self.name = "Option 4"

    def update(self):
        pass

    def get_option_name(self) -> str:
        return self.name


class Option5(MenuOption):
    def __init__(self):
        self.name = "Option 5"

    def update(self):
        pass

    def get_option_name(self) -> str:
        return self.name


class Option6(MenuOption):
    def __init__(self):
        self.name = "Option 6"

    def update(self):
        pass

    def get_option_name(self) -> str:
        return self.name


class SystemInfo(MenuOption):
    def __init__(self):
        self.name = "System Info"

    def update(self):
        pass

    def get_option_name(self) -> str:
        return self.name


class CPUName(MenuOption):
    def __init__(self):
        self.name = self.get_option_name()

    @staticmethod
    def get_cpu_name() -> str:
        cpu = platform.processor()
        return cpu

    def update(self):
        self.name = self.get_option_name()

    def get_option_name(self) -> str:
        cpu = self.get_cpu_name()
        return cpu


class CPUPerc(MenuOption):
    def __init__(self):
        self.name = self.get_option_name()

    @staticmethod
    def get_cpu_perc() -> int:
        perc = psutil.cpu_percent()
        perc = int(perc)
        return perc

    def update(self):
        self.name = self.get_option_name()

    def get_option_name(self) -> str:
        perc = self.get_cpu_perc()
        string = "Perc: {}%"
        string = string.format(perc)
        return string


class CPUFreq(MenuOption):
    def __init__(self):
        self.name = self.get_option_name()

    @staticmethod
    def get_cpu_freq() -> int:
        freq = psutil.cpu_freq().current
        freq = int(freq)
        return freq

    def update(self):
        self.name = self.get_option_name()

    def get_option_name(self) -> str:
        freq = self.get_cpu_freq()
        string = "Freq: {}Mhz"
        string = string.format(freq)
        return string
