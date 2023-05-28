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
    def get_string(self) -> str:
        pass


class OptionToggle(Option):
    def __init__(self, callback: Callable, state_callback: Callable):
        self.callback: Callable = callback
        self.state_callback: Callable = state_callback

    @abstractmethod
    def get_state(self):
        pass

    @abstractmethod
    def execute_callback(self):
        pass
