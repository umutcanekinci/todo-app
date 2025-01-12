from sqlite3 import connect

class Database:

    def __init__(self, path="database.db"):

        self.name = path

        self.Connect(path)

        self.cursor = self.connection.cursor()

    def Connect(self, path: str):

        self.connection = connect(path)

    def Execute(self, query: str, *args):

        self.cursor.execute(query, args)
        self.connection.commit()

    def FetchAll(self, query: str, *args):

        self.cursor.execute(query, args)
        return self.cursor.fetchall()

    def Disconnect(self):

        if self.cursor:
            self.cursor.close()

        if self.connection:
            self.connection.close()


