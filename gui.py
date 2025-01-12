from constants import *
from widgets.button import CustomButton
from widgets.canvas import CustomCanvas
from widgets.task import Task
from rect import Rect
from enums import Direction, Status
from utils import GetImage
from tkinter import *
from tkinter import colorchooser
from tkcalendar import Calendar, DateEntry

class GUI(Tk):
    
    #region Initialize Methods

    def __init__(self, rect: Rect = WINDOW_RECT):

        super().__init__()
        self.rect = rect
        self.windows = [None, None, None] # List of windows: infoWindow, detailWindow, addWindow
        self.tasks = [[] for _ in Status] # Open, In Progress, Done Task lists
        self.selectedTask = None
        self.colorchooserValue = BLACK

        self.SetWindowSettings(self, rect, TITLE)
        self.CreateWidgets()

    @staticmethod
    def SetWindowSettings(window: Toplevel | Misc, rect: Rect, title: str):

        GUI.Centerize(window, rect)
        GUI.SetBackgroundColor(window, MAIN_COLOR)
        GUI.SetTitle(window, title)
        GUI.SetUnresizable(window)
        GUI.RemoveTitleBar(window)
        window.bind('<Escape>', lambda e: GUI.CloseWindow(window))

    @staticmethod
    def SetUnresizable(window, width: bool = False, height: bool = False):
        
        window.resizable(width, height)

    @staticmethod
    def RemoveTitleBar(window: Misc):

        window.overrideredirect(True)

    @staticmethod
    def SetTitle(window: Misc, title: str):

        window.title(title)

    @staticmethod
    def Centerize(window: Misc, rect: Rect):

        # Calculating topleft position of window when it is at the center of screen.
        screenWidth, screenHeight = window.winfo_screenwidth(), window.winfo_screenheight()
        topleftX, topleftY = (screenWidth - rect.width) // 2, (screenHeight - rect.height) // 2
        window.geometry(f"{rect.width}x{rect.height}+{topleftX}+{topleftY}")

    @staticmethod
    def SetBackgroundColor(window: Misc, color: str):
        
        window.configure(bg = color)

    @staticmethod
    def LockWindow(window: Toplevel):

        window.grab_set()

    @staticmethod
    def CloseWindow(window: Toplevel | Misc | None):

        if window is None:
            return

        window.destroy()
        widndow = None

    @staticmethod
    def GetWindowPosition(event, window: Toplevel | Misc, rect: Rect, titleBar: CustomCanvas):

        topleftX = window.winfo_x()
        topleftY = window.winfo_y()
        startx, starty = event.x_root, event.y_root

        ywin = topleftY - starty
        xwin = topleftX - startx

        def Move(event):

            window.geometry(f"{rect.width}x{rect.height}+{event.x_root + xwin}+{event.y_root + ywin}")

        titleBar.bind('<B1-Motion>', Move)

    @staticmethod
    def GetWindowRect(window: Toplevel | Misc):

        window.update_idletasks() # https://stackoverflow.com/questions/34373533/winfo-width-returns-1-even-after-using-pack
        return Rect(window.winfo_x(), window.winfo_y(), window.winfo_width(), window.winfo_height())

    @staticmethod
    def CreateTitleBar(window: Toplevel | Misc, height: int, title: str, color: str, titleColor: str, titleFont: tuple):

        windowRect = GUI.GetWindowRect(window)
        rect = Rect(0, 0, windowRect.width, height)

        titleBar = CustomCanvas(window, color, rect)
        titleBar.create_text(rect.center, title, titleColor, titleFont)
        titleBar.bind('<Button-1>', lambda e: GUI.GetWindowPosition(e, window, windowRect, titleBar))

        return titleBar

    #endregion

    #region Titlebar Methods

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

    #region Window Methods

    def OpenWindow(self, index: int, rect: Rect, title: str, height: int, color: str, textColor: str, font: tuple):

        window = self.windows[index]
        
        if window is not None:
            return

        window = Toplevel(self)
        self.SetWindowSettings(window, rect, title)
        self.CreateTitleBar(window, height, title, color, textColor, font)
        self.LockWindow(window)
        return window

    def OpenInfoWindow(self):
        
        window = self.OpenWindow(0, INFO_RECT, INFO_TITLE, TITLEBAR_HEIGHT, TITLEBAR_COLOR, TEXT_COLOR, TITLE_FONT)
        
        if window is None:
            return
        
        Label(window, text="Arrow keys: move the selected task\nEnter: Add a task\nDel: Remove the selected task.\n\nMade by Umutcan Ekinci\ngithub.com/umutcanekinci", font=TEXT_FONT, justify='center', bg=MAIN_COLOR, fg=TEXT_COLOR).pack(pady=(50, 0))
        Button(window, text="Close", font=FONT, bg=TITLEBAR_COLOR, fg=TEXT_COLOR, command=lambda: self.CloseWindow(window)).pack(pady=PADDING, side=BOTTOM)

    def OpenDetailWindow(self, e):

        if not self.selectedTask:
            return
        
        task = self.GetCollidedTask(e.x, e.y)

        if not task:
            return

        window = self.OpenWindow(1, DETAIL_RECT, DETAIL_TITLE, TITLEBAR_HEIGHT, TITLEBAR_COLOR, TEXT_COLOR, TITLE_FONT)
        
        if window is None:
            return
        
        canvas = CustomCanvas(window, task.color, DETAIL_MAIN_RECT)

        canvas.create_text((PADDING, PADDING * 1 + TITLEBAR_HEIGHT), "TITLE", TEXT_COLOR, BOLD_FONT, 'w')
        canvas.create_text((PADDING, PADDING * 4 + TITLEBAR_HEIGHT), task.title, TEXT_COLOR, TEXT_FONT, 'w')

        canvas.create_text((PADDING, PADDING * 8 + TITLEBAR_HEIGHT), "DETAIL", TEXT_COLOR, BOLD_FONT, 'w')
        canvas.create_text((PADDING, PADDING * 11 + TITLEBAR_HEIGHT), task.detail, TEXT_COLOR, TEXT_FONT, 'w')
        
        canvas.create_text((PADDING, PADDING * 14 + TITLEBAR_HEIGHT), "STATUS", TEXT_COLOR, BOLD_FONT, 'w')
        canvas.create_text((PADDING, PADDING * 17 + TITLEBAR_HEIGHT), task.status.name, TEXT_COLOR, TEXT_FONT, 'w')

        canvas.create_text((PADDING, PADDING * 20 + TITLEBAR_HEIGHT), "DEADLINE", TEXT_COLOR, BOLD_FONT, 'w')
        canvas.create_text((PADDING, PADDING * 23 + TITLEBAR_HEIGHT), task.deadLine, TEXT_COLOR, TEXT_FONT, 'w')

        Button(window, text="Close", font=FONT, bg=TITLEBAR_COLOR, fg=TEXT_COLOR, command= lambda: self.CloseWindow(window)).pack(pady=PADDING, side=BOTTOM)
        
    def OpenAddWindow(self):

        window = self.OpenWindow(2, ADD_RECT, ADD_TITLE, TITLEBAR_HEIGHT, TITLEBAR_COLOR, TEXT_COLOR, TITLE_FONT)
        
        if window is None:
            return

        canvas = CustomCanvas(window, MAIN_COLOR, ADD_MAIN_RECT)

        canvas.create_text((PADDING, TITLEBAR_HEIGHT + PADDING), "Enter the task title:", TEXT_COLOR, FONT, 'w')
        self.titleText = Text(window, font=TEXT_FONT, bg=GRAY, fg=TEXT_COLOR, height=1)
        self.titleText.pack(pady=(TITLEBAR_HEIGHT + PADDING * 6, 0), padx=PADDING, side=TOP)

        canvas.create_text((PADDING, TITLEBAR_HEIGHT + PADDING * 10), "Enter the detail:", TEXT_COLOR, FONT, 'w')
        self.detailText = Text(window, font=TEXT_FONT, bg=GRAY, fg=TEXT_COLOR, height=3)
        self.detailText.pack(pady=(PADDING * 6, 0), padx=PADDING, side=TOP)
        
        self.statusVar = StringVar(window, "Open")
        canvas.create_text((PADDING, TITLEBAR_HEIGHT + PADDING * 24), "Select the status:", TEXT_COLOR, FONT, 'w')
        statusOption = OptionMenu(window, self.statusVar, "Open", "In Progress", "Done")
        statusOption.pack(anchor='nw', pady=PADDING * 3, padx=(PADDING * 22, 0), side=TOP)
        statusOption.config(bg=TITLEBAR_COLOR, fg=TEXT_COLOR, activebackground=TITLEBAR_COLOR, highlightbackground=TITLEBAR_COLOR, font=FONT)

        canvas.create_text((PADDING, TITLEBAR_HEIGHT + PADDING * 31), "Choose the color:", TEXT_COLOR, FONT, 'w')
        Button(window, text="Choose", font=FONT, bg=TITLEBAR_COLOR, fg=TEXT_COLOR, command=self.ChooseColor).pack(anchor='nw', padx=(PADDING * 21, 0), pady=0 , side=TOP)

        canvas.create_text((PADDING, TITLEBAR_HEIGHT + PADDING * 39), "Select the deadline:", TEXT_COLOR, FONT, 'w')
        self.deadLineEntry = DateEntry(window, font=TEXT_FONT, bg=GRAY, fg=TEXT_COLOR, selectbackground=TITLEBAR_COLOR)
        self.deadLineEntry.pack(anchor='nw', padx=(PADDING * 24, 0), pady=PADDING * 3, side=TOP)

        ButtonFrame = Frame(window, bg=MAIN_COLOR)
        ButtonFrame.pack(pady=PADDING * 2, side=BOTTOM)

        Button(ButtonFrame, text="Close", font=FONT, bg=TITLEBAR_COLOR, fg=TEXT_COLOR, command=lambda: self.CloseWindow(window)).pack(side=LEFT, padx=PADDING * 2)
        Button(ButtonFrame, text="Add", font=FONT, bg=TITLEBAR_COLOR, fg=TEXT_COLOR, command=self.CheckAddWindow).pack(side=LEFT, padx=PADDING * 2)

    def CheckAddWindow(self):

        title = self.titleText.get("1.0", "end-1c")

        if not title:
            return
        
        self.AddNewTask(Status[self.statusVar.get().upper()], title, self.detailText.get("1.0", "end-1c"), self.colorchooserValue, self.deadLineEntry.get())

    #endregion

    def ChooseColor(self):

        self.colorchooserValue = colorchooser.askcolor(title ="Choose task color")[1]

    def LoadImages(self):

        self.logoImage = GetImage(LOGO_PATH, LOGO_RECT)
        self.infoImage = GetImage(INFO_PATH, INFO_BUTTON_RECT)
        self.exitImage = GetImage(EXIT_PATH, EXIT_BUTTON_RECT)
        self.addImage =  GetImage(ADD_PATH,  ADD_BUTTON_RECT)

    def CreateWidgets(self):
    
        self.LoadImages()
        
        # Title Bar
        titleBar = self.CreateTitleBar(self, MAIN_TITLEBAR_HEIGHT, '', TITLEBAR_COLOR, TEXT_COLOR, TITLE_FONT)
        titleBar.create_image(LOGO_RECT, self.logoImage)
        titleBar.create_text(TITLE_POSITION, TITLE, TEXT_COLOR, TITLE_FONT, 'w')
        
        # Title Bar Buttons
        CustomButton(titleBar, INFO_BUTTON_RECT, self.OpenInfoWindow, TITLEBAR_COLOR, self.infoImage)
        CustomButton(titleBar, MINIMIZE_BUTTON_RECT, self.Minimize, TEXT_COLOR, None)
        CustomButton(titleBar, EXIT_BUTTON_RECT, lambda: self.CloseWindow(self), TITLEBAR_COLOR, image=self.exitImage)
        
        # Main Canvas
        self.mainCanvas = CustomCanvas(self, MAIN_COLOR, MAIN_RECT)
        self.mainCanvas.bind("<Map>", self.Unminimize)
        self.mainCanvas.bind('<Button-1>', self.SelectTask)

        self.mainCanvas.create_rectangle(OPEN_RECT,        GRAY)
        self.mainCanvas.create_rectangle(IN_PROGRESS_RECT, GRAY)
        self.mainCanvas.create_rectangle(DONE_RECT,        GRAY)

        self.mainCanvas.create_rectangle(OPEN_TITLE_BOX_RECT, OPEN_COLOR)
        self.mainCanvas.create_rectangle(IN_PROGRESS_TITLE_BOX_RECT, IN_PROGRESS_COLOR)
        self.mainCanvas.create_rectangle(DONE_TITLE_BOX_RECT, DONE_COLOR)
        
        self.mainCanvas.create_text(OPEN_TITLE_BOX_RECT.center, "OPEN",               TEXT_COLOR, BOLD_FONT)
        self.mainCanvas.create_text(IN_PROGRESS_TITLE_BOX_RECT.center, "IN PROGRESS", TEXT_COLOR, BOLD_FONT)
        self.mainCanvas.create_text(DONE_TITLE_BOX_RECT.center, "DONE",               TEXT_COLOR, BOLD_FONT)
        
        self.CreateAddButtons()
        
        # Key Bindings
        self.bind('<Right>', lambda e: self.MoveHorizontally(Direction.RIGHT))
        self.bind('<Left>', lambda e: self.MoveHorizontally(Direction.LEFT))
        self.bind('<Down>', lambda e: self.MoveVertically(Direction.DOWN))
        self.bind('<Up>', lambda e: self.MoveVertically(Direction.UP))
        self.bind('<Delete>', lambda e: self.RemoveTask(self.selectedTask))
        self.bind('<Double-Button-1>', self.OpenDetailWindow)

    #region Task Methods

    def GetRect(self, status: str):

        if status is None:
            raise ValueError("Status is None")
        
        return [OPEN_RECT, IN_PROGRESS_RECT, DONE_RECT][status.value]

    def GetList(self, status: str):

        if status is None:
            raise ValueError("Status is None")
        
        return self.tasks[status.value]

    def AddNewTask(self, status: str, title: str, detail: str, color: str, deadLine: str):

        if status is None:
            raise ValueError("Status is None")

        if not title or not color or not deadLine:
            return

        self.GetList(status).append(Task(self.mainCanvas, Rect(0, 0, TASK_RECT.width, TASK_RECT.height), color, WHITE, status, title, detail, deadLine))
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
        
        self.GetList(task.status).remove(task)
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
            collided_task.Select()
            
        self.selectedTask = collided_task
        
    def UpdateTasksPosition(self, status: Status):

        if status is None:
            raise ValueError("Status is None")

        list = self.GetList(status)

        if list is None:
            raise ValueError("List is None")
        
        for i, task in enumerate(list):
        
            if i:
                task.MoveTo(self.GetRect(status).left + PADDING, list[i - 1].rect.bottom + PADDING)
                continue
            
            task.MoveTo(self.GetRect(task.status).left + PADDING, TASK_RECT.y)

        self.UpdateAddButtonPosition(status)

    #region Add Button Functions

    def CreateAddButtons(self):

        self.addButtons = []
        for status in Status:
            self.addButtons.append(CustomButton(self.mainCanvas, Rect(), self.OpenAddWindow, GRAY, self.addImage))
            self.UpdateTasksPosition(status)

    def GetAddButton(self, status: str):

        if status is None:
            raise ValueError("Status is None")

        return self.addButtons[status.value]

    def UpdateAddButtonPosition(self, status: Status):

        list = self.GetList(status)        

        if list and list[-1].rect.bottom + PADDING * 2 + TASK_HEIGHT > self.GetRect(status).bottom:
            self.GetAddButton(status).place_forget()
            return

        if list:
            self.GetAddButton(list[0].status).place(Rect(list[0].rect.centerX - ADD_BUTTON_RECT.width // 2, list[-1].rect.bottom + PADDING * 2, ADD_BUTTON_RECT.width, ADD_BUTTON_RECT.height))
        
        else:
            self.GetAddButton(status).place(Rect(self.GetRect(status).centerX - ADD_BUTTON_RECT.width // 2, self.GetRect(status).top + TITLE_BOX_HEIGHT + PADDING * 2, ADD_BUTTON_RECT.width, ADD_BUTTON_RECT.height))

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
        self.GetList(self.selectedTask.status).append(self.selectedTask)
        self.UpdateTasksPosition(self.selectedTask.status)

    def MoveVertically(self, direction : Direction):

        if not self.selectedTask or not direction:
            return

        tasks = self.GetList(self.selectedTask.status)
        index = tasks.index(self.selectedTask)

        canMoveDown = direction == Direction.DOWN and index != len(tasks) - 1
        canMoveUp = direction == Direction.UP and index != 0

        if not (canMoveDown or canMoveUp):
            return
        
        tasks[index], tasks[index + direction.value] = tasks[index + direction.value], tasks[index]
        self.UpdateTasksPosition(self.selectedTask.status)

    #endregion

    def Run(self):

        self.mainloop()