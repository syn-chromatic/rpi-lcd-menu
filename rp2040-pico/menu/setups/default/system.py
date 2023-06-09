from configurations import LCDConfigABC

from options.abstracts import OptionABC
from options.customs import CPUArch, CPUPerc, CPUFreq, CPUCoreCount
from options.customs import MemoryTotal, MemoryFree, MemoryUsed, MemoryPerc
from options.item import MenuItem
from options.utils import MenuCreator


class SystemInfoMenu:
    def __init__(self, lcd_config: LCDConfigABC):
        self.lcd_config = lcd_config

    def get_menu_item(self) -> MenuItem:
        columns = self.lcd_config.lcd_columns
        return MenuItem(columns)

    def get_heads(self) -> list[OptionABC]:
        cpu_arch = CPUArch(self.get_menu_item())
        cpu_perc = CPUPerc(self.get_menu_item())
        cpu_freq = CPUFreq(self.get_menu_item())
        cpu_cores = CPUCoreCount(self.get_menu_item())
        mem_total = MemoryTotal(self.get_menu_item())
        mem_free = MemoryFree(self.get_menu_item())
        mem_used = MemoryUsed(self.get_menu_item())
        mem_perc = MemoryPerc(self.get_menu_item())

        heads = [
            cpu_arch,
            cpu_perc,
            cpu_freq,
            cpu_cores,
            mem_total,
            mem_free,
            mem_used,
            mem_perc,
        ]
        return heads

    def get_submenus(self, heads: list[OptionABC]) -> list[dict]:
        submenus = [{}] * len(heads)
        return submenus

    def get_menu(self) -> dict[OptionABC, dict]:
        heads = self.get_heads()
        submenus = self.get_submenus(heads)
        menu = MenuCreator(heads, submenus).create()
        return menu
