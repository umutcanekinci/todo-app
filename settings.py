from rect import Rect

#region PATH

ASSETS_PATH = "assets/"

#endregion

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

BACKGROUND_COLOR = BLACK
TOPBAR_COLOR = BLUE
TEXT_COLOR = WHITE

#endregion

#region RECTS

WINDOW_RECT = Rect(0, 0, 1440, 900)
INFO_RECT =   Rect(0, 0, 400, 200)
TOPBAR_RECT = Rect(0, 0, WINDOW_RECT.width, 40)
LOGO_RECT =   Rect(32.0, 21.0, 25, 25)
TITLE_RECT =  Rect(50, 8)

INFO_BUTTON_RECT =     Rect(WINDOW_RECT.width - 105, 8, 25, 25)
MINIMIZE_BUTTON_RECT = Rect(WINDOW_RECT.width - 70,  18, 25, 5)
EXIT_BUTTON_RECT =     Rect(WINDOW_RECT.width - 35,  8,  25, 25)

OPEN_RECT =        Rect(10,                          50, 466, 880)
IN_PROGRESS_RECT = Rect(OPEN_RECT.right + 10,        50, 466, 880)
DONE_RECT =        Rect(IN_PROGRESS_RECT.right + 10, 50, 466, 880)

OPEN_TITLE_BOX_RECT =        Rect(OPEN_RECT.x, OPEN_RECT.y, OPEN_RECT.width, 40)
IN_PROGRESS_TITLE_BOX_RECT = Rect(IN_PROGRESS_RECT.x, IN_PROGRESS_RECT.y, IN_PROGRESS_RECT.width, 40)
DONE_TITLE_BOX_RECT =        Rect(DONE_RECT.x, DONE_RECT.y, DONE_RECT.width, 40)

OPEN_TITLE_RECT =        Rect(OPEN_RECT.centerX - 25,        OPEN_RECT.y + 10)
IN_PROGRESS_TITLE_RECT = Rect(IN_PROGRESS_RECT.centerX - 75, IN_PROGRESS_RECT.y + 10)
DONE_TITLE_RECT =        Rect(DONE_RECT.centerX - 25,        DONE_RECT.y + 10)

ELEMENT_RECT = Rect(OPEN_RECT.x + 10, OPEN_TITLE_BOX_RECT.bottom + 10, OPEN_RECT.width - 20, OPEN_TITLE_BOX_RECT.height * 2)

#endregion

TITLE = "TODO APP"
FONT = ("Inter", 23 * -1)
