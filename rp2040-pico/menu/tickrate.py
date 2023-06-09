class Tickrate:
    def __init__(self, tick: int):
        self.tick = tick

    def get_tickrate(self) -> int:
        return self.tick

    def set_tickrate(self, tick: int):
        self.tick = tick
