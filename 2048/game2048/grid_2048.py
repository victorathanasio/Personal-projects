import random
import copy


def create_grid(n=4):
    grid = []
    for i in range(n):
        grid.append([' ' for j in range(n)])
    return grid


def fix_create_grid(n=4):
    grid = []
    for i in range(n):
        grid.append([0 for j in range(n)])
    return grid


def get_value_new_tile():
    if random.random() < 0.9:
        return 2
    else:
        return 4


def grid_add_new_tile_at_position(game_grid, x, y):
    game_grid[y][x] = get_value_new_tile()
    return game_grid


def get_all_tiles(game_grid):
    tiles = []
    for row in game_grid:
        for tile in row:
            if tile == ' ':
                tiles.append(0)
            else:
                tiles.append(tile)
    return tiles


def grid_get_value(grid, x, y):
    if grid[x][y] == ' ':
        return 0
    return grid[x][y]


def get_empty_tiles_positions(game_grid):
    positions = []
    for i in range(len(game_grid)):
        for j in range(len(game_grid[i])):
            if game_grid[i][j] in {0, ' '}:
                positions.append((i, j))
    return positions


def get_new_position(grid):
    positions = get_empty_tiles_positions(grid)
    return random.choice(positions)


def grid_add_new_tile(grid):
    x, y = get_new_position(grid)
    grid[x][y] = get_value_new_tile()
    return grid


def init_game(n):
    grid = create_grid(n)
    grid = grid_add_new_tile(grid)
    return grid_add_new_tile(grid)


# FUNCTIONALITY 2 TABLE TO STRING N STUFF

def grid_to_string(grid, n=4):
    a = ""
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            a += " ==="
        a += '\n'
        for j in range(len(grid[i])):
            if grid_get_value(grid, i, j) == 0:
                a += "|" + "   ".format()
            else:
                a += "|" + "{:^3d}".format(grid_get_value(grid, i, j))
        a += '|\n'
    for j in range(len(grid[i])):
        a += " ==="
    return a


def long_value(grid):
    longest_size = 0
    for i in grid:
        for j in i:
            if type(j) == int:
                if len(str(j)) > longest_size:
                    longest_size = len(str(j))
            else:
                if len(j) > longest_size:
                    longest_size = len(j)
    return longest_size


def grid_to_string_with_size(grid, n=4):
    size = long_value(grid)
    a = ""
    up_border = " " + "=" * (size + 2)
    formatting_num = "{:^" + str(size + 2) + "d}"
    empty = " " * (size + 2)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            a += up_border
        a += '\n'
        for j in range(len(grid[i])):
            if grid_get_value(grid, i, j) == 0:
                a += "|" + empty
            else:
                a += "|" + formatting_num.format(grid_get_value(grid, i, j))
        a += '|\n'
    for j in range(len(grid[i])):
        a += up_border
    return a


def long_value_with_theme(grid, THEME):
    longest_size = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            val = grid_get_value(grid, i, j)
            if (len(THEME[val]) > longest_size):
                longest_size = len(THEME[val])
    return longest_size


def grid_to_string_with_size(grid, n=4):
    size = long_value(grid)
    a = ""
    up_border = " " + "=" * (size + 2)
    formatting_num = "{:^" + str(size + 2) + "d}"
    empty = " " * (size + 2)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            a += up_border
        a += '\n'
        for j in range(len(grid[i])):
            if grid_get_value(grid, i, j) == 0:
                a += "|" + empty
            else:
                a += "|" + formatting_num.format(grid_get_value(grid, i, j))
        a += '|\n'
    for j in range(len(grid[i])):
        a += up_border
    return a


def grid_to_string_with_size_and_theme(grid, THEME, n=4):
    size = long_value_with_theme(grid, THEME)
    a = ""
    up_border = " " + "=" * (size + 2)
    formatting_num = "{:^" + str(size + 2) + "}"
    empty = " " * (size + 2)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            a += up_border
        a += '\n'
        for j in range(len(grid[i])):
            if grid_get_value(grid, i, j) == 0:
                a += "|" + empty
            else:
                a += "|" + \
                     formatting_num.format(THEME[grid_get_value(grid, i, j)])
        a += '|\n'
    for j in range(len(grid[i])):
        a += up_border
    return a


def move_row_left(row):
    n = len(row)
    # moving left
    for i in range(n):
        j = i
        while not j - 1 < 0:
            if row[j - 1] == 0:
                row[j - 1] = row[j]
                row[j] = 0
            j -= 1

    # merging
    for i in range(n - 1):
        if row[i] == row[i + 1]:
            row[i] = 2 * row[i]
            row[i + 1] = 0

    # moving left
    for i in range(n):
        j = i
        while not j - 1 < 0:
            if row[j - 1] == 0:
                row[j - 1] = row[j]
                row[j] = 0
            j -= 1
    return row


def move_row_right(row):
    n = len(row)
    # moving right
    for i in range(n):
        j = n - 1 - i
        while j + 1 < n:
            if row[j + 1] == 0:
                row[j + 1] = row[j]
                row[j] = 0
            j += 1
    # merging
    for i in range(n - 1):
        j = n - 1 - i
        if row[j] == row[j - 1]:
            row[j] = 2 * row[j]
            row[j - 1] = 0

    # moving right
    for i in range(n):
        j = n - 1 - i
        while j + 1 < n:
            if row[j + 1] == 0:
                row[j + 1] = row[j]
                row[j] = 0
            j += 1
    return row


def move_grid(grid, d):
    if d == 'left':
        for row in grid:
            row = move_row_left(row)

    elif d == 'right':
        for row in grid:
            row = move_row_right(row)

    elif d == 'up':
        for i in range(len(grid)):
            column = []
            for row in grid:
                column.append(row[i])
            column = move_row_left(column)
            for j in range(len(grid)):
                grid[j][i] = column[j]

    elif d == 'down':
        for i in range(len(grid)):
            column = []
            for row in grid:
                column.append(row[i])
            column = move_row_right(column)
            for j in range(len(grid)):
                grid[j][i] = column[j]

    return grid


def is_grid_full(grid):
    full = True
    for row in grid:
        for element in row:
            if element == 0:
                full = False
    return full


def move_possible(grid):
    move_direction = []
    direction = ['left', 'right', 'up', 'down']
    for d in direction:
        grid_d = copy.deepcopy(grid)
        grid_new = move_grid(grid_d, d)
        move_direction.append(compare_grid(grid, grid_new))

    return move_direction


def compare_grid(grid_old, grid_new):
    n = len(grid_old)
    diff = False
    for i in range(n):
        for j in range(n):
            if grid_old[i][j] != grid_new[i][j]:
                diff = True
    return diff


def is_game_over(grid):
    over = True
    moves = move_possible(grid)
    for element in moves:
        if element:
            over = False
    return over


def get_grid_tile_max(grid):
    maximum = 0
    for row in grid:
        for tile in row:
            if tile > maximum:
                maximum = tile
    return maximum


def is_gagnant(grid):
    if get_grid_tile_max(grid) >= 2048:
        return True
    else:
        return False
