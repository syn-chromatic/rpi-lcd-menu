from extensions.std.abc import ABC, abstractmethod


class CharABC(ABC):
    def __init__(self, value: int | list[int]):
        self.value: int | list[int] = value

    @abstractmethod
    def get_value(self) -> int | list[int]:
        pass

    @abstractmethod
    def set_value(self, value: int | list[int]):
        pass

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CharABC):
            return self.value == other.value
        return self == other

    def __ne__(self, other: object) -> bool:
        if isinstance(other, CharABC):
            return self.value != other.value
        return self != other


class ASCIICharABC(CharABC):
    def __init__(self, value: int):
        self.value: int = value

    @abstractmethod
    def get_value(self) -> int:
        pass

    @abstractmethod
    def set_value(self, value: int):
        pass


class ByteCharABC(CharABC):
    def __init__(self, char: int):
        self.value: int = char

    @abstractmethod
    def get_value(self) -> int:
        pass

    @abstractmethod
    def set_value(self, value: int):
        pass

    @abstractmethod
    def get_unicode_value(self) -> int:
        pass


class CustomCharABC(CharABC):
    def __init__(self, cgram: int, value: list[int]):
        self.cgram: int = cgram
        self.value: list[int] = value

    @abstractmethod
    def get_value(self) -> list[int]:
        pass

    @abstractmethod
    def set_value(self, value: list[int]):
        pass

    @abstractmethod
    def get_unicode_value(self) -> int:
        pass
