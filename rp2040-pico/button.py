from x_gpio import GPIOInput


class Button:
    def __init__(self, bcm_pin: int):
        self.gpio = GPIOInput(bcm_pin)
        self.state = 1
        self.p_state = 1

    def get_state(self) -> int:
        self.state = self.gpio.read()
        return self.state

    def is_pressed(self) -> bool:
        self.p_state = self.state
        state = self.get_state()
        if state == 1 and self.p_state == 0:
            return True
        return False
