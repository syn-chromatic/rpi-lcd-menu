from extensions import ABC, abstractmethod
from extensions import Callable
from extensions import Processor, System

from collections import OrderedDict as OrdDict

from characters import CharABC
from characters import (
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


class OptionABC(ABC):
    def __init__(self, item: MenuItem):
        pass

    @abstractmethod
    def back(self):
        pass

    @abstractmethod
    def prev(self):
        pass

    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def apply(self):
        pass

    @abstractmethod
    def get_hold_state(self) -> bool:
        pass

    @abstractmethod
    def get_char_array(self) -> list[CharABC]:
        pass

    @abstractmethod
    def get_item(self) -> MenuItem:
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def update_shift(self):
        pass


class ActionEvent:
    def __init__(
        self,
        action_callback: Callable[[], None],
    ):
        self.action_callback = action_callback

    def call(self):
        self.action_callback()


class IntEvent:
    def __init__(
        self,
        state_callback: Callable[[], int],
        assign_callback: Callable[[int], None],
    ):
        self.state_callback = state_callback
        self.assign_callback = assign_callback

    def get_state(self) -> int:
        return self.state_callback()

    def set_state(self, state: int):
        self.assign_callback(state)


class BoolEvent:
    def __init__(
        self,
        state_callback: Callable[[], bool],
        assign_callback: Callable[[bool], None],
    ):
        self.state_callback = state_callback
        self.assign_callback = assign_callback

    def get_state(self) -> bool:
        return self.state_callback()

    def set_state(self, state: bool):
        self.assign_callback(state)


class StrEvent:
    def __init__(
        self,
        state_callback: Callable[[], str],
        assign_callback: Callable[[str], None],
    ):
        self.state_callback = state_callback
        self.assign_callback = assign_callback

    def get_state(self) -> str:
        return self.state_callback()

    def set_state(self, state: str):
        self.assign_callback(state)


class StaticOption(OptionABC):
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


class SActionOptionEvent(OptionABC):
    def __init__(
        self,
        name: str,
        success_name: str,
        item: MenuItem,
        event: ActionEvent,
    ):
        self.name = name
        self.success_name = success_name
        self.item = item
        self.event = event
        self.executed = False
        self.item.set_string(self.name)

    def back(self):
        pass

    def prev(self):
        pass

    def next(self):
        pass

    def apply(self):
        if not self.executed:
            self.event.call()
            self.item.set_string(self.success_name)
            self.executed = True
        self.update()

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


class ActionOptionEvent(OptionABC):
    def __init__(
        self,
        name: str,
        item: MenuItem,
        event: ActionEvent,
    ):
        self.name = name
        self.item = item
        self.event = event
        self.item.set_string(self.name)

    def back(self):
        pass

    def prev(self):
        pass

    def next(self):
        pass

    def apply(self):
        self.event.call()
        self.update()

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


class ToggleOptionEventBase(OptionABC):
    def __init__(self, name: str, item: MenuItem, event: BoolEvent):
        self._name = name
        self._item = item
        self._event = event
        self._update_menu_item()

    def _update_menu_item(self):
        string = "{}; {}"
        state_str = self._get_state_str()
        string = string.format(self._name, state_str)
        self._item.set_string(string)

    def _get_state_str(self) -> str:
        if self._get_state():
            return "ON"
        return "OFF"

    def _get_state(self) -> bool:
        return self._event.get_state()

    def _switch_state(self):
        state = not self._event.get_state()
        self._event.set_state(state)


class ToggleOptionEvent(ToggleOptionEventBase):
    def __init__(self, name: str, item: MenuItem, event: BoolEvent):
        super().__init__(name, item, event)

    def back(self):
        pass

    def prev(self):
        pass

    def next(self):
        pass

    def apply(self):
        self._switch_state()
        self._item.reset()
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


class ToggleOptionBase(OptionABC):
    def __init__(self, name: str, item: MenuItem):
        self._name = name
        self._item = item
        self._state = False
        self._update_menu_item()

    def _update_menu_item(self):
        string = "{}; {}"
        state_str = self._get_state_str()
        string = string.format(self._name, state_str)
        self._item.set_string(string)

    def _get_state_str(self) -> str:
        if self._get_state():
            return "ON"
        return "OFF"

    def _get_state(self) -> bool:
        return self._state

    def _switch_state(self):
        state = not self._state
        self._state = state


class ToggleOption(ToggleOptionBase):
    def __init__(self, name: str, item: MenuItem):
        super().__init__(name, item)

    def back(self):
        pass

    def prev(self):
        pass

    def next(self):
        pass

    def apply(self):
        self._switch_state()
        self._item.reset()
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


class ListOptionBase(OptionABC):
    def __init__(self, name: str, item: MenuItem, item_list: list[str]):
        self._name = name
        self._item = item
        self._item_list = item_list
        self._idx = 0
        self._max_idx = len(item_list) - 1
        self._change_state = False
        self._update_menu_item()

    def _update_menu_item(self):
        string = "{}; {}"
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
        idx = self._idx + 1
        if idx <= self._max_idx:
            self._idx = idx

    def _decrement(self):
        idx = self._idx - 1
        if idx >= 0:
            self._idx = idx

    def _get_value(self) -> str:
        return self._item_list[self._idx]


class ListOption(ListOptionBase):
    def __init__(self, name: str, item: MenuItem, item_list: list[str]):
        super().__init__(name, item, item_list)

    def back(self):
        self._back_state()
        self._item.reset()
        self.update()

    def prev(self):
        self._decrement()
        self._item.reset()
        self.update()

    def next(self):
        self._increment()
        self._item.reset()
        self.update()

    def apply(self):
        self._advance_state()
        self._item.reset()
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


class ListOptionEventBase(OptionABC):
    def __init__(
        self,
        name: str,
        item: MenuItem,
        event: StrEvent,
        item_list: list[str],
    ):
        self._name = name
        self._item = item
        self._event = event
        self._item_list = item_list
        self._idx = 0
        self._max_idx = len(item_list) - 1
        self._change_state = False
        self._update_menu_item()

    def _update_menu_item(self):
        string = "{}; {}"
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
        idx = self._idx + 1
        if idx <= self._max_idx:
            self._idx = idx
            self._event.set_state(self._get_value())

    def _decrement(self):
        idx = self._idx - 1
        if idx >= 0:
            self._idx = idx
            self._event.set_state(self._get_value())

    def _get_value(self) -> str:
        return self._item_list[self._idx]


class ListOptionEvent(ListOptionEventBase):
    def __init__(
        self,
        name: str,
        item: MenuItem,
        event: StrEvent,
        item_list: list[str],
    ):
        super().__init__(name, item, event, item_list)

    def back(self):
        self._back_state()
        self._item.reset()
        self.update()

    def prev(self):
        self._decrement()
        self._item.reset()
        self.update()

    def next(self):
        self._increment()
        self._item.reset()
        self.update()

    def apply(self):
        self._advance_state()
        self._item.reset()
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


class RangeOptionEventBase(OptionABC):
    def __init__(
        self,
        name: str,
        item: MenuItem,
        event: IntEvent,
        step: int,
        min_range: int,
        max_range: int,
    ):
        self._name = name
        self._item = item
        self._event = event
        self._step = step
        self._min_range = min_range
        self._max_range = max_range
        self._change_state = False
        self._update_menu_item()

    def _update_menu_item(self):
        string = "{}; {}"
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

    def _get_state(self) -> int:
        return self._event.get_state()

    def _advance_state(self):
        if not self._change_state:
            self._change_state = True

    def _back_state(self):
        if self._change_state:
            self._change_state = False

    def _increment(self):
        state = self._get_state() + self._step
        if state <= self._max_range:
            self._event.set_state(state)

    def _decrement(self):
        state = self._get_state() - self._step
        if state >= self._min_range:
            self._event.set_state(state)


class RangeOptionEvent(RangeOptionEventBase):
    def __init__(
        self,
        name: str,
        item: MenuItem,
        event: IntEvent,
        step: int,
        min_range: int,
        max_range: int,
    ):
        super().__init__(name, item, event, step, min_range, max_range)

    def back(self):
        self._back_state()
        self._item.reset()
        self.update()

    def prev(self):
        self._decrement()
        self._item.reset()
        self.update()

    def next(self):
        self._increment()
        self._item.reset()
        self.update()

    def apply(self):
        self._advance_state()
        self._item.reset()
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


class RangeOptionBase(OptionABC):
    def __init__(
        self,
        name: str,
        item: MenuItem,
        step: int,
        min_range: int,
        max_range: int,
    ):
        self._name = name
        self._item = item
        self._value = min_range
        self._step = step
        self._min_range = min_range
        self._max_range = max_range
        self._change_state = False
        self._update_menu_item()

    def _update_menu_item(self):
        string = "{}; {}"
        state_str = self.get_state_str()
        string = string.format(self._name, state_str)
        self._item.set_string(string)

    def get_state_str(self) -> str:
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
        value = self._value + self._step
        if value <= self._max_range:
            self._value = value

    def _decrement(self):
        value = self._value - self._step
        if value >= self._min_range:
            self._value = value

    def _get_value(self) -> int:
        return self._value


class RangeOption(RangeOptionBase):
    def __init__(
        self,
        name: str,
        item: MenuItem,
        step: int,
        min_range: int,
        max_range: int,
    ):
        super().__init__(name, item, step, min_range, max_range)

    def back(self):
        self._back_state()
        self._item.reset()
        self.update()

    def prev(self):
        self._decrement()
        self._item.reset()
        self.update()

    def next(self):
        self._increment()
        self._item.reset()
        self.update()

    def apply(self):
        self._advance_state()
        self._item.reset()
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
        string = "{}; {}"
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


class TimeOption(TimeBase):
    def __init__(self, name: str, item: MenuItem):
        super().__init__(name, item)

    def back(self):
        self._back_state()
        self._item.reset()
        self.update()

    def prev(self):
        self.decrement()
        self._item.reset()
        self.update()

    def next(self):
        self._increment()
        self._item.reset()
        self.update()

    def apply(self):
        self._advance_state()
        self._item.reset()
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


class CPUArchBase(OptionABC):
    def __init__(self, item: MenuItem):
        self._item = item
        self._value = self._get_cpu_name()
        self._update_menu_item()

    def _get_value(self) -> str:
        self._value = self._get_cpu_name()
        return self._value

    def _update_menu_item(self):
        string = "CPU: {}"
        string = string.format(self._get_value())
        self._item.set_string(string)

    @staticmethod
    def _get_cpu_name() -> str:
        cpu = Processor().get_processor_name()
        return cpu


class CPUArch(CPUArchBase):
    def __init__(self, item: MenuItem):
        super().__init__(item)

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
        return self._item.get_char_array()

    def get_item(self) -> MenuItem:
        return self._item

    def update(self):
        self._update_menu_item()

    def update_shift(self):
        self._item.shift()


class CPUPercBase(OptionABC):
    def __init__(self, item: MenuItem):
        self._item = item
        self._value = self._get_cpu_perc()
        self._update_menu_item()

    def _get_value(self) -> float:
        self._value = self._get_cpu_perc()
        return self._value

    def _update_menu_item(self):
        string = "Perc: {}%"
        string = string.format(self._get_value())
        self._item.set_string(string)

    @staticmethod
    def _get_cpu_perc() -> float:
        perc = Processor().get_usage()
        return perc


class CPUPerc(CPUPercBase):
    def __init__(self, item: MenuItem):
        super().__init__(item)

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
        return self._item.get_char_array()

    def get_item(self) -> MenuItem:
        return self._item

    def update(self):
        self._update_menu_item()

    def update_shift(self):
        self._item.shift()


class CPUFreqBase(OptionABC):
    def __init__(self, item: MenuItem):
        self._item = item
        self._value = self._get_cpu_freq()
        self._update_menu_item()

    def _get_value(self) -> int:
        self._value = self._get_cpu_freq()
        return self._value

    def _update_menu_item(self):
        string = "Freq: {}Mhz"
        string = string.format(self._get_value())
        self._item.set_string(string)

    @staticmethod
    def _get_cpu_freq() -> int:
        freq = Processor().get_frequency_mhz()
        freq = int(freq)
        return freq


class CPUFreq(CPUFreqBase):
    def __init__(self, item: MenuItem):
        super().__init__(item)

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
        return self._item.get_char_array()

    def get_item(self) -> MenuItem:
        return self._item

    def update(self):
        self._update_menu_item()

    def update_shift(self):
        self._item.shift()


class CPUCoreCountBase(OptionABC):
    def __init__(self, item: MenuItem):
        self._item = item
        self._value = self._get_core_count()
        self._update_menu_item()

    def _get_value(self) -> int:
        return self._value

    def _update_menu_item(self):
        string = "Core Count: {}"
        string = string.format(self._get_value())
        self._item.set_string(string)

    @staticmethod
    def _get_core_count() -> int:
        core_count = Processor().get_core_count()
        return core_count


class CPUCoreCount(CPUCoreCountBase):
    def __init__(self, item: MenuItem):
        super().__init__(item)

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
        return self._item.get_char_array()

    def get_item(self) -> MenuItem:
        return self._item

    def update(self):
        self._update_menu_item()

    def update_shift(self):
        self._item.shift()


class MemoryTotalBase(OptionABC):
    def __init__(self, item: MenuItem):
        self._item = item
        self._value = self._get_total_memory()
        self._update_menu_item()

    def _get_value(self) -> float:
        self._value = self._get_total_memory()
        return self._value

    def _update_menu_item(self):
        string = "TMem: {:.1f}KB"
        string = string.format(self._get_value())
        self._item.set_string(string)

    @staticmethod
    def _get_total_memory() -> float:
        total_mem = System().get_total_memory_bytes()
        total_mem_kb = total_mem / 1024
        return total_mem_kb


class MemoryTotal(MemoryTotalBase):
    def __init__(self, item: MenuItem):
        super().__init__(item)

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
        return self._item.get_char_array()

    def get_item(self) -> MenuItem:
        return self._item

    def update(self):
        self._update_menu_item()

    def update_shift(self):
        self._item.shift()


class MemoryUsedBase(OptionABC):
    def __init__(self, item: MenuItem):
        self._item = item
        self._value = self._get_used_memory()
        self._update_menu_item()

    def _get_value(self):
        self._value = self._get_used_memory()
        return self._value

    def _update_menu_item(self):
        string = "UMem: {:.1f}KB"
        string = string.format(self._get_value())
        self._item.set_string(string)

    @staticmethod
    def _get_used_memory() -> float:
        used_mem = System().get_used_memory_bytes()
        used_mem_kb = used_mem / 1024
        return used_mem_kb


class MemoryUsed(MemoryUsedBase):
    def __init__(self, item: MenuItem):
        super().__init__(item)

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
        return self._item.get_char_array()

    def get_item(self) -> MenuItem:
        return self._item

    def update(self):
        self._update_menu_item()

    def update_shift(self):
        self._item.shift()


class MemoryFreeBase(OptionABC):
    def __init__(self, item: MenuItem):
        self._item = item
        self._value = self._get_free_memory()
        self._update_menu_item()

    def _get_value(self):
        self._value = self._get_free_memory()
        return self._value

    def _update_menu_item(self):
        string = "FMem: {:.1f}KB"
        string = string.format(self._get_value())
        self._item.set_string(string)

    @staticmethod
    def _get_free_memory() -> float:
        free_mem = System().get_free_memory_bytes()
        free_mem_kb = free_mem / 1024
        return free_mem_kb


class MemoryFree(MemoryFreeBase):
    def __init__(self, item: MenuItem):
        super().__init__(item)

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
        return self._item.get_char_array()

    def get_item(self) -> MenuItem:
        return self._item

    def update(self):
        self._update_menu_item()

    def update_shift(self):
        self._item.shift()


class MemoryPercBase(OptionABC):
    def __init__(self, item: MenuItem):
        self._item = item
        self._value = self._get_memory_percentage()
        self._update_menu_item()

    def _get_value(self) -> int:
        self._value = self._get_memory_percentage()
        return self._value

    def _update_menu_item(self):
        string = "PMem: {}%"
        string = string.format(self._get_value())
        self._item.set_string(string)

    @staticmethod
    def _get_memory_percentage() -> int:
        mem_perc = System().get_memory_usage()
        mem_perc = int(mem_perc)
        return mem_perc


class MemoryPerc(MemoryPercBase):
    def __init__(self, item: MenuItem):
        super().__init__(item)

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
        return self._item.get_char_array()

    def get_item(self) -> MenuItem:
        return self._item

    def update(self):
        self._update_menu_item()

    def update_shift(self):
        self._item.shift()


class MenuCreator:
    def __init__(
        self, heads: list[OptionABC], submenus: list[OrdDict[OptionABC, OrdDict]]
    ):
        self.heads = heads
        self.submenus = submenus

    def create(self) -> OrdDict[OptionABC, OrdDict]:
        if len(self.heads) != len(self.submenus):
            raise Exception("Heads and Submenus have different lengths.\n")

        menu = OrdDict()

        for idx, head in enumerate(self.heads):
            submenu = self.submenus[idx]
            menu.update({head: submenu})

        return menu
