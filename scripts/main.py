from constants import *
from gui import GUI
from tkinter import *

def main():
    
    app = GUI()
    app.Run()
    app.SaveTasks()
    del app


if __name__ == "__main__":

    main()
