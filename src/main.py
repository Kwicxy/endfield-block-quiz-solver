from entities import Block, Board
import format_utils as fu
import visualisation as vis
from matplotlib import pyplot as plt


class QuizSolver:
    def __init__(self):
        self.limits = fu.get_quiz_limits('../resources/quiz.toml')
        self.board = fu.get_quiz_board('../resources/quiz.toml')
        self.blocks = fu.get_quiz_blocks('../resources/quiz.toml')
        self.fixed_cells_map = fu.get_fixed_cells_map('../resources/quiz.toml')

    def can_place(self, block: Block, row: int, col: int) -> bool:
        """ Check if a block can be placed on the board at the specified position """
        # Check boundaries
        if row + len(block.shape) > self.board.nrows or col + len(block.shape[0]) > self.board.ncols:
            return False

        # Check for overlaps
        for (i, shape_row) in enumerate(block.shape):
            for (j, cell) in enumerate(shape_row):
                if cell == 1 and self.board.values[row + i][col + j] != 0:
                    return False

        return True

    def check_limits(self) -> int:
        """
        Check if the current board state respects the row and column limits for each block type
        Fixed cells (represented by negative values < -1) are counted towards their type's limits
        Returns:
            `-1` if limits are exceeded,
            `1` if limits are not yet reached,
            `0` if limits are exactly met
        """
        # Build a mapping of block index to block type
        block_type_map = {block.index: block.type for block in self.blocks}

        # Check limits for each type
        for block_type, limits in self.limits.items():
            # Check row limits (limits[1])
            for i in range(self.board.nrows):
                filled_cells = 0
                for j in range(self.board.ncols):
                    cell_val = self.board.values[i][j]
                    # Count fixed cells of this type (negative values)
                    if (i, j) in self.fixed_cells_map and self.fixed_cells_map[(i, j)] == block_type:
                        filled_cells += 1
                    # Count placed blocks of this type (positive values)
                    elif cell_val > 0 and block_type_map.get(cell_val) == block_type:
                        filled_cells += 1

                if filled_cells > limits[1][i]:
                    return -1
                elif filled_cells < limits[1][i]:
                    return 1

            # Check column limits (limits[0])
            for j in range(self.board.ncols):
                filled_cells = 0
                for i in range(self.board.nrows):
                    cell_val = self.board.values[i][j]
                    # Count fixed cells of this type
                    if (i, j) in self.fixed_cells_map and self.fixed_cells_map[(i, j)] == block_type:
                        filled_cells += 1
                    # Count placed blocks of this type
                    elif cell_val > 0 and block_type_map.get(cell_val) == block_type:
                        filled_cells += 1

                if filled_cells > limits[0][j]:
                    return -1
                elif filled_cells < limits[0][j]:
                    return 1

        return 0

    def display(self):
        """Display the board with limits for each type"""
        # Display limits for each type
        for block_type in sorted(self.limits.keys()):
            limits = self.limits[block_type]
            print(f"Type {block_type} Limits:")
            print('  ' + ' '.join([str(i) for i in limits[0]]))
            for (i, row) in enumerate(self.board.values):
                print(str(limits[1][i]) + ' ' + ' '.join([str(cell) if cell >= 0 else 'X' for cell in row]))
            print()

    def backtrack(self, used: list[bool], rotations: list[int]) -> bool:
        """
        Backtracking algorithm to solve the puzzle
        Args:
            used: Boolean array tracking which blocks have been placed
            rotations: Array tracking rotation state of each block
        Returns:
            True if a solution is found, False otherwise
        """
        # Check current state
        limit_state = self.check_limits()
        if limit_state == -1:
            # Limits exceeded, this path is invalid
            return False
        elif limit_state == 0:
            # All limits satisfied, puzzle solved!
            return True

        # Try placing each unused block
        for block_idx in range(len(self.blocks)):
            if used[block_idx]:
                continue

            block = self.blocks[block_idx]

            # Try all 4 rotations
            for rotation in range(4):
                # Try all positions on the board
                for row in range(self.board.nrows):
                    for col in range(self.board.ncols):
                        if self.can_place(block, row, col):
                            # Place the block
                            self.board.place_block(block, row, col)
                            used[block_idx] = True

                            # Recursively try to solve
                            if self.backtrack(used, rotations):
                                rotations[block_idx] = rotation
                                return True

                            # Backtrack: remove the block
                            self.board.remove_block(block, row, col)
                            used[block_idx] = False

                # Rotate for next iteration
                block.rotate()

            # Restore original rotation after trying all 4 rotations
            # (We've rotated 4 times, so it's back to original)

        return False

    def solve(self):
        """Solve the puzzle using backtracking algorithm"""
        print("Initial Board:")
        self.display()
        print()

        used = [False] * len(self.blocks)
        rotations = [0] * len(self.blocks)

        if self.backtrack(used, rotations):
            print("Solution Found!")
            self.display()
            print()
            print("Block Placements:")
            for idx, rotation in enumerate(rotations):
                if used[idx]:
                    print(f"Block {self.blocks[idx].index}: Rotated {rotation * 90} degrees")

            # Visualize the solution
            vis.visualize_solution(self.board, self.blocks, self.limits, self.fixed_cells_map)
            plt.show()

            return True
        else:
            print("No solution found.")
            return False


if __name__ == '__main__':
    solver = QuizSolver()
    solver.solve()
