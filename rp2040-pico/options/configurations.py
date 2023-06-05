import platform
import psutil

from options.abstracts import Option
from options.item import MenuItem


class CPUArch(Option):
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


class CPUCoreCount(Option):
    def __init__(self, item: MenuItem):
        self.item = item
        self.update_menu_item()

    def update_menu_item(self):
        string = "Core Count: {}"
        string = string.format(self.get_core_count())
        self.item.set_string(string)

    @staticmethod
    def get_core_count() -> int:
        core_count = psutil.cpu_count()
        return core_count

    def update(self):
        self.update_menu_item()

    def update_shift(self):
        self.item.shift()

    def get_string(self) -> str:
        return self.item.get_string()


class MemoryTotal(Option):
    def __init__(self, item: MenuItem):
        self.item = item
        self.update_menu_item()

    def update_menu_item(self):
        string = "TMem: {:.1f}GB"
        string = string.format(self.get_total_memory())
        self.item.set_string(string)

    @staticmethod
    def get_total_memory() -> float:
        total_mem = psutil.virtual_memory().total
        total_mem_gb = total_mem / 1024 / 1024 / 1024
        return total_mem_gb

    def update(self):
        self.update_menu_item()

    def update_shift(self):
        self.item.shift()

    def get_string(self) -> str:
        return self.item.get_string()


class MemoryUsed(Option):
    def __init__(self, item: MenuItem):
        self.item = item
        self.update_menu_item()

    def update_menu_item(self):
        string = "UMem: {:.1f}GB"
        string = string.format(self.get_used_memory())
        self.item.set_string(string)

    @staticmethod
    def get_used_memory() -> float:
        used_mem = psutil.virtual_memory().used
        used_mem_gb = used_mem / 1024 / 1024 / 1024
        return used_mem_gb

    def update(self):
        self.update_menu_item()

    def update_shift(self):
        self.item.shift()

    def get_string(self) -> str:
        return self.item.get_string()


class MemoryFree(Option):
    def __init__(self, item: MenuItem):
        self.item = item
        self.update_menu_item()

    def update_menu_item(self):
        string = "FMem: {:.1f}GB"
        string = string.format(self.get_free_memory())
        self.item.set_string(string)

    @staticmethod
    def get_free_memory() -> float:
        free_mem = psutil.virtual_memory().free
        free_mem_gb = free_mem / 1024 / 1024 / 1024
        return free_mem_gb

    def update(self):
        self.update_menu_item()

    def update_shift(self):
        self.item.shift()

    def get_string(self) -> str:
        return self.item.get_string()


class MemoryPerc(Option):
    def __init__(self, item: MenuItem):
        self.item = item
        self.update_menu_item()

    def update_menu_item(self):
        string = "PMem: {}%"
        string = string.format(self.get_memory_percentage())
        self.item.set_string(string)

    @staticmethod
    def get_memory_percentage() -> int:
        mem_perc = psutil.virtual_memory().percent
        mem_perc = int(mem_perc)
        return mem_perc

    def update(self):
        self.update_menu_item()

    def update_shift(self):
        self.item.shift()

    def get_string(self) -> str:
        return self.item.get_string()
