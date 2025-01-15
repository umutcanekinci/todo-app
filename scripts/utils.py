from PIL import Image, ImageTk
from rect import Rect
from datetime import datetime
from rects import *
from enums import Status

def GetImage(file: str, rect: Rect):

    if not file or not rect:
        return None
    
    if type(file) is not str or type(rect) is not Rect:
        return None

    # PhotoImage(file="'./assets/'+file") # Does not working for pngs somehow
    return ImageTk.PhotoImage(Image.open('./assets/' + file).resize(rect.size))
 
def isOverdue(deadLine: str):

    if not deadLine:
        return None
    
    if type(deadLine) is not str:
        return None

    return deadLine < datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def isPointInRectangle(rect: Rect, x: int, y: int):

    if not rect or x != None or y != None:
        return None
    
    return x > rect.left and x < rect.right and y > rect.top and y < rect.bottom

#region GetRects

def GetAddButtonRect(lastTaskRect: Rect) -> Rect:

    return Rect(lastTaskRect.centerX - ADD_BUTTON_RECT.width // 2, lastTaskRect.bottom + PADDING * 2, ADD_BUTTON_RECT.width, ADD_BUTTON_RECT.height)

def GetGroupRect(status: Status) -> Rect:

    return Rect(PADDING + (GROUP_WIDTH + PADDING) * status.value, PADDING, GROUP_WIDTH, GetMainCanvasRect(MAIN_TITLEBAR_HEIGHT, WINDOW_RECTS["main"]).height - PADDING * 2)

def GetTitleBoxRect(status: Status) -> Rect:

    return Rect(*GetGroupRect(status).topLeft, GROUP_WIDTH, TITLE_BOX_HEIGHT)

def GetMainCanvasRect(titleBarHeight: int, windowRect: Rect) -> Rect:

    return Rect(0, titleBarHeight, windowRect.width, windowRect.height - titleBarHeight)

def GetTaskRect() -> Rect:

    return Rect(0, 0, GROUP_WIDTH - PADDING * 2, MIN_TASK_HEIGHT)

#endregion