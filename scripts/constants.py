DATABASE_PATH = "database.db"

GROUPS = "OPEN", "IN PROGRESS", "DONE"
TITLES = "TODO APP", "INFO", "DETAILS", "ADD NEW TASK", "EDIT TASK"

#region FONTS

TEXT_FONT = ("Inter", 22 * -1)
FONT = ("Inter", 24 * -1)
BOLD_FONT = ("Inter", 24 * -1, 'bold')
TITLE_FONT = ("Inter", 25 * -1)
BUTTON_FONT = ("Inter", 20 * -1)
#endregion

#region COLORS

TEXT_COLOR = 'white'
THEME = 'Green'
THEMES = {
            'Brown' : ["#2C3639", "#3F4E4F", "#A27B5C", "#DCD7C9"],
            'Purple' : ["#1A1A2E", "#30305C", "#4F4F89", "#6968B3"],
            'Green' : ["#1B4332", "#2D6A4F", "#40916C", "#52B788"]
        }

TEXTBOX_COLORS = ["#578E7E", "#F08A5D", "#5CB338"]

#endregion

#region SIZES

# Window Sizes
WINDOW_SIZES = {
    "main" : (1440, 900),
    "info" : (550, 300),
    "detail" : (550, 600),
    "add" :  (550, 600)
}

PADDING = 10
ICON_SIZE = 25, 25
LOGO_SIZE = 35, 35
MAIN_TITLEBAR_HEIGHT = 45
TITLEBAR_HEIGHT = 30
TITLE_BOX_HEIGHT = 40
MIN_TASK_HEIGHT = 60 
GROUP_WIDTH = (WINDOW_SIZES["main"][0] - PADDING *  (len(GROUPS) + 1)) // len(GROUPS)
SCROLLBAR_WIDTH = 10
LOGO_POSITION = PADDING * 3, 21
TITLE_POSITION =  56, MAIN_TITLEBAR_HEIGHT // 2


#endregion


#region IMAGES

LOGO_PATH = "logo.png"
INFO_PATH = "info.png"
EXIT_PATH = "exit_button.png"
ADD_PATH =  "add_button.png"

#endregion
