from options.abstracts import OptionABC

# For interchangeable compatibility with MicroPython
from collections import OrderedDict as OrdDict


class MenuCreator:
    def __init__(
        self, heads: list[OptionABC], submenus: list[OrdDict[OptionABC, OrdDict]]
    ):
        self.heads = heads
        self.submenus = submenus

    def create(self) -> OrdDict[OptionABC, OrdDict]:
        if len(self.heads) != len(self.submenus):
            raise Exception()

        menu = OrdDict()

        for idx, head in enumerate(self.heads):
            submenu = self.submenus[idx]
            menu.update({head: submenu})

        return menu
