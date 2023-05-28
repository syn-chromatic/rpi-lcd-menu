class MenuItem:
    def __init__(self, chars: int, string: str = ""):
        self.chars = chars
        self.string = string
        self.st_range = 0
        self.is_selected = False

    def set_string(self, string: str):
        self.string = string

    def get_string(self) -> str:
        diff_length = self.get_diff_length()
        max_trim_chars = self.get_max_trim_chars()
        max_chars = self.get_max_chars()
        if len(self.string) > max_chars:
            if diff_length >= max_trim_chars:
                en_range = self.st_range + (self.chars - 4)
                new_string = self.string[self.st_range : en_range]
                new_string += ".."
                return new_string
        return self.string[self.st_range :]

    def get_diff_length(self) -> int:
        len_string = len(self.string)
        return len_string - self.st_range

    def get_max_trim_chars(self) -> int:
        return self.chars - 4

    def get_max_chars(self) -> int:
        return self.chars - 2

    def get_formatted(self) -> str:
        if self.is_selected:
            return "> " + self.get_string() + "\n"
        return "x " + self.get_string() + "\n"

    def increment_shift_item(self):
        diff_length = self.get_diff_length()
        max_trim_chars = self.get_max_trim_chars()
        max_chars = self.get_max_chars()
        if len(self.string) > max_chars:
            if diff_length > max_trim_chars and self.is_selected:
                self.st_range += 1
                return
        self.st_range = 0
