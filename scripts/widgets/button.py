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
        
        self.rect = rect
        self.place(rect.center)

    def place(self, position: tuple[int]):

        self.rect.center = position        
        super().place(x=position[0], y=position[1], width=self.rect.width, height=self.rect.height, anchor='center')

    def ChangeColor(self, color: str):

        self.config(bg=color, activebackground=color)