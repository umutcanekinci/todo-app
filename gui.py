from tkinter import *
from tkinter import ttk

class GUI(Tk):
    
    def __init__(self):
        super().__init__()

    def SetGeometry(self, width: int, height: int):

        self.geometry(width + "x" + height)

    def SetBackgroundColor(self, color: str):

        self.configure(bg = "#FFFFFF")

    def Run(self):

        self.mainloop()

    

