from tkinter import *
from scripts.rect import Rect

class CustomButton(Button):

    def __init__(self, master: Misc | None, rect: Rect, onClick, color: str, image: PhotoImage):
        
        super().__init__(master,
            image=image,
            borderwidth=0,
            highlightthickness=0,
            command=onClick,
            bg=color,
            activebackground=color,
            relief="flat"
        )

        self.place(rect)

    def place(self, rect: Rect):
        
        super().place(x=rect.x, y=rect.y, width=rect.width, height=rect.height)