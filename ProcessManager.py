#                                            Summary:
# This class is the go between for the handler classes and the frontend website, 
# converting arguments when required.
#
#
#
#                                           Data Members:
#
# EHandler, LHandler
#
#
#
#                                            Methods:
#
# "init": This is the class' constructor, it intializes and calls the handler classes.
#
# "passLogin": Gets the login input from the webpage and passes it to the handler.
#
# "passUsername": Gets the username input from the webpage and passes it to the handler.
#
# "passNewUser": Gets the newUser input from the webpage and passes it to the handler.
#
# "passEditUser": Gets the user input from the webpage and passes it to the handler for editing.
#
# "passRSVP": Gets the RSVP input from the webpage and passes it to the handler.
#
# "passLeaveRSVP": Gets the RSVP input from the webpage and passes it to the handler for leaving.
#
# "passGetRSVP": Gets the RSVP input from the webpage and passes it to the handler for the user.
#
# "passEDitEvent": Gets the event info from the webpage and passes it to the handler for editing.
#
# "passNewEvent": Gets the new event info from the webpage and passes it to the handler.
#
# "passRemEvent": Gets the remaining event info from the webpage and passes it to the handler.
#
# "passCheckActive":Passes events to the checkActive method.
#
# "getEvent": Returns the event info.
#
# "getOldEvents": Gets info for old events.
#
# "getAllEvents": Gets info for all events, and sorts them by chronological
# order.
#
# "getOldEvents": Gets info for all passed events, and sorts them by chronological
# order.
#
# "getPopularEvents": Gets info for the three events with the most RSVPs.
#
# "getOneDayEvents": Gets info for all events starting within 24 hours.
#
# "searchEvents": Searches for events by specified parameters.
#
# "searchEventsRSVP": Searches for events that have a specified user RSVP'd.
#
# "allowImageFile": Returns true if the image uploaded is allowed.
#
# "getNextEventImgName": Gets the name for the image associated with a given event.
#
# "getNextUserImageName": Gets the name of the next image associated with a specified user.

import os
from datetime import datetime
from typing import List
from EventHandler import EventHandler
from LoginHandler import LoginHandler
from dataClasses.EventData import EventData
from dataClasses.UserData import UserData
from dataClasses.extras import DATABASE_PATH, EVENT_IMAGES, USER_IMAGES

class ProcessManager:
    def __init__(self):
        self.EHandler = EventHandler()
        self.LHandler = LoginHandler()

    # Takes login input from web page and passes it to LoginHandler
    def passLogin(self, username: str, password: str) -> bool:
        return self.LHandler.isValidLogin(username, password)
    
    def passUsername(self, username: str) -> UserData:
        return self.LHandler.getUser(username)

    def passNewUser(self, username: str, password: str, phone: str, email: str, zip: str) -> bool:
        newUser = UserData(username, password, phone, email, zip)
        return self.LHandler.newUser(newUser)
    
    def passEditUser(self, username: str, phone: str, email: str) -> bool:
        if (not phone and not email):
            return True
        user = self.passUsername(username)
        if (phone):
            user.setPhone(phone)
        if (email):
            user.setEmail(email)
        return self.LHandler.replaceUser(user)

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
        
    def passCheckActive(self) -> List[EventData]:
        return self.EHandler.checkActive()

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
    
    # Returns 3 popular events (highest # RSVP's)
    def getPopularEvents(self) -> List[EventData]:
        return self.EHandler.searchPopular()

    # Returns list of events that start within 1 day
    def getOneDayEvents(self) -> List[EventData]:
        return self.EHandler.getOneDayEvents()

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
    
    # Returns True if filename extension is of an allowed filetype
    def allowedImageFile(self, filename: str) -> bool:
        if ('.' in filename):
            extension = filename.rsplit('.', 1)[1].lower()
            if (extension in ["png", "jpg", "jpeg"]):
                return True
            else:
                return False
        else:
            return False
    
    # Returns the next image filename (<event>.jpg# + 1) for a given event name
    def getNextEventImgName(self, eventName: str) -> str:
        eventPath = DATABASE_PATH + EVENT_IMAGES
        version = 0
        baseName = eventName + ".jpg"
        imageName = baseName + str(version)
        while(os.path.isfile(eventPath + imageName)):
            version = version + 1
            imageName = baseName + str(version)
        return imageName
    
    # Returns the next image filename (<event>.jpg# + 1) for a given user name
    def getNextUserImgName(self, username: str) -> str:
        userPath = DATABASE_PATH + USER_IMAGES
        version = 0
        baseName = username + ".jpg"
        imageName = baseName + str(version)
        while(os.path.isfile(userPath + imageName)):
            version = version + 1
            imageName = baseName + str(version)
        return imageName
