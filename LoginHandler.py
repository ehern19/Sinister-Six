# Login Handler: Stores user data and allows checking if a login is valid
from UserIO import UserIO
from UserData import UserData

class LoginHandler:
    def __init__(self):
        self.objIO = UserIO()
        self.objIO.loadData()
        self.users = self.objIO.getData()

    # Return True if given username+password match
    def isValidLogin(self, username, password):
        for user in self.users:
            if (user.isUser(username)):
                return user.checkPassword(password)
        return False