import sys


class ConsoleWriter:
    def __init__(self, rows: int):
        self.rows = rows

    def clear_line(self):
        sys.stdout.write("\033[K")

    def move_to_previous_line(self):
        sys.stdout.write("\033[F")

    def print(self, string: str):
        segments = string.split("\n")
        for _ in range(self.rows):
            self.move_to_previous_line()
            self.clear_line()

        for idx, line in enumerate(segments):
            end = "\n"
            if idx == len(segments) - 1:
                end = "\r"

            print(line, end=end)
