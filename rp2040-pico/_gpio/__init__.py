try:
    import machine
    from .gpio import GPIOInput, GPIOI2C

    __all__ = ["GPIOInput", "GPIOI2C"]

except ImportError:
    import logging
    from .dummyio import GPIOInput, GPIOI2C

    error = (
        "Machine library could not be loaded, "
        "fallback to Dummy GPIO for development."
    )
    logging.critical(error)

    __all__ = ["GPIOInput", "GPIOI2C"]
