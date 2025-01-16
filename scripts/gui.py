from constants import *
from utils import *
from widgets.button import CustomButton
from widgets.canvas import CustomCanvas
from widgets.task import Task
from rect import Rect
from enums import Direction, Status

from database import Database
from rects import *
from tkinter import Tk, Toplevel, Label, Button, Text, Frame, StringVar, OptionMenu, Event, Misc, TOP, LEFT, BOTTOM
from tkinter import colorchooser, ttk
from tkcalendar import DateEntry

class GUI(Tk):
    
    #region Initialize Methods

    def __init__(self, rect: Rect = WINDOW_RECTS["main"]) -> None:

        super().__init__()
        self.rect = rect
        self.windows = [None for _ in TITLES] # List of windows: infoWindow, detailWindow, addWindow, editWindow
        self.tasks = [[] for _ in Status] # Open, In Progress, Done Task Groups
        self.selectedTask = None
        self.colorchooserValue = None
        self.database = Database(DATABASE_PATH)

        self.themeElements = [[], [], [], []] # items in each list will have same color

        self.SetWindowSettings(self, rect, TITLES[0], None)
        self.CreateWidgets()
        self.LoadTasks()
        self.ChangeTheme(THEME)

    @staticmethod
    def SetWindowSettings(window: Toplevel | Misc, rect: Rect, title: str, color: str) -> None:

        GUI.Centerize(window, rect)
        GUI.SetBackgroundColor(window, color)
        GUI.SetTitle(window, title)
        GUI.SetUnresizable(window)
        GUI.RemoveTitleBar(window)
        window.bind('<Escape>', lambda e: GUI.CloseWindow(window))

    @staticmethod
    def SetUnresizable(window, width: bool = False, height: bool = False) -> None:
        
        window.resizable(width, height)

    @staticmethod
    def RemoveTitleBar(window: Misc) -> None:

        window.overrideredirect(True)

    @staticmethod
    def SetTitle(window: Misc, title: str) -> None:

        window.title(title)

    @staticmethod
    def Centerize(window: Misc, rect: Rect) -> None:

        # Calculating topleft position of window when it is at the center of screen.
        screenWidth, screenHeight = window.winfo_screenwidth(), window.winfo_screenheight()
        topleftX, topleftY = (screenWidth - rect.width) // 2, (screenHeight - rect.height) // 2
        window.geometry(f"{rect.width}x{rect.height}+{topleftX}+{topleftY}")

    @staticmethod
    def SetBackgroundColor(window: Misc, color: str) -> None:
        
        window.configure(bg = color)

    @staticmethod
    def LockWindow(window: Toplevel) -> None:

        window.grab_set()

    @staticmethod
    def FocusWindow(window: Toplevel) -> None:

        window.attributes("-topmost", True)
        window.focus_set()

    @staticmethod
    def CloseWindow(window: Toplevel | Misc | None) -> None:

        if not window.winfo_exists():
            return

        window.destroy()
        
    @staticmethod
    def GetWindowPosition(event, window: Toplevel | Misc, rect: Rect, titleBar: CustomCanvas) -> None:

        topleftX = window.winfo_x()
        topleftY = window.winfo_y()
        startx, starty = event.x_root, event.y_root

        ywin = topleftY - starty
        xwin = topleftX - startx

        def MoveWindow(event) -> None:

            window.geometry(f"{rect.width}x{rect.height}+{event.x_root + xwin}+{event.y_root + ywin}")

        titleBar.bind('<B1-Motion>', MoveWindow)

    @staticmethod
    def GetWindowRect(window: Toplevel | Misc) -> Rect:

        window.update_idletasks() # https://stackoverflow.com/questions/34373533/winfo-width-returns-1-even-after-using-pack
        return Rect(window.winfo_x(), window.winfo_y(), window.winfo_width(), window.winfo_height())

    def CreateTitleBar(self, window: Toplevel | Misc, height: int, title: str, color: str, titleColor: str, titleFont: tuple) -> CustomCanvas:

        windowRect = GUI.GetWindowRect(window)
        rect = Rect(0, 0, windowRect.width, height)

        titleBar = CustomCanvas(window, color, rect)
        titleBar.create_text(rect.center, title, titleColor, titleFont)
        titleBar.bind('<Button-1>', lambda e: GUI.GetWindowPosition(e, window, windowRect, titleBar))

        return titleBar

    def Run(self) -> None:

        self.mainloop()

    #endregion

    #region Main Title Bar Methods

    def Unminimize(self, e):
        
        self.update_idletasks()
        self.overrideredirect(True)
        self.state('normal')

    def Minimize(self):

        self.update_idletasks() # Reference: https://stackoverflow.com/questions/29186327/tclerror-cant-iconify-override-redirect-flag-is-set
        self.overrideredirect(False)
        #self.state('withdrawn')
        self.state('iconic')

        #self.iconify() # Giving error

    #endregion

    #region Database Methods

    def CreateTableIfNotExists(self) -> None:

        self.database.Execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, status TEXT, title TEXT, detail TEXT, color TEXT, deadLine TEXT)")

    def LoadTasks(self) -> None:

        self.CreateTableIfNotExists()
        rows = self.database.FetchAll("SELECT * FROM tasks")

        if not rows:
            return

        for row in rows:
            status, title, detail, color, deadLine = row[1:]
            self.AddNewTask(Status[status], title, detail, color, deadLine)

    def SaveTasks(self) -> None:
        
        self.database.Execute("DELETE FROM tasks")

        for taskGroup in self.tasks:
            for task in taskGroup:
                self.database.Execute("INSERT INTO tasks (status, title, detail, color, deadLine) VALUES (?, ?, ?, ?, ?)", task.status.name, task.title, task.detail, task.color, task.deadLine)

    #endregion

    #region Window Methods

    def GetColor(self, index: int) -> str:

        return THEMES[self.themeVar.get()][index]

    def OpenWindow(self, index: int, rect: Rect, title: str, height: int, textColor: str, font: tuple):

        backgroundColor = self.GetColor(0)
        themeColor = self.GetColor(2)
        window = self.windows[index]
        
        if window and window.winfo_exists():
            return

        window = self.windows[index] = Toplevel(self)
        self.SetWindowSettings(window, rect, title, backgroundColor)
        self.CreateTitleBar(window, height, title, themeColor, textColor, font)
        self.LockWindow(window)
        self.FocusWindow(window)

        if self.selectedTask:
            self.selectedTask.Unselect()
        
        return window

    def OpenInfoWindow(self):
        
        window = self.OpenWindow(0, WINDOW_RECTS["info"], TITLES[1], TITLEBAR_HEIGHT, TEXT_COLOR, TITLE_FONT)
        
        if window is None:
            return
        
        backgroundColor = self.GetColor(0)
        themeColor = self.GetColor(2)

        Label(window, text="Arrow keys: move the selected task\nEnter: Add a task\nDel: Remove the selected task.\n\nMade by Umutcan Ekinci\ngithub.com/umutcanekinci", font=TEXT_FONT, justify='center', bg=backgroundColor, fg=TEXT_COLOR).pack(pady=(50, 0))
        Button(window, text="Close", font=FONT, bg=themeColor, fg=TEXT_COLOR, command=lambda: self.CloseWindow(window)).pack(pady=PADDING, side=BOTTOM)

    def OpenDetailWindow(self, e):

        if not self.selectedTask:
            return
        
        task = self.GetCollidedTask(e.x, e.y)

        if not task:
            return

        window = self.OpenWindow(1, WINDOW_RECTS["detail"], TITLES[2], TITLEBAR_HEIGHT, TEXT_COLOR, TITLE_FONT)
        
        if window is None:
            return
        
        themeColor = self.GetColor(2)
        canvas = CustomCanvas(window, task.color, GetMainCanvasRect(TITLEBAR_HEIGHT, WINDOW_RECTS["detail"]))

        canvas.create_text((PADDING, PADDING * 1 + TITLEBAR_HEIGHT), "TITLE", TEXT_COLOR, BOLD_FONT, 'w')
        canvas.create_text((PADDING, PADDING * 4 + TITLEBAR_HEIGHT), task.title, TEXT_COLOR, TEXT_FONT, 'w')

        canvas.create_text((PADDING, PADDING * 9 + TITLEBAR_HEIGHT), "DETAIL", TEXT_COLOR, BOLD_FONT, 'w')
        canvas.create_text((PADDING, PADDING * 12 + TITLEBAR_HEIGHT), task.detail, TEXT_COLOR, TEXT_FONT, 'w')
        
        canvas.create_text((PADDING, PADDING * 22 + TITLEBAR_HEIGHT), "STATUS", TEXT_COLOR, BOLD_FONT, 'w')
        canvas.create_text((PADDING, PADDING * 25 + TITLEBAR_HEIGHT), task.status.name.replace('_', ' ').title(), TEXT_COLOR, TEXT_FONT, 'w')

        canvas.create_text((PADDING, PADDING * 30 + TITLEBAR_HEIGHT), "DEADLINE", TEXT_COLOR, BOLD_FONT, 'w')
        canvas.create_text((PADDING, PADDING * 33 + TITLEBAR_HEIGHT), task.deadLine, TEXT_COLOR, TEXT_FONT, 'w')

        # Buttons
        ButtonFrame = Frame(window, bg=task.color)
        ButtonFrame.pack(pady=PADDING * 2, side=BOTTOM)

        Button(ButtonFrame, text="Close", font=FONT, bg=themeColor, fg=TEXT_COLOR, command= lambda: self.CloseWindow(window)).pack(side=LEFT, padx=PADDING)
        Button(ButtonFrame, text="Edit", font=FONT, bg=themeColor, fg=TEXT_COLOR, command= self.OpenEditWindow).pack(side=LEFT, padx=PADDING)
        
    def OpenAddWindow(self):

        window = self.OpenWindow(2, WINDOW_RECTS["add"], TITLES[3], TITLEBAR_HEIGHT, TEXT_COLOR, TITLE_FONT)
        
        if window is None:
            return

        backgroundColor = self.GetColor(0)
        themeColor = self.GetColor(2)

        canvas = CustomCanvas(window, backgroundColor, GetMainCanvasRect(TITLEBAR_HEIGHT, WINDOW_RECTS["add"]))

        canvas.create_text((PADDING, TITLEBAR_HEIGHT + PADDING), "Enter the task title:", TEXT_COLOR, FONT, 'w')
        self.titleText = Text(window, font=TEXT_FONT, bg=themeColor, fg=TEXT_COLOR, height=1)
        self.titleText.pack(pady=(TITLEBAR_HEIGHT + PADDING * 6, 0), padx=PADDING, side=TOP)

        canvas.create_text((PADDING, TITLEBAR_HEIGHT + PADDING * 10), "Enter the detail:", TEXT_COLOR, FONT, 'w')
        self.detailText = Text(window, font=TEXT_FONT, bg=themeColor, fg=TEXT_COLOR, height=3)
        self.detailText.pack(pady=(PADDING * 6, 0), padx=PADDING, side=TOP)
        
        self.statusVar = StringVar(window, "Open")
        canvas.create_text((PADDING, TITLEBAR_HEIGHT + PADDING * 24), "Select the status:", TEXT_COLOR, FONT, 'w')
        statusOption = OptionMenu(window, self.statusVar, "Open", "In Progress", "Done")
        statusOption.pack(anchor='nw', pady=PADDING * 3, padx=(PADDING * 22, 0), side=TOP)
        statusOption.config(bg=themeColor, fg=TEXT_COLOR, activeforeground=TEXT_COLOR, activebackground=themeColor, highlightbackground=themeColor, font=FONT)

        canvas.create_text((PADDING, TITLEBAR_HEIGHT + PADDING * 31), "Choose the color:", TEXT_COLOR, FONT, 'w')
        Button(window, text="Choose", font=FONT, bg=themeColor, fg=TEXT_COLOR, command=self.ChooseColor).pack(anchor='nw', padx=(PADDING * 21, 0), pady=0 , side=TOP)

        canvas.create_text((PADDING, TITLEBAR_HEIGHT + PADDING * 39), "Select the deadline:", TEXT_COLOR, FONT, 'w')
        self.deadLineEntry = DateEntry(window, font=TEXT_FONT, firstweekday='monday', selectbackground=themeColor)

        self.deadLineEntry.pack(anchor='nw', padx=(PADDING * 24, 0), pady=PADDING * 3, side=TOP)

        ButtonFrame = Frame(window, bg=backgroundColor)
        ButtonFrame.pack(pady=PADDING * 2, side=BOTTOM)

        Button(ButtonFrame, text="Close", font=FONT, bg=themeColor, fg=TEXT_COLOR, command=lambda: self.CloseWindow(window)).pack(side=LEFT, padx=PADDING)
        Button(ButtonFrame, text="Add", font=FONT, bg=themeColor, fg=TEXT_COLOR, command=self.CheckAddWindow).pack(side='right', padx=PADDING)

    def CheckAddWindow(self):

        title = self.titleText.get("1.0", "end-1c")

        if not title:
            return
        
        status = Status[self.statusVar.get().upper().replace(' ', '_')]
        self.AddNewTask(status, title, self.detailText.get("1.0", "end-1c"), self.colorchooserValue if self.colorchooserValue else self.GetColor(0), self.deadLineEntry.get())

    def OpenEditWindow(self):

        window = self.OpenWindow(2, WINDOW_RECTS["edit"], TITLES[4], TITLEBAR_HEIGHT, TEXT_COLOR, TITLE_FONT)
        
        if not window:
            return


    #endregion

    def ChooseColor(self):

        self.colorchooserValue = colorchooser.askcolor(title ="Choose task color")[1]

    #region Widget Methods

    def CreateWidgets(self):
    
        self.LoadImages()
        self.CreateMainTitleBar()
        self.CreateMainCanvas()
        self.CreateGroups()
        self.CreateAddButtons()
        self.SetKeyBindings()

    def LoadImages(self):

        self.logoImage = GetImage(LOGO_PATH, LOGO_RECT)
        self.infoImage = GetImage(INFO_PATH, INFO_BUTTON_RECT)
        self.exitImage = GetImage(EXIT_PATH, EXIT_BUTTON_RECT)
        self.addImage =  GetImage(ADD_PATH,  ADD_BUTTON_RECT)

    def CreateMainCanvas(self):

        self.mainCanvas = CustomCanvas(self, None, GetMainCanvasRect(MAIN_TITLEBAR_HEIGHT, self.rect))
        self.mainCanvas.bind("<Map>", self.Unminimize)
        self.mainCanvas.bind('<Button-1>', self.SelectTask)
        self.themeElements[0].append(self.mainCanvas)

    def CreateMainTitleBar(self):

        # Title Bar
        self.titleBar = self.CreateTitleBar(self, MAIN_TITLEBAR_HEIGHT, '', None, TEXT_COLOR, TITLE_FONT)
        self.themeElements[2].append(self.titleBar)
        self.titleBar.create_image(LOGO_RECT, self.logoImage)
        self.titleBar.create_text(TITLE_POSITION, TITLES[0], TEXT_COLOR, TITLE_FONT, 'w')
        
        # Title Bar Buttons
        self.themeVar = StringVar(self, THEME)
        #canvas.create_text((PADDING, TITLEBAR_HEIGHT + PADDING * 24), "Select the status:", TEXT_COLOR, FONT, 'w')
        themeOption = OptionMenu(self, self.themeVar, *THEMES.keys(), command=self.ChangeTheme)
        themeOption.place(anchor='w', x=THEME_OPTION_RECT.x, y=THEME_OPTION_RECT.y, width=THEME_OPTION_RECT.width, height=THEME_OPTION_RECT.height)
        themeOption.config(fg=TEXT_COLOR, activeforeground=TEXT_COLOR, font=BUTTON_FONT)
        self.themeElements[2].append(themeOption)

        self.themeElements[2].append(CustomButton(self.titleBar, INFO_BUTTON_RECT, self.OpenInfoWindow, None, self.infoImage))
        CustomButton(self.titleBar, MINIMIZE_BUTTON_RECT, self.Minimize, TEXT_COLOR, None)
        self.themeElements[2].append(CustomButton(self.titleBar, EXIT_BUTTON_RECT, lambda: self.CloseWindow(self), None, image=self.exitImage))
        
    def CreateGroups(self):

        for groupStatus in Status:
            
            self.CreateAGroup(groupStatus)
    
    def CreateAGroup(self, status: Status):

        self.themeElements[1].append(self.mainCanvas.create_rectangle(GetGroupRect(status)))
        self.mainCanvas.create_rectangle(GetTitleBoxRect(status), TEXTBOX_COLORS[status.value])
        self.mainCanvas.create_text(GetTitleBoxRect(status).center, TASK_GROUPS[status.value], TEXT_COLOR, BOLD_FONT)

    def SetKeyBindings(self):

        self.bind('<Right>', lambda e: self.MoveHorizontally(Direction.RIGHT))
        self.bind('<Left>', lambda e: self.MoveHorizontally(Direction.LEFT))
        self.bind('<Down>', lambda e: self.MoveVertically(Direction.DOWN))
        self.bind('<Up>', lambda e: self.MoveVertically(Direction.UP))
        self.bind('<Delete>', lambda e: self.RemoveTask(self.selectedTask))
        self.bind('<Double-Button-1>', self.OpenDetailWindow)

    def ChangeTheme(self, value):
        
        theme = THEMES[self.themeVar.get()]

        for i, element in enumerate(self.themeElements):
            for item in element:

                color = theme[i]

                if hasattr(item, 'ChangeColor'):
                    item.ChangeColor(color)

                elif type(item) == int:
                    self.mainCanvas.itemconfig(item, fill=color)
                
                elif type(item) == OptionMenu:
                    item.config(bg=color, activebackground=color, highlightbackground=color)

        if self.selectedTask:
            self.selectedTask.Select(self.GetColor(3))

        for addButton in self.addButtons:
            addButton.ChangeColor(theme[1])

    #endregion

    #region Task Methods

    def GetGroup(self, status: str):

        if status is None:
            raise ValueError("Status is None")
        
        return self.tasks[status.value]

    def AddNewTask(self, status: str, title: str, detail: str, color: str, deadLine: str):

        if status is None:
            raise ValueError("Status is None")

        if not title or not color or not deadLine:
            return

        self.GetGroup(status).append(Task(self.mainCanvas, GetTaskRect(), color, status, title, detail, deadLine))
        self.UpdateTasksPosition(status)

    def RemoveTask(self, task: Task):
        
        if task is None:
            raise ValueError("Task is None")

        self.RemoveTaskFromList(task)
        self.mainCanvas.delete(task.id)
        self.mainCanvas.delete(task.textId)
        self.selectedTask = None

    def RemoveTaskFromList(self, task: Task):
        
        if task is None:
            return
        
        self.GetGroup(task.status).remove(task)
        self.UpdateTasksPosition(task.status)

    def GetCollidedTask(self, x: int, y: int):

        for task in sum(self.tasks, []):
            if task.isCollide(x, y):
                return task
        return None

    def SelectTask(self, event: Event):

        collided_task = self.GetCollidedTask(event.x, event.y)

        if self.selectedTask:
            self.selectedTask.Unselect()
        
        if self.selectedTask is collided_task:
            self.selectedTask = None
            return
        
        if collided_task:
            collided_task.Select(self.GetColor(3))
            
        self.selectedTask = collided_task
        
    def UpdateTasksPosition(self, status: Status):

        if status is None:
            raise ValueError("Status is None")

        group = self.GetGroup(status)

        if group is None:
            raise ValueError("List is None")
        
        for i, task in enumerate(group):
        
            if i:
                task.MoveTo(GetGroupRect(status).left + PADDING, group[i - 1].rect.bottom + PADDING)
                continue
            
            task.MoveTo(GetGroupRect(task.status).left + PADDING, GetTitleBoxRect(task.status).bottom + PADDING)

        self.UpdateAddButtonPosition(status)

    #region Add Button Functions

    def CreateAddButtons(self):

        self.addButtons = []
        for status in Status:
            self.addButtons.append(CustomButton(self.mainCanvas, Rect(), self.OpenAddWindow, None, self.addImage))
            self.UpdateTasksPosition(status)

    def GetAddButton(self, status: str):

        if status is None:
            raise ValueError("Status is None")

        return self.addButtons[status.value]

    def UpdateAddButtonPosition(self, status: Status):

        group = self.GetGroup(status)        

        if not group:
            self.GetAddButton(status).place(Rect(GetGroupRect(status).centerX - ADD_BUTTON_RECT.width // 2, GetGroupRect(status).top + TITLE_BOX_HEIGHT + PADDING * 2, ADD_BUTTON_RECT.width, ADD_BUTTON_RECT.height))
            return
        
        lastTask = group[-1]

        if lastTask.rect.bottom + PADDING * 2 + MIN_TASK_HEIGHT > GetGroupRect(status).bottom:
            self.GetAddButton(status).place_forget()
            return

        self.GetAddButton(status).place(GetAddButtonRect(lastTask.rect))
        

    #endregion

    def MoveHorizontally(self, direction: Direction):

        if not self.selectedTask or not direction:
            return
        
        canMoveRight = direction == Direction.RIGHT and self.selectedTask.status is not Status.DONE
        canMoveLeft = direction == Direction.LEFT and self.selectedTask.status is not Status.OPEN

        if not (canMoveRight or canMoveLeft):
            return
        
        self.RemoveTaskFromList(self.selectedTask)
        self.selectedTask.status = Status(self.selectedTask.status.value + direction.value) 
        self.GetGroup(self.selectedTask.status).append(self.selectedTask)
        self.UpdateTasksPosition(self.selectedTask.status)

    def MoveVertically(self, direction : Direction):

        if not self.selectedTask or not direction:
            return

        tasks = self.GetGroup(self.selectedTask.status)
        index = tasks.index(self.selectedTask)

        canMoveDown = direction == Direction.DOWN and index != len(tasks) - 1
        canMoveUp = direction == Direction.UP and index != 0

        if not (canMoveDown or canMoveUp):
            return
        
        tasks[index], tasks[index + direction.value] = tasks[index + direction.value], tasks[index]
        self.UpdateTasksPosition(self.selectedTask.status)

    #endregion

