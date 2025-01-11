from rect import Rect

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
        self.text = text

    def isCollide(self, x: int, y: int):

        return x > self.rect.left and x < self.rect.right and y < self.rect.bottom and y > self.rect.top

    def Select(self):

        self.canvas.itemconfig(self.id, fill=self.selectedColor)

    def Unselect(self):

        self.canvas.itemconfig(self.id, fill=self.color)

    def MoveTo(self, x: int, y: int):

        self.rect.topLeft = x, y
        self.canvas.coords(self.id, self.rect.left, self.rect.top, self.rect.right, self.rect.bottom)