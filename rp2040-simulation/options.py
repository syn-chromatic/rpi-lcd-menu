from collections import OrderedDict as OrdDict
from abc import ABC, abstractmethod
from typing import Callable


class MenuItemBase:
    def __init__(self, columns: int, shift_hold: int, string: str = ""):
        self._columns = columns
        self._string = string
        self._shift_hold = shift_hold
        self._st_range = 0
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

    def _get_reset_condition(self):
        if not self._is_selected and self._st_range != 0:
            return True
        return False

    def _increment_shift(self):
        shift_condition = self._get_shift_condition()

        if shift_condition:
            if not self._hold_shift_start():
                self._st_range += 1
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


class Option(ABC):
    def __init__(self, item: MenuItem):
        self.item: MenuItem = item

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def update_shift(self):
        pass

    @abstractmethod
    def get_string(self) -> str:
        pass


class OptionToggle(Option):
    def __init__(self, callback: Callable, state_callback: Callable):
        self.callback: Callable = callback
        self.state_callback: Callable = state_callback

    @abstractmethod
    def get_state(self) -> bool:
        pass

    @abstractmethod
    def execute_callback(self):
        pass


class OptionRange(Option):
    def __init__(
        self,
        min_range: int,
        max_range: int,
        step: int,
        assign_callback: Callable,
        state_callback: Callable,
    ):
        self.min_range: int = min_range
        self.max_range: int = max_range
        self.step: int = step
        self.assign_callback: Callable = assign_callback
        self.state_callback: Callable = state_callback
        self.change_state: bool = False

    @abstractmethod
    def get_value(self) -> int:
        pass

    @abstractmethod
    def get_hold_state(self) -> bool:
        pass

    @abstractmethod
    def advance_state(self):
        pass

    @abstractmethod
    def back_state(self):
        pass

    @abstractmethod
    def increment(self):
        pass

    def decrement(self):
        pass


class OptionTimeHM(Option):
    def __init__(self):
        self.hours: int = 0
        self.minutes: int = 0
        self.selected: int = 0
        self.select_state: bool = False
        self.change_state: bool = False

    @abstractmethod
    def get_hold_state(self) -> bool:
        pass

    @abstractmethod
    def advance_state(self):
        pass

    @abstractmethod
    def back_state(self):
        pass

    @abstractmethod
    def increment(self):
        pass

    def decrement(self):
        pass


class StaticBase(Option):
    def __init__(self, name: str, item: MenuItem):
        self.name = name
        self.item = item
        self.update_menu_item()

    def update_menu_item(self):
        self.item.set_string(self.name)

    def update(self):
        pass

    def update_shift(self):
        self.item.shift()

    def get_string(self) -> str:
        return self.item.get_string()


class ToggleBase(OptionToggle):
    def __init__(self, name: str, item: MenuItem, callback, state_callback):
        self.name = name
        self.item = item
        self.callback = callback
        self.state_callback = state_callback
        self.update_menu_item()

    def update_menu_item(self):
        string = "{}: {}"
        state_str = self.get_state_str()
        string = string.format(self.name, state_str)
        self.item.set_string(string)

    def get_state_str(self) -> str:
        if self.get_state():
            return "ON"
        return "OFF"

    def update(self):
        self.update_menu_item()

    def update_shift(self):
        self.item.shift()

    def get_string(self) -> str:
        return self.item.get_string()

    def get_state(self) -> bool:
        return self.state_callback()

    def execute_callback(self):
        state = not self.get_state()
        self.callback(state)


class RangeBase(OptionRange):
    def __init__(
        self,
        name: str,
        item: MenuItem,
        min_range: int,
        max_range: int,
        step: int,
        assign_callback,
        state_callback,
    ):
        self.name = name
        self.item = item
        self.min_range = min_range
        self.max_range = max_range
        self.step = step
        self.assign_callback = assign_callback
        self.state_callback = state_callback
        self.change_state = False
        self.update_menu_item()

    def get_state_str(self) -> str:
        if self.change_state:
            string = "<{}>"
            string = string.format(self.get_value())
            return string
        string = "{}"
        string = string.format(self.get_value())
        return string

    def update_menu_item(self):
        string = "{}: {}"
        state_str = self.get_state_str()
        string = string.format(self.name, state_str)
        self.item.set_string(string)

    def update(self):
        self.update_menu_item()

    def update_shift(self):
        self.item.shift()

    def get_string(self) -> str:
        return self.item.get_string()

    def get_value(self):
        return self.state_callback()

    def get_hold_state(self) -> bool:
        if self.change_state:
            return True
        return False

    def advance_state(self):
        if not self.change_state:
            self.change_state = True

    def back_state(self):
        if self.change_state:
            self.change_state = False

    def increment(self):
        value = self.get_value() + self.step
        if value <= self.max_range:
            self.assign_callback(value)

    def decrement(self):
        value = self.get_value() - self.step
        if value >= self.min_range:
            self.assign_callback(value)


