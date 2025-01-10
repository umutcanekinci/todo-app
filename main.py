from settings import *
from gui import GUI
from tkinter import *

def main():
    
    app = GUI()
    app.Initialize()
    app.CreateWidgets()
    app.Run()

if __name__ == "__main__":

    main()