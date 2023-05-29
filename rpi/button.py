import lgpio as gp
from typing import Literal


class Button:
    def __init__(self, bcm_pin: int):
        self.bcm_pin = bcm_pin
        self.handle = self.register_pin()
        self.state = 1
        self.p_state = 1

    def register_pin(self):
        handle = gp.gpiochip_open(0)
        gp.gpio_claim_input(handle, self.bcm_pin, 32)
        return handle

    def get_state(self) -> Literal[0, 1]:
        self.state = gp.gpio_read(self.handle, self.bcm_pin)
        return self.state

    def is_pressed(self) -> bool:
        self.p_state = self.state
        state = self.get_state()
        if state == 1 and self.p_state == 0:
            return True
        return False

    def __del__(self):
        if hasattr(self, "handle"):
            gp.gpiochip_close(self.handle)
