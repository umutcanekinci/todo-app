from rect import Rect
from settings import PADDING, BORDER_COLOR

class Element:
    
    def __init__(self, canvas, rect: Rect, color: str, selectedColor: str, status: int, text):
        
        self.rect = rect
        self.color, self.selectedColor = color, selectedColor
        self.status = status
        self.canvas = canvas
        self.id =  canvas.create_rectangle(rect, color)
        self.textId = canvas.create_text(Rect(), text, "white", ("Arial", 12), "nw")
        
        
        isTextWidthGreater = canvas.GetItemWidth(self.textId) > rect.width - PADDING * 2
        if  isTextWidthGreater:
            canvas.SetItemWidth(self.textId, rect.width - PADDING * 2)

        isTextHeightGreater = canvas.GetItemHeight(self.textId) > rect.height - PADDING * 2
        if isTextHeightGreater:
            self.rect.height = canvas.GetItemHeight(self.textId) + PADDING * 2

        self.textWidth, self.textHeight = canvas.GetItemSize(self.textId)

    def isCollide(self, x: int, y: int):

        return x > self.rect.left and x < self.rect.right and y < self.rect.bottom and y > self.rect.top

    def Select(self):

        self.canvas.itemconfig(self.id, outline=BORDER_COLOR, width=2)

    def Unselect(self):

        self.canvas.itemconfig(self.id, fill=self.color, outline="", width=0)

    def MoveTo(self, x: int, y: int):

        self.rect.topLeft = x, y
        textRect = Rect(0, 0, self.textWidth, self.textHeight)
        textRect.center = self.rect.center

        self.canvas.SetRectanglePosition(self.id, self.rect)
        self.canvas.SetTextPosition(self.textId, textRect)