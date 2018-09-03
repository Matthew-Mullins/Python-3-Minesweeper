from tkinter import *

import random
import pprint

class Minesweeper(Frame):

    def __init__(self, parent=None, num_rows=10, num_cols=10, num_mine=10):
        #Frame Initialization
        Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=1)

        #Initialize Variables
        self._parent = parent
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._num_mine = num_mine

        #Run Initialization
        self._Init()

    def _Init(self):
        #Initialize Variables
        self._isStarted = False
        self._isPaused = False
        self._playTime = 0.00
        self._uncoveredTiles = 0
        self._buttons = []
        self._tiles = []
        self._colors = {
            -1: 'purple4',
            0: 'white',
            1: 'blue',
            2: 'green',
            3: 'red',
            4: 'navy',
            5: 'red4',
            6: 'cyan4',
            7: 'black',
            8: 'gray'
        }

        #Build Board
        self._BuildBoard()

        #Begin Update Loop
        self._Update()

        print("Game Has Been Initialized")

    def _Update(self):
        if self._isStarted and not self._isPaused:
            if self._uncoveredTiles == ((self._num_rows * self._num_cols) - self._num_mine):
                self._EndGame(True)
            elif self._uncoveredTiles == -1:
                self._EndGame(False)
            else:
                self._playTime += 0.01
                self._timerText.set(format(self._playTime, '.2f'))
                self._parent.after(10, self._Update)
        else:
            self._parent.after(10, self._Update)

    def _BuildBoard(self):
        #Generate Mine Locations
        num_tiles = (self._num_rows * self._num_cols)
        mine_tiles = []
        while len(mine_tiles) < self._num_mine:
            r = random.randint(0, num_tiles)
            if r not in mine_tiles:
                mine_tiles.append(r)
        print(mine_tiles)
        #Create Grid of Tiles
        #Default Tiles to 0
        for i in range(0, self._num_rows):
            self._tiles.append([0] * self._num_cols)
        #Add Mines to _tiles
        for i in mine_tiles:
            mine_row = int(i / self._num_rows)
            mine_col = int(i % self._num_cols)
            self._tiles[mine_row][mine_col] = -1
        #Increment Surrounding Mine Tiles
        for i in mine_tiles:
            mine_row = int(i / self._num_rows)
            mine_col = int(i % self._num_cols)
            for y in range(-1, 2):
                for x in range(-1, 2):
                    temp_mine_row = mine_row + y
                    temp_mine_col = mine_col + x
                    if (temp_mine_row >= 0 and temp_mine_row < self._num_rows) and (temp_mine_col >= 0 and temp_mine_col < self._num_cols):
                        if self._tiles[temp_mine_row][temp_mine_col] >= 0:
                            self._tiles[temp_mine_row][temp_mine_col] += 1
        pprint.pprint(self._tiles)
        #Create GUI
        self._CreateGUI()

    def _CreateGUI(self):
        #Initialize Variables
        self._pauseButtonText = StringVar()
        self._timerText = StringVar()

        if self._num_cols % 2 == 0:
            timer_span = 2
        else:
            timer_span = 3
        button_span = int((self._num_cols - 4 - timer_span) / 2)

        #Create Start Button
        Button(self, text="Start", command=self._StartGame).grid(row=0, column=1, columnspan=button_span, sticky=N+E+S+W)
        #Create Pause Button
        Button(self, textvariable=self._pauseButtonText, command=self._PauseGame).grid(row=0, column=(self._num_cols - button_span - 1), columnspan=button_span, sticky=N+E+S+W)
        self._pauseButtonText.set("Pause")
        #Create Timer Label
        Label(self, textvariable=self._timerText).grid(row=0, column=int((self._num_cols - 1) / 2), columnspan=timer_span, sticky=N+E+S+W)
        self._timerText.set(self._playTime)
        #Add Tile Buttons
        for y in range(1, self._num_rows + 1):
            for x in range(0, self._num_cols):
                b = Button(self, text=str(self._tiles[y-1][x]), command=lambda row=y-1, col=x: self._ButtonClick(row, col), bg='light grey', fg='light grey', activeforeground='light grey', activebackground='light grey', relief='ridge')
                b.grid(row=y, column=x, sticky=N+E+S+W)
                self._buttons.append(b)
                self.grid_columnconfigure(x, minsize=30)
                self.grid_rowconfigure(y, minsize=30)
        print(self._buttons)

    def _StartGame(self):
        if not self._isStarted:
            self._isStarted = True
            print("Game Has Been Started")
        else:
            print("The Game Has Already Begun")

    def _PauseGame(self):
        if self._isStarted:
            if not self._isPaused:
                self._isPaused = True
                self._pauseButtonText.set("Resume")
                print("The Game Has Been Paused")
            else:
                self._isPaused = False
                self._pauseButtonText.set("Pause")
                print("The Game Has Resumed")

    def _EndGame(self, win):
        if win:
            print("You Won!")
        else:
            print("You Lost!")

    def _ButtonClick(self, row, col):
        if self._tiles[row][col] == 0:
            self._buttons[(row * self._num_cols) + col].config(state=DISABLED, disabledforeground=self._colors[self._tiles[row][col]], bg='white')
            self._uncoveredTiles += 1
            for y in range(-1, 2):
                for x in range(-1, 2):
                    temp_row = row + y
                    temp_col = col + x
                    if (temp_row >= 0 and temp_row < self._num_rows) and (temp_col >= 0 and temp_col < self._num_cols):
                        if str(self._buttons[(temp_row * self._num_cols) + temp_col]['state']) != 'disabled':
                            self._ButtonClick(temp_row, temp_col)
        elif self._tiles[row][col] > 0:
            self._buttons[(row * self._num_cols) + col].config(state=DISABLED, disabledforeground=self._colors[self._tiles[row][col]], bg='white')
            self._uncoveredTiles += 1
        else:
            self._uncoveredTiles = -1
