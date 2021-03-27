# Login Handler: Stores user data and allows checking if a login is valid
from UserIO import UserIO
from dataClasses.UserData import UserData

class LoginHandler:
    def __init__(self):
        self.objIO = UserIO()
        self.objIO.loadData()
        self.users = self.objIO.getData()

    # Return user object that matches given username
    def getUser(self, username):
        for user in self.users:
            if (user.isUsername(username)):
                return user
        return None

    # Takes as input a new UserData object, store it in users list, then save to file
    # Returns True if user is created
    def newUser(self, newUserData):
        # Check if user already exists (same exact username)
        for user in self.users:
            if (user.isUser(newUserData)):
                return False

        self.users.append(newUserData)
        self.objIO.setData(self.users)
        self.objIO.saveData()
        return True

    # Return True if given username and password match
    def isValidLogin(self, username, password):
        for user in self.users:
            if (user.isUsername(username)):
                return user.checkPassword(password)
        return None