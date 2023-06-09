from std.abc import ABC, abstractmethod
from character.abstracts import CharABC


class WriterABC(ABC):
    def __init__(self, rows: int, columns: int):
        self.rows = rows
        self.columns = columns

    @abstractmethod
    def write_with_cursor(self, chars: list[list[CharABC]], hold_time: float):
        pass

    @abstractmethod
    def write(self, chars: list[list[CharABC]], hold_time: float):
        pass

    @abstractmethod
    def set_backlight(self, backlight_bool: bool):
        pass

    @abstractmethod
    def get_backlight_state(self) -> bool: # type: ignore
        pass
