# Event Handler
from RSVPHandler import *
from EventData import *

class EventHandler:
    def __init__(self):
        self.eventNames = []
        self.events = []
        self.RSVPHandler = RSVPHandler()
    
    # Return names of all events
    def getAllEvents(self):
        return self.eventNames

    # Return dictionary of {eventName:time}
    def getAllEventTimes(self):
        times = {}
        for event in self.events:
            times.update({event.getName():event.getTime()})
        return times

    # Return dictionary of {eventName:[tags]}
    def getAllEventTags(self):
        tags = {}
        for event in self.events:
            tags.update({event.getName():event.getTags()})
        return tags

    # Return dictionary of {eventName:[RSVPList]}
    def getAllRSVPLists(self):
        allRSVPLists = {}
        for event in self.events:
            allRSVPLists.update({event.getName():event.getRSVPList()})
        return allRSVPLists
    
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
    def addEvent(self, name, time, tags, user):
        if (name in self.eventNames):
            print(f"Event ({name}) already exists")
            return False
        else:
            tagList = []
            tags = tags.split()
            # Replace "_" with " " ("_" is in the file so that tags with " " are still read as one tag)
            for tag in tags:
                tag = tag.replace('_', ' ')
                # Check if a tag is duplicated for the event
                if tag in tagList:
                    print(f"Error: {name} has duplicate tag \"{tag}\" in new event creation")
                    return False
                tagList.append(tag)

            self.eventNames.append(name)
            newEvent = EventData(name, time, tags)
            newEvent.addRSVP(user)
            self.events.append(newEvent)
            print(f"Successfully created {name} event")
            return True

    # Printing for debugging
    def printAllEvents(self):
        for event in self.events:
            event.printAllData()