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

    # Support new coordinate-based format
    if 'nrows' in data and 'ncols' in data:
        nrows = data['nrows']
        ncols = data['ncols']
        board = Board(nrows, ncols)

        # Mark invalid cells
        if 'invalid' in data:
            for coord in data['invalid']:
                row, col = coord
                board.values[row][col] = -1

        # Mark fixed cells for each type
        for key in data:
            if key.startswith('fixed_type'):
                type_num = int(key.replace('fixed_type', ''))
                for coord in data[key]:
                    row, col = coord
                    board.values[row][col] = -(type_num + 2)  # -2 for type0, -3 for type1, etc.

    # Support old matrix-based format
    elif 'board' in data:
        nrows = len(data['board'])
        ncols = len(data['board'][0]) if nrows > 0 else 0
        board = Board(nrows, ncols)
        board.fill_from_matrix(data['board'])
    else:
        raise ValueError("Invalid board format in config file")

    return board

def get_quiz_limits(file_path: str) -> dict[int, list[list[int]]]:
    """
    Get limits for each block type from quiz file.
    Returns a dict mapping type -> limits array
    """
    with open(file_path, 'rb') as file:
        data = tomllib.load(file)

    limits_dict = {}
    # Support old format with single 'limits' key
    if 'limits' in data:
        limits_dict[0] = data['limits']

    # Support new format with 'limits_type0', 'limits_type1', etc.
    for key in data:
        if key.startswith('limits_type'):
            type_num = int(key.replace('limits_type', ''))
            limits_dict[type_num] = data[key]

    return limits_dict

def get_quiz_blocks(file_path: str) -> list[Block]:
    with open(file_path, 'rb') as file:
        data = tomllib.load(file)
    blocks = []

    # New format: blocks array in quiz.toml
    if 'blocks' in data:
        for block_data in data['blocks']:
            blocks.append(Block(
                block_data['shape'],
                index=block_data['index'],
                type=block_data.get('type', 0)
            ))
    else:
        # Old format: separate candidates file with numbered sections
        for index in data:
            if isinstance(data[index], dict) and 'shape' in data[index]:
                blocks.append(Block(
                    data[index]['shape'],
                    index=int(index),
                    type=data[index].get('type', 0)
                ))

    return blocks


def get_fixed_cells_map(file_path: str) -> dict[tuple[int, int], int]:
    """
    Get a mapping of fixed cell coordinates to their types
    Returns: dict mapping (row, col) -> block_type
    """
    with open(file_path, 'rb') as file:
        data = tomllib.load(file)

    fixed_map = {}
    for key in data:
        if key.startswith('fixed_type'):
            type_num = int(key.replace('fixed_type', ''))
            for coord in data[key]:
                row, col = coord
                fixed_map[(row, col)] = type_num

    return fixed_map


if __name__ == '__main__':
    print(get_quiz_blocks('../test/blocks.toml')[2])