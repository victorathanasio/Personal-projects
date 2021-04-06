from tkinter import *
import random
from sympy import *
import numpy as np
import random
import copy
import pandas as pd
import numba as nb

pieces = [2] * 9 + [4]

THEMES = {"0": {"name": "Default", 0: "", 2: "2", 4: "4", 8: "8", 16: "16", 32: "32", 64: "64", 128: "128", 256: "256",
                512: "512", 1024: "1024", 2048: "2048", 4096: "4096", 8192: "8192"},
          "1": {"name": "Chemistry", 0: "", 2: "H", 4: "He", 8: "Li", 16: "Be", 32: "B", 64: "C", 128: "N", 256: "O",
                512: "F", 1024: "Ne", 2048: "Na", 4096: "Mg", 8192: "Al"},
          "2": {"name": "Alphabet", 0: "", 2: "A", 4: "B", 8: "C", 16: "D", 32: "E", 64: "F", 128: "G", 256: "H",
                512: "I", 1024: "J", 2048: "K", 4096: "L", 8192: "M"}}

colors_dict = {0: '#aea59b', 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
               16: "#f59563", 32: "#f67c60", 64: "#f65e3b", 128: "#edcf73",
               256: "#edcc62", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22d",
               4096: "#939c9f", 8192: "#898dc4"}

dir_ar = {
    'Down': (0, 1),
    'Left': (1, 0),
    'Up': (0, 0),
    'Right': (1, 1)
}


def move_matrix(M, dir):
    global dir_ar
    axis = dir_ar[dir][0]
    r = dir_ar[dir][1]
    for i in range(M.shape[0]):
        if axis:
            M[i:i + 1, :] = reorder_vec(M[i:i + 1, :], r).reshape(M[i:i + 1, :].shape)
        else:
            M[:, i:i + 1] = reorder_vec(M[:, i:i + 1], r)
    return M


def reorder_vec(vec, r):
    vec = np.array(vec)
    if r:
        vec = np.flip(vec)
    size = max(vec.shape)
    vec = vec[vec != 0]
    for i in range(vec.shape[0] - 1):
        if vec[i] == vec[i + 1]:
            vec[i] = vec[i] * 2
            vec[i + 1] = 0
    vec = vec[vec != 0]
    result = np.zeros(size, np.int64)
    result[:vec.shape[0]] = vec
    vec = result
    if r:
        vec = np.flip(vec)
    return vec


def add_random_piece(M):
    M = np.array(M)
    size = M.shape[0]
    emp_spaces = size * size - np.count_nonzero(M) - 1
    pos = random.randint(0, emp_spaces)
    c = 0
    for i in range(size):
        for j in range(size):
            if M[i, j] == 0:
                if c == pos:
                    M[i, j] = random.choice(pieces)
                    return Matrix(M)
                c += 1


def check_move(M, dir):
    M_m = copy.deepcopy(M)
    M_m = move_matrix(M_m, dir)
    if np.sum(np.abs(M_m - M)) != 0:
        return True


def check_loose(M):
    for move in dir_ar:
        M_m = move_matrix(copy.deepcopy(M), move)
        if np.sum(np.abs(M_m - M)) != 0:
            return True

def Board():
    newWindow = Toplevel(app)
    grid = Frame(newWindow, bg='gray')
    grid.pack(fill=BOTH, expand=1)
    # for x in range(6):
    #     Grid.columnconfigure(grid, x, weight=1)
    # for y in range(6):
    #     Grid.rowconfigure(grid, y, weight=1)
    scores = pd.read_csv('scoreboard.csv')
    for i in range(scores.shape[0]):
        cell = Label(grid, text='{}:{}'.format(scores.loc[i]['Player'], scores.loc[i]['Score']), font=("Courier", 25),
                     height=2, bg=colors_dict[2 ** (6 - i)])
        cell.pack(fill=BOTH)


def enresgistrer_score(sco):
    newWindow = Toplevel(app)
    grid = Frame(newWindow, bg='gray')
    grid.pack(fill=BOTH, expand=1)

    cell = Label(grid, text='Your score is {}!'.format(sco), font=("Courier", 25), height=2, bg='snow2', relief=RAISED)
    cell.pack(fill=BOTH)

    fra = Frame(grid)
    L1 = Label(fra, text="Your name:", font=("Courier", 25))
    L1.pack(side=LEFT)
    E1 = Entry(fra, bd=5, font=("Courier", 20), justify=LEFT)
    E1.pack(side=RIGHT)
    fra.pack(fill=BOTH)

    btn = Button(grid, text='Save', font=("Courier", 25), bd=5, bg="#eee4da",
                 command=lambda: save_score(E1.get(), sco, newWindow))
    btn.pack(fill=BOTH)


def save_score(player, sco, win):
    if player != '':
        scores = pd.read_csv('scoreboard.csv')
        data = pd.DataFrame({'Player': [player],
                             'Score': [sco]
                             })
        scores = pd.concat([scores, data], axis=0)

        scores.sort_values('Score', inplace=True, ascending=False)
        scores = scores.head()
        scores = scores.reset_index(drop=True)
        scores.to_csv('scoreboard.csv')
        win.destroy()
        Board()

