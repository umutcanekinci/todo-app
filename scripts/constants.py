DATABASE_PATH = "database.db"

#region TITLES

TITLE = "TODO APP"
INFO_TITLE = "INFO"
DETAIL_TITLE = "DETAILS"
ADD_TITLE = "ADD NEW TASK"

#endregion

#region FONTS

TEXT_FONT = ("Inter", 22 * -1)
FONT = ("Inter", 24 * -1)
BOLD_FONT = ("Inter", 24 * -1, 'bold')
TITLE_FONT = ("Inter", 25 * -1)

#endregion

#region COLORS

# Using that color palette for this application in order to get a harmonical and beatiful color theme:
# https://colorhunt.co/palette/222831393e4600adb5eeeeee

BLACK = "#2C3639"
GRAY = "#3F4E4F"
BLUE = "#A27B5C"
WHITE = "#DCD7C9"

RED = "#578E7E"
YELLOW = "#F08A5D"
GREEN = "#5CB338"

BORDER_COLOR = BLUE
TEXT_COLOR = WHITE
TITLEBAR_COLOR = BLUE
MAIN_COLOR = BLACK

OPEN_COLOR = RED
IN_PROGRESS_COLOR = YELLOW
DONE_COLOR = GREEN

#endregion

#region SIZES

WINDOW_SIZE = 1440, 900
INFO_SIZE = 550, 300
DETAIL_SIZE = 550, 600
ADD_SIZE = 550, 600

PADDING = 10
ICON_SIZE = 25
LOGO_SIZE = 35

MAIN_TITLEBAR_HEIGHT = 45
TITLEBAR_HEIGHT = 30

PANEL_WIDTH = 466
TITLE_BOX_HEIGHT = 40
TASK_HEIGHT = 60 # This is initial height of the tasks but it can be changed according to the text size

#endregion

#region RECTS

TITLE_POSITION =  56, MAIN_TITLEBAR_HEIGHT // 2

from rect import Rect

# Window Rects
WINDOW_RECT = Rect(0, 0, *WINDOW_SIZE)
INFO_RECT =   Rect(0, 0, *INFO_SIZE)
DETAIL_RECT = Rect(0, 0, *DETAIL_SIZE)
ADD_RECT =    Rect(0, 0, *ADD_SIZE)

# Canvas Rects
MAIN_RECT = Rect(0, MAIN_TITLEBAR_HEIGHT, WINDOW_RECT.width, WINDOW_RECT.height - TITLEBAR_HEIGHT)
DETAIL_MAIN_RECT = Rect(0, TITLEBAR_HEIGHT, DETAIL_RECT.width, DETAIL_RECT.height - TITLEBAR_HEIGHT)
ADD_MAIN_RECT = Rect(0, TITLEBAR_HEIGHT, ADD_RECT.width, ADD_RECT.height - TITLEBAR_HEIGHT)
# Top Widgets Rects
LOGO_RECT =   Rect(PADDING * 3, 21, LOGO_SIZE, LOGO_SIZE)
EXIT_BUTTON_RECT =     Rect(WINDOW_RECT.width         - ICON_SIZE - PADDING,  PADDING,     ICON_SIZE, ICON_SIZE)
MINIMIZE_BUTTON_RECT = Rect(EXIT_BUTTON_RECT.left     - ICON_SIZE - PADDING,  PADDING * 2, ICON_SIZE, ICON_SIZE // 5)
INFO_BUTTON_RECT =     Rect(MINIMIZE_BUTTON_RECT.left - ICON_SIZE - PADDING,  PADDING,     ICON_SIZE, ICON_SIZE)
ADD_BUTTON_RECT = Rect(0, 0, ICON_SIZE, ICON_SIZE)
DETAIL_CLOSE_BUTTON_RECT = Rect(DETAIL_RECT.width - ICON_SIZE - PADDING // 2, DETAIL_RECT.bottom - ICON_SIZE - PADDING // 2, ICON_SIZE, ICON_SIZE)

OPEN_RECT =        Rect(PADDING,                          PADDING, PANEL_WIDTH, MAIN_RECT.height - PADDING * 2)   
IN_PROGRESS_RECT = Rect(OPEN_RECT.right + PADDING,        PADDING, PANEL_WIDTH, MAIN_RECT.height - PADDING * 2)
DONE_RECT =        Rect(IN_PROGRESS_RECT.right + PADDING, PADDING, PANEL_WIDTH, MAIN_RECT.height - PADDING * 2)

OPEN_TITLE_BOX_RECT =        Rect(OPEN_RECT.x,        OPEN_RECT.y,        OPEN_RECT.width,        TITLE_BOX_HEIGHT)
IN_PROGRESS_TITLE_BOX_RECT = Rect(IN_PROGRESS_RECT.x, IN_PROGRESS_RECT.y, IN_PROGRESS_RECT.width, TITLE_BOX_HEIGHT)
DONE_TITLE_BOX_RECT =        Rect(DONE_RECT.x,        DONE_RECT.y,        DONE_RECT.width,        TITLE_BOX_HEIGHT)

TASK_RECT = Rect(0, OPEN_TITLE_BOX_RECT.bottom + PADDING, PANEL_WIDTH - PADDING * 2, TASK_HEIGHT)

#endregion

#region IMAGES

LOGO_PATH = "logo.png"
INFO_PATH = "info.png"
EXIT_PATH = "exit_button.png"
ADD_PATH =  "add_button.png"

#endregion