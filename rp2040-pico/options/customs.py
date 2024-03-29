from options.abstracts import OptionABC
from options.item import MenuItem
from character.abstracts import CharABC
from extensions.general import Processor, System


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
        cpu = Processor().get_processor_name()
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
        perc = Processor().get_usage()
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
        freq = Processor().get_frequency_mhz()
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
        core_count = Processor().get_core_count()
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
        string = "TMem: {:.1f}KB"
        string = string.format(self._get_value())
        self._item.set_string(string)

    @staticmethod
    def _get_total_memory() -> float:
        total_mem = System().get_total_memory_bytes()
        total_mem_kb = total_mem / 1024
        return total_mem_kb


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
        string = "UMem: {:.1f}KB"
        string = string.format(self._get_value())
        self._item.set_string(string)

    @staticmethod
    def _get_used_memory() -> float:
        used_mem = System().get_used_memory_bytes()
        used_mem_kb = used_mem / 1024
        return used_mem_kb


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
        string = "FMem: {:.1f}KB"
        string = string.format(self._get_value())
        self._item.set_string(string)

    @staticmethod
    def _get_free_memory() -> float:
        free_mem = System().get_free_memory_bytes()
        free_mem_kb = free_mem / 1024
        return free_mem_kb


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
        mem_perc = System().get_memory_usage()
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
