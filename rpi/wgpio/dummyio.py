class InputGPIO:
    def __init__(self, pin: int):
        pass

    def set_pull_up(self):
        pass

    def set_pull_down(self):
        pass

    def set_pull_off(self):
        pass

    def read(self) -> int:
        return 1


class OutputGPIO:
    def __init__(self, pin: int):
        pass

    def write(self, state: bool):
        pass


class I2CGPIO:
    def __init__(self, bus: int, address: int):
        pass

    def write_device(self, buffer: list[int]):
        pass

    def close(self):
        pass

    def __del__(self):
        self.close()
