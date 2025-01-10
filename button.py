from tkinter import *

class CustomButton(Button):

    def __init__(self, master: Misc | None, onClick, color: str, image: PhotoImage):
        
        super().__init__(master,
            image=image,
            borderwidth=0,
            highlightthickness=0,
            command=onClick,
            bg=color,
            activebackground=color,
            relief="flat"
        )

    def place(self, rect: tuple[int, int, int, int]):
        
        super().place(x=rect[0], y=rect[1], width=rect[2], height=rect[3])