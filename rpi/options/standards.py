from options.abstracts import OptionABC

from options.states import StateInt, LinkedStateBool, LinkedStateInt
from options.item import MenuItem

from character.abstracts import CharABC


class StaticStd(OptionABC):
    def __init__(self, name: str, item: MenuItem):
        self.name = name
        self.item = item
        self.item.set_string(self.name)

    def back(self):
        pass

    def prev(self):
        pass

    def next(self):
        pass

    def apply(self):
        pass

    def get_hold_state(self) -> bool:
        return False

    def get_char_array(self) -> list[CharABC]:
        return self.item.get_char_array()

    def get_item(self) -> MenuItem:
        return self.item

    def update(self):
        pass

    def update_shift(self):
        self.item.shift()


class ToggleBase(OptionABC):
    def __init__(self, name: str, item: MenuItem, state: LinkedStateBool):
        self._name = name
        self._item = item
        self._state = state
        self._update_menu_item()

    def _update_menu_item(self):
        string = "{}: {}"
        state_str = self._get_state_str()
        string = string.format(self._name, state_str)
        self._item.set_string(string)

    def _get_state_str(self) -> str:
        if self._get_state():
            return "ON"
        return "OFF"

    def _get_state(self) -> bool:
        return self._state.get_state()

    def _switch_state(self):
        state = not self._state.get_state()
        self._state.set_state(state)


class ToggleStd(ToggleBase):
    def __init__(self, name: str, item: MenuItem, state: LinkedStateBool):
        super().__init__(name, item, state)

    def back(self):
        pass

    def prev(self):
        pass

    def next(self):
        pass

    def apply(self):
        self._switch_state()
        self.update()

    def get_hold_state(self) -> bool:
        return False

    def get_char_array(self) -> list[CharABC]:
        return self._item.get_char_array()

    def get_item(self) -> MenuItem:
        return self._item

    def update(self):
        self._update_menu_item()

    def update_shift(self):
        self._item.shift()


class ListBase(OptionABC):
    def __init__(self, name: str, item: MenuItem, item_list: list[str]):
        self._name = name
        self._item = item
        self._item_list = item_list
        self._max_idx = len(item_list) - 1
        self._state = StateInt(0)
        self._change_state = False
        self._update_menu_item()

    def _update_menu_item(self):
        string = "{}: {}"
        state_str = self._get_state_str()
        string = string.format(self._name, state_str)
        self._item.set_string(string)

    def _get_state_str(self) -> str:
        if self._change_state:
            string = "<{}>"
            string = string.format(self._get_value())
            return string
        string = "{}"
        string = string.format(self._get_value())
        return string

    def _advance_state(self):
        if not self._change_state:
            self._change_state = True

    def _back_state(self):
        if self._change_state:
            self._change_state = False

    def _increment(self):
        idx = self._state.get_state() + 1
        if idx <= self._max_idx:
            self._state.set_state(idx)

    def _decrement(self):
        idx = self._state.get_state() - 1
        if idx >= 0:
            self._state.set_state(idx)

    def _get_value(self) -> str:
        idx = self._state.get_state()
        return self._item_list[idx]


class ListStd(ListBase):
    def __init__(self, name: str, item: MenuItem, item_list: list[str]):
        super().__init__(name, item, item_list)

    def back(self):
        self._back_state()
        self.update()

    def prev(self):
        self._decrement()
        self.update()

    def next(self):
        self._increment()
        self.update()

    def apply(self):
        self._advance_state()
        self.update()

    def get_hold_state(self) -> bool:
        if self._change_state:
            return True
        return False

    def get_char_array(self) -> list[CharABC]:
        return self._item.get_char_array()

    def get_item(self) -> MenuItem:
        return self._item

    def update(self):
        self._update_menu_item()

    def update_shift(self):
        self._item.shift()


class RangeBase(OptionABC):
    def __init__(
        self,
        name: str,
        item: MenuItem,
        state: LinkedStateInt,
        step: int,
        min_range: int,
        max_range: int,
    ):
        self._name = name
        self._item = item
        self._state = state
        self._step = step
        self._min_range = min_range
        self._max_range = max_range
        self._change_state = False
        self._update_menu_item()

    def _update_menu_item(self):
        string = "{}: {}"
        state_str = self.get_state_str()
        string = string.format(self._name, state_str)
        self._item.set_string(string)

    def get_state_str(self) -> str:
        if self._change_state:
            string = "<{}>"
            string = string.format(self._get_state())
            return string
        string = "{}"
        string = string.format(self._get_state())
        return string

    def _get_state(self):
        return self._state.get_state()

    def _advance_state(self):
        if not self._change_state:
            self._change_state = True

    def _back_state(self):
        if self._change_state:
            self._change_state = False

    def _increment(self):
        state = self._get_state() + self._step
        if state <= self._max_range:
            self._state.set_state(state)

    def _decrement(self):
        state = self._get_state() - self._step
        if state >= self._min_range:
            self._state.set_state(state)


