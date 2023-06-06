# from options.bases import ItemListBase, RangeBase
# from options.item import MenuItem


# class AddDeviceMenu:
#     def __init__(self, columns: int):
#         self.columns = columns

#     def gpio_selection_item(self):
#         name = "GPIO:"
#         item_list = ["Input", "Output"]
#         assign_callback = lambda x: x
#         menu_item = MenuItem(self.columns)
#         option = ItemListBase(name, menu_item, item_list, assign_callback)
#         return option

#     def pin_selection_item(self):
#         name = "Pin:"
#         assign_callback = lambda x: x
#         state_callback = lambda x: x
#         menu_item = MenuItem(self.columns)
#         option = RangeBase(name, menu_item, 0, 40, 1, assign_callback, state_callback)

#     # def


# # GPIO: Input
# # Pin: 16
