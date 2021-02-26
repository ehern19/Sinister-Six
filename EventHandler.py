# Event Handler
from RSVPHandler import *
from EventData import *

class EventHandler:
    def __init__(self):
        self.eventNames = []
        self.events = []
        self.RSVPHandler = RSVPHandler()
    
    # Return names of all events
    def getEventList(self):
        return self.eventNames
    
    # Load events to memory (EventData objects in self.events)
    def loadEvents(self, names, times, tags):
        self.eventNames = names
        for eventName in names:
            self.events.append(EventData(eventName, times[eventName], tags[eventName]))
    
    # Load RSVPLists to event objects
    def loadRSVPLists(self, listData):
        self.RSVPHandler.setLists(listData)
        for event in self.events:
            event.loadRSVPList(self.RSVPHandler.loadList(event.getName()))
    
    # Add user to event RSVPList
    def addRSVP(self, eventName, userName):
        if not eventName in self.eventNames:
            print("Event not found")
            return False
        else:
            for event in self.events:
                if event.getName() == eventName:
                    return event.addRSVP(userName)
    
    # Remove user from event RSVPList
    def removeRSVP(self, eventName, userName):
        if not eventName in self.eventNames:
            print("Event not found")
            return False
        else:
            for event in self.events:
                if event.getName() == eventName:
                    return event.removeRSVP(userName)
    
    # Create a new event
    def addEvent(self, name, time, tags):
        if (name in self.eventNames):
            print(f"Event ({name}) already exists")
            return False
        else:
            
            # TODO
            print(f"Successfully created {name} event")
            return True