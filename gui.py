from settings import *
from tkinter import *
from tkinter import ttk

class GUI(Tk):
    
    def __init__(self):
        super().__init__()

    def SetSize(self, width: int, height: int):

        self.size = self.width, self.height = width, height

        # Calculating topleft position of window when it is at the center of screen.
        screenWidth, screenHeight = self.winfo_screenwidth(), self.winfo_screenheight()
        topleftX, topleftY = (screenWidth - width) // 2, (screenHeight - height) // 2

        self.geometry(f"{width}x{height}+{topleftX}+{topleftY}")

    def SetBackgroundColor(self, color: str):

        self.configure(bg = color)

    def SetUnresizable(self):
        
        self.resizable(False, False)

    def RemoveTitleBar(self):

        self.overrideredirect(True)

    def GetPosition(self, event):

        topleftX = self.winfo_x()
        topleftY = self.winfo_y()
        startx = event.x_root
        starty = event.y_root

        ywin = topleftY - starty
        xwin = topleftX - startx

        def Move(event):

            self.geometry(f"{self.width}x{self.height}+{event.x_root + xwin}+{event.y_root + ywin}")

        self.topBar.bind('<B1-Motion>', Move)


    def Initialize(self):

        self.SetSize(*WINDOW_SIZE)
        self.SetUnresizable()
        self.RemoveTitleBar()

        mainCanvas = Canvas(
            self,
            bg = BACKGROUND_COLOR,
            height = WINDOW_HEIGHT,
            width = WINDOW_WIDTH,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        mainCanvas.place(x = 0, y = 0)

        # TopBar
        """ // Can't use that because I need an object to assign hold and drag function to move window.
        mainCanvas.create_rectangle(
            0.0,
            0.0,
            WINDOW_WIDTH,
            40.0,
            fill=TOPBAR_COLOR,
            outline="")
        """
        self.topBar = Frame(mainCanvas, bg=TOPBAR_COLOR, relief='raised', bd=2)
        self.topBar.place(x=0, y=0, width=WINDOW_WIDTH, height=40)
        self.topBar.bind('<Button-1>', self.GetPosition) # Move window with topbar. Reference: https://stackoverflow.com/questions/23836000/can-i-change-the-title-bar-in-tkinter

        



    def Run(self):

        self.mainloop()

    

