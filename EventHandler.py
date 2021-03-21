# Event Handler: Stores event data and allows searching for events
from EventIO import EventIO
from EventData import EventData

class EventHandler:
    def __init__(self):
        self.objIO = EventIO()
        self.objIO.loadData()
        self.events = self.objIO.getData()
    
    # Return all events
    def getAllEvents(self):
        return self.events

    # Take as input a new EventData object, store it in events list, then save to file
    # Returns True if event is created
    def newEvent(self, newEvent):
        # Check if event already exists (same exact name)
        for event in self.events:
            if event.isEvent(newEvent):
                return False

        self.events.append(newEvent)
        self.objIO.setData(self.events)
        self.objIO.saveData()
        return True

    # Return events matching given name (If the name is a substring of the event name)
    def searchName(self, name):
        retEvents = []
        for event in self.events:
            if name in event.getName():
                retEvents.append(event)
        return retEvents

    # Return all events at given date/time (time not necessary)
    def searchDate(self,date, time=None):
        retEvents = []
        if (time == None):
            for event in self.events:
                if (event.getDate() == date):
                    retEvents.append(event)
        else:
            for event in self.events:
                if (event.getDate() == date and event.getTime() == time):
                    retEvents.append(event)
        return retEvents
