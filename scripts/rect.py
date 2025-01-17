class Rect():

    def __init__(self, x: int = 0, y: int = 0, width: int = 0, height: int = 0):
        
        self.x, self.y = x, y
        self.width, self.height = width, height

    def __str__(self):
        
        return f"Rect({self.x}, {self.y}, {self.width}, {self.height})"

    def __add__(self, other):

        return Rect(self.x + other.x, self.y + other.y, self.width, self.height)
    
    def __sub__(self, other):

        return Rect(self.x - other.x, self.y - other.y, self.width, self.height)

    def Move(self, x: int, y: int):

        self.x += x
        self.y += y


    #region Properties

    @property
    def topLeft(self):

        return self.x, self.y

    @topLeft.setter
    def topLeft(self, value):
        
        self.x, self.y = value

    @property
    def left(self):

        return self.x
    
    @left.setter
    def left(self, value):

        self.x = value

    @property
    def top(self):

        return self.y
    
    @top.setter
    def top(self, value):

        self.y = value

    @property
    def right(self):

        return self.x + self.width
    
    @right.setter
    def right(self, value):

        self.x = value - self.width

    @property
    def bottom(self):

        return self.y + self.height
    
    @bottom.setter
    def bottom(self, value):

        self.y = value - self.height

    @property
    def centerX(self):

        return self.x + self.width // 2
    
    @centerX.setter
    def centerX(self, value):

        self.x = value - self.width // 2

    @property
    def centerY(self):

        return self.y + self.height // 2
    
    @centerY.setter
    def centerY(self, value):

        self.y = value - self.height // 2

    @property
    def center(self):

        return self.centerX, self.centerY
    
    @center.setter
    def center(self, value):

        self.centerX, self.centerY = value

    @property
    def size(self):

        return self.width, self.height
    
    #endregion