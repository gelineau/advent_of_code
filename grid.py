class Grid:
    def __init__(self, input: list[str]):
        self.values = [[int(char) for char in line] for line in input]

    def row_max(self):
        return len(self.values)

    def col_max(self):
        return len(self.values[0])

    def is_in_grid(self, row, column):
        if row < 0 or column < 0 or row >= self.row_max() or column >= self.col_max():
            return False
        return True

    def get(self, row: int, column: int) -> int:
        if self.is_in_grid(row, column):
            return self.values[row][column]
        raise IndexError

    def __repr__(self):
        result = "\n"
        for row in range(self.row_max()):
            result += (
                "".join(str(self.get(row, column)) for column in range(self.col_max()))
                + "\n"
            )

        return result