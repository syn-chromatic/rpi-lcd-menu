import platform
import psutil

from options.abstracts import OptionABC
from options.item import MenuItem

from character.abstracts import CharABC


class CPUArchBase(OptionABC):
    def __init__(self, item: MenuItem):
        self._item = item
        self._value = self._get_cpu_name()
        self._update_menu_item()

    def _get_value(self) -> str:
        self._value = self._get_cpu_name()
        return self._value

    def _update_menu_item(self):
        string = "CPU: {}"
        string = string.format(self._get_value())
        self._item.set_string(string)

    @staticmethod
    def _get_cpu_name() -> str:
        cpu = platform.processor()
        return cpu


class CPUArch(CPUArchBase):
    def __init__(self, item: MenuItem):
        super().__init__(item)

    def back(self):
        pass

    def prev(self):
        pass

    def next(self):
        pass

    def apply(self):
        pass

    def get_hold_state(self) -> bool:
        return False

    def get_char_array(self) -> list[CharABC]:
        return self._item.get_char_array()

    def get_item(self) -> MenuItem:
        return self._item

    def update(self):
        self._update_menu_item()

    def update_shift(self):
        self._item.shift()


class CPUPercBase(OptionABC):
    def __init__(self, item: MenuItem):
        self._item = item
        self._value = self._get_cpu_perc()
        self._update_menu_item()

    def _get_value(self) -> float:
        self._value = self._get_cpu_perc()
        return self._value

    def _update_menu_item(self):
        string = "Perc: {}%"
        string = string.format(self._get_value())
        self._item.set_string(string)

    @staticmethod
    def _get_cpu_perc() -> float:
        perc = psutil.cpu_times_percent().user
        return perc


class CPUPerc(CPUPercBase):
    def __init__(self, item: MenuItem):
        super().__init__(item)

    def back(self):
        pass

    def prev(self):
        pass

    def next(self):
        pass

    def apply(self):
        pass

    def get_hold_state(self) -> bool:
        return False

    def get_char_array(self) -> list[CharABC]:
        return self._item.get_char_array()

    def get_item(self) -> MenuItem:
        return self._item

    def update(self):
        self._update_menu_item()

    def update_shift(self):
        self._item.shift()


class CPUFreqBase(OptionABC):
    def __init__(self, item: MenuItem):
        self._item = item
        self._value = self._get_cpu_freq()
        self._update_menu_item()

    def _get_value(self) -> int:
        self._value = self._get_cpu_freq()
        return self._value

    def _update_menu_item(self):
        string = "Freq: {}Mhz"
        string = string.format(self._get_value())
        self._item.set_string(string)

    @staticmethod
    def _get_cpu_freq() -> int:
        freq = psutil.cpu_freq().current
        freq = int(freq)
        return freq


class CPUFreq(CPUFreqBase):
    def __init__(self, item: MenuItem):
        super().__init__(item)

    def back(self):
        pass

    def prev(self):
        pass

    def next(self):
        pass

    def apply(self):
        pass

    def get_hold_state(self) -> bool:
        return False

    def get_char_array(self) -> list[CharABC]:
        return self._item.get_char_array()

    def get_item(self) -> MenuItem:
        return self._item

    def update(self):
        self._update_menu_item()

    def update_shift(self):
        self._item.shift()


class CPUCoreCountBase(OptionABC):
    def __init__(self, item: MenuItem):
        self._item = item
        self._value = self._get_core_count()
        self._update_menu_item()

    def _get_value(self) -> int:
        return self._value

    def _update_menu_item(self):
        string = "Core Count: {}"
        string = string.format(self._get_value())
        self._item.set_string(string)

    @staticmethod
    def _get_core_count() -> int:
        core_count = psutil.cpu_count()
        return core_count


class CPUCoreCount(CPUCoreCountBase):
    def __init__(self, item: MenuItem):
        super().__init__(item)

    def back(self):
        pass

    def prev(self):
        pass

    def next(self):
        pass

    def apply(self):
        pass

    def get_hold_state(self) -> bool:
        return False

    def get_char_array(self) -> list[CharABC]:
        return self._item.get_char_array()

    def get_item(self) -> MenuItem:
        return self._item

    def update(self):
        self._update_menu_item()

    def update_shift(self):
        self._item.shift()


