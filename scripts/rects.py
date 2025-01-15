from rect import Rect
from constants import *

WINDOW_RECTS = {
    "main"   : Rect(0, 0, *WINDOW_SIZES["main"]),
    "info"   : Rect(0, 0, *WINDOW_SIZES["info"]),
    "detail" : Rect(0, 0, *WINDOW_SIZES["detail"]),
    "add"    : Rect(0, 0, *WINDOW_SIZES["add"]),
    "edit"   : Rect(0, 0, *WINDOW_SIZES["add"])
}

ADD_BUTTON_RECT      = Rect(0, 0, *ICON_SIZE)

# Top Widget Rects
LOGO_RECT            = Rect(*LOGO_POSITION, *LOGO_SIZE)
EXIT_BUTTON_RECT     = Rect(WINDOW_RECTS["main"].width - ICON_SIZE[0] - PADDING, PADDING, *ICON_SIZE)
MINIMIZE_BUTTON_RECT = Rect(EXIT_BUTTON_RECT.left      - ICON_SIZE[0] - PADDING, PADDING * 2, ICON_SIZE[0], ICON_SIZE[1] // 5)
INFO_BUTTON_RECT     = Rect(MINIMIZE_BUTTON_RECT.left  - ICON_SIZE[0] - PADDING, PADDING, *ICON_SIZE)
THEME_OPTION_RECT    = Rect(INFO_BUTTON_RECT.left - PADDING * 13, MAIN_TITLEBAR_HEIGHT // 2, 120, MAIN_TITLEBAR_HEIGHT - PADDING * 2 + 5)

