try:
    from grid_2048 import *
except:
    from game2048.grid_2048 import *

def read_player_command():
    valid_input = False
    while (not valid_input):
        move = input(
            "Entrez votre commande (a (gauche), d (droite), w (haut), s (bas)):")
        if move not in ['w', 'a', 's', 'd']:
            print("Commande non valide!")
        else:
            valid_input = True
    return move


def read_size_grid():
    def is_number(s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    valid_input = False
    while (not valid_input):
        move = input("Entrez la taille de la grille (minimum 3):")
        if not is_number(move) or int(move) < 3:
            print("Commande non valide!")
        else:
            valid_input = True
    return int(move)


def read_theme_grid():
    valid_input = False
    while (not valid_input):
        move = input(
            "Entrez le thème (0 (Default), 1 (Chemistry), 2 (Alphabet):")
        if move not in {'0', '1', '2'}:
            print("Commande non valide!")
        else:
            valid_input = True
    return move


def random_play(size=4, theme_chosen='1'):
    THEMES = {
        "0": {"name": "Default", 0: " ", 2: "2", 4: "4", 8: "8", 16: "16", 32: "32", 64: "64", 128: "128", 256: "256",
              512: "512", 1024: "1024", 2048: "2048", 4096: "4096", 8192: "8192", 16384: "16384", 32768: "32768",
              65536: "65536", 131072: "131072", 262144: "262144", 524288: "524288", 1048576: "1048576",
              2097152: "2097152"},
        "1": {"name": "Chemistry", 0: "", 2: "H", 4: "He", 8: "Li", 16: "Be", 32: "B", 64: "C", 128: "N", 256: "O",
              512: "F", 1024: "Ne", 2048: "Na", 4096: "Mg", 8192: "Al"},
        "2": {"name": "Alphabet", 0: "", 2: "A", 4: "B", 8: "C", 16: "D", 32: "E", 64: "F", 128: "G", 256: "H",
              512: "I", 1024: "J", 2048: "K", 4096: "L", 8192: "M"}}
    theme = THEMES[theme_chosen]
    grid = fix_create_grid(n=size)
    grid_add_new_tile(grid)
    iter = 1
    while not (is_game_over(grid)):
        possible_moves = move_possible(grid)
        choice_to_move = {"left": 0, "right": 1, "up": 2, "down": 3}

        command = random.choice(["left", "right", "up", "down"])
        while (possible_moves[choice_to_move[command]]) == False:
            command = random.choice(["left", "right", "up", "down"])

        move_grid(grid, command)
        grid_add_new_tile(grid)
        if (iter == 1):
            print(command)
            print(grid_to_string_with_size_and_theme(grid, theme))
            iter = 0
        iter += 1
    print(grid_to_string_with_size_and_theme(grid, theme))


def game_play(theme=False, size=False):
    THEMES = {
        "0": {"name": "Default", 0: " ", 2: "2", 4: "4", 8: "8", 16: "16", 32: "32", 64: "64", 128: "128", 256: "256",
              512: "512", 1024: "1024", 2048: "2048", 4096: "4096", 8192: "8192", 16384: "16384", 32768: "32768",
              65536: "65536", 131072: "131072", 262144: "262144", 524288: "524288", 1048576: "1048576",
              2097152: "2097152"},
        "1": {"name": "Chemistry", 0: "", 2: "H", 4: "He", 8: "Li", 16: "Be", 32: "B", 64: "C", 128: "N", 256: "O",
              512: "F", 1024: "Ne", 2048: "Na", 4096: "Mg", 8192: "Al"},
        "2": {"name": "Alphabet", 0: "", 2: "A", 4: "B", 8: "C", 16: "D", 32: "E", 64: "F", 128: "G", 256: "H",
              512: "I", 1024: "J", 2048: "K", 4096: "L", 8192: "M"}}
    if not theme:
        theme = THEMES[read_theme_grid()]
    else:
        theme = THEMES[theme]
    if not size:
        grid = fix_create_grid(read_size_grid())
    else:
        grid = fix_create_grid(int(size))
    grid_add_new_tile(grid)
    grid_add_new_tile(grid)
    print(grid_to_string_with_size_and_theme(grid, theme))
    while not (is_game_over(grid)):
        possible_moves = move_possible(grid)
        choice_to_move = {"a": 0, "d": 1, "w": 2, "s": 3}
        move_to_written = {"a": "left", "d": "right", "w": "up", "s": "down"}

        command = read_player_command()
        while not (possible_moves[choice_to_move[command]]):
            command = read_player_command()

        move_grid(grid, move_to_written[command])
        grid_add_new_tile(grid)
        print(grid_to_string_with_size_and_theme(grid, theme))
        if get_grid_tile_max(grid) == 2048:
            print("YOU WIN!!!!!!!!!!!!!")
            return
    print("YOU LOST")


def game_step(grid, move):
    if not not (is_game_over(grid)):
        possible_moves = move_possible(grid)
        choice_to_move = {"a": 0, "d": 1, "w": 2, "s": 3}
        move_to_written = {"a": "left", "d": "right", "w": "up", "s": "down"}
        if possible_moves[choice_to_move[move]]:
            move_grid(grid, move_to_written[move])
            grid_add_new_tile(grid)
            if get_grid_tile_max(grid) == 2048:
                print("YOU WIN!!!!!!!!!!!!!")
    else:
        print('You lost!')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("theme", nargs='?', default=False)
    parser.add_argument("size", nargs='?', default=False)
    args = parser.parse_args()
    game_play(args.theme, args.size)
    exit(1)
