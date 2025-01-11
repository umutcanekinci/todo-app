from rect import Rect

class Element:
    
    OPEN = 0
    IN_PROGRESS = 1
    DONE = 2

    def __init__(self, canvas, rect: Rect, color: str, selectedColor: str, status: int):
        
        self.rect = rect
        self.color, self.selectedColor = color, selectedColor
        self.status = status
        self.canvas = canvas
        self.id =  canvas.create_rectangle(rect, color)
        

    def isCollide(self, x: int, y: int):

        return x > self.rect.left and x < self.rect.right and y < self.rect.bottom and y > self.rect.top

    def Select(self):

        self.canvas.itemconfig(self.id, fill=self.selectedColor)

    def Unselect(self):

        self.canvas.itemconfig(self.id, fill=self.color)

    def MoveTo(self, x: int, y: int):

        self.rect.topLeft = x, y
        self.canvas.coords(self.id, self.rect.left, self.rect.top, self.rect.right, self.rect.bottom)