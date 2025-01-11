from rect import Rect
from settings import PADDING, BORDER_COLOR

class Direction:
    
    LEFT = -1
    RIGHT = 1

    UP = -1
    DOWN = 1

class Status:

    OPEN = 0
    IN_PROGRESS = 1
    DONE = 2

class Element:
    
    def __init__(self, canvas, rect: Rect, color: str, selectedColor: str, status: int, text):
        
        self.rect = rect
        self.color, self.selectedColor = color, selectedColor
        self.status = status
        self.canvas = canvas
        self.id =  canvas.create_rectangle(rect, color)
        self.textId = canvas.create_text(Rect(rect.x, rect.x), text, "white", ("Arial", 12), "nw")
        self.text = text

    def isCollide(self, x: int, y: int):

        return x > self.rect.left and x < self.rect.right and y < self.rect.bottom and y > self.rect.top

    def Select(self):

        self.canvas.itemconfig(self.id, outline=BORDER_COLOR, width=2)

    def Unselect(self):

        self.canvas.itemconfig(self.id, fill=self.color, outline="", width=0)

    def MoveTo(self, x: int, y: int):

        self.rect.topLeft = x, y
        self.canvas.coords(self.id, self.rect.left, self.rect.top, self.rect.right, self.rect.bottom)
        self.canvas.coords(self.textId, self.rect.x + PADDING, self.rect.y + PADDING)