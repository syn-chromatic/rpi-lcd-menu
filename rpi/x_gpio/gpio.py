import pigpio


class GPIOInputBase:
    def __init__(self, pin: int):
        self._pi = pigpio.pi()
        self._pin = pin

    def _setup_input_mode(self):
        self._pi.set_mode(self._pin, pigpio.INPUT)


class GPIOInput(GPIOInputBase):
    def __init__(self, pin: int):
        super().__init__(pin)

    def set_pull_up(self):
        self._pi.set_pull_up_down(self._pin, pigpio.PUD_UP)

    def set_pull_down(self):
        self._pi.set_pull_up_down(self._pin, pigpio.PUD_DOWN)

    def set_pull_off(self):
        self._pi.set_pull_up_down(self._pin, pigpio.PUD_OFF)

    def read(self) -> int:
        return self._pi.read(self._pin)


class GPIOI2CBase:
    def __init__(self, bus: int, address: int):
        self._pi = pigpio.pi()
        self._bus = bus
        self._address = address
        self._handle = self._setup_i2c()

    def _setup_i2c(self):
        return self._pi.i2c_open(self._bus, self._address)


class GPIOI2C(GPIOI2CBase):
    def __init__(self, bus: int, address: int):
        super().__init__(bus, address)

    def write_device(self, buffer: list[int]):
        self._pi.i2c_write_device(self._handle, buffer)

    def close(self):
        if hasattr(self, "_handle"):
            self._pi.i2c_close(self._handle)

    def __del__(self):
        self.close()
