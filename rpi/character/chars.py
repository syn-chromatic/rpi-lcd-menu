from character.abstracts import CharABC, ASCIICharABC, ByteCharABC


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
