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

    if not rect or x == None or y == None:
        return None
    
    return x > rect.left and x < rect.right and y > rect.top and y < rect.bottom

#region GetRects

def GetTitleBoxRect(status: Status) -> Rect:

    return Rect(PADDING + (GROUP_WIDTH + PADDING) * status.value, PADDING, GROUP_WIDTH, TITLE_BOX_HEIGHT)

def GetGroupRect(status: Status) -> Rect:

    return Rect(PADDING + (GROUP_WIDTH + PADDING) * status.value,TITLE_BOX_HEIGHT + PADDING * 2, GROUP_WIDTH, GetMainCanvasRect(MAIN_TITLEBAR_HEIGHT, WINDOW_RECTS["main"]).height - PADDING * 2 - TITLE_BOX_HEIGHT)

def GetMainCanvasRect(titleBarHeight: int, windowRect: Rect) -> Rect:

    return Rect(0, titleBarHeight, windowRect.width, windowRect.height - titleBarHeight)

def GetTaskRect() -> Rect:

    return Rect(0, 0, GROUP_WIDTH - PADDING * 2, MIN_TASK_HEIGHT)

def GetNextTaskPosition(status, group, i: int) -> tuple[int]:

    if not status or i == None:
        return None

    return PADDING, group[i - 1].rect.bottom + PADDING if i else PADDING

#endregion