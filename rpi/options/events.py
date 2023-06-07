from typing import Callable


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
