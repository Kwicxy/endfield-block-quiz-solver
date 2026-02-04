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

    nrows = data['nrows']
    ncols = data['ncols']
    board = Board(nrows, ncols)

    # Mark invalid cells
    if 'invalid' in data:
        for coord in data['invalid']:
            row, col = coord
            board.values[row][col] = -1

    return board


def get_quiz_limits(file_path: str) -> dict[int, list[list[int]]]:
    """
    Get limits for each block type from quiz file.
    Returns a dict mapping type -> [cols_limits, rows_limits]
    """
    with open(file_path, 'rb') as file:
        data = tomllib.load(file)

    limits_dict = {}
    if 'limits' in data:
        for limit_entry in data['limits']:
            block_type = limit_entry['type']
            limits_dict[block_type] = [limit_entry['cols'], limit_entry['rows']]

    return limits_dict


def get_quiz_blocks(file_path: str) -> list[Block]:
    with open(file_path, 'rb') as file:
        data = tomllib.load(file)

    blocks = []
    if 'blocks' in data:
        for block_data in data['blocks']:
            blocks.append(Block(
                block_data['shape'],
                index=block_data['index'],
                type=block_data.get('type', 0)
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
    if 'fixed' in data:
        for fixed_entry in data['fixed']:
            block_type = fixed_entry['type']
            coords = fixed_entry.get('coords', [])
            for coord in coords:
                row, col = coord
                fixed_map[(row, col)] = block_type

    return fixed_map


if __name__ == '__main__':
    print(get_quiz_blocks('../test/blocks.toml')[2])
