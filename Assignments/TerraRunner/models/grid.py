import math
import config

# Number of cells horizontally and vertically
num_cells_x = math.ceil((config.HARD_BOUND_RIGHT - config.HARD_BOUND_LEFT) / config.CELL_SIZE)
num_cells_y = math.ceil((config.HARD_BOUND_BOTTOM - config.HARD_BOUND_TOP) / config.CELL_SIZE)

def get_cell_index(x, y):
    """
    Given world coordinates (x, y), return the grid cell (i, j)
    that the point belongs to. If outside the grid, returns (-1, -1).
    """

    # Compute grid indices relative to hard-bound origin
    i = int((x - config.HARD_BOUND_LEFT) // config.CELL_SIZE)
    j = int((y - config.HARD_BOUND_TOP) // config.CELL_SIZE)

    # Clamp to out-of-bounds marker
    if not (0 <= i < num_cells_x):
        i = -1
    if not (0 <= j < num_cells_y):
        j = -1

    return i, j


def get_cell_top_left(i, j):
    """
    Given a grid cell (i, j), return the world-space top-left
    coordinate (x, y) of that cell.
    Useful for debugging or drawing in another module.
    """

    x = config.HARD_BOUND_LEFT + i * config.CELL_SIZE
    y = config.HARD_BOUND_TOP + j * config.CELL_SIZE
    return x, y


def get_cell_bounds(i, j):
    """
    Returns (x0, y0, x1, y1) for the bounding box of a cell.
    Also useful for debugging and optional rendering elsewhere.
    """

    x0 = config.HARD_BOUND_LEFT + i * config.CELL_SIZE
    y0 = config.HARD_BOUND_TOP + j * config.CELL_SIZE
    x1 = x0 + config.CELL_SIZE
    y1 = y0 + config.CELL_SIZE
    return x0, y0, x1, y1
