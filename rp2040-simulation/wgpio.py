from machine import Pin, I2C


class GPIOInputBase:
    def __init__(self, pin: int):
        self._pin = pin
        self._handle = Pin(self._pin, Pin.IN)


class GPIOInput(GPIOInputBase):
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


class GPIOI2CBase:
    def __init__(self, bus: int, address: int):
        self._handle = self._register_i2c(bus)
        self._bus = bus
        self._address = address

    def _register_i2c(self, bus: int) -> I2C:
        return I2C(bus, sda=Pin(0), scl=Pin(1))


class GPIOI2C(GPIOI2CBase):
    def __init__(self, bus: int, address: int):
        super().__init__(bus, address)

    def write_device(self, buffer: list[int]):
        self._handle.writeto(self._address, bytes(buffer))
