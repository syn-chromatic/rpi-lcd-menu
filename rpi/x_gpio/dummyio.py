class GPIO:
    def __init__(self, chip: int = 0):
        pass

    def claim_input(self, pin: int, flag: int = 0):
        pass

    def read(self, pin: int) -> int:
        return 1

    def close(self):
        pass

    def __del__(self):
        self.close()


class GPIOI2C:
    def __init__(self, bus: int, address: int):
        pass

    def write_device(self, buffer: list[int]):
        pass

    def close(self):
        pass

    def __del__(self):
        self.close()
