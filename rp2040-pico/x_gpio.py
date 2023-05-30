from machine import Pin, I2C


class GPIOInputBase:
    def __init__(self, pin: int):
        self._handle = self._register_pin(pin)

    def _register_pin(self, pin: int):
        return Pin(pin, Pin.IN, Pin.PULL_UP)


class GPIOInput(GPIOInputBase):
    def __init__(self, pin: int):
        super().__init__(pin)

    def read(self):
        return self._handle.value()


class GPIOI2CBase:
    def __init__(self, bus: int, address: int, frequency: int):
        self._handle = self._register_i2c(bus, frequency)
        self._bus = bus
        self._address = address
        self._frequency = frequency

    def _register_i2c(self, bus: int, frequency: int):
        return I2C(bus, sda=Pin(0), scl=Pin(1), freq=frequency)


class GPIOI2C(GPIOI2CBase):
    def __init__(self, bus: int, address: int, frequency: int):
        super().__init__(bus, address, frequency)

    def write_device(self, buffer: list[int]):
        self._handle.writeto(self._address, bytes(buffer))
