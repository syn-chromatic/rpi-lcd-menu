from extensions import ABC, abstractmethod


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


class ASCIIChar(ASCIICharABC):
    def __init__(self, value: int):
        self.value = value

    def get_value(self) -> int:
        return self.value

    def set_value(self, value: int):
        self.value = value


class SpaceChar(ASCIICharABC):
    def __init__(self):
        self.value = ord(" ")

    def get_value(self) -> int:
        return self.value

    def set_value(self, value: int):
        self.value = value


class RightAngleChar(ASCIICharABC):
    def __init__(self):
        self.value = ord(">")

    def get_value(self) -> int:
        return self.value

    def set_value(self, value: int):
        self.value = value


class LeftArrowChar(ByteCharABC):
    def __init__(self):
        self.value = ord("\u007f")

    def get_value(self) -> int:
        return self.value

    def get_unicode_value(self) -> int:
        return ord("←")

    def set_value(self, value: int):
        self.value = value


class RightArrowChar(ByteCharABC):
    def __init__(self):
        self.value = ord("\u007e")

    def get_value(self) -> int:
        return self.value

    def get_unicode_value(self) -> int:
        return ord("→")

    def set_value(self, value: int):
        self.value = value


class CharArray:
    def __init__(self):
        pass

    def get_ascii_char_array(self, string: str) -> list[CharABC]:
        char_array = []
        for ch_str in string:
            ascii_char = ASCIIChar(ord(ch_str))
            char_array.append(ascii_char)
        return char_array
