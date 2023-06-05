from options.abstracts import Option


class MenuCreator:
    def __init__(self, heads: list[Option], submenus: list[dict[Option, dict]]):
        self.heads = heads
        self.submenus = submenus

    def create(self) -> dict[Option, dict]:
        if len(self.heads) != len(self.submenus):
            raise Exception()

        menu = {}

        for idx, head in enumerate(self.heads):
            submenu = self.submenus[idx]
            menu.update({head: submenu})

        return menu
