from typing import Callable


class StateBool:
    def __init__(self, state: bool):
        self.state = state

    def get_state(self) -> bool:
        return self.state

    def set_state(self, state: bool):
        self.state = state


class StateInt:
    def __init__(self, state: int):
        self.state = state

    def get_state(self) -> int:
        return self.state

    def set_state(self, state: int):
        self.state = state


class LinkedStateBool:
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


class LinkedStateInt:
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