class window_2048(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.THEME = str(0)

        self.g_size = 4

        n = self.g_size
        M = Matrix.zeros(n, n)
        M = add_random_piece(M)
        self.Matrix = M
        self.score = np.sum(self.Matrix)

        self.create_string_vars()
        self.show_score()
        self.up_string_vars()

        self.create_grid_()
        self.anciennes = []

    def init_window(self):
        self.master.title('2048')
        self.pack(fill=BOTH, expand=1)

        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu)
        file.add_command(label="Exit", command=self.client_exit)
        file.add_command(label="Reset", command=self.Reset_game)
        file.add_command(label="Undo", command=self.Undo)
        file.add_command(label="Scoreboard", command=Board)
        file.add_command(label="Save score", command=lambda: enresgistrer_score(self.score))
        menu.add_cascade(label="File", menu=file)

        grid_siz = Menu(menu)
        grid_siz.add_command(label="4", command=lambda: self.resize(4))
        grid_siz.add_command(label="5", command=lambda: self.resize(5))
        grid_siz.add_command(label="6", command=lambda: self.resize(6))
        menu.add_cascade(label="Grid_size", menu=grid_siz)

        theme = Menu(menu)
        theme.add_command(label="Numbers", command=lambda: self.change_theme(0))
        theme.add_command(label="Letters", command=lambda: self.change_theme(2))
        theme.add_command(label="Atoms", command=lambda: self.change_theme(1))
        menu.add_cascade(label="Theme", menu=theme)

        self.bind_all("<Control-z>", self.Undo)

    def show_score(self):
        text = Label(self, textvariable=self.vars['score'])
        text.config(font=("Courier", 44))
        text.pack()
        self.score_ = text

    def client_exit(self):
        exit()

    def Reset_game(self):
        n = self.g_size
        M = Matrix.zeros(n, n)
        M = add_random_piece(M)
        self.Matrix = M
        self.score = np.sum(self.Matrix)
        self.create_string_vars()
        self.grid.destroy()
        self.create_grid_()
        self.up_string_vars()
        self.up_colors()

    def Undo(self, event=None):
        self.Matrix = self.anciennes[-1]
        # self.prochaines.append(self.anciennes[-1])
        self.anciennes = self.anciennes[:-1]
        self.up_string_vars()
        self.up_colors()


    def resize(self, n):
        ''''resizes the board'''
        self.g_size = n
        self.Reset_game()

    def change_theme(self, theme):
        ''''changes the theme'''
        self.THEME = str(theme)
        self.score = np.sum(self.Matrix)
        self.up_string_vars()

    def create_string_vars(self):
        self.vars = {}
        self.vars['score'] = StringVar()
        n = self.g_size
        for i in range(n):
            for j in range(n):
                self.vars['{}{}'.format(i, j)] = StringVar()

    def up_string_vars(self):
        self.score_.config(textvariable=self.vars['score'])
        self.score = np.sum(self.Matrix)
        self.vars['score'].set("Score: " + str(self.score))
        if type(self.score) == str:
            self.vars['score'].set('You lost!')

        n = self.g_size
        for i in range(n):
            for j in range(n):
                self.vars['{}{}'.format(i, j)].set(THEMES[self.THEME][self.Matrix[i, j]])

    def create_grid_(self):
        grid = Frame(self.master, bg='gray')
        grid.pack(fill=BOTH, expand=1)
        self.grid = grid
        for x in range(6):
            Grid.columnconfigure(grid, x, weight=1)
        for y in range(6):
            Grid.rowconfigure(grid, y, weight=1)
        self.cells = {}
        n = self.g_size
        width = 400 // n
        height = 450 // n
        for i in range(n):
            for j in range(n):
                # text = '{}'.format(THEMES[self.THEME][choix])
                cell = Label(grid, textvariable=self.vars['{}{}'.format(i, j)], font=("Courier", 25), width=width,
                             height=height, relief=RAISED, bg=colors_dict[self.Matrix[i, j]])
                cell.grid(row=i, column=j, sticky=NSEW)
                self.cells['{}{}'.format(i, j)] = cell

    def up_colors(self):
        n = self.g_size
        for i in range(n):
            for j in range(n):
                self.cells['{}{}'.format(i, j)].config(bg=colors_dict[self.Matrix[i, j]])





def key(event):
    global app
    """shows key or tk code for the key"""
    if event.keysym == 'Escape':
        root.destroy()
    if event.char == event.keysym:
        pass
        # normal number and letter characters
        # print('Normal Key %r' % event.char)
    elif len(event.char) == 1:
        pass
        # charcters like []/.,><#$ also Return and ctrl/key
        # print('Punctuation Key %r (%r)' % (event.keysym, event.char))
    else:
        # f1 to f12, shift keys, caps lock, Home, End, Delete ...
        # print( 'Special Key %r' % event.keysym )
        dir = event.keysym
        keep = check_loose(app.Matrix)
        if not keep:
            app.vars['score'].set('You lost!')

        if check_move(app.Matrix, dir):
            if len(app.anciennes) < 10:
                app.anciennes.append(copy.deepcopy(app.Matrix))
            else:
                app.anciennes = app.anciennes[1:] + [app.Matrix]
            app.Matrix = move_matrix(app.Matrix, dir)
            app.Matrix = add_random_piece(app.Matrix)

            app.up_string_vars()
            app.up_colors()
            goal = 2 ** (len(pieces) - 2) * 100
            if app.score > goal:
                pieces.append(pieces[-1] * 2)





root = Tk()
root.geometry("400x500")
root.bind_all('<Key>', key)
app = window_2048(root)
root.mainloop()
