from tkinter import *
from rect import Rect


class CustomButton(Button):

    def __init__(self, master: Misc | None, rect: Rect, onClick, color: str, image: PhotoImage, text=''):
        
        super().__init__(master,
            image=image,
            text = text,
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

    def ChangeColor(self, color: str):

        self.config(bg=color, activebackground=color)