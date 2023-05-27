import lgpio as gp
from typing import Literal


class Button:
    def __init__(self, bcm_pin: int):
        self.bcm_pin = bcm_pin
        self.handle = self.register_pin()
        self.state = 0
        self.p_state = 1

    def register_pin(self):
        handle = gp.gpiochip_open(0)
        gp.gpio_claim_input(handle, self.bcm_pin, 32)
        return handle

    def get_state(self) -> Literal[0, 1]:
        self.state = gp.gpio_read(self.handle, self.bcm_pin)
        return self.state

    def is_pressed(self) -> bool:
        state = self.get_state()
        bool_state = False
        if self.p_state == 0 and state == 1:
            bool_state = True
        self.p_state = state
        return bool_state

    def __del__(self):
        if hasattr(self, "hanlde"):
            gp.gpiochip_close(self.handle)
