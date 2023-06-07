from options.abstracts import OptionABC

from options.events import ActionEvent, BoolEvent, IntEvent, StrEvent
from options.item import MenuItem

from character.abstracts import CharABC


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
