# try:
#     import pigpio
#     from .gpio import GPIOInput, GPIOI2C

#     if not pigpio.pi().connected:
#         raise Exception(
#             "PiGPIO library could not be loaded, "
#             "fallback to Dummy GPIO for development."
#         )

#     __all__ = ["GPIOInput", "GPIOI2C"]

# except Exception as error:
import logging
from .dummyio import GPIOInput, GPIOI2C

# logging.critical(error)

__all__ = ["GPIOInput", "GPIOI2C"]
