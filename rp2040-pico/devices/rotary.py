from extensions.wgpio import InputGPIO
from extensions.std.typing import Optional, Literal


class RotaryEncoderBase:
    def __init__(self, a_pin: int, b_pin: int, sw_pin: int):
        self._a_gpio = self._register_pin(a_pin)
        self._b_gpio = self._register_pin(b_pin)
        self._sw_gpio = self._register_pin(sw_pin)
        self._a_state = 0
        self._b_state = 0
        self._sw_state = 1
        self._ap_state = 1
        self._bp_state = 1
        self._swp_state = 1

    def _register_pin(self, pin: int) -> InputGPIO:
        gpio = InputGPIO(pin)
        return gpio


class RotaryEncoder(RotaryEncoderBase):
    def __init__(self, a_pin: int, b_pin: int, sw_pin: int):
        super().__init__(a_pin, b_pin, sw_pin)

    def get_a_state(self):
        self.a_state = self._a_gpio.read()
        return self.a_state

    def get_b_state(self):
        self.b_state = self._b_gpio.read()
        return self.b_state

    def get_sw_state(self):
        self.sw_state = self._sw_gpio.read()
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
