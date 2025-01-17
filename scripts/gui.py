from constants import *
from utils import *
from widgets.button import CustomButton
from widgets.canvas import CustomCanvas
from widgets.task import Task
from rect import Rect
from enums import Direction, Status
from group import Group

from database import Database
from rects import *
from tkinter import Tk, Toplevel, Label, Button, Text, Frame, StringVar, OptionMenu, Event, Misc, TOP, LEFT, BOTTOM
from tkinter import colorchooser, ttk
from tkcalendar import DateEntry

class GUI(Tk):
    
    #region Initialize Methods

    def __init__(self) -> None:

        super().__init__()

        self.windows       = [None for _ in TITLES] # List of windows: infoWindow, detailWindow, addWindow, editWindow
        self.groups        = [None for _ in GROUPS] # Group Canvases
        self.themeElements = [[]   for _ in THEMES[THEME]] # items in each list will have same color
        
        self.rect = WINDOW_RECTS["main"]
        self.selectedTask = None
        self.colorchooserValue = None
        self.isTaskMoving = False
        self.database = Database(DATABASE_PATH)

        self.SetWindowSettings(self, self.rect, TITLES[0], None)
        self.SetStyle()
        self.CreateWidgets()
        self.LoadTasks()
        self.ChangeTheme(THEME)
        self.UpdateGroups()

    def UpdateGroups(self):

        for group in self.groups:
            group.UpdatePosition()

    @staticmethod
    def SetWindowSettings(window: Toplevel | Misc, rect: Rect, title: str, color: str, topWindow: Misc | Toplevel = None) -> None:

        GUI.Centerize(window, rect)
        GUI.SetBackgroundColor(window, color)
        GUI.SetTitle(window, title)
        GUI.SetUnresizable(window)
        GUI.RemoveTitleBar(window)
        window.bind('<Escape>', lambda e: GUI.CloseWindow(window, topWindow))

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
    def CloseWindow(window: Toplevel | Misc | None, topWindow: Toplevel | Misc = None) -> None:

        if not window.winfo_exists():
            return

        window.destroy()

        if topWindow and topWindow.winfo_exists():
            GUI.FocusWindow(topWindow)
        
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

    def SetStyle(self) -> None:

        self.style = ttk.Style()
        self.style.theme_use('clam')

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

        self.database.Execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, status INTEGER, title TEXT, detail TEXT, color TEXT, deadLine TEXT)")

    def LoadTasks(self) -> None:

        self.CreateTableIfNotExists()
        rows = self.database.FetchAll("SELECT * FROM tasks")

        if not rows:
            return

        for row in rows:

            status, title, detail, color, deadLine = row[1:]
            self.AddNewTask(self.GetGroup(list(Status)[status]), title, detail, color, deadLine)

    def SaveTasks(self) -> None:
        
        self.database.Execute("DELETE FROM tasks")

        for group in self.groups:
            for task in group.tasks:
                self.database.Execute("INSERT INTO tasks (status, title, detail, color, deadLine) VALUES (?, ?, ?, ?, ?)", task.group.name.value, task.title, task.detail, task.color, task.deadLine)

    #endregion

    #region Window Methods

    def GetColor(self, index: int) -> str:

        return THEMES[self.themeVar.get()][index]

    def OpenWindow(self, index: int, rect: Rect, title: str, height: int, textColor: str, font: tuple, topWindow: Toplevel | Misc = None) -> Toplevel:

        backgroundColor = self.GetColor(0)
        themeColor = self.GetColor(2)
        window = self.windows[index]
        
        if window and window.winfo_exists():
            return

        window = self.windows[index] = Toplevel(self)
        self.SetWindowSettings(window, rect, title, backgroundColor, topWindow)
        self.CreateTitleBar(window, height, title, themeColor, textColor, font)
        self.LockWindow(window)
        self.FocusWindow(window)

        if self.selectedTask:
            self.selectedTask.Unselect()
        
        return window

    def OpenInfoWindow(self):
        
        window = self.OpenWindow(0, WINDOW_RECTS["info"], TITLES[1], TITLEBAR_HEIGHT, TEXT_COLOR, TITLE_FONT, self)
        
        if window is None:
            return
        
        backgroundColor = self.GetColor(0)
        themeColor = self.GetColor(2)

        Label(window, text="Arrow keys: move the selected task\nEnter: Add a task\nDel: Remove the selected task.\n\nMade by Umutcan Ekinci\ngithub.com/umutcanekinci", font=TEXT_FONT, justify='center', bg=backgroundColor, fg=TEXT_COLOR).pack(pady=(50, 0))
        Button(window, text="Close", font=FONT, bg=themeColor, fg=TEXT_COLOR, command=lambda: self.CloseWindow(window, self)).pack(pady=PADDING, side=BOTTOM)

    def OpenDetailWindow(self, e):
        
        if not self.selectedTask:
            return

        window = self.OpenWindow(1, WINDOW_RECTS["detail"], TITLES[2], TITLEBAR_HEIGHT, TEXT_COLOR, TITLE_FONT, self)
        
        if window is None:
            return
        
        themeColor = self.GetColor(2)
        canvas = CustomCanvas(window, self.selectedTask.color, GetMainCanvasRect(TITLEBAR_HEIGHT, WINDOW_RECTS["detail"]))

        canvas.create_text((PADDING, PADDING * 1 + TITLEBAR_HEIGHT), "TITLE", TEXT_COLOR, BOLD_FONT, 'w')
        canvas.create_text((PADDING, PADDING * 4 + TITLEBAR_HEIGHT), self.selectedTask.title, TEXT_COLOR, TEXT_FONT, 'w')

        canvas.create_text((PADDING, PADDING * 9 + TITLEBAR_HEIGHT), "DETAIL", TEXT_COLOR, BOLD_FONT, 'w')
        canvas.create_text((PADDING, PADDING * 12 + TITLEBAR_HEIGHT), self.selectedTask.detail, TEXT_COLOR, TEXT_FONT, 'w')
        
        canvas.create_text((PADDING, PADDING * 22 + TITLEBAR_HEIGHT), "STATUS", TEXT_COLOR, BOLD_FONT, 'w')
        canvas.create_text((PADDING, PADDING * 25 + TITLEBAR_HEIGHT), self.selectedTask.group.name.name.replace('_', ' ').title(), TEXT_COLOR, TEXT_FONT, 'w')

        canvas.create_text((PADDING, PADDING * 30 + TITLEBAR_HEIGHT), "DEADLINE", TEXT_COLOR, BOLD_FONT, 'w')
        canvas.create_text((PADDING, PADDING * 33 + TITLEBAR_HEIGHT), self.selectedTask.deadLine, TEXT_COLOR, TEXT_FONT, 'w')

        # Buttons
        ButtonFrame = Frame(window, bg=self.selectedTask.color)
        ButtonFrame.pack(pady=PADDING * 2, side=BOTTOM)

        Button(ButtonFrame, text="Close", font=FONT, bg=themeColor, fg=TEXT_COLOR, command= lambda: self.CloseWindow(window, self)).pack(side=LEFT, padx=PADDING)
        Button(ButtonFrame, text="Edit", font=FONT, bg=themeColor, fg=TEXT_COLOR, command= self.OpenEditWindow).pack(side=LEFT, padx=PADDING)
        
    def OpenAddWindow(self):

        def CheckInputs():

            title = self.titleText.get("1.0", "end-1c")

            if not title:
                return
            
            group = self.GetGroup(Status[self.statusVar.get().upper().replace(' ', '_')])
            self.AddNewTask(group, title, self.detailText.get("1.0", "end-1c"), self.colorchooserValue if self.colorchooserValue else self.GetColor(0), self.deadLineEntry.get())
            group.UpdatePosition()

        window = self.OpenWindow(2, WINDOW_RECTS["add"], TITLES[3], TITLEBAR_HEIGHT, TEXT_COLOR, TITLE_FONT, self)
        
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

        Button(ButtonFrame, text="Close", font=FONT, bg=themeColor, fg=TEXT_COLOR, command=lambda: self.CloseWindow(window, self)).pack(side=LEFT, padx=PADDING)
        Button(ButtonFrame, text="Add", font=FONT, bg=themeColor, fg=TEXT_COLOR, command=CheckInputs).pack(side='right', padx=PADDING)

    def OpenEditWindow(self):

        def CheckInputs():

            title = self.titleText.get("1.0", "end-1c")

            if not title:
                return
            
            group = self.GetGroup(Status[self.statusVar.get().upper().replace(' ', '_')])
    
            self.UpdateTask(self.selectedTask, title, self.detailText.get("1.0", "end-1c"), self.colorchooserValue if self.colorchooserValue else self.GetColor(0), self.deadLineEntry.get(), group)
            self.CloseWindow(self.windows[2], self)

        window = self.OpenWindow(2, WINDOW_RECTS["edit"], TITLES[4], TITLEBAR_HEIGHT, TEXT_COLOR, TITLE_FONT, self)
        self.CloseWindow(self.windows[1], self)
        self.colorchooserValue = self.selectedTask.color

        if not window:
            return
        
        backgroundColor = self.selectedTask.color
        themeColor = self.GetColor(2)

        canvas = CustomCanvas(window, backgroundColor, GetMainCanvasRect(TITLEBAR_HEIGHT, WINDOW_RECTS["add"]))

        canvas.create_text((PADDING, TITLEBAR_HEIGHT + PADDING), "Enter the task title:", TEXT_COLOR, FONT, 'w')
        self.titleText = Text(window, font=TEXT_FONT, bg=themeColor, fg=TEXT_COLOR, height=1)
        self.titleText.pack(pady=(TITLEBAR_HEIGHT + PADDING * 6, 0), padx=PADDING, side=TOP)
        self.titleText.insert("1.0", self.selectedTask.title)

        canvas.create_text((PADDING, TITLEBAR_HEIGHT + PADDING * 10), "Enter the detail:", TEXT_COLOR, FONT, 'w')
        self.detailText = Text(window, font=TEXT_FONT, bg=themeColor, fg=TEXT_COLOR, height=3)
        self.detailText.pack(pady=(PADDING * 6, 0), padx=PADDING, side=TOP)
        self.detailText.insert("1.0", self.selectedTask.detail)

        self.statusVar = StringVar(window, GROUPS[self.selectedTask.group.name.value].capitalize())
        canvas.create_text((PADDING, TITLEBAR_HEIGHT + PADDING * 24), "Select the status:", TEXT_COLOR, FONT, 'w')
        statusOption = OptionMenu(window, self.statusVar, "Open", "In Progress", "Done")
        statusOption.pack(anchor='nw', pady=PADDING * 3, padx=(PADDING * 22, 0), side=TOP)
        statusOption.config(bg=themeColor, fg=TEXT_COLOR, activeforeground=TEXT_COLOR, activebackground=themeColor, highlightbackground=themeColor, font=FONT)

        canvas.create_text((PADDING, TITLEBAR_HEIGHT + PADDING * 31), "Choose the color:", TEXT_COLOR, FONT, 'w')
        Button(window, text="Choose", font=FONT, bg=themeColor, fg=TEXT_COLOR, command=self.ChooseColor).pack(anchor='nw', padx=(PADDING * 21, 0), pady=0 , side=TOP)

        canvas.create_text((PADDING, TITLEBAR_HEIGHT + PADDING * 39), "Select the deadline:", TEXT_COLOR, FONT, 'w')
        self.deadLineEntry = DateEntry(window, font=TEXT_FONT, firstweekday='monday', selectbackground=themeColor)
        self.deadLineEntry.pack(anchor='nw', padx=(PADDING * 24, 0), pady=PADDING * 3, side=TOP)
        self.deadLineEntry.set_date(self.selectedTask.deadLine)
        
        ButtonFrame = Frame(window, bg=backgroundColor)
        ButtonFrame.pack(pady=PADDING * 2, side=BOTTOM)

        Button(ButtonFrame, text="Cancel", font=FONT, bg=themeColor, fg=TEXT_COLOR, command=lambda: self.CloseWindow(window, self)).pack(side=LEFT, padx=PADDING)
        Button(ButtonFrame, text="Apply", font=FONT, bg=themeColor, fg=TEXT_COLOR, command=CheckInputs).pack(side='right', padx=PADDING)

    #endregion

    def ChooseColor(self):

        self.colorchooserValue = colorchooser.askcolor(initialcolor=self.colorchooserValue, title ="Choose task color")[1]

    #region Create Widgets

    def CreateWidgets(self):
    
        self.LoadImages()
        self.CreateMainTitleBar()
        self.CreateMainCanvas()
        self.CreateGroups()
        self.SetKeyBindings()

    def LoadImages(self):

        self.logoImage = GetImage(LOGO_PATH, LOGO_RECT)
        self.infoImage = GetImage(INFO_PATH, INFO_BUTTON_RECT)
        self.exitImage = GetImage(EXIT_PATH, EXIT_BUTTON_RECT)
        self.addImage =  GetImage(ADD_PATH,  ADD_BUTTON_RECT)

    def CreateMainTitleBar(self):

        def CreateTitleBar() -> None:

            self.titleBar = self.CreateTitleBar(self, MAIN_TITLEBAR_HEIGHT, '', None, TEXT_COLOR, TITLE_FONT)
            self.themeElements[2].append(self.titleBar)
        
        def CreateLogoAndTitle() -> None:

            self.titleBar.create_image(LOGO_RECT, self.logoImage)
            self.titleBar.create_text(TITLE_POSITION, TITLES[0], TEXT_COLOR, TITLE_FONT, 'w')
        
        def CreateThemeOption() -> None:

            self.themeVar = StringVar(self, THEME)
            themeOption = OptionMenu(self, self.themeVar, *THEMES.keys(), command=self.ChangeTheme)
            themeOption.place(anchor='w', x=THEME_OPTION_RECT.x, y=THEME_OPTION_RECT.y, width=THEME_OPTION_RECT.width, height=THEME_OPTION_RECT.height)
            themeOption.config(fg=TEXT_COLOR, activeforeground=TEXT_COLOR, font=BUTTON_FONT)
            self.themeElements[2].append(themeOption)

        def CreateTitleBarButtons() -> None:

            self.themeElements[2].append(CustomButton(self.titleBar, INFO_BUTTON_RECT, self.OpenInfoWindow, None, self.infoImage))
            CustomButton(self.titleBar, MINIMIZE_BUTTON_RECT, self.Minimize, TEXT_COLOR, None)
            self.themeElements[2].append(CustomButton(self.titleBar, EXIT_BUTTON_RECT, lambda: self.CloseWindow(self), None, image=self.exitImage))
       
        CreateTitleBar()
        CreateLogoAndTitle()
        CreateThemeOption()
        CreateTitleBarButtons()
        
    def CreateMainCanvas(self):

        self.mainCanvas = CustomCanvas(self, None, GetMainCanvasRect(MAIN_TITLEBAR_HEIGHT, self.rect))
        self.themeElements[0].append(self.mainCanvas)
 
    def CreateGroups(self):

        for groupStatus in Status:
            
            self.CreateGroup(groupStatus)
    
    def CreateGroup(self, status: Status):

        group = Group(self.mainCanvas, status)
        canvas = group.canvas
        group.CreateAddButton(self.OpenAddWindow, self.addImage)

        self.groups[status.value] = group
        self.themeElements[1].append(canvas)
        #canvas.bind('<B1-Motion>' , self.MoveTask)
        canvas.bind('<Button-1>'  , lambda e: self.SelectTask(e, group))
    
    def SetKeyBindings(self):

        self.bind('<Right>', lambda e: self.MoveHorizontally(Direction.RIGHT))
        self.bind('<Left>', lambda e: self.MoveHorizontally(Direction.LEFT))
        self.bind('<Down>', lambda e: self.MoveVertically(Direction.DOWN))
        self.bind('<Up>', lambda e: self.MoveVertically(Direction.UP))
        self.bind('<Delete>', lambda e: self.selectedTask.group.DeleteTask(self.selectedTask))
        self.mainCanvas.bind_all('<Double-Button-1>', self.OpenDetailWindow)
        self.bind('<ButtonRelease-1>', self.LocateTask)

        self.mainCanvas.bind("<Map>", self.Unminimize)

    #endregion

    def GetGroup(self, status: str):

        if status is None:
            raise ValueError("Status is None")
        
        return self.groups[status.value]
   
    def ChangeTheme(self, value):
        
        theme = THEMES[self.themeVar.get()]
        self.style.configure("Vertical.TScrollbar", troughcolor=self.GetColor(0), background=self.GetColor(1), bordercolor=self.GetColor(2))
        
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

        for group in self.groups:
            group.addButton.ChangeColor(theme[1])

    #region Task Methods

    def AddNewTask(self, group: str, title: str, detail: str, color: str, deadLine: str):

        if group is None:
            raise ValueError("Group is None")

        if not title or not color or not deadLine:
            return

        group.AddTask(Task(group, GetTaskRect(), color, title, detail, deadLine))
        
    def UpdateTask(self, task: Task, title: str, detail: str, color: str, deadLine: str, group: Group = None):

        if task is None:
            raise ValueError("Task is None")

        if not title or not color or not deadLine:
            return

        task.color, task.deadLine, task.detail = color, deadLine, detail

        task.UpdateTitle(title)
        task.UpdateColor(color)
        self.SetTaskGroup(task, group)

    def GetCollidedTask(self, group, x: int, y: int):
        
        # Actually I didn't use that ref but I will keep it here for future reference
        #ref: https://stackoverflow.com/questions/38982313/python-tkinter-identify-object-on-click
        
        if group is None:
            raise ValueError("Group is None")
        
        if x is None or y is None:
            raise ValueError("X or Y is None")

        x, y = group.canvas.canvasx(x), group.canvas.canvasy(y)
        for task in group.tasks:
            if task.isCollide(x, y):
                return task
        return None
    
    def SelectTask(self, event: Event, group: Group):

        collidedTask = self.GetCollidedTask(group, event.x, event.y)
        
        if self.selectedTask:
            self.selectedTask.Unselect()
        
        if self.selectedTask and self.selectedTask is collidedTask:
            self.selectedTask.Select(self.GetColor(3))
            return
        
        if collidedTask:
            collidedTask.Select(self.GetColor(3))
            
        self.selectedTask = collidedTask
        self.mainCanvas.startPos = Rect(event.x, event.y)

    def MoveHorizontally(self, direction: Direction):

        if not self.selectedTask or not direction:
            return
        
        canMoveRight = direction == Direction.RIGHT and self.selectedTask.group.name is not Status.DONE
        canMoveLeft = direction == Direction.LEFT and self.selectedTask.group.name is not Status.OPEN

        if not (canMoveRight or canMoveLeft):
            return
        
        newGroup = self.GetGroup(Status(self.selectedTask.group.name.value + direction.value))
        self.SetTaskGroup(self.selectedTask, newGroup)
        #newGroup.canvas.yview_moveto(1)
        newGroup.UpdatePosition()

    def MoveVertically(self, direction : Direction):

        if not self.selectedTask or not direction:
            return

        tasks = self.selectedTask.group.tasks
        index = tasks.index(self.selectedTask)

        canMoveDown = direction == Direction.DOWN and index != len(tasks) - 1
        canMoveUp = direction == Direction.UP and index != 0

        if not (canMoveDown or canMoveUp):
            return
        
        tasks[index], tasks[index + direction.value] = tasks[index + direction.value], tasks[index]
        self.selectedTask.group.UpdatePosition()
        #selectedTask.group.canvas.yview_scroll(direction.value, "units")

    def SetTaskGroup(self, task: Task, newGroup: Group):

        self.AddNewTask(newGroup, task.title, task.detail, task.color, task.deadLine)
        task.group.DeleteTask(task)
        task.group.UpdatePosition()
        self.selectedTask = newGroup.tasks[-1]
        self.selectedTask.Select(self.GetColor(3))

    def LocateTask(self, event: Event):

        if self.selectedTask is None:
            return

        if not self.isTaskMoving:
            return
        
        self.isTaskMoving = False
        self.selectedTask.Unselect()

        # Get nearest group and locate the task in that group
        for group in self.groups:
            if isPointInRectangle(group.rect, event.x, event.y):
                
                group.DeleteTask(self.selectedTask)
                self.selectedTask.group = group.name
                
                for task in group:
                    if isPointInRectangle(task.rect, event.x, event.y):
                        group.insert(group.index(task), self.selectedTask)
                        break
                else:
                    group.AddTask(self.selectedTask)
                
                break
        else:
            self.selectedTask.group.UpdatePosition()

    def MoveTask(self, event):

        if not self.selectedTask:
            return

        self.isTaskMoving = True

        # topmost object in the canvas
        self.mainCanvas.tag_raise(self.selectedTask.id)
        self.mainCanvas.tag_raise(self.selectedTask.titleId)
        
        #hide add buttons
        for group in self.groups:
            group.addButton.place_forget()
        
        newRect = Rect(event.x, event.y) - self.mainCanvas.startPos
        self.selectedTask.Move(*newRect.topLeft)
        self.mainCanvas.startPos = Rect(event.x, event.y)

    #region Update Position Methods

    #endregion
