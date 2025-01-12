TITLE = "TODO APP"
INFO_TITLE = "INFO"
FONT = ("Inter", 23 * -1, 'bold')
TITLE_FONT = ("Inter", 25 * -1)

#region COLORS

# Using that color palette for this application in order to get a harmonical and beatiful color theme:
# https://colorhunt.co/palette/222831393e4600adb5eeeeee

BLACK = "#2C3639"
GRAY = "#3F4E4F"
BLUE = "#A27B5C"

#BLACK = "#222831"
WHITE = "#DCD7C9"

RED = "#578E7E"
YELLOW = "#F08A5D"
GREEN = "#5CB338"

BORDER_COLOR = BLUE
TEXT_COLOR = WHITE
TOP_COLOR = BLUE
MAIN_COLOR = BLACK

OPEN_COLOR = RED
IN_PROGRESS_COLOR = YELLOW
DONE_COLOR = GREEN

#endregion

#region SIZES

WINDOW_SIZE = (1440, 900)
INFO_SIZE = (550, 300)
PADDING = 10
ICON_SIZE = 25
LOGO_SIZE = 35
TOP_HEIGHT = 45
TOP_INFO_HEIGHT = 30
PANEL_WIDTH = 466
TITLE_BOX_HEIGHT = 40
ELEMENT_HEIGHT = 60 # This is initial height of the element but it can be changed according to the text size

#endregion

#region RECTS

from rect import Rect

# Window Rects
WINDOW_RECT = Rect(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1])
INFO_RECT =   Rect(0, 0, INFO_SIZE[0], INFO_SIZE[1])

# Canvas Rects
TOP_RECT = Rect(0, 0, WINDOW_RECT.width, TOP_HEIGHT)
MAIN_RECT = Rect(0, TOP_RECT.bottom, WINDOW_RECT.width, WINDOW_RECT.height - TOP_RECT.height)

# Top Widgets Rects
LOGO_RECT =   Rect(PADDING * 3, 21, LOGO_SIZE, LOGO_SIZE)
EXIT_BUTTON_RECT =     Rect(WINDOW_RECT.width         - ICON_SIZE - PADDING,  PADDING,     ICON_SIZE, ICON_SIZE)
MINIMIZE_BUTTON_RECT = Rect(EXIT_BUTTON_RECT.left     - ICON_SIZE - PADDING,  PADDING * 2, ICON_SIZE, ICON_SIZE // 5)
INFO_BUTTON_RECT =     Rect(MINIMIZE_BUTTON_RECT.left - ICON_SIZE - PADDING,  PADDING,     ICON_SIZE, ICON_SIZE)
ADD_BUTTON_RECT = Rect(0, 0, ICON_SIZE, ICON_SIZE)

OPEN_RECT =        Rect(PADDING,                          PADDING, PANEL_WIDTH, MAIN_RECT.height - PADDING * 2)   
IN_PROGRESS_RECT = Rect(OPEN_RECT.right + PADDING,        PADDING, PANEL_WIDTH, MAIN_RECT.height - PADDING * 2)
DONE_RECT =        Rect(IN_PROGRESS_RECT.right + PADDING, PADDING, PANEL_WIDTH, MAIN_RECT.height - PADDING * 2)

OPEN_TITLE_BOX_RECT =        Rect(OPEN_RECT.x,        OPEN_RECT.y,        OPEN_RECT.width,        TITLE_BOX_HEIGHT)
IN_PROGRESS_TITLE_BOX_RECT = Rect(IN_PROGRESS_RECT.x, IN_PROGRESS_RECT.y, IN_PROGRESS_RECT.width, TITLE_BOX_HEIGHT)
DONE_TITLE_BOX_RECT =        Rect(DONE_RECT.x,        DONE_RECT.y,        DONE_RECT.width,        TITLE_BOX_HEIGHT)

ELEMENT_RECT = Rect(0, OPEN_TITLE_BOX_RECT.bottom + PADDING, OPEN_RECT.width - PADDING * 2, ELEMENT_HEIGHT)

#endregion

#region TEXT RECTS

TITLE_RECT =  Rect(56, 9)
INFO_TITLE_RECT = Rect(INFO_RECT.centerX - 30, 3)
OPEN_TITLE_RECT =        Rect(OPEN_RECT.centerX - 25,        OPEN_RECT.y + PADDING - 1)
IN_PROGRESS_TITLE_RECT = Rect(IN_PROGRESS_RECT.centerX - 75, IN_PROGRESS_RECT.y + PADDING - 1)
DONE_TITLE_RECT =        Rect(DONE_RECT.centerX - 25,        DONE_RECT.y + PADDING - 1)

#endregion

#region IMAGES

LOGO_IMAGE = "logo.png"
INFO_IMAGE = "info.png"
EXIT_IMAGE = "exit_button.png"
ADD_IMAGE = "add_button.png"
#endregion
