from window import *

WINDOW_TITLE = "Minesweeper"

def main():
    Initialize()

def Initialize():
    root = Tk()
    root.title(str(WINDOW_TITLE))
    root.resizable(0, 0)
    main_window = Window(root)
    root.mainloop()

if __name__ == "__main__":
    main()
