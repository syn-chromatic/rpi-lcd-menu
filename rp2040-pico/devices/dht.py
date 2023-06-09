import time
import pigpio


class DHT11Result:
    NO_ERROR = 0
    ERR_MISSING_DATA = 1
    ERR_CRC = 2

    def __init__(self, temperature: float, humidity: float, error_code: int = NO_ERROR):
        self.temperature = temperature
        self.humidity = humidity
        self.error_code = error_code

    def is_valid(self):
        return self.error_code == self.NO_ERROR


class DHT11:
    def __init__(self, pin: int):
        self._pin = pin
        self._pi = pigpio.pi()

    def read(self) -> DHT11Result:
        self._pi.set_mode(self._pin, pigpio.OUTPUT)
        self._send_and_sleep(pigpio.HIGH, 0.05)
        self._send_and_sleep(pigpio.LOW, 0.02)
        self._pi.set_mode(self._pin, pigpio.INPUT)
        self._pi.set_pull_up_down(self._pin, pigpio.PUD_UP)

        data = self._collect_input()
        pull_up_lengths = self._parse_data_pull_up_lengths(data)
        if len(pull_up_lengths) != 40:
            return DHT11Result(0, 0, DHT11Result.ERR_MISSING_DATA)

        bits = self._calculate_bits(pull_up_lengths)
        the_bytes = self._bits_to_bytes(bits)

        checksum = self._calculate_checksum(the_bytes)
        if the_bytes[4] != checksum:
            return DHT11Result(0, 0, DHT11Result.ERR_CRC)

        # The meaning of the return sensor values
        # the_bytes[0]: humidity int
        # the_bytes[1]: humidity decimal
        # the_bytes[2]: temperature int
        # the_bytes[3]: temperature decimal

        temperature = the_bytes[2] + float(the_bytes[3]) / 10
        humidity = the_bytes[0] + float(the_bytes[1]) / 10

        return DHT11Result(temperature, humidity)

    def _send_and_sleep(self, output: int, sleep: float):
        self._pi.write(self._pin, output)
        time.sleep(sleep)

    def _collect_input(self) -> list[int]:
        unchanged_count = 0
        max_unchanged_count = 100

        last = -1
        data = []
        while True:
            current = self._pi.read(self._pin)
            data.append(current)
            if last != current:
                unchanged_count = 0
                last = current
            else:
                unchanged_count += 1
                if unchanged_count > max_unchanged_count:
                    break

        return data

    def _parse_data_pull_up_lengths(self, data: list[int]) -> list[int]:
        state_init_pull_down = 1
        state_init_pull_up = 2
        state_data_first_pull_down = 3
        state_data_pull_up = 4
        state_data_pull_down = 5

        state = state_init_pull_down

        lengths = []
        current_length = 0

        for i in range(len(data)):
            current = data[i]
            current_length += 1

            if state == state_init_pull_down:
                if current == pigpio.LOW:
                    state = state_init_pull_up

            elif state == state_init_pull_up:
                if current == pigpio.HIGH:
                    state = state_data_first_pull_down

            elif state == state_data_first_pull_down:
                if current == pigpio.LOW:
                    state = state_data_pull_up

            elif state == state_data_pull_up:
                if current == pigpio.HIGH:
                    current_length = 0
                    state = state_data_pull_down

            elif state == state_data_pull_down:
                if current == pigpio.LOW:
                    lengths.append(current_length)
                    state = state_data_pull_up

        return lengths

    def _calculate_bits(self, pull_up_lengths) -> list[int]:
        shortest_pull_up = 1000
        longest_pull_up = 0

        for i in range(0, len(pull_up_lengths)):
            length = pull_up_lengths[i]
            if length < shortest_pull_up:
                shortest_pull_up = length
            if length > longest_pull_up:
                longest_pull_up = length

        halfway = shortest_pull_up + (longest_pull_up - shortest_pull_up) / 2
        bits = []

        for i in range(0, len(pull_up_lengths)):
            bit = False
            if pull_up_lengths[i] > halfway:
                bit = True
            bits.append(bit)

        return bits

    def _bits_to_bytes(self, bits: list[int]) -> list[int]:
        the_bytes = []
        byte = 0

        for i in range(0, len(bits)):
            byte = byte << 1
            if bits[i]:
                byte = byte | 1
            else:
                byte = byte | 0
            if (i + 1) % 8 == 0:
                the_bytes.append(byte)
                byte = 0

        return the_bytes

    def _calculate_checksum(self, bytes: list[int]):
        return bytes[0] + bytes[1] + bytes[2] + bytes[3] & 255
