from machine import freq
from gc import mem_alloc, mem_free


class Processor:
    def get_processor_name(self) -> str:
        return "RP2040"

    def get_usage(self) -> float:
        return 0.0

    def get_frequency_mhz(self) -> float:
        return freq() / 1e6

    def get_core_count(self) -> int:
        return 2


class System:
    def get_system_name(self) -> str:
        return ""

    def get_total_memory_bytes(self) -> int:
        used_mem = self.get_used_memory_bytes()
        free_mem = self.get_free_memory_bytes()
        return used_mem + free_mem

    def get_used_memory_bytes(self) -> int:
        return mem_alloc()

    def get_free_memory_bytes(self) -> int:
        return mem_free()

    def get_memory_usage(self) -> float:
        used_mem = self.get_used_memory_bytes()
        free_mem = self.get_free_memory_bytes()
        total_mem = used_mem + free_mem

        percentage = (used_mem / total_mem) * 100
        return percentage
