#                                            Summary:
#
# This class is the main event handler for our program. It allows for the managing and creation
# of events and event data, the creation and application of event tags, the creation and editing
# of RSVPs, and the searching of different events through tags, popularity, location,
# and organization.
#
#                                           Data members:
#
# events, oldEvents, setData, saveData
#
#
#                                            Methods:
#
# "init": This is the "constructor" method, it initializes variables and makes calls
# to other classes.
#
# "saveChanges": This method passes data to the "EventIO" class and saves it.
#
# "getEvent": This method returns the name of each event.
#
# "getAllEvents": This short method returns all events to the "EventData" list.
#
# "getOldEvent": Returns an event that has already passed.
#
# "getOldEvents": Returns every out of date event.
#
# "getOneDayEvents": Appends the list by returning all events that start within
# 24 hours.
#
# "addRSVP": Allows users to RSVP by adding them to the event. Has a self check
# which returns "true" if the addition was sucessful.
#
# "removeRSVP": Removes users from the RSVP list, but will not change the organizer. 
# Also contains a self check that will return "true" if the change was sucessful.
#
# "newEvent": Reads user input to create a new event and saves it to the "database". 
# It will first check to see if an event exists with the same name, and will return 
# "true" if the event is sucessfully created.
#
# "removeEvent": Removes an event from the registry, and then updates the "database".
#
# "replaceEvent": Replaces an event, and then updates the "database".
#
# "retireEvent": Locates passed event as a retired event, and updates the "database".
#
# "searchName": Searches the databse for events by name, and returns events with
# matching names.
#
# "searchOrganizer": Searches for events by the specified organizer, and returns
# matching searches.
#
# "searchRSVP": Returns a list of users who RSVP'd to an event.
#
# "searchZIP": Searches for events in the database by ZIP code.
#
# "refineSearchDate": Narrows the search by applying a date parameter.
#
# "searchPopular": Returns the three events with the most RSVPs. 
#
# "refineSearchTags": Narrow the search by applying tags to searched events.
#
# "checkActive": Scans every event and removed passed events.

from typing import List
from EventIO import EventIO
from dataClasses.EventData import EventData

class EventHandler:
    def __init__(self):
        self.objIO: EventIO = EventIO()
        self.objIO.loadData()
        self.events: List[EventData] = self.objIO.getData()
        self.oldEvents: List[EventData] = self.objIO.getOldData()
    
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
    
    # Returns events starting within 1 day
    def getOneDayEvents(self) -> List[EventData]:
        retEvents = []
        for event in self.events:
            if event.isNextDay():
                retEvents.append(event)
        return retEvents
    
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
        if (not newEvent.isValidRecurring()):
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
                if oldEvent.isRecurring():
                    self.events.append(oldEvent.getNextRecurringEvent())
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

    # Returns 3 events with the most RSVP's
    def searchPopular(self):
        retEvents = []
        currentPopular = None
        if (len(self.events) <= 3):
            return self.events
        for i in range(3):
            numRSVP = 0
            for event in self.events:
                currentNameList = [entry.getName() for entry in retEvents]
                if (event.getName() in currentNameList):
                    continue
                else:
                    eventRSVPNum = event.getRSVPNum()
                    if (eventRSVPNum > numRSVP):
                        numRSVP = eventRSVPNum
                        currentPopular = event
            retEvents.append(currentPopular)
        return retEvents
    
    # Checks all events and removes out-of-date events
    def checkActive(self) -> List[EventData]:
        retEvents = []
        for event in self.events:
            if not event.isActive():
                retEvents.append(event)
                self.retireEvent(event)
        return retEvents
