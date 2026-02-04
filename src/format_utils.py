import tomllib

from entities import Block, Board

def read_toml_file(file_path: str) -> dict:
    """Reads a TOML file and returns its contents as a dictionary."""
    with open(file_path, 'rb') as file:
        data = tomllib.load(file)
    return data

def get_quiz_board(file_path: str) -> Board:
    with open(file_path, 'rb') as file:
        data = tomllib.load(file)
    nrows = len(data['board'])
    ncols = len(data['board'][0]) if nrows > 0 else 0
    board = Board(nrows, ncols)
    board.fill_from_matrix(data['board'])
    return board

def get_quiz_limits(file_path: str) -> list[list[int]]:
    with open(file_path, 'rb') as file:
        data = tomllib.load(file)
    return data['limits']

def get_quiz_blocks(file_path: str) -> list[Block]:
    with open(file_path, 'rb') as file:
        data = tomllib.load(file)
    blocks = []
    for index in data:
        blocks.append(Block(data[index]['shape'], index=int(index), type=data[index].get('type', 0)))

    return blocks

def get_test_answer(file_path: str) -> list[list[int]]:
    with open(file_path, 'rb') as file:
        data = tomllib.load(file)
    nrows = len(data['board'])
    ncols = len(data['board'][0]) if nrows > 0 else 0
    board = Board(nrows, ncols)
    board.fill_from_matrix(data['board'])
    return board

if __name__ == '__main__':
    print(get_quiz_blocks('../test/blocks.toml')[2])