from lcd.i2c import I2CLCD
from time import sleep

from writers.abstracts import WriterABC
from character.abstracts import CharABC, ASCIICharABC, ByteCharABC
from character.chars import SpaceChar


class LCDWriterBase(WriterABC):
    def __init__(self, rows: int, columns: int):
        self._rows = rows
        self._columns = columns
        self._lcd = self._get_lcd()
        self._row_states: list[int] = [0] * rows
        self._row_data: list[list[CharABC]] = [[]] * rows

    def _get_lcd(self) -> I2CLCD:
        lcd = I2CLCD(1, 0x27, self._rows, self._columns)
        return lcd

    def _set_row_state(self, chars: list[CharABC], row: int):
        self._row_states[row] = len(chars)

    def _fill_chars(self, chars: list[CharABC], row: int):
        row_state = self._row_states[row]
        fill = row_state - len(chars)
        if fill > 0:
            for _ in range(fill):
                chars.append(SpaceChar())

    def _insert_row_data(self, chars: list[CharABC], row: int):
        self._row_data[row] = chars

    def _get_char_changes(
        self, chars: list[CharABC], prev_chars: list[CharABC]
    ) -> list[tuple[CharABC, int]]:
        changes = []
        max_idx = len(prev_chars) - 1
        for idx in range(len(chars)):
            char1 = chars[idx]
            if idx <= max_idx:
                char2 = prev_chars[idx]
                if char1 != char2:
                    changes.append((char1, idx))
                continue
            changes.append((char1, idx))
        return changes

    def _write_char(self, char: CharABC, column: int, row: int):
        if isinstance(char, ASCIICharABC):
            self._lcd.move_to(column, row)
            value = char.get_value()
            self._lcd.putchar(value)
            return

        elif isinstance(char, ByteCharABC):
            self._lcd.move_to(column, row)
            value = char.get_value()
            self._lcd.putchar(value)
            return

        raise NotImplementedError(f"Not Implemented: {char}")

    def _write_row(self, segment: list[CharABC], row: int):
        len_chars = len(segment)
        prev_chars = self._row_data[row]
        self._fill_chars(segment, row)
        changes = self._get_char_changes(segment, prev_chars)

        for char, column in changes:
            self._write_char(char, column, row)

        self._lcd.move_to(len_chars, row)
        self._insert_row_data(segment, row)
        self._set_row_state(segment, row)

    def _write_with_cursor(self, chars: list[list[CharABC]], hold_time: float):
        self._lcd.blink_cursor_on()
        for idx, segment in enumerate(chars):
            self._write_row(segment, idx)
        sleep(hold_time)
        self._lcd.blink_cursor_off()

    def _write(self, chars: list[list[CharABC]], hold_time: float):
        self._lcd.hide_cursor()
        for idx, segment in enumerate(chars):
            self._write_row(segment, idx)
        sleep(hold_time)


class LCDWriter(LCDWriterBase):
    def __init__(self, rows: int, columns: int):
        super().__init__(rows, columns)

    def write_with_cursor(self, chars: list[list[CharABC]], hold_time: float):
        self._write_with_cursor(chars, hold_time)

    def write(self, chars: list[list[CharABC]], hold_time: float):
        self._write(chars, hold_time)

    def set_backlight(self, backlight_bool: bool):
        if backlight_bool:
            self._lcd.backlight_on()
            return
        self._lcd.backlight_off()

    def get_backlight_state(self) -> bool:
        return self._lcd.backlight
