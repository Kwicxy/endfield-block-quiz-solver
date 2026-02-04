class Block:
    def __init__(self, shape: list[list[int]], index: int = 1, type: int = 0):
        self.index = index
        self.type = type
        self.shape = shape

    def rotate(self):
        """ Rotate the shape 90 degrees clockwise """
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def __str__(self) -> str:
        """ String representation of the block """
        shape_str = ""
        for row in self.shape:
            shape_str += ' '.join(str(cell) for cell in row) + "\n"
        return f"Block Type: {self.type}, Index: {self.index}, Shape:\n{shape_str}"


class Board:
    def __init__(self, nrows: int, ncols: int):
        self.nrows = nrows
        self.ncols = ncols
        self.values = self.init_board()

    def init_board(self) -> list:
        """ Initialize an empty board """
        return [[0 for j in range(self.ncols)] for i in range(self.nrows)]

    def fill_from_matrix(self, matrix: list[list[int]]) -> None:
        """ Fill the board from a given matrix """
        for i in range(self.nrows):
            for j in range(self.ncols):
                self.values[i][j] = matrix[i][j]

    def place_block(self, block: Block, row: int, col: int) -> None:
        """ Place a block on the board at the specified position """
        for (i, shape_row) in enumerate(block.shape):
            for (j, cell) in enumerate(shape_row):
                if cell == 1:
                    self.values[row + i][col + j] = block.index

    def remove_block(self, block: Block, row: int, col: int) -> None:
        """ Remove a block from the board at the specified position """
        for (i, shape_row) in enumerate(block.shape):
            for (j, cell) in enumerate(shape_row):
                if cell == 1:
                    self.values[row + i][col + j] = 0

    def __str__(self) -> str:
        """ String representation of the board """
        board_str = ""
        for row in self.values:
            board_str += ' '.join(str(cell) if cell >=0 else 'X' for cell in row) + "\n"
        return board_str