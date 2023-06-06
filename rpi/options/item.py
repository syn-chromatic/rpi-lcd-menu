from character.abstracts import CharABC
from character.chars import (
    CharArray,
    LeftArrowChar,
    RightArrowChar,
    RightAngleChar,
    SpaceChar,
)


class MenuItemBase:
    def __init__(self, columns: int, shift_hold: int):
        self._columns = columns
        self._char_array: list[CharABC] = []
        self._shift_hold = shift_hold
        self._st_idx = 0
        self._shift_hold_st = 0
        self._shift_hold_en = 0
        self._is_selected = False

    def _get_shifted_length(self) -> int:
        len_string = len(self._char_array)
        return len_string - self._st_idx

    def _get_trimmed_columns(self) -> int:
        available_columns = self._get_available_columns()
        st_range = self._st_idx

        if st_range > 0:
            available_columns -= 1

        if available_columns != len(self._char_array):
            available_columns -= 1

        return available_columns

    def _get_available_columns(self) -> int:
        return self._columns - 2

    def _get_shift_condition(self) -> bool:
        shifted_length = self._get_shifted_length()
        trimmed_columns = self._get_trimmed_columns()
        available_columns = self._get_available_columns()
        if len(self._char_array) > available_columns:
            if shifted_length > trimmed_columns and self._is_selected:
                return True
        return False

    def _get_reset_condition(self):
        if not self._is_selected and self._st_idx != 0:
            return True
        return False

    def _increment_shift(self):
        shift_condition = self._get_shift_condition()

        if shift_condition:
            if not self._hold_shift_start():
                self._st_idx += 1
            return

        if not shift_condition and self._is_selected:
            if not self._hold_shift_end():
                self._reset()
            return

        if self._get_reset_condition():
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

    def _fill_preceding_char(self, char_array: list[CharABC], st_range: int):
        if st_range > 0:
            char_array.append(LeftArrowChar())

    def _fill_proceeding_char(self, char_array: list[CharABC], en_range: int):
        if en_range != len(self._char_array):
            char_array.append(RightArrowChar())

    def _fill_char_array(self, char_array: list[CharABC]):
        shifted_length = self._get_shifted_length()
        trimmed_columns = self._get_trimmed_columns()
        available_columns = self._get_available_columns()

        if len(self._char_array) > available_columns:
            if shifted_length >= trimmed_columns:
                st_range = self._st_idx
                en_range = self._st_idx + trimmed_columns
                self._fill_preceding_char(char_array, self._st_idx)
                for idx in range(st_range, en_range):
                    char_array.append(self._char_array[idx])
                self._fill_proceeding_char(char_array, en_range)
                return

        for idx in range(self._st_idx, len(self._char_array)):
            char_array.append(self._char_array[idx])

    def _get_prefix_char_array(self) -> list[CharABC]:
        if self._is_selected:
            return [RightAngleChar(), SpaceChar()]
        return [SpaceChar(), SpaceChar()]

    def _reset(self):
        self._st_idx = 0
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
        char_array = CharArray().get_ascii_char_array(string)
        self._char_array = char_array

    def set_char_array(self, char_array: list[CharABC]):
        self._char_array = char_array

    def get_char_array(self) -> list[CharABC]:
        char_array = self._get_prefix_char_array()
        self._fill_char_array(char_array)
        return char_array

    def shift(self):
        self._increment_shift()

    def reset(self):
        self._reset()
