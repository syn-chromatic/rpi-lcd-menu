class MenuItemBase:
    def __init__(self, columns: int, shift_hold: int, string: str = ""):
        self._columns = columns
        self._string = string
        self._st_range = 0
        self._shift_hold = shift_hold
        self._shift_hold_st = 0
        self._shift_hold_en = 0
        self._is_selected = False

    def _get_diff_length(self) -> int:
        len_string = len(self._string)
        return len_string - self._st_range

    def _get_max_trim_columns(self) -> int:
        return self._columns - 4

    def _get_max_columns(self) -> int:
        return self._columns - 2

    def _get_shift_condition(self) -> bool:
        diff_length = self._get_diff_length()
        max_trim_cols = self._get_max_trim_columns()
        max_cols = self._get_max_columns()
        if len(self._string) > max_cols:
            if diff_length > max_trim_cols and self._is_selected:
                return True
        return False

    def _increment_shift(self):
        shift_condition = self._get_shift_condition()
        if shift_condition:
            if not self._hold_shift_start():
                self._st_range += 1
            return
        if not self._hold_shift_end():
            self._reset()

    def _hold_shift_start(self):
        if self._shift_hold_st < self._shift_hold:
            self._shift_hold_st += 1
            return True
        return False

    def _hold_shift_end(self):
        if self._shift_hold_en < self._shift_hold:
            self._shift_hold_en += 1
            return True
        return False

    def _get_raw_string(self) -> str:
        diff_length = self._get_diff_length()
        max_trim_cols = self._get_max_trim_columns()
        max_cols = self._get_max_columns()
        if len(self._string) > max_cols:
            if diff_length >= max_trim_cols:
                en_range = self._st_range + (self._columns - 4)
                new_string = self._string[self._st_range : en_range]
                new_string += ".."
                return new_string
        return self._string[self._st_range :]

    def _reset(self):
        self._st_range = 0
        self._shift_hold_st = 0
        self._shift_hold_en = 0


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
        self._increment_shift()

    def reset(self):
        self._reset()
