from typing import Callable

from options.abstracts import Option, OptionToggle, OptionRange, OptionTimeHM
from options.item import MenuItem


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
    def __init__(
        self, name: str, item: MenuItem, callback: Callable, state_callback: Callable
    ):
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
        assign_callback: Callable,
        state_callback: Callable,
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
