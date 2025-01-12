from scripts.rect import Rect
from constants import PADDING, BORDER_COLOR

class Task:
    
    def __init__(self, canvas, rect: Rect, color: str, selectedColor: str, status: int, title, detail, deadLine):
        
        self.rect = rect
        self.color, self.selectedColor = color, selectedColor
        self.title, self.detail = title, detail
        self.status = status
        self.canvas = canvas
        self.deadLine = deadLine
        self.id =  canvas.create_rectangle(rect, color)
        self.titleId = canvas.create_text(self.rect.center, title, "white", ("Arial", 12))
        
        isTextWidthGreater = canvas.GetItemWidth(self.titleId) > rect.width - PADDING * 2
        if  isTextWidthGreater:
            canvas.SetItemWidth(self.titleId, rect.width - PADDING * 2)

        isTextHeightGreater = canvas.GetItemHeight(self.titleId) > rect.height - PADDING * 2
        if isTextHeightGreater:
            self.rect.height = canvas.GetItemHeight(self.titleId) + PADDING * 2

        self.textWidth, self.textHeight = canvas.GetItemSize(self.titleId)

    def isCollide(self, x: int, y: int):

        return x > self.rect.left and x < self.rect.right and y < self.rect.bottom and y > self.rect.top

    def Select(self):

        self.canvas.itemconfig(self.id, outline=BORDER_COLOR, width=2)

    def Unselect(self):

        self.canvas.itemconfig(self.id, fill=self.color, outline="", width=0)

    def MoveTo(self, x: int, y: int):

        self.rect.topLeft = x, y
        
        self.canvas.SetRectanglePosition(self.id, self.rect)
        self.canvas.SetTextPosition(self.titleId, self.rect.center)