from x_gpio import GPIO


class Button:
    def __init__(self, bcm_pin: int):
        self.bcm_pin = bcm_pin
        self.gpio = self.register_pin()
        self.state = 1
        self.p_state = 1

    def register_pin(self) -> GPIO:
        gpio = GPIO()
        gpio.claim_input(self.bcm_pin, 32)
        return gpio

    def get_state(self) -> int:
        self.state = self.gpio.read(self.bcm_pin)
        return self.state

    def is_pressed(self) -> bool:
        self.p_state = self.state
        state = self.get_state()
        if state == 1 and self.p_state == 0:
            return True
        return False
