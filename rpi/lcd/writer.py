from lcd.i2c import I2CLCD
from time import sleep


class LCDWriterBase:
    def __init__(self, rows: int, columns: int):
        self._columns = columns
        self._rows = rows
        self._lcd = self._get_lcd()
        self._row_states: list[int] = [0] * rows
        self._row_data: list[list[str]] = [[]] * rows

    def _get_lcd(self) -> I2CLCD:
        lcd = I2CLCD(1, 0x27, self._rows, self._columns)
        return lcd

    def _set_row_state(self, chars: list[str], row: int):
        self._row_states[row] = len(chars)

    def _fill_chars(self, chars: list[str], row: int):
        row_state = self._row_states[row]
        fill = row_state - len(chars)
        if fill > 0:
            for _ in range(fill):
                chars.append(" ")

    def _insert_row_data(self, chars: list[str], row: int):
        self._row_data[row] = chars

    def _get_string_changes(
        self, chars: list[str], prev_chars: list[str]
    ) -> list[tuple[str, int]]:
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

    def _write_row(self, chars: list[str], row: int):
        len_chars = len(chars)
        prev_chars = self._row_data[row]
        self._fill_chars(chars, row)
        changes = self._get_string_changes(chars, prev_chars)

        for char, column in changes:
            self._validate_column(column)
            self._lcd.move_to(column, row)
            self._lcd.putchar(char)

        self._lcd.move_to(len_chars, row)
        self._insert_row_data(chars, row)
        self._set_row_state(chars, row)

    def _seg_string(self, string: str) -> list[list[str]]:
        segments = []
        line = []
        for char in string:
            if char == "\n" and line:
                segments.append(line)
                line = []
                continue
            line.append(char)
        return segments

    def _validate_segments(self, segments: list[list[str]]):
        if self._rows > len(segments):
            error = "Data passed to LCDWriter exceeds LCD Rows:\n{}"
            error = error.format(segments)
            raise Exception(error)

    def _validate_column(self, idx: int):
        if idx >= self._columns:
            error = "Data passed to LCDWriter exceeds LCD Columns:\n{}"
            error = error.format(idx)
            raise Exception(error)

    def _write_with_cursor(self, string: str, hold_time: float):
        self._lcd.blink_cursor_on()
        segments = self._seg_string(string)
        self._validate_segments(segments)
        for idx, segment in enumerate(segments):
            self._write_row(segment, idx)
        sleep(hold_time)
        self._lcd.blink_cursor_off()

    def _write(self, string: str, hold_time: float):
        self._lcd.hide_cursor()
        segments = self._seg_string(string)
        self._validate_segments(segments)
        for idx, segment in enumerate(segments):
            self._write_row(segment, idx)
        sleep(hold_time)


class LCDWriter(LCDWriterBase):
    def __init__(self, rows: int, columns: int):
        super().__init__(rows, columns)

    def write_with_cursor(self, string: str, hold_time: float):
        self._write_with_cursor(string, hold_time)

    def write(self, string: str, hold_time: float):
        self._write(string, hold_time)

    def set_backlight(self, backlight_bool: bool):
        if backlight_bool:
            self._lcd.backlight_on()
            return
        self._lcd.backlight_off()
