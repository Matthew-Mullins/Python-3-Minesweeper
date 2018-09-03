from minesweeper import *

def main():
    root = Tk()
    root.resizable(0, 0)
    minesweeper = Minesweeper(root)
    root.mainloop()

if __name__ == "__main__":
    main()
