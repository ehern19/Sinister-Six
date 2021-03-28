# Process Manager: Provides methods that can be called by the website application
# Passes arguments from website to handlers and data from handlers to website
# Where required, converts from website arguments to function arguments
from datetime import datetime
from typing import List
from EventHandler import EventHandler
from LoginHandler import LoginHandler
from dataClasses.EventData import EventData
from dataClasses.UserData import UserData

class ProcessManager:
    def __init__(self):
        self.EHandler = EventHandler()
        self.LHandler = LoginHandler()

    # Takes login input from web page and passes it to LoginHandler
    def passLogin(self, username: str, password: str) -> bool:
        return self.LHandler.isValidLogin(username, password)
    
    def passUsername(self, username: str) -> UserData:
        return self.LHandler.getUser(username)

    def passNewUser(self, username: str, password: str, phone: str, email: str) -> bool:
        newUser = UserData(username, password, phone, email)
        return self.LHandler.newUser(newUser)

    # Takes user input from web page and passes it to EventHandler
    def passRSVP(self, username: str, eventName: str) -> bool:
        return self.EHandler.addRSVP(username, eventName)

    def passLeaveRSVP(self, username: str, eventName: str) -> bool:
        return self.EHandler.removeRSVP(username, eventName)
    
    def passGetRSVP(self, event: EventData) -> List[UserData]:
        retRSVP = []
        for username in event.getRSVP():
            user = self.LHandler.getUser(username)
            if user:
                retRSVP.append(user)
        return retRSVP
    
    def passEditEvent(self, eventName: str, reset: bool, time: str, location: str, zip: str, tags: List[str], summary: str) -> bool:
        event = self.getEvent(eventName)
        if (reset):
            event.resetOptional()
        if (not time == ""):
            event.setTime(time)
        if (not location == ""):
            event.setLocation(location)
        if (not zip == ""):
            event.setZip(zip)
        if (not tags == []):
            event.setTags(tags)
        if (not summary == ""):
            event.setSummary(summary)
        return self.EHandler.replaceEvent(event)

    def passNewEvent(self, name: str, date: str, organizer: str, recurring: str, time: str="TBD", location: str="TBD", zip: str="TBD", tags: List[str]=[], summary: str="") -> bool:
        newEvent = EventData.EventBuilder(name, date, organizer, recurring)
        if (not time == "TBD"):
            newEvent.Time(time)
        if (not location == "TBD"):
            newEvent.Location(location)
        if (not zip == "TBD"):
            newEvent.Zip(zip)
        if (not tags == []):
            newEvent.Tags(tags)
        if (not summary == ""):
            newEvent.Summary(summary)
        newEvent = newEvent.build()
        return self.EHandler.newEvent(newEvent)

    def passRemEvent(self, event: EventData) -> bool:
        return self.EHandler.removeEvent(event)
        
    def passCheckActive(self) -> bool:
        self.EHandler.checkActive()

    # Returns the named event
    def getEvent(self, name: str) -> EventData:
        return self.EHandler.getEvent(name)
    
    # Returns the named out-of-date event
    def getOldEvent(self, name: str) -> EventData:
        return self.EHandler.getOldEvent(name)

    # Returns all events after sorting by chronological order
    def getAllEvents(self) -> List[EventData]:
        retEvents = self.EHandler.getAllEvents().copy()
        retEvents.sort()
        return retEvents
    
    # Returns all out-of-date events after sorting by chronological order
    def getOldEvents(self) -> List[EventData]:
        retEvents = self.EHandler.getOldEvents().copy()
        retEvents.sort()
        return retEvents

    # Return appropriate search results
    def searchEvents(self, searchType: str, searchValue: str, searchDate: str="", searchTags: List[str]=[""]) -> List[EventData]:
        if (searchType == "name"):
            retEvents = self.EHandler.searchName(searchValue)
        elif (searchType == "organizer"):
            retEvents = self.EHandler.searchOrganizer(searchValue)
        else:
            retEvents = self.EHandler.searchZip(searchValue)
        
        # Refine search
        if (not searchDate == ""):
            searchDate = datetime.strptime(searchDate, "%Y-%m-%d").date()
            retEvents = self.EHandler.refineSearchDate(retEvents, searchDate)
        if (not searchTags == [""]):
            retEvents = self.EHandler.refineSearchTags(retEvents, searchTags)

        retEvents.sort()
        return retEvents

    # Returns events with specific user in RSVP
    def searchEventsRSVP(self, user: UserData) -> List[EventData]:
        username = user.getUsername()
        retEvents = self.EHandler.searchRSVP(username)
        retEvents.sort()
        return retEvents
    