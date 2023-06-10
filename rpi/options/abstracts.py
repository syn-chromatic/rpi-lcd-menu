from extensions.std.abc import ABC, abstractmethod
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
    def get_hold_state(self) -> bool:
        pass

    @abstractmethod
    def get_char_array(self) -> list[CharABC]:
        pass

    @abstractmethod
    def get_item(self) -> MenuItem:
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def update_shift(self):
        pass
