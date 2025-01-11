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
        startx, starty = event.x_root, event.y_root

        ywin = topleftY - starty
        xwin = topleftX - startx

        def Move(event):

            self.geometry(f"{self.rect.width}x{self.rect.height}+{event.x_root + xwin}+{event.y_root + ywin}")

        self.topCanvas.bind('<B1-Motion>', Move)

    def OpenInfo(self):

        infoWindow = Toplevel(self)
        CenterizeWindow(infoWindow, INFO_RECT)
        Label(infoWindow, text="Made by Umucan Ekinci", font=FONT).place(x=50, y=50)

    #endregion


    def CreateWidgets(self):
    
        # load images
        logoImage = GetImage('logo.png', LOGO_RECT)
        infoImage = GetImage('info.png', INFO_BUTTON_RECT)
        exitImage = GetImage('exit_button.png', EXIT_BUTTON_RECT)

        # Top Canvas
        self.topCanvas = CustomCanvas(self, TOP_COLOR, TOP_RECT)
        self.topCanvas.bind('<Button-1>', self.GetPosition) # Move window with topCanvas. Reference: https://stackoverflow.com/questions/23836000/can-i-change-the-title-bar-in-tkinter

        # Logo and Title
        self.topCanvas.create_image(LOGO_RECT, logoImage)
        self.topCanvas.create_text(TITLE_RECT, TITLE, TEXT_COLOR, FONT)
        
        # Buttons
        infoButton = CustomButton(self.topCanvas, self.OpenInfo, TOP_COLOR, infoImage)
        infoButton.place(INFO_BUTTON_RECT)

        minimizeButton = CustomButton(self.topCanvas, self.Minimize, TEXT_COLOR, None)
        minimizeButton.place(MINIMIZE_BUTTON_RECT)

        exitButton = CustomButton(self.topCanvas, lambda: self.destroy(), TOP_COLOR, image=exitImage)
        exitButton.place(EXIT_BUTTON_RECT)

        # Main Canvas
        self.mainCanvas = CustomCanvas(self, MAIN_COLOR, MAINCANVAS_RECT)
        self.mainCanvas.bind("<Map>", self.Unminimize)
        self.mainCanvas.bind('<Button-1>', self.SelectElement)

        self.mainCanvas.create_rectangle(OPEN_RECT, GRAY)
        self.mainCanvas.create_rectangle(IN_PROGRESS_RECT, GRAY)
        self.mainCanvas.create_rectangle(DONE_RECT, GRAY)

        self.mainCanvas.create_rectangle(OPEN_TITLE_BOX_RECT, RED)
        self.mainCanvas.create_rectangle(IN_PROGRESS_TITLE_BOX_RECT, YELLOW)
        self.mainCanvas.create_rectangle(DONE_TITLE_BOX_RECT, GREEN)
        
        self.mainCanvas.create_text(OPEN_TITLE_RECT, "OPEN", TEXT_COLOR, font= FONT)
        self.mainCanvas.create_text(IN_PROGRESS_TITLE_RECT, "IN PROGRESS", TEXT_COLOR, font= FONT)
        self.mainCanvas.create_text(DONE_TITLE_RECT, "DONE", TEXT_COLOR, font= FONT)
        
        # Elements
        self.selectedElement = None
        self.open = []
        self.inProgress = []
        self.done = []

        
        self.AddNewElement(Element.OPEN)
        self.AddNewElement(Element.OPEN)

        self.bind('<Right>', lambda e: self.MoveElement(1))
        self.bind('<Left>', lambda e: self.MoveElement(-1))

    def GetRect(self, status: str):

        if status == Element.OPEN:
            return OPEN_RECT
        
        elif status == Element.IN_PROGRESS:
            return IN_PROGRESS_RECT
        
        elif status == Element.DONE:
            return DONE_RECT

    def GetList(self, status: str):

        if status == Element.OPEN:
            return self.open
        
        elif status == Element.IN_PROGRESS:
            return self.inProgress
        
        elif status == Element.DONE:
            return self.done

    def AddNewElement(self, status: str):
        
        width = self.GetRect(status).width - 20
        height = ELEMENT_RECT.height
        x = self.GetRect(status).left + 10
        y = ELEMENT_RECT.y + len(self.open) * (height + 10)
        
        self.GetList(status).append(Element(self.mainCanvas, Rect(x, y, width, height), BLACK, WHITE, status))
    
    def RemoveElementFromList(self, element: Element):

        self.GetList(element.status).remove(element)

    def SelectElement(self, event: Event):

        collided_element = None
        for element in self.open + self.inProgress + self.done:
            if element.isCollide(event.x, event.y):
                collided_element = element
                break

        if self.selectedElement:
            
            self.selectedElement.Unselect()
        
        if self.selectedElement == collided_element:

            self.selectedElement = None

        else:

            if collided_element:

                collided_element.Select()
                
            self.selectedElement = collided_element
        
        """ Doesn't work properly
        startx, starty = event.x, event.y
        deltax, deltay = element.rect.left - startx, element.rect.top - starty

        def MoveElement(event: Event):
            nonlocal element
            for element in self.elements:

                if element.isCollide(startx, starty):
                    element.topleft = deltax + event.x, deltay + event.y
                    element.canvas.coords(element.id, self.rect.left, self.rect.top, self.rect.right, self.rect.bottom)
                    break
                
        self.mainCanvas.bind('<B1-Motion>', MoveElement)
        """

    def UpdateList(self, list: list):

        for element in list:
        
            element.MoveTo(self.GetRect(element.status).left + 10, ELEMENT_RECT.y + list.index(element) * (ELEMENT_RECT.height + 10))

    def MoveElement(self, direction: int):

        if self.selectedElement:

            canMoveRight = direction == 1 and self.selectedElement.status != Element.DONE
            canMoveLeft = direction == -1 and self.selectedElement.status != Element.OPEN

            if canMoveRight or canMoveLeft:

                self.RemoveElementFromList(self.selectedElement)
                self.UpdateList(self.GetList(self.selectedElement.status))
                self.selectedElement.status += direction
                self.GetList(self.selectedElement.status).append(self.selectedElement)
                self.UpdateList(self.GetList(self.selectedElement.status))


    def Run(self):

        self.mainloop()