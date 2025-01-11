from settings import *
from button import CustomButton
from rect import Rect
from canvas import CustomCanvas
from element import Element

from tkinter import *
from PIL import Image, ImageTk


def GetImage(file: str, rect: Rect):

    # PhotoImage(file="'./assets/'+file") # Does not working for pngs somehow
    return ImageTk.PhotoImage(Image.open('./assets/' + file).resize(rect.size))

def CenterizeWindow(window, rect: Rect):

     # Calculating topleft position of window when it is at the center of screen.
    screenWidth, screenHeight = window.winfo_screenwidth(), window.winfo_screenheight()
    topleftX, topleftY = (screenWidth - rect.width) // 2, (screenHeight - rect.height) // 2
    window.geometry(f"{rect.width}x{rect.height}+{topleftX}+{topleftY}")


class GUI(Tk):
    
    #region Initialize

    def __init__(self, rect: Rect = WINDOW_RECT):

        super().__init__()
        self.SetSize(rect)
        self.SetUnresizable()
        self.RemoveTitleBar()
        self.CreateWidgets()

    def SetSize(self, rect: Rect):

        self.rect = rect
        CenterizeWindow(self, self.rect)

    def SetBackgroundColor(self, color: str):

        self.configure(bg = color)

    def SetUnresizable(self):
        
        self.resizable(False, False)

    def RemoveTitleBar(self):

        self.overrideredirect(True)

    #endregion

    #region Titlebar Functions

    def Unminimize(self,e):
        
        self.update_idletasks()
        self.overrideredirect(True)
        self.state('normal')

    def Minimize(self):

        self.update_idletasks() # Reference: https://stackoverflow.com/questions/29186327/tclerror-cant-iconify-override-redirect-flag-is-set
        self.overrideredirect(False)
        #self.state('withdrawn')
        self.state('iconic')

        #self.iconify() # Giving error

    def GetPosition(self, event):

        topleftX = self.winfo_x()
        topleftY = self.winfo_y()
        startx = event.x_root
        starty = event.y_root

        ywin = topleftY - starty
        xwin = topleftX - startx

        def Move(event):

            self.geometry(f"{self.rect.width}x{self.rect.height}+{event.x_root + xwin}+{event.y_root + ywin}")

        self.topBar.bind('<B1-Motion>', Move)

    def OpenInfo(self):

        infoWindow = Toplevel(self)
        CenterizeWindow(infoWindow, INFO_RECT)
        Label(infoWindow, text="Made by Umucan Ekinci", font=FONT).place(x=50, y=50)

    #endregion

    def CreateWidgets(self):

        # Main Canvas
        mainCanvas = CustomCanvas(self, BACKGROUND_COLOR, WINDOW_RECT)
        mainCanvas.bind("<Map>", self.Unminimize)
        mainCanvas.bind('<Button-1>', self.SelectElement)

        # TopBar Canvas
        # Can't use mainCanvas.create_rectangle() because I need an object to assign hold and drag function to move window.
        self.topBar = CustomCanvas(mainCanvas, TOPBAR_COLOR, TOPBAR_RECT)
        self.topBar.bind('<Button-1>', self.GetPosition) # Move window with topbar. Reference: https://stackoverflow.com/questions/23836000/can-i-change-the-title-bar-in-tkinter

        # Logo
        logoImage = GetImage('logo.png', LOGO_RECT)
        self.topBar.create_image(LOGO_RECT, logoImage)

        # Title
        self.topBar.create_text(TITLE_RECT, TITLE, TEXT_COLOR, FONT)
        
        infoImage = GetImage('info.png', INFO_BUTTON_RECT)
        infoButton = CustomButton(self.topBar, self.OpenInfo, TOPBAR_COLOR, infoImage)
        infoButton.place(INFO_BUTTON_RECT)

        minimizeButton = CustomButton(self.topBar, self.Minimize, TEXT_COLOR, None)
        minimizeButton.place(MINIMIZE_BUTTON_RECT)

        exitImage = GetImage('exit_button.png', EXIT_BUTTON_RECT)
        exitButton = CustomButton(self.topBar, lambda: self.destroy(), TOPBAR_COLOR, image=exitImage)
        exitButton.place(EXIT_BUTTON_RECT)

        mainCanvas.create_rectangle(OPEN_RECT, GRAY)
        mainCanvas.create_rectangle(IN_PROGRESS_RECT, GRAY)
        mainCanvas.create_rectangle(DONE_RECT, GRAY)

        mainCanvas.create_rectangle(OPEN_TITLE_BOX_RECT, RED)
        mainCanvas.create_rectangle(IN_PROGRESS_TITLE_BOX_RECT, YELLOW)
        mainCanvas.create_rectangle(DONE_TITLE_BOX_RECT, GREEN)
        
        mainCanvas.create_text(OPEN_TITLE_RECT, "OPEN", TEXT_COLOR, font= FONT)
        mainCanvas.create_text(IN_PROGRESS_TITLE_RECT, "IN PROGRESS", TEXT_COLOR, font= FONT)
        mainCanvas.create_text(DONE_TITLE_RECT, "DONE", TEXT_COLOR, font= FONT)
        
        self.elements = []
        self.elements.append(Element(mainCanvas, ELEMENT_RECT, BLACK, WHITE, Element.OPEN))

    def SelectElement(self, event: Event):

        for element in self.elements:

            if element.isCollide(event.x, event.y):
                element.Select()



    def Run(self):

        self.mainloop()