from options.abstracts import OptionABC


class MenuCreator:
    def __init__(self, heads: list[OptionABC], submenus: list[dict[OptionABC, dict]]):
        self.heads = heads
        self.submenus = submenus

    def create(self) -> dict[OptionABC, dict]:
        if len(self.heads) != len(self.submenus):
            raise Exception()

        menu = {}

        for idx, head in enumerate(self.heads):
            submenu = self.submenus[idx]
            menu.update({head: submenu})

        return menu
