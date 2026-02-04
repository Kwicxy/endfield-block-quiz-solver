from matplotlib import pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from entities import Board, Block

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 200

def visualize_solution(board: Board, blocks: list[Block], limits: dict[int, list[list[int]]]):
    """
    Visualize the puzzle solution using matplotlib

    Args:
        board: The solved board
        blocks: List of blocks used in the puzzle
        limits: Dictionary mapping block type to [col_limits, row_limits]
    """
    # Build mapping from block index to block type
    block_type_map = {block.index: block.type for block in blocks}

    # Create color matrix based on block types
    nrows, ncols = board.nrows, board.ncols
    color_matrix = np.zeros((nrows, ncols))

    for i in range(nrows):
        for j in range(ncols):
            cell_val = board.values[i][j]
            if cell_val == -1:
                color_matrix[i][j] = -1  # Disabled cell
            elif cell_val == 0:
                color_matrix[i][j] = 0  # Empty cell
            else:
                # Color based on block type (offset by 1 to distinguish from empty)
                block_type = block_type_map.get(cell_val, 0)
                color_matrix[i][j] = block_type + 1

    # Create color map: disabled=-1(gray), empty=0(white), type0=1(light blue), type1=2(light red), etc.
    colors = ['#808080', '#FFFFFF', '#90EE90', '#ADD8E6', '#FFB6C1', '#FFD700', '#FFA07A']
    max_color_idx = int(np.max(color_matrix))
    cmap = ListedColormap(colors[:max_color_idx + 2])

    # Create figure
    fig, ax = plt.subplots(figsize=(5, 4))

    # Display the color matrix
    # Set vmin to -1 and vmax to max_color_idx to properly map colors
    im = ax.imshow(color_matrix, cmap=cmap, vmin=-1, vmax=max_color_idx, aspect='equal')

    # Add selective grid lines (only between different blocks)
    # Draw horizontal lines
    for i in range(nrows + 1):
        for j in range(ncols):
            # Check if we need a horizontal line between (i-1, j) and (i, j)
            if i == 0 or i == nrows:
                # Border lines
                ax.plot([j - 0.5, j + 0.5], [i - 0.5, i - 0.5], 'k-', linewidth=2)
            else:
                # Internal lines: draw if cells have different block indices
                upper_cell = board.values[i - 1][j]
                lower_cell = board.values[i][j]
                if upper_cell != lower_cell:
                    ax.plot([j - 0.5, j + 0.5], [i - 0.5, i - 0.5], 'k-', linewidth=2)

    # Draw vertical lines
    for i in range(nrows):
        for j in range(ncols + 1):
            # Check if we need a vertical line between (i, j-1) and (i, j)
            if j == 0 or j == ncols:
                # Border lines
                ax.plot([j - 0.5, j - 0.5], [i - 0.5, i + 0.5], 'k-', linewidth=2)
            else:
                # Internal lines: draw if cells have different block indices
                left_cell = board.values[i][j - 1]
                right_cell = board.values[i][j]
                if left_cell != right_cell:
                    ax.plot([j - 0.5, j - 0.5], [i - 0.5, i + 0.5], 'k-', linewidth=2)

    # Add block index labels in each cell
    for i in range(nrows):
        for j in range(ncols):
            cell_val = board.values[i][j]
            if cell_val > 0:
                ax.text(j, i, str(cell_val), ha='center', va='center',
                       fontsize=14, fontweight='bold', color='black')
            elif cell_val == -1:
                ax.text(j, i, 'X', ha='center', va='center',
                       fontsize=12, color='white')

    # Set up axes labels with limits
    # Get all block types
    all_types = sorted(limits.keys())

    # Format column limits for x-axis
    col_labels = []
    for j in range(ncols):
        label_parts = []
        for block_type in all_types:
            col_limit = limits[block_type][0][j]
            if col_limit > 0:
                label_parts.append(f"{col_limit}")
        col_labels.append(' '.join(label_parts) if label_parts else '0')

    # Format row limits for y-axis
    row_labels = []
    for i in range(nrows):
        label_parts = []
        for block_type in all_types[::-1]:  # Reverse order for y-axis
            row_limit = limits[block_type][1][i]
            if row_limit > 0:
                label_parts.append(f"{row_limit}")
        row_labels.append('\n'.join(label_parts) if label_parts else '0')

    # Set tick positions and labels
    ax.set_xticks(np.arange(ncols))
    ax.set_yticks(np.arange(nrows))
    ax.set_xticklabels(col_labels, fontsize=12)
    ax.set_yticklabels(row_labels, fontsize=12)

    # Move x-axis labels to top
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')

    # Add title
    ax.set_title('Solution', fontsize=16, fontweight='bold')

    # Add legend
    legend_elements = []
    legend_labels = []
    for block_type in all_types:
        color_idx = block_type + 2
        if color_idx < len(colors):
            legend_elements.append(plt.Rectangle((0, 0), 1, 1, fc=colors[color_idx]))
            legend_labels.append(f'Type {block_type}')

    if legend_elements:
        ax.legend(legend_elements, legend_labels, loc='center left',
                 bbox_to_anchor=(1, 0.5), fontsize=10)

    plt.tight_layout()
    return fig


if __name__ == '__main__':
    import format_utils as fu

    # Load test data
    limits = fu.get_quiz_limits('../resources/quiz.toml')
    board = fu.get_quiz_board('../resources/quiz.toml')
    blocks = fu.get_quiz_blocks('../resources/quiz.toml')

    # For testing, place some blocks manually
    board.values = [
        [1, 1, 3, 3],
        [2, 2, 3, 4],
        [0, 0, -1, 4],
        [0, 0, 0, -1]
    ]

    visualize_solution(board, blocks, limits)
    plt.show()

