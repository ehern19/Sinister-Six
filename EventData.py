# Event Data: Stores the data for one event

class EventData:
    def __init__(self, newName, newTime, newDate, newLocation, newTags, newRSVP):
        self.name = newName
        self.time = newTime
        self.date = newDate
        self.location = newLocation
        self.tags = newTags
        self.organizer = newRSVP[0]
        self.RSVP = newRSVP[1:]
        self.summary = ""
    
    # Get methods for data stored in object
    def getName(self):
        return self.name
    
    def getTime(self):
        return self.time

    def getDate(self):
        return self.date

    def getLocation(self):
        return self.location
    
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

    # Printing for debugging
    def printAllData(self):
        print(f"Event: {self.name}\n\tTime: {self.time}\n\tDate: {self.date}\n\tLocation: {self.location}\n\tTags: {self.tags}\n\tOrganizer: {self.organizer}\n\tRSVP List: {self.RSVP}\n")