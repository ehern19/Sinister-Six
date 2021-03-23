# Process Manager: Provides methods that can be called by the website application
# Passes arguments from website to handlers and data from handlers to website
# Where required, converts from website arguments to function arguments
from os import name
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
    
    def passUsername(self, username):
        return self.LHandler.getUser(username)

    # Takes user input from web page and passes it to EventHandler
    def passRSVP(self, username, eventName):
        return self.EHandler.addRSVP(username, eventName)

    def passLeaveRSVP(self, username, eventName):
        return self.EHandler.removeRSVP(username, eventName)
    
    def passNewEvent(self, name, time, date, location, tags, organizer):
        newEvent = EventData(name, time, date, location, tags, [organizer])
        return self.EHandler.newEvent(newEvent)

    # Returns the named event
    def getEvent(self, name):
        return self.EHandler.getEvent(name)

    # Returns all events
    def getAllEvents(self):
        return self.EHandler.getAllEvents()
