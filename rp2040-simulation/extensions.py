from gc import mem_alloc, mem_free
from machine import freq
from machine import Pin, I2C


class abstractmethod:
    "Dummy abstractmethod wrapper."


class ABC:
    "Dummy ABC type."


class Callable:
    "Dummy Callable type."


class Optional:
    "Dummy Optional type."


class Literal:
    "Dummy Literal type."


class InputGPIOBase:
    def __init__(self, pin: int):
        self._pin = pin
        self._handle = Pin(self._pin, Pin.IN)


class InputGPIO(InputGPIOBase):
    def __init__(self, pin: int):
        super().__init__(pin)

    def set_pull_up(self):
        self._handle = Pin(self._pin, Pin.IN, Pin.PULL_UP)

    def set_pull_down(self):
        self._handle = Pin(self._pin, Pin.IN, Pin.PULL_DOWN)

    def set_pull_off(self):
        self._handle = Pin(self._pin, Pin.IN)

    def read(self) -> int:
        return self._handle.value()


class OutputGPIOBase:
    def __init__(self, pin: int):
        self._pin = Pin(pin, Pin.OUT)


class OutputGPIO(OutputGPIOBase):
    def __init__(self, pin: int):
        super().__init__(pin)

    def write(self, state: bool):
        self._pin.value(int(state))


class I2CGPIOBase:
    def __init__(self, bus: int, address: int):
        self._handle = self._register_i2c(bus)
        self._bus = bus
        self._address = address

    def _register_i2c(self, bus: int) -> I2C:
        return I2C(bus, sda=Pin(0), scl=Pin(1))


class I2CGPIO(I2CGPIOBase):
    def __init__(self, bus: int, address: int):
        super().__init__(bus, address)

    def write_device(self, buffer: list[int]):
        self._handle.writeto(self._address, bytes(buffer))


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
