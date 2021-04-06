
from game2048.textual_2048 import game_play

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("textual", nargs='?', default=0)
    args = parser.parse_args()
    print(args.textual)
    if args.textual!=0:
        game_play()
    else:
        import game2048.interface
        root = Tk()
        root.geometry("400x500")
        root.bind_all('<Key>', main)
        app = window_2048(root)
        root.mainloop()


    exit(1)

