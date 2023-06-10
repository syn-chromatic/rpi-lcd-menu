import platform
import psutil

# For compatibility with MicroPython.
# The MicroPython codebase will have its own implementation here.


class Processor:
    def get_processor_name(self) -> str:
        return platform.processor()

    def get_usage(self) -> float:
        return psutil.cpu_times_percent().user

    def get_frequency(self) -> float:
        return psutil.cpu_freq().current

    def get_core_count(self) -> int:
        return psutil.cpu_count()


class System:
    def get_system_name(self) -> str:
        return ""

    def get_total_memory_bytes(self) -> int:
        return psutil.virtual_memory().total

    def get_used_memory_bytes(self) -> int:
        return psutil.virtual_memory().used

    def get_free_memory_bytes(self) -> int:
        return psutil.virtual_memory().free

    def get_memory_usage(self) -> float:
        return psutil.virtual_memory().percent
