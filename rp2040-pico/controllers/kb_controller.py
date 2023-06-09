from configurations import KBCtrlConfigABC
from msvcrt import getch, kbhit

from std.typing import Callable


class KBControllerBase:
    def __init__(self, ctrl_config: KBCtrlConfigABC):
        self._back_key = ctrl_config.back_key
        self._prev_key = ctrl_config.prev_key
        self._next_key = ctrl_config.next_key
        self._apply_key = ctrl_config.apply_key
        self._back_callback = None
        self._prev_callback = None
        self._next_callback = None
        self._apply_callback = None

    def _execute_back_callback(self):
        if self._back_callback:
            self._back_callback()

    def _execute_prev_callback(self):
        if self._prev_callback:
            self._prev_callback()

    def _execute_next_callback(self):
        if self._next_callback:
            self._next_callback()

    def _execute_apply_callback(self):
        if self._apply_callback:
            self._apply_callback()


class KBController(KBControllerBase):
    def __init__(self, ctrl_config: KBCtrlConfigABC):
        super().__init__(ctrl_config)

    def register_back_callback(self, callback: Callable):
        self._back_callback = callback

    def register_prev_callback(self, callback: Callable):
        self._prev_callback = callback

    def register_next_callback(self, callback: Callable):
        self._next_callback = callback

    def register_apply_callback(self, callback: Callable):
        self._apply_callback = callback

    def check(self):
        if kbhit():
            key = ord(getch())

            if key == self._back_key:
                self._execute_back_callback()

            if key == self._prev_key:
                self._execute_prev_callback()

            if key == self._next_key:
                self._execute_next_callback()

            if key == self._apply_key:
                self._execute_apply_callback()
