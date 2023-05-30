try:
    import lgpio

    if len(dir(lgpio)) <= 8:
        raise ImportError()

    from .gpio import GPIO, GPIOI2C

    __all__ = ["GPIO", "GPIOI2C"]

except ImportError:
    import logging
    from .dummyio import GPIO, GPIOI2C

    error = "LGPIO library could not be loaded, fallback to Dummy GPIO for development."
    logging.critical(error)

    __all__ = ["GPIO", "GPIOI2C"]
