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

    def passNewUser(self, username, password, phone, email):
        newUser = UserData(username, password, phone, email)
        return self.LHandler.newUser(newUser)

    # Takes user input from web page and passes it to EventHandler
    def passRSVP(self, username, eventName):
        return self.EHandler.addRSVP(username, eventName)

    def passLeaveRSVP(self, username, eventName):
        return self.EHandler.removeRSVP(username, eventName)
    
    def passNewEvent(self, name, time, date, location, zip, tags, organizer, summary):
        newEvent = EventData(name, time, date, location, zip, tags, [organizer], summary)
        return self.EHandler.newEvent(newEvent)

    # Returns the named event
    def getEvent(self, name):
        return self.EHandler.getEvent(name)

    # Returns all events
    def getAllEvents(self):
        return self.EHandler.getAllEvents()

    # Return appropriate search results
    def searchEvents(self, searchType, searchValue, searchDate = "", searchTags = [""]):
        if (searchType == "name"):
            retEvents = self.EHandler.searchName(searchValue)
        elif (searchType == "organizer"):
            retEvents = self.EHandler.searchOrganizer(searchValue)
        else:
            retEvents = self.EHandler.searchZip(searchValue)
        
        # Refine search
        if (not searchDate == ""):
            retEvents = self.EHandler.refineSearchDate(retEvents, searchDate)
        if (not searchTags == [""]):
            retEvents = self.EHandler.refineSearchTags(retEvents, searchTags)

        return retEvents

    # Returns events with specific user in RSVP
    def searchEventsRSVP(self, user):
        username = user.getUsername()
        retEvents = self.EHandler.searchRSVP(username)
        return retEvents