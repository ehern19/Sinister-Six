#                                                    Summary:
#
# This class allows users to log in to their account by storing user data and checking if the login
# matches a registered user.
#
#
#
#                                                    Data Members:
#
# user
#
#
#
#                                                    Methods:
#
# "init": This is the class' constructor method, it initializes and makes calls to the 
# other classes.
#
# "getUser": Checks for a user object that matches the login attempt, and returns it if found.
#
# "newUser": Creates a new user object by storing the input in the database list.
# Will return "true" if the user is successfully created.
#
# "replaceUser": Searches for if the inputted user matches with a user in the memory, and
# then saves to file. Returns "true" if successful.
#
# "isValidLogin": Returns "true" if the inputted username and password match.

from UserIO import UserIO
from dataClasses.UserData import UserData

class LoginHandler:
    def __init__(self):
        self.objIO = UserIO()
        self.objIO.loadData()
        self.users = self.objIO.getData()

    # Return user object that matches given username
    def getUser(self, username: str) -> UserData:
        for user in self.users:
            if (user.isUsername(username)):
                return user
        return None

    # Takes as input a new UserData object, store it in users list, then save to file
    # Returns True if user is created
    def newUser(self, newUserData: UserData) -> bool:
        # Check if user already exists (same exact username)
        for user in self.users:
            if (user.isUser(newUserData)):
                return False

        self.users.append(newUserData)
        self.objIO.setData(self.users)
        self.objIO.saveData()
        return True

    # Replace matching user in memory with input user (matches by username), then save to file
    # Returns True if user is replaced
    def replaceUser(self, newUser: UserData) -> bool:
        for user in self.users:
            if (user.isUser(newUser)):
                user = newUser
                self.objIO.setData(self.users)
                self.objIO.saveData()
                return True
        return False

    # Return True if given username and password match
    def isValidLogin(self, username: str, password: str) -> bool:
        for user in self.users:
            if (user.isUsername(username)):
                return user.checkPassword(password)
        return None