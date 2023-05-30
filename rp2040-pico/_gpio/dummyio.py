class GPIOInputBase:
    def __init__(self, pin: int):
        self._handle = self._register_pin(pin)

    def _register_pin(self, pin: int):
        pass


class GPIOInput(GPIOInputBase):
    def __init__(self, pin: int):
        super().__init__(pin)

    def read(self):
        return 1


class GPIOI2CBase:
    def __init__(self, bus: int, address: int, frequency: int):
        self._handle = self._register_i2c(bus, address, frequency)
        self._bus = bus
        self._address = address
        self._frequency = frequency

    def _register_i2c(self, bus: int, address: int, frequency: int):
        pass


class GPIOI2C(GPIOI2CBase):
    def __init__(self, bus: int, address: int, frequency: int):
        super().__init__(bus, address, frequency)

    def write_device(self, buffer: list[int]):
        pass
