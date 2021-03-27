# Event Data: Stores the data for one event
from datetime import date, datetime

class EventData:
    def __init__(self, newName, newTime, newDate, newLocation, newZip, newTags, newRSVP, newSummary):
        self.name = newName
        self.time = newTime
        self.date = datetime.strptime(newDate, "%Y-%m-%d").date()
        self.location = newLocation
        self.zip = newZip
        self.tags = newTags
        self.organizer = newRSVP[0]
        self.RSVP = newRSVP[1:]
        self.summary = newSummary
    
    # Get methods for data stored in object
    def getName(self):
        return self.name
    
    def getTime(self):
        return self.time

    def getDate(self):
        return self.date

    def getDateStr(self):
        return self.date.strftime("%Y-%m-%d")

    def getLocation(self):
        return self.location
    
    def getZip(self):
        return self.zip
    
    def getTags(self):
        return self.tags

    def getOrganizer(self):
        return self.organizer

    def getRSVP(self):
        return self.RSVP

    def getSummary(self):
        return self.summary
    
    # Returns True if given event matches the object's name
    def isEvent(self, otherEvent):
        return otherEvent.getName().lower() == self.name.lower()

    # Returns True if given event name matches the object's name
    def isEventname(self, otherName):
        return otherName.lower() == self.name.lower()

    # Returns True if given user name matches the object's organizer name
    def isOrganizerName(self, username):
        return username.lower() == self.organizer.lower()

    # Returns True if given zip code matches the object's zip code
    def inZipCode(self, zip):
        return self.zip == zip
    
    # Returns True if given date matches the object's date
    def isOnDate(self, date):
        return self.date == date
        
    # Returns True if given username is in the object's RSVP list
    def hasUserRSVP(self, username):
        return username in self.RSVP

    # Returns True if given tag list is in the object's tag list 
    # (Has all tags, can have more)
    def hasTags(self, tags):
        for tag in tags:
            if (tag not in self.tags):
                return False
        return True

    # Returns True if the object's date is on or after the current date
    def isActive(self):
        now = date.today()
        return now <= self.date

    # Add user to RSVP list (Returns True if successful)
    def addRSVP(self, username):
        if username in self.RSVP:
            return False
        else:
            self.RSVP.append(username)
            return True
    
    # Remove user from RSVP list (Returns True if successful)
    def removeRSVP(self, user):
        if not user in self.RSVP:
            return False
        else:
            self.RSVP.remove(user)
            return True

    # Defines less than operator for EventData objects
    # Defined to compare dates first, then names
    # Used in sorting list of events
    def __lt__(self, other):
        return (self.date, self.name) < (other.date, other.name)

    # Printing for debugging
    def printAllData(self):
        print(f"Event: {self.name}\n\tTime: {self.time}\n\tDate: {self.getDateStr()}\n\tLocation: {self.location}\n\tTags: {self.tags}\n\tOrganizer: {self.organizer}\n\tRSVP List: {self.RSVP}\n")
    
    def printName(self):
        print(f"Event: {self.name}")