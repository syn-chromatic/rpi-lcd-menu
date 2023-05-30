import platform
import psutil

from options.abstracts import Option
from options.item import MenuItem


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

    def update_shift(self):
        self.item.shift()

    def get_string(self) -> str:
        return self.item.get_string()


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

    def update_shift(self):
        self.item.shift()

    def get_string(self) -> str:
        return self.item.get_string()


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

    def update_shift(self):
        self.item.shift()

    def get_string(self) -> str:
        return self.item.get_string()
