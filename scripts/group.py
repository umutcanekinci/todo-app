from widgets.canvas import CustomCanvas
from widgets.button import CustomButton
from utils import GetTitleBoxRect, GetGroupRect, GetNextTaskPosition, GetTaskRect
from constants import TEXTBOX_COLORS, TEXT_COLOR, BOLD_FONT, TASK_GROUPS, PADDING
from rects import ADD_BUTTON_RECT
from enums import Status
from tkinter.ttk import Scrollbar
from rect import Rect

class Group:

    OPEN = 0
    IN_PROGRESS = 1
    DONE = 2

    def __init__(self, mainCanvas: CustomCanvas, name: Status):
        
        self.name = name
        self.mainCanvas = mainCanvas
        self.scrollBar = None
        self.tasks = []

        self.CreateCanvas()
        self.CreateTitleBox()
    
    def CreateCanvas(self) -> None:
        
        self.rect = GetGroupRect(self.name)
        self.canvas = CustomCanvas(self.mainCanvas, None, self.rect)

    def CreateTitleBox(self) -> None:

        self.mainCanvas.create_rectangle(GetTitleBoxRect(self.name), TEXTBOX_COLORS[self.name.value])
        self.mainCanvas.create_text(GetTitleBoxRect(self.name).center, TASK_GROUPS[self.name.value], TEXT_COLOR, BOLD_FONT)
            
    def CreateAddButton(self, onClick, image) -> None:
        
        self.addButton = CustomButton(self.canvas, ADD_BUTTON_RECT, onClick, None, image)

    def UpdatePosition(self) -> None:

        self.UpdateTasksPosition()
        self.UpdateAddButtonPosition()
        
        isThereEnoughSpace = self.addButton.rect.bottom + PADDING * 4 < self.rect.bottom
        self.Resize()
        
        if not isThereEnoughSpace and not self.scrollBar:
            self.CreateScrollBar()
            return
        
        self.DeleteScrollBar()

    def Resize(self):
        
        region = self.canvas.bbox("all")
        
        if not region:
            return
        
        region = 0, 0, region[2], region[3] + ADD_BUTTON_RECT.height + PADDING * 6 
        self.canvas.configure(scrollregion=region)

    def UpdateTasksPosition(self):
        
        for i, task in enumerate(self.tasks):
            
            position = GetNextTaskPosition(self, i)
            task.MoveTo(*position)

    def UpdateAddButtonPosition(self):
        
        addButton = self.addButton
             
        x, y = GetNextTaskPosition(self, len(self.tasks))
        
        if self.scrollBar: # Update y position with movement of scrollbar
            y -= self.canvas.canvasy(0) 

        rect = Rect(x, y, *GetTaskRect().size)
        addButton.place(rect.center)

    def CreateScrollBar(self):
        
        # I don't know why but when I not get status from parameter, it becomes the last status

        if self.scrollBar:
            return

        self.scrollBar = Scrollbar(self.mainCanvas, orient='vertical', command=self.canvas.yview)
        self.scrollBar.place(x=self.rect.right - PADDING, y=self.rect.top, height=self.rect.height)
        
        self.canvas.config(yscrollcommand= lambda x0, x1: self.HandleScrollbar(x0, x1))
        
    def HandleScrollbar(self, x0, x1):
        
        if not self.scrollBar:
            return
        
        self.scrollBar.set(x0, x1)
        self.UpdateAddButtonPosition()

    def DeleteScrollBar(self) -> None:

        if not self.scrollBar:
            return

        self.scrollBar.place_forget()
        self.scrollBar = None
