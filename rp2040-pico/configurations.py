from std.abc import ABC, abstractmethod


class CtrlConfigABC(ABC):
    @property
    @abstractmethod
    def back_pin(self) -> int:
        pass

    @property
    @abstractmethod
    def prev_pin(self) -> int:
        pass

    @property
    @abstractmethod
    def next_pin(self) -> int:
        pass

    @property
    @abstractmethod
    def apply_pin(self) -> int:
        pass


class KBCtrlConfigABC(ABC):
    @property
    @abstractmethod
    def back_key(self) -> int:
        pass

    @property
    @abstractmethod
    def prev_key(self) -> int:
        pass

    @property
    @abstractmethod
    def next_key(self) -> int:
        pass

    @property
    @abstractmethod
    def apply_key(self) -> int:
        pass


class LCDConfigABC(ABC):
    @property
    @abstractmethod
    def lcd_rows(self) -> int:
        pass

    @property
    @abstractmethod
    def lcd_columns(self) -> int:
        pass


class CtrlConfig(CtrlConfigABC):
    prev_pin: int = 6
    next_pin: int = 5
    apply_pin: int = 4
    back_pin: int = 27


class KBCtrlConfig(KBCtrlConfigABC):
    prev_key: int = ord("2")
    next_key: int = ord("3")
    apply_key: int = ord("4")
    back_key: int = ord("1")


class LCD1602Config(LCDConfigABC):
    lcd_rows: int = 2
    lcd_columns: int = 16


class LCD2004Config(LCDConfigABC):
    lcd_rows: int = 4
    lcd_columns: int = 20
