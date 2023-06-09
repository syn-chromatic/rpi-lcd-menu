try:
    raise Exception()
    import pigpio
    from .gpio import InputGPIO, OutputGPIO, I2CGPIO

    if not pigpio.pi().connected:
        raise Exception(
            "PiGPIO library could not be loaded, "
            "fallback to Dummy GPIO for development."
        )

    __all__ = ["InputGPIO", "OutputGPIO", "I2CGPIO"]

except Exception as error:
    import logging
    from .dummyio import InputGPIO, OutputGPIO, I2CGPIO

    logging.critical(error)

    __all__ = ["InputGPIO", "OutputGPIO", "I2CGPIO"]