class TimeBase(OptionTimeHM):
    def __init__(self, name: str, item: MenuItem):
        self.name = name
        self.item = item
        self.hours = 0
        self.minutes = 0
        self.selected = 0
        self.select_state = False
        self.change_state = False
        self.update_menu_item()

    def get_hours_str(self) -> str:
        if len(str(self.hours)) == 1:
            return "0" + str(self.hours)
        return str(self.hours)

    def get_minutes_str(self) -> str:
        if len(str(self.minutes)) == 1:
            return "0" + str(self.minutes)
        return str(self.minutes)

    def get_time_str(self, segments: list[str]) -> str:
        len_segments = len(segments) - 1
        string = ""
        for idx, seg in enumerate(segments):
            string += seg

            if idx != len_segments:
                string += ":"
        return string

    def get_segments(self):
        hours = self.get_hours_str()
        minutes = self.get_minutes_str()
        segments = [hours, minutes]
        return segments

    def get_time_select(self) -> str:
        segments = self.get_segments()
        for idx, seg in enumerate(segments):
            if self.selected == idx:
                segments[idx] = f"[{seg}]"
        string = self.get_time_str(segments)
        return string

    def get_time_change(self) -> str:
        segments = self.get_segments()
        for idx, seg in enumerate(segments):
            if self.selected == idx:
                segments[idx] = f"<{seg}>"
        string = self.get_time_str(segments)
        return string

    def get_state_str(self) -> str:
        if self.select_state and not self.change_state:
            string = self.get_time_select()
            return string

        elif self.select_state and self.change_state:
            string = self.get_time_change()
            return string

        segments = self.get_segments()
        string = self.get_time_str(segments)
        return string

    def update_menu_item(self):
        string = "{}: {}"
        state_str = self.get_state_str()
        string = string.format(self.name, state_str)
        self.item.set_string(string)

    def update(self):
        self.update_menu_item()

    def update_shift(self):
        self.item.shift()

    def get_string(self) -> str:
        return self.item.get_string()

    def get_hold_state(self) -> bool:
        if self.select_state or self.change_state:
            return True
        return False

    def advance_state(self):
        if not self.select_state:
            self.select_state = True
            return
        self.change_state = True

    def back_state(self):
        if self.change_state:
            self.change_state = False
            return
        self.select_state = False
        self.selected = 0

    def increment_selected(self):
        if self.selected < 1:
            self.selected += 1
            return
        self.selected = 0

    def increment_time(self):
        if self.selected == 0:
            if self.hours + 1 < 24:
                self.hours += 1

        elif self.selected == 1:
            if self.minutes + 1 < 60:
                self.minutes += 1

    def decrement_time(self):
        if self.selected == 0:
            if self.hours - 1 >= 0:
                self.hours -= 1

        elif self.selected == 1:
            if self.minutes - 1 >= 0:
                self.minutes -= 1

    def increment(self):
        if self.select_state and not self.change_state:
            self.increment_selected()
            return
        if self.select_state and self.change_state:
            self.increment_time()

    def decrement(self):
        if self.select_state and not self.change_state:
            self.increment_selected()
            return
        if self.select_state and self.change_state:
            self.decrement_time()


class CPUName(Option):
    def __init__(self, item: MenuItem):
        self.item = item
        self.update_menu_item()

    def update_menu_item(self):
        string = "CPU: {}"
        string = string.format(self.get_cpu_name())
        self.item.set_string(string)

    @staticmethod
    def get_cpu_name() -> str:
        cpu = "Test CPU"
        return cpu

    def update(self):
        self.update_menu_item()

    def update_shift(self):
        self.item.shift()

    def get_string(self) -> str:
        return self.item.get_string()


class CPUPerc(Option):
    def __init__(self, item: MenuItem):
        self.item = item
        self.update_menu_item()

    def update_menu_item(self):
        string = "Perc: {}%"
        string = string.format(self.get_cpu_perc())
        self.item.set_string(string)

    @staticmethod
    def get_cpu_perc() -> float:
        perc = 1.0
        return perc

    def update(self):
        self.update_menu_item()

    def update_shift(self):
        self.item.shift()

    def get_string(self) -> str:
        return self.item.get_string()


class CPUFreq(Option):
    def __init__(self, item: MenuItem):
        self.item = item
        self.update_menu_item()

    def update_menu_item(self):
        string = "Freq: {}Mhz"
        string = string.format(self.get_cpu_freq())
        self.item.set_string(string)

    @staticmethod
    def get_cpu_freq() -> int:
        freq = 1
        freq = int(freq)
        return freq

    def update(self):
        self.update_menu_item()

    def update_shift(self):
        self.item.shift()

    def get_string(self) -> str:
        return self.item.get_string()


class MenuCreator:
    def __init__(self, heads: list[Option], submenus: list[OrdDict[Option, OrdDict]]):
        self.heads = heads
        self.submenus = submenus

    def create(self) -> OrdDict[Option, OrdDict]:
        if len(self.heads) != len(self.submenus):
            raise Exception()

        menu = OrdDict()

        for idx, head in enumerate(self.heads):
            submenu = self.submenus[idx]
            menu.update({head: submenu})

        return menu
