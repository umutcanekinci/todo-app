from settings import *
from widgets.button import CustomButton
from widgets.canvas import CustomCanvas
from widgets.task import Task
from rect import Rect
from enums import Direction, Status
from utils import GetImage
from tkinter import *
from tkinter import simpledialog

class GUI(Tk):
    
    #region Initialize

    def __init__(self, rect: Rect = WINDOW_RECT):

        super().__init__()
        self.rect = rect
        self.SetWindowSettings(self, rect, TITLE)
        self.CreateWidgets()
        self.windows = [None, None, None] # List of windows: infoWindow, detailWindow, addWindow

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
    def GetWindowPosition(event, window: Toplevel | Misc, rect: Rect, topCanvas: CustomCanvas):

        topleftX = window.winfo_x()
        topleftY = window.winfo_y()
        startx, starty = event.x_root, event.y_root

        ywin = topleftY - starty
        xwin = topleftX - startx

        def Move(event):

            window.geometry(f"{rect.width}x{rect.height}+{event.x_root + xwin}+{event.y_root + ywin}")

        topCanvas.bind('<B1-Motion>', Move)

    @staticmethod
    def GetWindowRect(window: Toplevel | Misc):

        window.update_idletasks() 
        return Rect(window.winfo_x(), window.winfo_y(), window.winfo_width(), window.winfo_height())

    @staticmethod
    def CreateTitleBar(window: Toplevel | Misc, height: int, title: str, color: str, titleColor: str, titleFont: tuple):

        windowRect = GUI.GetWindowRect(window)
        rect = Rect(0, 0, windowRect.width, height)

        topCanvas = CustomCanvas(window, color, rect)
        topCanvas.create_text(rect.center, title, titleColor, titleFont)
        topCanvas.bind('<Button-1>', lambda e: GUI.GetWindowPosition(e, window, windowRect, topCanvas))

        return topCanvas

    #endregion

    #region Titlebar Functions

    def Unminimize(self,e):
        
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

    def OpenInfoWindow(self):
        
        if self.windows[0] is not None:
            return

        self.windows[0] = Toplevel(self)
        window = self.windows[0]

        self.SetWindowSettings(window, INFO_RECT, INFO_TITLE)

        self.CreateTitleBar(window, TOP_INFO_HEIGHT, INFO_TITLE, TOP_COLOR, TEXT_COLOR, TITLE_FONT)

        Label(window, text="Arrow keys: move the selected task\nEnter: Add a task\nDel: Remove the selected task.\n\nMade by Umutcan Ekinci\ngithub.com/umutcanekinci", font=FONT, justify='center', bg=MAIN_COLOR, fg=TEXT_COLOR).pack(pady=(50, 0))
        Button(window, text="Close", font=FONT, bg=TOP_COLOR, fg=TEXT_COLOR, command=lambda: self.CloseWindow(window)).pack(pady=10)

        self.LockWindow(window)

    def OpenDetailWindow(self, e):

        if not self.selectedTask:
            return
        
        task = self.GetCollidedTask(e.x, e.y)

        if not task:
            return

        if self.windows[1] is not None:
            return

        self.windows[1] = Toplevel(self)
        window = self.windows[1]

        self.SetWindowSettings(window, DETAIL_RECT, DETAIL_TITLE)

        self.CreateTitleBar(window, TOP_INFO_HEIGHT, DETAIL_TITLE, TOP_COLOR, TEXT_COLOR, TITLE_FONT)
        
    
        Label(window, text=f"Text: {task.text}", font=FONT, justify='left', bg=MAIN_COLOR, fg=TEXT_COLOR).pack(pady=(50, 0), padx=0)
        Button(window, text="Close", font=FONT, bg=TOP_COLOR, fg=TEXT_COLOR, command= lambda: self.CloseWindow(window)).pack(pady=10)

        self.LockWindow(window)

    def OpenAddWindow(self):

        if self.windows[2] is not None:
            return

        self.windows[2] = Toplevel(self)
        window = self.windows[2]

        self.SetWindowSettings(window, ADD_RECT, ADD_TITLE)
        self.CreateTitleBar(window, TOP_INFO_HEIGHT, ADD_TITLE, TOP_COLOR, TEXT_COLOR, TITLE_FONT)

        Label(window, text="Enter the text", font=FONT, justify='center', bg=MAIN_COLOR, fg=TEXT_COLOR).pack(pady=(50, 0))
        Button(window, text="Close", font=FONT, bg=TOP_COLOR, fg=TEXT_COLOR, command= lambda: self.CloseWindow(window)).pack(pady=10)

        self.LockWindow(window)

    def CreateWidgets(self):
    
        # load images
        self.logoImage = GetImage(LOGO_IMAGE, LOGO_RECT)
        self.infoImage = GetImage(INFO_IMAGE, INFO_BUTTON_RECT)
        self.exitImage = GetImage(EXIT_IMAGE, EXIT_BUTTON_RECT)
        self.addImage = GetImage(ADD_IMAGE, ADD_BUTTON_RECT)
        
        # Top Canvas
        topCanvas = self.CreateTitleBar(self, TOP_HEIGHT, '', TOP_COLOR, TEXT_COLOR, TITLE_FONT)

        # Logo and Title
        topCanvas.create_image(LOGO_RECT, self.logoImage)
        topCanvas.create_text(TITLE_POSITION, TITLE, TEXT_COLOR, TITLE_FONT, 'w')
        
        # Buttons
        infoButton =     CustomButton(topCanvas, self.OpenInfoWindow, TOP_COLOR, self.infoImage)
        minimizeButton = CustomButton(topCanvas, self.Minimize, TEXT_COLOR, None)
        exitButton =     CustomButton(topCanvas, lambda: self.CloseWindow(self), TOP_COLOR, image=self.exitImage)
        
        minimizeButton.place(MINIMIZE_BUTTON_RECT)
        infoButton.place(INFO_BUTTON_RECT)
        exitButton.place(EXIT_BUTTON_RECT)

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
        
        self.mainCanvas.create_text(OPEN_TITLE_BOX_RECT.center, "OPEN",               TEXT_COLOR, FONT)
        self.mainCanvas.create_text(IN_PROGRESS_TITLE_BOX_RECT.center, "IN PROGRESS", TEXT_COLOR, FONT)
        self.mainCanvas.create_text(DONE_TITLE_BOX_RECT.center, "DONE",               TEXT_COLOR, FONT)
        
        # Tasks
        self.selectedTask = None
        self.tasks = [[] for _ in Status] # Open, In Progress, Done lists

        self.addButtons = []
        for status in Status:
            self.addButtons.append(CustomButton(self.mainCanvas, lambda status=status: self.AddNewTask(status), GRAY, self.addImage))
            self.UpdateTasksPosition(status)
            
        # Key Bindings
        self.bind('<Right>', lambda e: self.MoveHorizontally(Direction.RIGHT))
        self.bind('<Left>', lambda e: self.MoveHorizontally(Direction.LEFT))
        self.bind('<Down>', lambda e: self.MoveVertically(Direction.DOWN))
        self.bind('<Up>', lambda e: self.MoveVertically(Direction.UP))
        self.bind('<Delete>', lambda e: self.RemoveTask(self.selectedTask))
        self.bind('<Double-Button-1>', self.OpenDetailWindow)

    #region Task Functions

    def GetInput(self):

        return simpledialog.askstring("Add a task", "Enter the text", parent=self)

    def GetRect(self, status: str):

        if status is None:
            raise ValueError("Status is None")
        
        return [OPEN_RECT, IN_PROGRESS_RECT, DONE_RECT][status.value]

    def GetList(self, status: str):

        if status is None:
            raise ValueError("Status is None")
        
        return self.tasks[status.value]

    def GetAddButton(self, status: str):

        if status is None:
            raise ValueError("Status is None")

        return self.addButtons[status.value]

    def AddNewTask(self, status: str):

        if status is None:
            raise ValueError("Status is None")

        text = self.GetInput()

        if not text:
            return

        self.GetList(status).append(Task(self.mainCanvas, Rect(0, 0, TASK_RECT.width, TASK_RECT.height), BLACK, WHITE, status, text))
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

    def UpdateAddButtonPosition(self, status: Status):

        list = self.GetList(status)        

        if list and list[-1].rect.bottom + PADDING * 2 + TASK_HEIGHT > self.GetRect(status).bottom:
            self.GetAddButton(status).place_forget()
            return

        if list:
            self.GetAddButton(list[0].status).place(Rect(list[0].rect.centerX - ADD_BUTTON_RECT.width // 2, list[-1].rect.bottom + PADDING * 2, ADD_BUTTON_RECT.width, ADD_BUTTON_RECT.height))
        
        else:
            self.GetAddButton(status).place(Rect(self.GetRect(status).centerX - ADD_BUTTON_RECT.width // 2, self.GetRect(status).top + TITLE_BOX_HEIGHT + PADDING * 2, ADD_BUTTON_RECT.width, ADD_BUTTON_RECT.height))

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