from rect import Rect

class Element:
    
    OPEN = "STATUS_OPEN"
    IN_PROGRESS = "STATUS_IN_PROGRESS"
    DONE = "STATUS_IN_PROGRESS"

    def __init__(self, canvas, rect: Rect, color: str, selectedColor: str, status: str):
        
        self.rect = rect
        self.color, self.selectedColor = color, selectedColor
        self.status = status
        self.canvas = canvas
        self.id =  canvas.create_rectangle(rect, color)
        

    def isCollide(self, x: int, y: int):

        return x > self.rect.left and x < self.rect.right and y < self.rect.bottom and y > self.rect.top

    def Move(self, x: int, y: int):

        self.rect.topLeft = x, y
        self.canvas.coords(self.id, )

    def Select(self):

        self.canvas.itemconfig(self.id, fill=self.selectedColor)

    def Unselect(self):

        self.canvas.itemconfig(self.id, fill=self.color)