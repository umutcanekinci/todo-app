from settings import *
from button import CustomButton
from rect import Rect
from canvas import CustomCanvas
from element import Element, Direction, Status

from tkinter import *
from PIL import Image, ImageTk


def GetImage(file: str, rect: Rect):

    # PhotoImage(file="'./assets/'+file") # Does not working for pngs somehow
    return ImageTk.PhotoImage(Image.open('./assets/' + file).resize(rect.size))

class GUI(Tk):
    
    #region Initialize

    def __init__(self, rect: Rect = WINDOW_RECT):

        super().__init__()
        self.SetSize(rect)
        self.SetUnresizable(self)
        self.RemoveTitleBar(self)
        self.CreateWidgets()
        self.bind('<Escape>', lambda e: self.Exit())
        self.SetTitle(self, TITLE)
        self.infoWindow = None

    def SetSize(self, rect: Rect):

        self.rect = rect
        self.Centerize(self, self.rect)

    @staticmethod
    def SetUnresizable(window, width: bool = False, height: bool = False):
        
        window.resizable(width, height)

    @staticmethod
    def RemoveTitleBar(window: Misc):

        window.overrideredirect(True)

    @staticmethod
    def SetTitle(window: Misc, title: str):

        window.title(title)

    @staticmethod
    def Centerize(window: Misc, rect: Rect):

        # Calculating topleft position of window when it is at the center of screen.
        screenWidth, screenHeight = window.winfo_screenwidth(), window.winfo_screenheight()
        topleftX, topleftY = (screenWidth - rect.width) // 2, (screenHeight - rect.height) // 2
        window.geometry(f"{rect.width}x{rect.height}+{topleftX}+{topleftY}")

    @staticmethod
    def SetBackgroundColor(window: Misc, color: str):
        
        window.configure(bg = color)

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

    def GetPositionInfo(self, event):

        topleftX = self.infoWindow.winfo_x()
        topleftY = self.infoWindow.winfo_y()
        startx, starty = event.x_root, event.y_root

        ywin = topleftY - starty
        xwin = topleftX - startx

        def Move(event):

            self.infoWindow.geometry(f"{INFO_RECT.width}x{INFO_RECT.height}+{event.x_root + xwin}+{event.y_root + ywin}")

        self.infoWindow.bind('<B1-Motion>', Move)

    def Lock(self):

        self.infoWindow.grab_set()

    def Unlock(self):

        self.infoWindow.grab_release()

    def CloseInfo(self):

        self.infoWindow.destroy()
        self.infoWindow = None

    def OpenInfo(self):
        
        if self.infoWindow is not None:
            return

        self.infoWindow = Toplevel(self)
        self.Centerize(self.infoWindow, INFO_RECT)
        self.SetBackgroundColor(self.infoWindow, MAIN_COLOR)
        self.SetTitle(self.infoWindow, INFO_TITLE)
        self.SetUnresizable(self.infoWindow)
        self.RemoveTitleBar(self.infoWindow)

        topCanvas = CustomCanvas(self.infoWindow, TOP_COLOR, Rect(0, 0, INFO_RECT.width, TOP_INFO_HEIGHT))
        self.infoWindow.bind('<Button-1>', lambda e: self.GetPositionInfo(e))

        topCanvas.create_text(INFO_TITLE_RECT, INFO_TITLE, TEXT_COLOR, TITLE_FONT)
        Label(self.infoWindow, text="Arrow keys: move the selected element\nEnter: Add an element\nDel: Remove the selected element.\n\nMade by Umutcan Ekinci\ngithub.com/umutcanekinci", font=FONT, justify='center', bg=MAIN_COLOR, fg=TEXT_COLOR).pack(pady=(50, 0))
        Button(self.infoWindow, text="Close", font=FONT, bg=TOP_COLOR, fg=TEXT_COLOR, command=self.CloseInfo).pack(pady=10)

        self.Lock()

    #endregion

    def CreateWidgets(self):
    
        # load images
        logoImage = GetImage(LOGO_IMAGE, LOGO_RECT)
        infoImage = GetImage(INFO_IMAGE, INFO_BUTTON_RECT)
        exitImage = GetImage(EXIT_IMAGE, EXIT_BUTTON_RECT)

        # Top Canvas
        self.topCanvas = CustomCanvas(self, TOP_COLOR, TOP_RECT)
        self.topCanvas.bind('<Button-1>', self.GetPosition) # Move window with topCanvas. Reference: https://stackoverflow.com/questions/23836000/can-i-change-the-title-bar-in-tkinter

        # Logo and Title
        self.topCanvas.create_image(LOGO_RECT, logoImage)
        self.topCanvas.create_text(TITLE_RECT, TITLE, TEXT_COLOR, TITLE_FONT)
        
        # Buttons
        infoButton =     CustomButton(self.topCanvas, self.OpenInfo, TOP_COLOR, infoImage)
        minimizeButton = CustomButton(self.topCanvas, self.Minimize, TEXT_COLOR, None)
        exitButton =     CustomButton(self.topCanvas, self.Exit, TOP_COLOR, image=exitImage)
        
        minimizeButton.place(MINIMIZE_BUTTON_RECT)
        infoButton.place(INFO_BUTTON_RECT)
        exitButton.place(EXIT_BUTTON_RECT)

        # Main Canvas
        self.mainCanvas = CustomCanvas(self, MAIN_COLOR, MAIN_RECT)
        self.mainCanvas.bind("<Map>", self.Unminimize)
        self.mainCanvas.bind('<Button-1>', self.SelectElement)

        self.mainCanvas.create_rectangle(OPEN_RECT,        GRAY)
        self.mainCanvas.create_rectangle(IN_PROGRESS_RECT, GRAY)
        self.mainCanvas.create_rectangle(DONE_RECT,        GRAY)

        self.mainCanvas.create_rectangle(OPEN_TITLE_BOX_RECT, OPEN_COLOR)
        self.mainCanvas.create_rectangle(IN_PROGRESS_TITLE_BOX_RECT, IN_PROGRESS_COLOR)
        self.mainCanvas.create_rectangle(DONE_TITLE_BOX_RECT, DONE_COLOR)
        
        self.mainCanvas.create_text(OPEN_TITLE_RECT, "OPEN",               TEXT_COLOR, font= FONT)
        self.mainCanvas.create_text(IN_PROGRESS_TITLE_RECT, "IN PROGRESS", TEXT_COLOR, font= FONT)
        self.mainCanvas.create_text(DONE_TITLE_RECT, "DONE",               TEXT_COLOR, font= FONT)
        
        # Elements
        self.selectedElement = None
        self.open = []
        self.inProgress = []
        self.done = []

        # Add some elements
        for i in range(3):
            self.AddNewElement(Status.OPEN)
            self.AddNewElement(Status.IN_PROGRESS)
            self.AddNewElement(Status.DONE)
 
        # Key Bindings
        self.bind('<Right>', lambda e: self.MoveHorizontally(1))
        self.bind('<Left>', lambda e: self.MoveHorizontally(-1))
        self.bind('<Down>', lambda e: self.MoveVertically(1))
        self.bind('<Up>', lambda e: self.MoveVertically(-1))
        self.bind('<Return>', lambda e: self.AddNewElement(Status.OPEN))
        self.bind('<Delete>', lambda e: self.RemoveElement(self.selectedElement))

    #region Element Functions

    def GetRect(self, status: str):

        if status is Status.OPEN:
            return OPEN_RECT
        
        elif status is Status.IN_PROGRESS:
            return IN_PROGRESS_RECT
        
        elif status is Status.DONE:
            return DONE_RECT
        return None

    def GetList(self, status: str):

        if status is Status.OPEN:
            return self.open
        
        elif status is Status.IN_PROGRESS:
            return self.inProgress
        
        elif status is Status.DONE:
            return self.done
        return None

    def AddNewElement(self, status: str):
    
        if status is None:
            return

        self.GetList(status).append(Element(self.mainCanvas, Rect(0, 0, ELEMENT_RECT.width, ELEMENT_RECT.height), BLACK, WHITE, status, ""))
        self.UpdateElementsPosition(self.GetList(status))

    def RemoveElement(self, element: Element):

        self.RemoveElementFromList(element)
        self.mainCanvas.delete(element.id)
        self.selectedElement = None

    def RemoveElementFromList(self, element: Element):
        
        if element is None:
            return
        
        self.GetList(element.status).remove(element)
        self.UpdateElementsPosition(self.GetList(element.status))

    def GetCollidedElement(self, x: int, y: int):

        for element in self.open + self.inProgress + self.done:
            if element.isCollide(x, y):
                return element
        return None

    def SelectElement(self, event: Event):

        collided_element = self.GetCollidedElement(event.x, event.y)

        if self.selectedElement:
            self.selectedElement.Unselect()
        
        if self.selectedElement is collided_element:
            self.selectedElement = None
            return
        
        if collided_element:
            collided_element.Select()
            
        self.selectedElement = collided_element
        
        """ Hold and Move doesn't work properly
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

    def UpdateElementsPosition(self, list: list):

        if list is None:
            return
        
        for element in list:
        
            element.MoveTo(self.GetRect(element.status).left + PADDING, ELEMENT_RECT.y + list.index(element) * (ELEMENT_RECT.height + PADDING))

    def MoveHorizontally(self, direction: Direction):

        if not self.selectedElement or not direction:
            return

        canMoveRight = direction is Direction.RIGHT and self.selectedElement.status is not Status.DONE
        canMoveLeft = direction is Direction.LEFT and self.selectedElement.status is not Status.OPEN

        if not (canMoveRight or canMoveLeft):
            return
        
        self.RemoveElementFromList(self.selectedElement)
        self.selectedElement.status += direction
        self.GetList(self.selectedElement.status).append(self.selectedElement)
        self.UpdateElementsPosition(self.GetList(self.selectedElement.status))

    def MoveVertically(self, direction : Direction):

        if not self.selectedElement or not direction:
            return

        elements = self.GetList(self.selectedElement.status)
        index = elements.index(self.selectedElement)

        canMoveDown = direction is Direction.DOWN and index != len(elements) - 1
        canMoveUp = direction is Direction.UP and index != 0

        if not (canMoveDown or canMoveUp):
            return
        
        elements[index], elements[index + direction] = elements[index + direction], elements[index]
        self.UpdateElementsPosition(elements)

    #endregion

    def Run(self):

        self.mainloop()

    def Exit(self):

        self.destroy()