# Event Handler: Stores event data and allows searching for events
from typing import List
from EventIO import EventIO
from dataClasses.EventData import EventData

class EventHandler:
    def __init__(self):
        self.objIO = EventIO()
        self.objIO.loadData()
        self.events = self.objIO.getData()
        self.oldEvents = self.objIO.getOldData()
    
    # Sends events to EventIO and saves data
    def saveChanges(self) -> None:
        self.objIO.setData(self.events)
        self.objIO.saveData()
    
    # Returns named event
    def getEvent(self, name: str) -> EventData:
        for event in self.events:
            if event.isEventname(name):
                return event
        return None

    # Returns all events
    def getAllEvents(self) -> List[EventData]:
        return self.events
    
    # Returns named out-of-date event
    def getOldEvent(self, name: str) -> EventData:
        for event in self.oldEvents:
            if event.isEventname(name):
                return event
        return None

    # Returns all out-of-date events
    def getOldEvents(self) -> List[EventData]:
        return self.oldEvents
    
    # Add user to event (Returns True if successful)
    def addRSVP(self, username: str, eventName: str) -> bool:
        for event in self.events:
            if event.isEventname(eventName):
                event.addRSVP(username)
                self.saveChanges()
                return True
        return False
    
    # Remove user from event (Returns True if successful)
    # Will not remove the organizer
    def removeRSVP(self, username: str, eventName: str) -> bool:
        for event in self.events:
            if event.isEventname(eventName):
                if (event.isOrganizerName(username)):
                    return False
                event.removeRSVP(username)
                self.saveChanges()
                return True
        return False

    # Take as input a new EventData object, stores it in events list, then saves to file
    # Returns True if event is created
    def newEvent(self, newEvent: EventData) -> bool:
        # Check if event already exists (same exact name)
        for event in self.events:
            if event.isEvent(newEvent):
                return False
        # Check if valid recurring (if monthly, only allows day <28)
        if (not newEvent.isValidMonthly()):
            return False

        self.events.append(newEvent)
        self.saveChanges()
        return True

    # Deletes event from memory, then saves to file
    def removeEvent(self, remEvent: EventData) -> bool:
        for event in self.events:
            if event.isEvent(remEvent):
                self.events.remove(event)
                self.saveChanges()
                return True
        return False
    
    # Replaces event in memory, then saves to file
    def replaceEvent(self, newEvent: EventData) -> bool:
        for event in self.events:
            if event.isEvent(newEvent):
                self.events.remove(event)
                self.events.append(newEvent)
                self.saveChanges()
                return True
        return False

    # Moves event to old events, then saves to file
    def retireEvent(self, oldEvent: EventData) -> bool:
        for event in self.events:
            if event.isEvent(oldEvent):
                self.events.remove(event)
                self.oldEvents.append(event)
                self.saveChanges()
                return True
        return False

    # Returns events matching given name (If the name is a substring of the event name)
    def searchName(self, name: str) -> List[EventData]:
        retEvents = []
        for event in self.events:
            if name in event.getName():
                retEvents.append(event)
        return retEvents

    # Returns events with given organizer
    def searchOrganizer(self, organizer: str) -> List[EventData]:
        retEvents = []
        for event in self.events:
            if event.isOrganizerName(organizer):
                retEvents.append(event)
        return retEvents

    # Returns events with given username in RSVP list
    def searchRSVP(self, username: str) -> List[EventData]:
        retEvents = []
        for event in self.events:
            if event.hasUserRSVP(username):
                retEvents.append(event)
        return retEvents

    # Returns events in given zip code
    def searchZip(self, zip: str) -> List[EventData]:
        retEvents = []
        for event in self.events:
            if event.inZipCode(zip):
                retEvents.append(event)
        return retEvents

    # Returns events at given date that are in eventList
    def refineSearchDate(self, eventList: List[EventData], date: str):
        retEvents = []
        for event in eventList:
            if (event.isOnDate(date)):
                retEvents.append(event)

        return retEvents

    # Returns events with given tags that are in eventList
    def refineSearchTags(self, eventList: List[EventData], tags: List[str]):
        retEvents = []
        for event in eventList:
            if (event.hasTags(tags)):
                retEvents.append(event)
        
        return retEvents
    
    # Checks all events and removes out-of-date events
    def checkActive(self) -> bool:
        for event in self.events:
            if not event.isActive():
                self.retireEvent(event)