class RangeStd(RangeBase):
    def __init__(
        self,
        name: str,
        item: MenuItem,
        state: LinkedStateInt,
        step: int,
        min_range: int,
        max_range: int,
    ):
        super().__init__(name, item, state, step, min_range, max_range)

    def back(self):
        self._back_state()
        self.update()

    def prev(self):
        self._decrement()
        self.update()

    def next(self):
        self._increment()
        self.update()

    def apply(self):
        self._advance_state()
        self.update()

    def get_hold_state(self) -> bool:
        if self._change_state:
            return True
        return False

    def get_char_array(self) -> list[CharABC]:
        return self._item.get_char_array()

    def get_item(self) -> MenuItem:
        return self._item

    def update(self):
        self._update_menu_item()

    def update_shift(self):
        self._item.shift()


class TimeBase(OptionABC):
    def __init__(self, name: str, item: MenuItem):
        self._name = name
        self._item = item
        self._hours = 0
        self._minutes = 0
        self._selected = 0
        self._select_state = False
        self._change_state = False
        self._update_menu_item()

    def _update_menu_item(self):
        string = "{}: {}"
        state_str = self._get_state_str()
        string = string.format(self._name, state_str)
        self._item.set_string(string)

    def _get_hours_str(self) -> str:
        if len(str(self._hours)) == 1:
            return "0" + str(self._hours)
        return str(self._hours)

    def _get_minutes_str(self) -> str:
        if len(str(self._minutes)) == 1:
            return "0" + str(self._minutes)
        return str(self._minutes)

    def _get_time_str(self, segments: list[str]) -> str:
        len_segments = len(segments) - 1
        string = ""
        for idx, seg in enumerate(segments):
            string += seg

            if idx != len_segments:
                string += ":"
        return string

    def _get_segments(self):
        hours = self._get_hours_str()
        minutes = self._get_minutes_str()
        segments = [hours, minutes]
        return segments

    def _get_time_select(self) -> str:
        segments = self._get_segments()
        for idx, seg in enumerate(segments):
            if self._selected == idx:
                segments[idx] = f"[{seg}]"
        string = self._get_time_str(segments)
        return string

    def _get_time_change(self) -> str:
        segments = self._get_segments()
        for idx, seg in enumerate(segments):
            if self._selected == idx:
                segments[idx] = f"<{seg}>"
        string = self._get_time_str(segments)
        return string

    def _get_state_str(self) -> str:
        if self._select_state and not self._change_state:
            string = self._get_time_select()
            return string

        elif self._select_state and self._change_state:
            string = self._get_time_change()
            return string

        segments = self._get_segments()
        string = self._get_time_str(segments)
        return string

    def _advance_state(self):
        if not self._select_state:
            self._select_state = True
            return
        self._change_state = True

    def _back_state(self):
        if self._change_state:
            self._change_state = False
            return
        self._select_state = False
        self._selected = 0

    def _increment_selected(self):
        if self._selected < 1:
            self._selected += 1
            return
        self._selected = 0

    def _increment_time(self):
        if self._selected == 0:
            if self._hours + 1 < 24:
                self._hours += 1

        elif self._selected == 1:
            if self._minutes + 1 < 60:
                self._minutes += 1

    def _decrement_time(self):
        if self._selected == 0:
            if self._hours - 1 >= 0:
                self._hours -= 1

        elif self._selected == 1:
            if self._minutes - 1 >= 0:
                self._minutes -= 1

    def _increment(self):
        if self._select_state and not self._change_state:
            self._increment_selected()
            return
        if self._select_state and self._change_state:
            self._increment_time()

    def decrement(self):
        if self._select_state and not self._change_state:
            self._increment_selected()
            return
        if self._select_state and self._change_state:
            self._decrement_time()


class TimeStd(TimeBase):
    def __init__(self, name: str, item: MenuItem):
        super().__init__(name, item)

    def back(self):
        self._back_state()
        self.update()

    def prev(self):
        self.decrement()
        self.update()

    def next(self):
        self._increment()
        self.update()

    def apply(self):
        self._advance_state()
        self.update()

    def get_hold_state(self) -> bool:
        if self._select_state or self._change_state:
            return True
        return False

    def get_char_array(self) -> list[CharABC]:
        return self._item.get_char_array()

    def get_item(self) -> MenuItem:
        return self._item

    def update(self):
        self._update_menu_item()

    def update_shift(self):
        self._item.shift()
