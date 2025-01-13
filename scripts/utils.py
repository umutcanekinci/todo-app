from PIL import Image, ImageTk
from rect import Rect
from datetime import datetime

def GetImage(file: str, rect: Rect):

    # PhotoImage(file="'./assets/'+file") # Does not working for pngs somehow
    return ImageTk.PhotoImage(Image.open('./assets/' + file).resize(rect.size))

def isOverdue(deadLine: str):

    return deadLine < datetime.now().strftime("%Y-%m-%d %H:%M:%S")