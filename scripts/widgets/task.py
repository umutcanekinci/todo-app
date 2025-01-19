from rect import Rect
from constants import PADDING
from utils import isPointInRectangle
from group import Group

class Task:
    
    def __init__(self, group: Group, rect: Rect, color: str, title, detail, deadLine):
        
        self.rect = rect
        self.color = color
        self.title, self.detail = title, detail
        self.group = group
        self.canvas = group.canvas
        self.deadLine = deadLine
        self.id =  self.canvas.create_rectangle(rect, color)
        self.titleId = self.canvas.create_text(self.rect.center, title, "white", ("Arial", 12))
        
        isTextWidthGreater = self.canvas.GetItemWidth(self.titleId) > rect.width - PADDING * 2
        if  isTextWidthGreater:
            self.canvas.SetItemWidth(self.titleId, rect.width - PADDING * 2)

        isTextHeightGreater = self.canvas.GetItemHeight(self.titleId) > rect.height - PADDING * 2
        if isTextHeightGreater:
            self.rect.height = self.canvas.GetItemHeight(self.titleId) + PADDING * 2

        self.textWidth, self.textHeight = self.canvas.GetItemSize(self.titleId)

    def isCollide(self, x: int, y: int):

        return isPointInRectangle(self.rect, x, y)

    def Select(self, borderColor: str):

        self.canvas.itemconfig(self.id, outline=borderColor, width=2)

    def Unselect(self):

        self.canvas.itemconfig(self.id, fill=self.color, outline="", width=0)

    def MoveTo(self, x: int, y: int):

        self.rect.topLeft = x, y
        
        self.canvas.SetRectanglePosition(self.id, self.rect)
        self.canvas.SetTextPosition(self.titleId, self.rect.center)

    def Move(self, dx: int, dy: int):

        return self.MoveTo(self.rect.x + dx, self.rect.y + dy)
    
    def UpdateTitle(self, title: str):

        self.title = title
        self.canvas.itemconfig(self.titleId, text=title)

    def UpdateColor(self, color: str):

        self.color = color
        self.canvas.itemconfig(self.id, fill=color)

    def Delete(self):

        self.canvas.delete(self.id)
        self.canvas.delete(self.titleId)
        