import format_utils as fu
import visualisation as vis
from matplotlib import pyplot as plt

# Load test data
limits = fu.get_quiz_limits('../resources/quiz.toml')
board = fu.get_quiz_board('../resources/quiz.toml')
blocks = fu.get_quiz_blocks('../resources/quiz.toml')

print("Loaded blocks:")
for block in blocks:
    print(f"Block {block.index}, Type {block.type}")

print("\nLimits:")
for block_type, limit in limits.items():
    print(f"Type {block_type}: {limit}")

# Create a test solution (manually placed blocks)
# Place block 1 (type 0) at position (0, 0)
board.values = [
    [1, 1, 3, 0],
    [1, 3, 3, 3],
    [1, 1, 3, 2],
    [2, 2, 2, 2]
]

print("\nBoard state:")
print(board)

# Visualize
vis.visualize_solution(board, blocks, limits)
plt.show()
