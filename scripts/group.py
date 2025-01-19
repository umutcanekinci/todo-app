from widgets.canvas import CustomCanvas
from widgets.button import CustomButton
from utils import GetTitleBoxRect, GetGroupRect
from constants import TEXTBOX_COLORS, TEXT_COLOR, BOLD_FONT, TASK_GROUPS
from rects import ADD_BUTTON_RECT
from enums import Status


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
        
        self.canvas = CustomCanvas(self.mainCanvas, None, GetGroupRect(self.name))

    def CreateTitleBox(self) -> None:

        self.mainCanvas.create_rectangle(GetTitleBoxRect(self.name), TEXTBOX_COLORS[self.name.value])
        self.mainCanvas.create_text(GetTitleBoxRect(self.name).center, TASK_GROUPS[self.name.value], TEXT_COLOR, BOLD_FONT)
            
    def CreateAddButton(self, onClick, image) -> None:
        
        self.addButton = CustomButton(self.canvas, ADD_BUTTON_RECT, onClick, None, image)
