class MenuItemBase:
    def __init__(self, chars: int, shift_hold: int, string: str = ""):
        self._chars = chars
        self._string = string
        self._st_range = 0
        self._shift_hold = shift_hold
        self._shift_hold_counter = 0
        self._is_selected = False

    def _get_diff_length(self) -> int:
        len_string = len(self._string)
        return len_string - self._st_range

    def _get_max_trim_chars(self) -> int:
        return self._chars - 4

    def _get_max_chars(self) -> int:
        return self._chars - 2

    def _get_shift_condition(self) -> bool:
        diff_length = self._get_diff_length()
        max_trim_chars = self._get_max_trim_chars()
        max_chars = self._get_max_chars()
        if len(self._string) > max_chars:
            if diff_length > max_trim_chars and self._is_selected:
                return True
        return False

    def _increment_shift(self):
        if self._shift_hold_counter == self._shift_hold:
            self._st_range += 1
            return
        self._shift_hold_counter += 1

    def _get_raw_string(self) -> str:
        diff_length = self._get_diff_length()
        max_trim_chars = self._get_max_trim_chars()
        max_chars = self._get_max_chars()
        if len(self._string) > max_chars:
            if diff_length >= max_trim_chars:
                en_range = self._st_range + (self._chars - 4)
                new_string = self._string[self._st_range : en_range]
                new_string += ".."
                return new_string
        return self._string[self._st_range :]


class MenuItem(MenuItemBase):
    def __init__(self, chars: int, shift_hold: int = 3):
        super().__init__(chars, shift_hold)

    def is_selected(self) -> bool:
        return self._is_selected

    def set_selected(self, state: bool):
        self._is_selected = state

    def set_string(self, string: str):
        self._string = string

    def get_string(self) -> str:
        if self._is_selected:
            return "> " + self._get_raw_string() + "\n"
        return "  " + self._get_raw_string() + "\n"

    def shift(self):
        shift_condition = self._get_shift_condition()
        if shift_condition:
            self._increment_shift()
            return
        self.reset()

    def reset(self):
        self._st_range = 0
        self._shift_hold_counter = 0
