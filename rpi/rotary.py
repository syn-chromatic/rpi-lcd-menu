import lgpio as gp
from typing import Optional, Literal


class RotaryEncoder:
    def __init__(self, a_pin: int, b_pin: int, sw_pin: int):
        self.a_pin = a_pin
        self.b_pin = b_pin
        self.sw_pin = sw_pin
        self.handle = gp.gpiochip_open(0)
        self.a_state = 0
        self.b_state = 0
        self.sw_state = 1
        self.ap_state = 1
        self.bp_state = 1
        self.swp_state = 1

    def set_inputs(self):
        gp.gpio_claim_input(self.handle, self.a_pin, 32)
        gp.gpio_claim_input(self.handle, self.b_pin, 32)
        gp.gpio_claim_input(self.handle, self.sw_pin, 32)

    def get_a_state(self):
        self.a_state = gp.gpio_read(self.handle, self.a_pin)
        return self.a_state

    def get_b_state(self):
        self.b_state = gp.gpio_read(self.handle, self.b_pin)
        return self.b_state

    def get_sw_state(self):
        self.sw_state = gp.gpio_read(self.handle, self.sw_pin)
        return self.sw_state

    def get_direction(self) -> Optional[Literal[1, -1]]:
        self.ap_state = self.a_state
        self.bp_state = self.b_state

        a_state = self.get_a_state()
        b_state = self.get_b_state()

        p_state = self.ap_state == 1 and self.bp_state == 1

        if a_state == 1 and b_state == 0 and p_state:
            return 1
        elif a_state == 0 and b_state == 1 and p_state:
            return -1

    def is_pressed(self) -> bool:
        self.swp_state = self.sw_state
        state = self.get_sw_state()
        if state == 1 and self.swp_state == 0:
            return True
        return False

    def __del__(self):
        gp.gpiochip_close(self.handle)
