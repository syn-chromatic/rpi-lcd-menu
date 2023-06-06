from abc import ABC, abstractmethod


class CharABC(ABC):
    def __init__(self, value: tuple[str] | list[int]):
        self.value: tuple[str] | list[int] = value

    @abstractmethod
    def get_value(self) -> str | list[int]:
        pass

    @abstractmethod
    def set_value(self, value: tuple[str] | list[int]):
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
    def __init__(self, value: tuple[str]):
        self.value: tuple[str] = value

    @abstractmethod
    def get_value(self) -> str:
        pass

    @abstractmethod
    def set_value(self, value: tuple[str]):
        pass


class ByteCharABC(CharABC):
    def __init__(self, char: tuple[str]):
        self.value: tuple[str] = char

    @abstractmethod
    def get_value(self) -> str:
        pass

    @abstractmethod
    def set_value(self, value: tuple[str]):
        pass

    @abstractmethod
    def get_unicode_value(self) -> str:
        pass


class CustomCharABC(CharABC):
    def __init__(self, value: list[int]):
        self.value: list[int] = value

    @abstractmethod
    def get_value(self) -> list[int]:
        pass

    @abstractmethod
    def set_value(self, value: list[int]):
        pass

    @abstractmethod
    def get_unicode_value(self) -> str:
        pass


class ASCIIChar(ASCIICharABC):
    def __init__(self, value: tuple[str] = tuple([""])):
        self.value: tuple[str] = value

    def get_value(self) -> str:
        return self.value[0]

    def set_value(self, value: tuple[str]):
        self.value = value


class SpaceChar(ASCIICharABC):
    def __init__(self):
        self.value = tuple([" "])

    def get_value(self) -> str:
        return self.value[0]

    def set_value(self, value: tuple[str]):
        self.value = value


class RightAngleChar(ASCIICharABC):
    def __init__(self):
        self.value = tuple([">"])

    def get_value(self) -> str:
        return self.value[0]

    def set_value(self, value: tuple[str]):
        self.value = value


class LeftArrowChar(ByteCharABC):
    def __init__(self):
        self.value = tuple(["\u007f"])

    def get_value(self) -> str:
        return self.value[0]

    def get_unicode_value(self) -> str:
        return "←"

    def set_value(self, value: tuple[str]):
        self.value = value


class RightArrowChar(ByteCharABC):
    def __init__(self):
        self.value = tuple(["\u007e"])

    def get_value(self) -> str:
        return self.value[0]

    def get_unicode_value(self) -> str:
        return "→"

    def set_value(self, value: tuple[str]):
        self.value = value


class CharArray:
    def __init__(self):
        pass

    def get_ascii_char_array(self, string: str) -> list[CharABC]:
        char_array = []
        for ch_str in string:
            ascii_char = ASCIIChar(tuple([ch_str]))
            char_array.append(ascii_char)
        return char_array
