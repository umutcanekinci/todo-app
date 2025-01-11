from rect import Rect

#region COLORS

# Using that color palette for this application in order to get a harmonical and beatiful color theme:
# https://colorhunt.co/palette/222831393e4600adb5eeeeee
BLACK = "#222831"
GRAY = "#393E46"
BLUE = "#00ADB5"
WHITE = "#EEEEEE"
RED = "#CDC1FF"
YELLOW = "#FFC145"
GREEN = "#5CB338"

TOP_COLOR = BLUE
MAIN_COLOR = BLACK
TEXT_COLOR = WHITE

#endregion

#region RECTS

# Window Rects
WINDOW_RECT = Rect(0, 0, 1440, 900)
INFO_RECT =   Rect(0, 0, 400, 200)

PADDING = 10
ICON_SIZE = 25
PANEL_WIDTH = 466
TITLE_BOX_HEIGHT = 40
ELEMENT_HEIGHT = 80

# Canvas Rects
TOP_RECT = Rect(0, 0, WINDOW_RECT.width, 45)
MAIN_RECT = Rect(0, TOP_RECT.bottom, WINDOW_RECT.width, WINDOW_RECT.height - TOP_RECT.height)

# Top Widgets Rects
LOGO_RECT =   Rect(0, 21, 25, 25)
TITLE_RECT =  Rect(50, 8)
EXIT_BUTTON_RECT =     Rect(WINDOW_RECT.width         - ICON_SIZE - PADDING,  PADDING,     ICON_SIZE, ICON_SIZE)
MINIMIZE_BUTTON_RECT = Rect(EXIT_BUTTON_RECT.left     - ICON_SIZE - PADDING,  PADDING * 2, ICON_SIZE, ICON_SIZE // 5)
INFO_BUTTON_RECT =     Rect(MINIMIZE_BUTTON_RECT.left - ICON_SIZE - PADDING,  PADDING,     ICON_SIZE, ICON_SIZE)


OPEN_RECT =        Rect(PADDING,                          PADDING, PANEL_WIDTH, WINDOW_RECT.height - PADDING * 2)   
IN_PROGRESS_RECT = Rect(OPEN_RECT.right + PADDING,        PADDING, PANEL_WIDTH, WINDOW_RECT.height - PADDING * 2)
DONE_RECT =        Rect(IN_PROGRESS_RECT.right + PADDING, PADDING, PANEL_WIDTH, WINDOW_RECT.height - PADDING * 2)

OPEN_TITLE_BOX_RECT =        Rect(OPEN_RECT.x,        OPEN_RECT.y,        OPEN_RECT.width,        TITLE_BOX_HEIGHT)
IN_PROGRESS_TITLE_BOX_RECT = Rect(IN_PROGRESS_RECT.x, IN_PROGRESS_RECT.y, IN_PROGRESS_RECT.width, TITLE_BOX_HEIGHT)
DONE_TITLE_BOX_RECT =        Rect(DONE_RECT.x,        DONE_RECT.y,        DONE_RECT.width,        TITLE_BOX_HEIGHT)

OPEN_TITLE_RECT =        Rect(OPEN_RECT.centerX - 25,        OPEN_RECT.y + 10)
IN_PROGRESS_TITLE_RECT = Rect(IN_PROGRESS_RECT.centerX - 75, IN_PROGRESS_RECT.y + 10)
DONE_TITLE_RECT =        Rect(DONE_RECT.centerX - 25,        DONE_RECT.y + 10)

ELEMENT_RECT = Rect(0, OPEN_TITLE_BOX_RECT.bottom + PADDING, OPEN_RECT.width - PADDING * 2, ELEMENT_HEIGHT)

#endregion

TITLE = "TODO APP"
FONT = ("Inter", 23 * -1)
