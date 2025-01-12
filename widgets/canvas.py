from tkinter import *
from rect import Rect
class CustomCanvas(Canvas):

    def __init__(self, master: Misc | None, color: str, rect: Rect):
        
        self.rect = rect
        super().__init__(
            master,
            bg = color,
            width = rect.width,
            height = rect.height,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.place(x=rect.x, y=rect.y)

    def create_image(self, rect: Rect, image: PhotoImage):
        
        return super().create_image(rect.x, rect.y, image=image)
    
    def create_text(self, position: tuple[int], text: str, color: str, font, anchor: str = 'center'):

        return super().create_text(*position, anchor=anchor, text=text, fill=color, font=font)
        
    def create_rectangle(self, rect: Rect, color: str):

        return super().create_rectangle(rect.left, rect.top, rect.right, rect.bottom, fill=color)
    
    def GetItemWidth(self, id: int):

        return self.bbox(id)[2] - self.bbox(id)[0]
    
    def GetItemHeight(self, id: int):

        return self.bbox(id)[3] - self.bbox(id)[1]

    def GetItemSize(self, id: int):

        return self.GetItemWidth(id), self.GetItemHeight(id)
    
    def SetItemWidth(self, id: int, width: int):

        self.itemconfig(id, width=width)

    def SetItemHeight(self, id: int, height: int):

        self.itemconfig(id, height=height)

    def SetItemSize(self, id: int, width: int, height: int):

        self.itemconfig(id, width=width, height=height)
    
    def SetRectanglePosition(self, id: int, rect: Rect):

        self.coords(id, rect.left, rect.top, rect.right, rect.bottom)

    def SetTextPosition(self, id: int, position: tuple[int]):

        self.coords(id, *position)