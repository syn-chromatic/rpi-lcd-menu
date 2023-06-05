from typing import Callable
from abc import ABC, abstractmethod

from options.item import MenuItem


class Option(ABC):
    def __init__(self, item: MenuItem):
        self.item: MenuItem = item

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def update_shift(self):
        pass

    @abstractmethod
    def get_string(self) -> str:
        pass

    def __repr__(self) -> str:
        return self.item._string


class OptionToggle(Option):
    def __init__(self, callback: Callable, state_callback: Callable):
        self.callback: Callable = callback
        self.state_callback: Callable = state_callback

    @abstractmethod
    def get_state(self) -> bool:
        pass

    @abstractmethod
    def execute_callback(self):
        pass


class OptionRange(Option):
    def __init__(
        self,
        min_range: int,
        max_range: int,
        step: int,
        assign_callback: Callable,
        state_callback: Callable,
    ):
        self.min_range: int = min_range
        self.max_range: int = max_range
        self.step: int = step
        self.assign_callback: Callable = assign_callback
        self.state_callback: Callable = state_callback
        self.change_state: bool = False

    @abstractmethod
    def get_value(self) -> int:
        pass

    @abstractmethod
    def get_hold_state(self) -> bool:
        pass

    @abstractmethod
    def advance_state(self):
        pass

    @abstractmethod
    def back_state(self):
        pass

    @abstractmethod
    def increment(self):
        pass

    def decrement(self):
        pass


class OptionTimeHM(Option):
    def __init__(self):
        self.hours: int = 0
        self.minutes: int = 0
        self.selected: int = 0
        self.select_state: bool = False
        self.change_state: bool = False

    @abstractmethod
    def get_hold_state(self) -> bool:
        pass

    @abstractmethod
    def advance_state(self):
        pass

    @abstractmethod
    def back_state(self):
        pass

    @abstractmethod
    def increment(self):
        pass

    def decrement(self):
        pass
