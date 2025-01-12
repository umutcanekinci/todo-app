from settings import *
from widgets.button import CustomButton
from widgets.canvas import CustomCanvas
from widgets.element import Element
from rect import Rect
from enums import Direction, Status
from utils import GetImage
from tkinter import *
from tkinter import simpledialog

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
        self.logoImage = GetImage(LOGO_IMAGE, LOGO_RECT)
        self.infoImage = GetImage(INFO_IMAGE, INFO_BUTTON_RECT)
        self.exitImage = GetImage(EXIT_IMAGE, EXIT_BUTTON_RECT)
        self.addImage = GetImage(ADD_IMAGE, ADD_BUTTON_RECT)
        
        # Top Canvas
        self.topCanvas = CustomCanvas(self, TOP_COLOR, TOP_RECT)
        self.topCanvas.bind('<Button-1>', self.GetPosition) # Move window with topCanvas. Reference: https://stackoverflow.com/questions/23836000/can-i-change-the-title-bar-in-tkinter

        # Logo and Title
        self.topCanvas.create_image(LOGO_RECT, self.logoImage)
        self.topCanvas.create_text(TITLE_RECT, TITLE, TEXT_COLOR, TITLE_FONT)
        
        # Buttons
        infoButton =     CustomButton(self.topCanvas, self.OpenInfo, TOP_COLOR, self.infoImage)
        minimizeButton = CustomButton(self.topCanvas, self.Minimize, TEXT_COLOR, None)
        exitButton =     CustomButton(self.topCanvas, self.Exit, TOP_COLOR, image=self.exitImage)
        
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
        self.elements = [[] for _ in Status] # Open, In Progress, Done lists

        self.addButtons = []
        for status in Status:
            self.addButtons.append(CustomButton(self.mainCanvas, lambda status=status: self.AddNewElement(status), GRAY, self.addImage))
            self.UpdateElementsPosition(status)
            
        # Key Bindings
        self.bind('<Right>', lambda e: self.MoveHorizontally(Direction.RIGHT))
        self.bind('<Left>', lambda e: self.MoveHorizontally(Direction.LEFT))
        self.bind('<Down>', lambda e: self.MoveVertically(Direction.DOWN))
        self.bind('<Up>', lambda e: self.MoveVertically(Direction.UP))
        self.bind('<Delete>', lambda e: self.RemoveElement(self.selectedElement))

    #region Element Functions

    def GetInput(self):

        return simpledialog.askstring("Add an element", "Enter the text", parent=self)

    def GetRect(self, status: str):

        if status is None:
            raise ValueError("Status is None")
        
        return [OPEN_RECT, IN_PROGRESS_RECT, DONE_RECT][status.value]

    def GetList(self, status: str):

        if status is None:
            raise ValueError("Status is None")
        
        return self.elements[status.value]

    def GetAddButton(self, status: str):

        if status is None:
            raise ValueError("Status is None")

        return self.addButtons[status.value]

    def AddNewElement(self, status: str):

        if status is None:
            raise ValueError("Status is None")

        text = self.GetInput()

        if not text:
            return

        self.GetList(status).append(Element(self.mainCanvas, Rect(0, 0, ELEMENT_RECT.width, ELEMENT_RECT.height), BLACK, WHITE, status, text))
        self.UpdateElementsPosition(status)

    def RemoveElement(self, element: Element):
        
        if element is None:
            raise ValueError("Element is None")

        self.RemoveElementFromList(element)
        self.mainCanvas.delete(element.id)
        self.mainCanvas.delete(element.textId)
        self.selectedElement = None

    def RemoveElementFromList(self, element: Element):
        
        if element is None:
            return
        
        self.GetList(element.status).remove(element)
        self.UpdateElementsPosition(element.status)

    def GetCollidedElement(self, x: int, y: int):

        for element in sum(self.elements, []):
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
        
    def UpdateElementsPosition(self, status: Status):

        if status is None:
            raise ValueError("Status is None")

        list = self.GetList(status)

        if list is None:
            raise ValueError("List is None")
        
        for i, element in enumerate(list):
        
            if i:
                element.MoveTo(self.GetRect(status).left + PADDING, list[i - 1].rect.bottom + PADDING)
                continue
            
            element.MoveTo(self.GetRect(element.status).left + PADDING, ELEMENT_RECT.y)

        self.UpdateAddButtonPosition(status)

    def UpdateAddButtonPosition(self, status: Status):

        list = self.GetList(status)        

        if list and list[-1].rect.bottom + PADDING * 2 + ELEMENT_HEIGHT > self.GetRect(status).bottom:
            self.GetAddButton(status).place_forget()
            return

        if list:
            self.GetAddButton(list[0].status).place(Rect(list[0].rect.centerX - ADD_BUTTON_RECT.width // 2, list[-1].rect.bottom + PADDING * 2, ADD_BUTTON_RECT.width, ADD_BUTTON_RECT.height))
        
        else:
            self.GetAddButton(status).place(Rect(self.GetRect(status).centerX - ADD_BUTTON_RECT.width // 2, self.GetRect(status).top + TITLE_BOX_HEIGHT + PADDING * 2, ADD_BUTTON_RECT.width, ADD_BUTTON_RECT.height))

    def MoveHorizontally(self, direction: Direction):

        if not self.selectedElement or not direction:
            return
        
        canMoveRight = direction == Direction.RIGHT and self.selectedElement.status is not Status.DONE
        canMoveLeft = direction == Direction.LEFT and self.selectedElement.status is not Status.OPEN

        if not (canMoveRight or canMoveLeft):
            return
        
        self.RemoveElementFromList(self.selectedElement)
        self.selectedElement.status = Status(self.selectedElement.status.value + direction.value) 
        self.GetList(self.selectedElement.status).append(self.selectedElement)
        self.UpdateElementsPosition(self.selectedElement.status)

    def MoveVertically(self, direction : Direction):

        if not self.selectedElement or not direction:
            return

        elements = self.GetList(self.selectedElement.status)
        index = elements.index(self.selectedElement)

        canMoveDown = direction == Direction.DOWN and index != len(elements) - 1
        canMoveUp = direction == Direction.UP and index != 0

        if not (canMoveDown or canMoveUp):
            return
        
        elements[index], elements[index + direction.value] = elements[index + direction.value], elements[index]
        self.UpdateElementsPosition(self.selectedElement.status)

    #endregion

    def Run(self):

        self.mainloop()

    def Exit(self):

        self.destroy()