# Event Handler: Stores event data and allows searching for events
from EventIO import EventIO
from EventData import EventData

class EventHandler:
    def __init__(self):
        self.objIO = EventIO()
        self.objIO.loadData()
        self.events = self.objIO.getData()
    
    # Sends events to EventIO and saves data
    def saveChanges(self):
        self.objIO.setData(self.events)
        self.objIO.saveData()
    
    # Returns named event
    def getEvent(self, name):
        for event in self.events:
            if event.isEventname(name):
                return event
        return None

    # Returns all events
    def getAllEvents(self):
        return self.events
    
    # Add user to event (Returns True if successful)
    def addRSVP(self, username, eventName):
        for event in self.events:
            if event.isEventname(eventName):
                event.addRSVP(username)
                self.saveChanges()
                return True
        return False
    
    # Remove user from event (Returns True if successful)
    # Will not remove the organizer
    def removeRSVP(self, username, eventName):
        for event in self.events:
            if event.isEventname(eventName):
                if (event.isOrganizerName(username)):
                    return False
                event.removeRSVP(username)
                self.saveChanges()
                return True
        return False

    # Take as input a new EventData object, store it in events list, then save to file
    # Returns True if event is created
    def newEvent(self, newEvent):
        # Check if event already exists (same exact name)
        for event in self.events:
            if event.isEvent(newEvent):
                return False

        self.events.append(newEvent)
        self.saveChanges()
        return True

    # Returns events matching given name (If the name is a substring of the event name)
    def searchName(self, name):
        retEvents = []
        for event in self.events:
            if name in event.getName():
                retEvents.append(event)
        return retEvents

    # Returns events with given organizer
    def searchOrganizer(self, organizer):
        retEvents = []
        for event in self.events:
            if event.isOrganizerName(organizer):
                retEvents.append(event)
        return retEvents

    # Returns events in given zip code
    def searchZip(self, zip):
        retEvents = []
        for event in self.events:
            if event.inZipCode(zip):
                retEvents.append(event)
        return retEvents

    # Returns events at given date that are in eventList
    def refineSearchDate(self, eventList, date):
        retEvents = []
        for event in eventList:
            if (event.isOnDate(date)):
                retEvents.append(event)

        return retEvents

    # Returns events with given tags that are in eventList
    def refineSearchTags(self, eventList, tags):
        retEvents = []
        for event in eventList:
            if (event.hasTags(tags)):
                retEvents.append(event)
        
        return retEvents
