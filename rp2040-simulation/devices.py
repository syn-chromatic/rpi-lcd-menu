from extensions import InputGPIO, OutputGPIO


class Button:
    def __init__(self, bcm_pin: int):
        self.bcm_pin = bcm_pin
        self.gpio = self.register_pin()
        self.state = 1
        self.p_state = 1

    def register_pin(self) -> InputGPIO:
        gpio = InputGPIO(self.bcm_pin)
        gpio.set_pull_up()
        return gpio

    def get_state(self) -> int:
        self.state = self.gpio.read()
        return self.state

    def is_pressed(self) -> bool:
        self.p_state = self.state
        state = self.get_state()
        if state == 1 and self.p_state == 0:
            return True
        return False


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
