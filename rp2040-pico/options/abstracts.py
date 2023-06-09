from std.abc import ABC, abstractmethod
from options.item import MenuItem

from character.abstracts import CharABC


class OptionABC(ABC):
    def __init__(self, item: MenuItem):
        pass

    @abstractmethod
    def back(self):
        pass

    @abstractmethod
    def prev(self):
        pass

    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def apply(self):
        pass

    @abstractmethod
    def get_hold_state(self) -> bool: # type: ignore
        pass

    @abstractmethod
    def get_char_array(self) -> list[CharABC]: # type: ignore
        pass

    @abstractmethod
    def get_item(self) -> MenuItem: # type: ignore
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def update_shift(self):
        pass

