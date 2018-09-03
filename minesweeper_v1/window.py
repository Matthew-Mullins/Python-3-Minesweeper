from tkinter import *
import time
import random

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self._num_rows = StringVar()
        self._num_cols = StringVar()
        self._num_mine = StringVar()
        self._paused = False
        self._game_started = False

    def init_window(self):
        self.pack(fill=BOTH, expand=1)

        #Add Start Button
        start_button = Button(self, text="Start", command=self.StartGame).grid(row=0, column=1, columnspan=2, sticky=N+E+S+W)

        #Add Pause Button
        self._pause_button_text = StringVar()
        pause_button = Button(self, textvariable=self._pause_button_text, command=self.PauseGame).grid(row=0, column=7, columnspan=2, sticky=N+E+S+W)
        self._pause_button_text.set("Pause")

        #Add Menu System
        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu, tearoff=0)
        file.add_command(label='New Game...', command=self.NewGameSettings)
        file.add_command(label='Exit', command=self.master.quit)

        menu.add_cascade(label='File', menu=file)

        #Start a New Game
        self.NewGame()
        """
        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu)
        file.add_command(label='Exit', command=self.client_exit)

        edit = Menu(menu)
        edit.add_command(label='Show Image', command=self.show_image)
        edit.add_command(label='Show Text', command=self.show_text)

        menu.add_cascade(label='File', menu=file)
        menu.add_cascade(label='Edit', menu=edit)
        """

    def StartGame(self):
        if not self._game_started:
            self._game_started = True
            self._game_time = 0.0
            #Start Update Loop
            self.Update()

    def PauseGame(self):
        if self._paused:
            self._paused = False
            self._pause_button_text.set("Pause")
        else:
            self._paused = True
            self._pause_button_text.set("Resume")

    def NewGameSettings(self):
        pass

    def NewGame(self, num_rows=10, num_cols=10, num_mine=10):
        #Size Window
        self.master.geometry("%sx%s" % (num_cols * 30, (num_rows * 30) + 26))

        #MineLocations
        mine_locations = []
        #Create 2D Array of Tiles
        while len(mine_locations) < num_mine:
            rand = random.randint(0, num_rows*num_cols)
            if rand not in mine_locations:
                mine_locations.append(rand)
        print(mine_locations)

        #Tiles
        self._tiles = []
        for x in range(0, num_cols):
            self._tiles.append([0] * num_rows)
        for x in range(0, len(mine_locations)):
            row = int(mine_locations[x] / 10)
            col = mine_locations[x] % 10
            self._tiles[row][col] = -1
            for j in range(-1, 2):
                for i in range(-1, 2):
                    new_row = row + j
                    new_col = col + i
                    if (new_row >= 0 and new_row < num_rows) and (new_col >= 0 and new_col < num_cols):
                        if (i != 0 or j != 0):
                            self._tiles[new_row][new_col] += 1

        print(self._tiles)

        #Create Timer Label
        self._timer_text = StringVar()
        timer_label = Label(self, textvariable=self._timer_text, background="black", foreground="red").grid(row=0, column=4, sticky=N+E+S+W, columnspan=2)
        self._timer_text.set("%s" % (0.00))

        #Create Grid of Buttons
        for y in range(1, num_rows + 1):
            for x in range(0, num_cols):
                b = Button(self, relief="ridge", padx=1, pady=1, command=lambda r=y-1, c=x: self.CheckTile(r, c)).grid(row=y, column=x, sticky=N+E+S+W)
                self.grid_columnconfigure(x, minsize=30)
                self.grid_rowconfigure(y, minsize=30)

    def CheckTile(self, row, col):
        print(self._tiles[row][col])

    def Update(self):
        if self._game_started:
            if not self._paused:
                self._game_time += 0.01
                self._timer_text.set("%s" % format(self._game_time, '.2f'))
            self.master.after(10, self.Update)
