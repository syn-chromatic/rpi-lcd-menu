try:
    import pigpio
    from .gpio import GPIOInput, GPIOI2C

    if not pigpio.pi().connected:
        raise Exception()

    __all__ = ["GPIOInput", "GPIOI2C"]

except Exception:
    import logging
    from .dummyio import GPIOInput, GPIOI2C

    error = (
        "PiGPIO library could not be loaded, fallback to Dummy GPIO for development."
    )
    logging.critical(error)

    __all__ = ["GPIOInput", "GPIOI2C"]
