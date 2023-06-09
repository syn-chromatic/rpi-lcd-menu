from wgpio import OutputGPIO


class RelayDevice:
    def __init__(self, pin: int):
        self.gpio = OutputGPIO(pin)
        self.state = False
        self.gpio.write(self.state)

    def get_state(self) -> bool:
        return self.state

    def set_state(self, state: bool):
        self.state = state
        self.gpio.write(self.state)

    def switch(self):
        self.state = not self.state
        self.gpio.write(self.state)

    def switch_on(self):
        self.state = True
        self.gpio.write(self.state)

    def switch_off(self):
        self.state = False
        self.gpio.write(self.state)
