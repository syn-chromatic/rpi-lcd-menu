from character.abstracts import CharABC, ASCIICharABC, ByteCharABC


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
