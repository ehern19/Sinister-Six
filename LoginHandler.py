#LoginHandler

class LoginHandler:
    def __init__(self):
        self.userData = {}
    
    def loadUsers(self, userData):
        self.userData = userData
        return

    def checkLogin(self, loginData):
        if not loginData[0] in self.userData:
            return False
        if (self.userData[loginData[0]] == loginData[1]):
            return True #if the user credentials check out, it will clear the login
        else:
            return False
            
    def newUser(self, newUserData):
        if not newUserData[0] in self.userData:
            self.userData.update(newUserData)
            return True
        else:
            return "Login already exists"