import dht
from machine import Pin


class DHT22Base:
    def __init__(self, pin: int, interval: int = 3):
        self._sensor = self._get_sensor(pin)
        self._interval = interval
        self._interval_counter = 0

    def _get_sensor(self, pin: int):
        sensor = dht.DHT22(Pin(pin))
        sensor.measure()
        return sensor

    def _measure(self):
        if self._interval_counter >= self._interval:
            self._sensor.measure()
            self._interval_counter = 0
            return
        self._interval_counter += 1


class DHT22(DHT22Base):
    def __init__(self, pin: int):
        super().__init__(pin)

    def temperature(self) -> str:
        self._measure()
        temp = self._sensor.temperature()
        return f"{temp:.2f}"

    def humidity(self) -> str:
        self._measure()
        humidity = self._sensor.humidity()
        return f"{humidity:.2f}"
