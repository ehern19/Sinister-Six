# Event Data: Stores the data for one event

class EventData:
    def __init__(self, eventName, eventTime, eventDate, eventLocation, eventTags, eventRSVP):
        self.name = eventName
        self.time = eventTime
        self.date = eventDate
        self.location = eventLocation
        self.tags = eventTags
        self.organizer = eventRSVP[0]
        self.RSVP = eventRSVP[1:]
    
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
    
    # Add user to RSVP list (Returns True if successful)
    def addRSVP(self, user):
        if user in self.RSVP:
            return False
        else:
            self.RSVP.append(user)
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