class MemoryTotalBase(OptionABC):
    def __init__(self, item: MenuItem):
        self._item = item
        self._value = self._get_total_memory()
        self._update_menu_item()

    def _get_value(self) -> float:
        self._value = self._get_total_memory()
        return self._value

    def _update_menu_item(self):
        string = "TMem: {:.1f}GB"
        string = string.format(self._get_value())
        self._item.set_string(string)

    @staticmethod
    def _get_total_memory() -> float:
        total_mem = psutil.virtual_memory().total
        total_mem_gb = total_mem / 1024 / 1024 / 1024
        return total_mem_gb


class MemoryTotal(MemoryTotalBase):
    def __init__(self, item: MenuItem):
        super().__init__(item)

    def back(self):
        pass

    def prev(self):
        pass

    def next(self):
        pass

    def apply(self):
        pass

    def get_hold_state(self) -> bool:
        return False

    def get_char_array(self) -> list[CharABC]:
        return self._item.get_char_array()

    def get_item(self) -> MenuItem:
        return self._item

    def update(self):
        self._update_menu_item()

    def update_shift(self):
        self._item.shift()


class MemoryUsedBase(OptionABC):
    def __init__(self, item: MenuItem):
        self._item = item
        self._value = self._get_used_memory()
        self._update_menu_item()

    def _get_value(self):
        self._value = self._get_used_memory()
        return self._value

    def _update_menu_item(self):
        string = "UMem: {:.1f}GB"
        string = string.format(self._get_value())
        self._item.set_string(string)

    @staticmethod
    def _get_used_memory() -> float:
        used_mem = psutil.virtual_memory().used
        used_mem_gb = used_mem / 1024 / 1024 / 1024
        return used_mem_gb


class MemoryUsed(MemoryUsedBase):
    def __init__(self, item: MenuItem):
        super().__init__(item)

    def back(self):
        pass

    def prev(self):
        pass

    def next(self):
        pass

    def apply(self):
        pass

    def get_hold_state(self) -> bool:
        return False

    def get_char_array(self) -> list[CharABC]:
        return self._item.get_char_array()

    def get_item(self) -> MenuItem:
        return self._item

    def update(self):
        self._update_menu_item()

    def update_shift(self):
        self._item.shift()


class MemoryFreeBase(OptionABC):
    def __init__(self, item: MenuItem):
        self._item = item
        self._value = self._get_free_memory()
        self._update_menu_item()

    def _get_value(self):
        self._value = self._get_free_memory()
        return self._value

    def _update_menu_item(self):
        string = "FMem: {:.1f}GB"
        string = string.format(self._get_value())
        self._item.set_string(string)

    @staticmethod
    def _get_free_memory() -> float:
        free_mem = psutil.virtual_memory().free
        free_mem_gb = free_mem / 1024 / 1024 / 1024
        return free_mem_gb


class MemoryFree(MemoryFreeBase):
    def __init__(self, item: MenuItem):
        super().__init__(item)

    def back(self):
        pass

    def prev(self):
        pass

    def next(self):
        pass

    def apply(self):
        pass

    def get_hold_state(self) -> bool:
        return False

    def get_char_array(self) -> list[CharABC]:
        return self._item.get_char_array()

    def get_item(self) -> MenuItem:
        return self._item

    def update(self):
        self._update_menu_item()

    def update_shift(self):
        self._item.shift()


class MemoryPercBase(OptionABC):
    def __init__(self, item: MenuItem):
        self._item = item
        self._value = self._get_memory_percentage()
        self._update_menu_item()

    def _get_value(self) -> int:
        self._value = self._get_memory_percentage()
        return self._value

    def _update_menu_item(self):
        string = "PMem: {}%"
        string = string.format(self._get_value())
        self._item.set_string(string)

    @staticmethod
    def _get_memory_percentage() -> int:
        mem_perc = psutil.virtual_memory().percent
        mem_perc = int(mem_perc)
        return mem_perc


class MemoryPerc(MemoryPercBase):
    def __init__(self, item: MenuItem):
        super().__init__(item)

    def back(self):
        pass

    def prev(self):
        pass

    def next(self):
        pass

    def apply(self):
        pass

    def get_hold_state(self) -> bool:
        return False

    def get_char_array(self) -> list[CharABC]:
        return self._item.get_char_array()

    def get_item(self) -> MenuItem:
        return self._item

    def update(self):
        self._update_menu_item()

    def update_shift(self):
        self._item.shift()
