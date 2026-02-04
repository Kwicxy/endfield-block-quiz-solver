from entities import Block
import format_utils as fu
import visualisation as vis

QUIZ_FILE_PATH = '../resources/quiz.toml'


class QuizSolver:
    def __init__(self):
        self.limits = fu.get_quiz_limits(QUIZ_FILE_PATH)
        self.board = fu.get_quiz_board(QUIZ_FILE_PATH)
        self.blocks = fu.get_quiz_blocks(QUIZ_FILE_PATH)
        self.fixed_cells_map = fu.get_fixed_cells_map(QUIZ_FILE_PATH)

        # Pre-calculate data structures for efficient checking
        self.block_type_map = {block.index: block.type for block in self.blocks}
        self.row_cnt = [[0] * self.board.nrows for _ in range(len(self.limits))]
        self.col_cnt = [[0] * self.board.ncols for _ in range(len(self.limits))]
        self._init_fixed_cnt()

        # Pre-calculate block complexities for heuristic ordering
        self.block_complexity = self._calc_block_complexity()

    def _init_fixed_cnt(self) -> None:
        """Initialize row and column counts based on fixed cells"""
        for (row, col), block_type in self.fixed_cells_map.items():
            self.row_cnt[block_type][row] += 1
            self.col_cnt[block_type][col] += 1

    def _calc_block_complexity(self) -> list[int]:
        """Calculate complexity of each block based on occupied cells (used for heuristic ordering)"""
        complexity = []
        for block in self.blocks:
            cell_cnt = sum(sum(row) for row in block.shape)
            complexity.append(cell_cnt)
        return complexity

    def can_place(self, block: Block, row: int, col: int) -> bool:
        """Check if a block can be placed at the specified position"""
        # Boundary check
        if row + len(block.shape) > self.board.nrows or col + len(block.shape[0]) > self.board.ncols:
            return False

        # Counts of affected rows and cols
        row_add = [0] * self.board.nrows
        col_add = [0] * self.board.ncols

        # Overlap check
        for (i, shape_row) in enumerate(block.shape):
            for (j, cell) in enumerate(shape_row):
                if cell == 1:
                    if self.board.values[row + i][col + j] != 0:
                        return False
                    # Count affected rows and cols
                    row_add[row + i] += 1
                    col_add[col + j] += 1

        # Check if placing the block would exceed limits
        block_type = block.type
        if block_type in self.limits:
            limits = self.limits[block_type]

            # Check row limits
            for r in range(self.board.nrows):
                if row_add[r] > 0 and self.row_cnt[block_type][r] + row_add[r] > limits[1][r]:
                    return False

            # Check column limits
            for c in range(self.board.ncols):
                if col_add[c] > 0 and self.col_cnt[block_type][c] + col_add[c] > limits[0][c]:
                    return False

        return True

    def update_cnt(self, block: Block, row: int, col: int, delta: int) -> None:
        """Update row and column counts when placing/removing a block
        Args:
            block: Block that is being placed/removed
            row: Destination row
            col: Destination column
            delta: `1` for placing, `-1` for removing
        """
        block_type = block.type
        for (i, shape_row) in enumerate(block.shape):
            for (j, cell) in enumerate(shape_row):
                if cell == 1:
                    self.row_cnt[block_type][row + i] += delta
                    self.col_cnt[block_type][col + j] += delta

    def check_limits(self) -> int:
        """
        Check if current board state meets the limits
        Returns:
            `-1` if limits are exceeded,
            `1` if limits are not yet reached,
            `0` if limits are exactly met
        """
        for block_type, limits in self.limits.items():
            # Check row limits
            for i in range(self.board.nrows):
                if self.row_cnt[block_type][i] > limits[1][i]:
                    return -1
                elif self.row_cnt[block_type][i] < limits[1][i]:
                    return 1

            # Check column limits
            for j in range(self.board.ncols):
                if self.col_cnt[block_type][j] > limits[0][j]:
                    return -1
                elif self.col_cnt[block_type][j] < limits[0][j]:
                    return 1

        return 0

    def display(self) -> None:
        """Print the current board state along with limits"""
        for block_type in sorted(self.limits.keys()):
            limits = self.limits[block_type]
            print(f"Type {block_type} Limits:")
            print('  ' + ' '.join([str(i) for i in limits[0]]))
            for (i, row) in enumerate(self.board.values):
                print(str(limits[1][i]) + ' ' + ' '.join([str(cell) if cell >= 0 else 'X' for cell in row]))
            print()

    def backtrack(self, used: list[bool], rotations: list[int]) -> bool:
        """
        Optimized backtracking solver with heuristic ordering and incremental checks.
        Args:
            used: Boolean array indicating whether each block has been used
            rotations: Array to store the rotation state of each block
        Returns:
            True if a solution is found, False otherwise
        """
        # Incremental limit check
        limit_state = self.check_limits()
        if limit_state == -1:
            return False
        elif limit_state == 0:
            return True

        # Prioritize blocks based on complexity (number of occupied cells)
        block_indices = [i for i in range(len(self.blocks)) if not used[i]]
        if not block_indices:
            return limit_state == 0

        block_indices.sort(key=lambda i: self.block_complexity[i], reverse=True)

        # Pick the most complex unused block
        block_idx = block_indices[0]
        block = self.blocks[block_idx]

        # Try all 4 rotations
        for rotation in range(4):
            # Find all valid positions for the current rotation
            valid_positions = []
            for row in range(self.board.nrows):
                for col in range(self.board.ncols):
                    if self.can_place(block, row, col):
                        valid_positions.append((row, col))

            # Continue to next rotation if no valid positions
            if not valid_positions:
                block.rotate()
                continue

            # Try placing the block in all valid positions
            for row, col in valid_positions:
                # Try placing the block
                self.board.place_block(block, row, col)
                self.update_cnt(block, row, col, 1)
                used[block_idx] = True

                # Try to solve recursively
                if self.backtrack(used, rotations):
                    rotations[block_idx] = rotation
                    return True

                # Backtrack: remove the block
                self.board.remove_block(block, row, col)
                self.update_cnt(block, row, col, -1)
                used[block_idx] = False

            # Try next rotation
            block.rotate()

        return False

    def solve(self):
        print("Initial Board:")
        self.display()
        print()

        used = [False] * len(self.blocks)
        rotations = [0] * len(self.blocks)

        if self.backtrack(used, rotations):
            print(f"\nSolution Found!")

            self.display()
            print()
            print("Block Placements:")
            for idx, rotation in enumerate(rotations):
                if used[idx]:
                    print(f"Block {self.blocks[idx].index}: Rotated {rotation * 90} degrees")

            vis.visualize_solution(self.board, self.blocks, self.limits, self.fixed_cells_map)

            return True
        else:
            print(f"\nNo solution found.")
            return False


if __name__ == '__main__':
    solver = QuizSolver()
    solver.solve()
