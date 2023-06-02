from actuators.button import Button
from typing import Callable


class ControllerBase:
    def __init__(self, back_pin: int, prev_pin: int, next_pin: int, apply_pin: int):
        self._back_pin = back_pin
        self._prev_pin = prev_pin
        self._next_pin = next_pin
        self._apply_pin = apply_pin
        self._back_button = self._register_back_button()
        self._prev_button = self._register_prev_button()
        self._next_button = self._register_next_button()
        self._apply_button = self._register_apply_button()
        self._back_callback = None
        self._prev_callback = None
        self._next_callback = None
        self._apply_callback = None

    def _register_back_button(self) -> Button:
        button = Button(self._back_pin)
        return button

    def _register_prev_button(self) -> Button:
        button = Button(self._prev_pin)
        return button

    def _register_next_button(self) -> Button:
        button = Button(self._next_pin)
        return button

    def _register_apply_button(self) -> Button:
        button = Button(self._apply_pin)
        return button

    def _execute_back_callback(self):
        if self._back_callback:
            self._back_callback()

    def _execute_prev_callback(self):
        if self._prev_callback:
            self._prev_callback()

    def _execute_next_callback(self):
        if self._next_callback:
            self._next_callback()

    def _execute_apply_callback(self):
        if self._apply_callback:
            self._apply_callback()


class Controller(ControllerBase):
    def __init__(self, back_pin: int, prev_pin: int, next_pin: int, apply_pin: int):
        super().__init__(back_pin, prev_pin, next_pin, apply_pin)

    def register_back_callback(self, callback: Callable):
        self._back_callback = callback

    def register_prev_callback(self, callback: Callable):
        self._prev_callback = callback

    def register_next_callback(self, callback: Callable):
        self._next_callback = callback

    def register_apply_callback(self, callback: Callable):
        self._apply_callback = callback

    def check(self):
        if self._back_button.is_pressed():
            self._execute_back_callback()

        if self._prev_button.is_pressed():
            self._execute_prev_callback()

        if self._next_button.is_pressed():
            self._execute_next_callback()

        if self._apply_button.is_pressed():
            self._execute_apply_callback()
