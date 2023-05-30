import lgpio as gp


class GPIO:
    def __init__(self, chip: int = 0):
        self.handle = gp.gpiochip_open(chip)

    def claim_input(self, pin: int, flag: int = 0):
        gp.gpio_claim_input(self.handle, pin, flag)

    def read(self, pin: int) -> int:
        return gp.gpio_read(self.handle, pin)

    def close(self):
        if hasattr(self, "handle"):
            gp.gpiochip_close(self.handle)

    def __del__(self):
        self.close()


class GPIOI2C:
    def __init__(self, bus: int, address: int):
        self.handle = gp.i2c_open(bus, address)

    def write_device(self, buffer: list[int]):
        gp.i2c_write_device(self.handle, buffer)

    def close(self):
        if hasattr(self, "handle"):
            gp.i2c_close(self.handle)

    def __del__(self):
        self.close()
