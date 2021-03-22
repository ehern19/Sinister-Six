# Process Manager: Provides methods that can be called by the website application
# Passes arguments from website to handlers and vice versa
from EventHandler import EventHandler
from LoginHandler import LoginHandler
from EventData import EventData
from UserData import UserData

class ProcessManager:
    def __init__(self):
        self.EHandler = EventHandler()
        self.LHandler = LoginHandler()

    # Takes login input from web page and passes it to LoginHandler
    def passLogin(self, username, password):
        return self.LHandler.isValidLogin(username, password)
    
    # Takes username input from web page and passes it to LoginHandler
    def passUsername(self, username):
        return self.LHandler.getUser(username)