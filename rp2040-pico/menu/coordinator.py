from options.abstracts import OptionABC
from character.abstracts import CharABC
from character.chars import SpaceChar


class MenuCoordinatorBase:
    def __init__(self, rows: int, columns: int, options: dict[OptionABC, dict]):
        self._rows: int = rows
        self._columns: int = columns
        self._selected: int = 0
        self._options: dict[OptionABC, dict] = options
        self._entries: list[tuple[int, OptionABC]] = []
        self._initiate_options(self._options)

    def _initiate_options(self, options: dict[OptionABC, dict]):
        for option in options.keys():
            option_item = option.get_item()
            option_item.set_selected(True)
            return

    def _get_options(self) -> dict[OptionABC, dict]:
        options = self._options
        for _, entry_option in self._entries:
            if entry_option in options:
                options = options[entry_option]
                continue
            self._entries.pop()
            self._selected = 0
            option = list(options)[0]
            option.get_item().set_selected(True)
        return options

    def _get_options_list(self) -> list[OptionABC]:
        options = self._get_options()
        options_list = list(options)
        return options_list

    def _get_option_range(self) -> tuple[int, int]:
        if self._selected < self._rows:
            st_range = 0
            en_range = self._rows
            return st_range, en_range

        st_range = self._selected - (self._rows - 1)
        en_range = st_range + self._rows
        return st_range, en_range

    def _set_option_selected(self, option: OptionABC):
        option_item = option.get_item()
        option_item.set_selected(True)

    def _set_option_deselected(self, option: OptionABC):
        option_item = option.get_item()
        option_item.set_selected(False)
        option_item.reset()

    def _add_entry(self, option: OptionABC):
        options = self._get_options()
        option.apply()
        if option in options:
            new_options = options[option]
            if new_options:
                entry_idx = self._selected
                self._entries.append((entry_idx, option))
                self._selected = 0
                option.get_item().reset()
                self._initiate_options(new_options)
                return

    def _back_entry(self, option: OptionABC):
        if self._entries:
            entry_idx, _ = self._entries.pop(-1)
            self._selected = entry_idx

            option.get_item().set_selected(False)
            option.get_item().reset()

    def _get_option(self, options_list: list[OptionABC], idx: int):
        if len(options_list) > idx:
            return options_list[idx]


class MenuCoordinator(MenuCoordinatorBase):
    def __init__(self, rows: int, columns: int, options: dict[OptionABC, dict]):
        super().__init__(rows, columns, options)

    def get_increment_select(self, select: int, options_list: list[OptionABC]) -> int:
        if select < len(options_list) - 1:
            select += 1
            return select
        select = 0
        return select

    def get_decrement_select(self, select: int, options_list: list[OptionABC]) -> int:
        if select > 0:
            select -= 1
            return select
        select = len(options_list) - 1
        return select

    def increment_selection(self):
        options_list = self._get_options_list()
        cur_select = self._selected
        cur_option = options_list[cur_select]

        if cur_option.get_hold_state():
            cur_option.next()
            return

        new_select = self.get_increment_select(cur_select, options_list)
        new_option = options_list[new_select]

        self._set_option_deselected(cur_option)
        self._set_option_selected(new_option)
        self._selected = new_select

    def decrement_selection(self):
        options_list = self._get_options_list()
        cur_select = self._selected
        cur_option = options_list[cur_select]

        if cur_option.get_hold_state():
            cur_option.prev()
            return

        new_select = self.get_decrement_select(cur_select, options_list)
        new_option = options_list[new_select]

        self._set_option_deselected(cur_option)
        self._set_option_selected(new_option)
        self._selected = new_select

    def get_chars(self) -> list[list[CharABC]]:
        st_range, en_range = self._get_option_range()
        options_list = self._get_options_list()

        chars: list[list[CharABC]] = []
        added_rows = 0
        for idx in range(st_range, en_range):
            option = self._get_option(options_list, idx)
            if option:
                option_name = option.get_char_array()
                option.update()
                option.update_shift()
                chars.append(option_name)
                added_rows += 1

        for _ in range(self._rows - added_rows):
            row_spaces: list[CharABC] = [SpaceChar()] * self._columns
            chars.append(row_spaces)

        return chars

    def apply_selection(self):
        options_list = self._get_options_list()
        option = options_list[self._selected]
        self._add_entry(option)
        return

    def back_selection(self):
        options_list = self._get_options_list()
        option = options_list[self._selected]

        if option.get_hold_state():
            option.back()
            return

        self._back_entry(option)
