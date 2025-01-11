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
    
    def create_text(self, rect: Rect, text: str, color: str, font, anchor: str = "nw"):

        return super().create_text(rect.x, rect.y, anchor=anchor, text=text, fill=color, font=font)
    
    def create_rectangle(self, rect: Rect, color: str):

        return super().create_rectangle(rect.left, rect.top, rect.right, rect.bottom, fill=color)