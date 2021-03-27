# Event Data: Stores the data for one event
from datetime import date, datetime
from pytz import timezone

# Calculates offset between Central Time and UTC
# Time is stored as a datetime object in UTC
# This is done to prevent errors due to daylight savings
def setOffset():
    centralTime = datetime.now()
    centralTime = centralTime.astimezone(timezone("US/Central"))
    return centralTime.utcoffset()

class EventData:
    # For use converting Central Time to UTC
    CentralOffset = setOffset()

    def __init__(self, builder):
        # Required Fields
        self.name = builder.name
        self.date = builder.date
        self.organizer = builder.organizer

        # Optional Fields
        self.time = builder.time
        self.location = builder.location
        self.zip = builder.zip
        self.tags = builder.tags
        self.RSVP = builder.rsvp
        self.summary = builder.summary
    
    # Get methods for data stored in object
    def getName(self):
        return self.name

    def getTimeStr(self):
        if (self.time == "TBD"):
            return self.time
        else:
            time = self.time + self.CentralOffset
            return time.strftime("%H:%M")

    def getDateStr(self):
        return self.date.strftime("%Y-%m-%d")

    def getLocation(self):
        return self.location
    
    def getZip(self):
        return self.zip
    
    # def getTags(self):
    #     return self.tags
    
    def getTagStrs(self):
        tags = [entry.replace('_', ' ') for entry in self.tags]
        return tags

    def getOrganizer(self):
        return self.organizer

    def getRSVP(self):
        return self.RSVP

    def getSummary(self):
        return self.summary
    
    # Set methods for optional data stored in object
    # Used when editing events
    # Cannot change required fields (name, date, organizer)
    def setTime(self, newCentralTime):
        centralTime = datetime.strptime(newCentralTime, "%H:%M")
        self.time = centralTime - self.CentralOffset

    def setLocation(self, newLocation):
        self.location = newLocation

    def setZip(self, newZip):
        self.zip = newZip

    def setTags(self, newTags):
        self.tags = newTags

    def setSummary(self, newSummary):
        self.summary = newSummary
    
    def resetOptional(self):
        self.time = "TBD"
        self.location = "TBD"
        self.zip = "TBD"
        self.tags = ["No Tags"]
        self.summary = "No Summary"
    
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

    # Returns True if the object's date is on or after the current date and time
    def isActive(self):
        now = datetime.now() - self.CentralOffset
        today = now.date()
        if (today < self.date):
            return True
        else:
            return self.time.time() < now.time()

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
    # Defined to compare dates first, then times, then names
    # Used in sorting list of events
    def __lt__(self, other):
        return (self.date, self.getTimeStr(), self.name) < (other.date, self.getTimeStr(), other.name)

    # Printing for debugging
    def printAllData(self):
        print(f"Event: {self.name}\n  Date: {self.getDateStr()}\n  Time: {self.getTimeStr()}\n  Location: {self.location}\n  Tags: {self.tags}\n  Organizer: {self.organizer}\n  RSVP List: {self.RSVP}\n")
    
    def printName(self):
        print(f"Event: {self.name}")

    class EventBuilder:
        def __init__(self, newName, newDate, newOrganizer):
            # Required Fields
            self.name = newName
            self.date = datetime.strptime(newDate, "%Y-%m-%d").date()
            self.organizer = newOrganizer

            # Optional Fields
            self.time = "TBD"
            self.location = "TBD"
            self.zip = "TBD"
            self.tags = []
            self.rsvp = []
            self.summary = "No Summary"
        
        def __new__(cls, newName, newDate, newOrganizer):
            return super(EventData.EventBuilder, cls).__new__(cls)
        
        def build(self):
            event = EventData(self)
            return event
        
        # Optional Field Constructors
        def Time(self, newCentralTime):
            if (newCentralTime == "TBD" or newCentralTime == ""):
                self.time = "TBD"
                return self
            else:
                centralTime = datetime.strptime(newCentralTime, "%H:%M")
                self.time = centralTime - EventData.CentralOffset
                return self
        
        def Location(self, newLocation):
            if (newLocation == ""):
                self.location = "TBD"
            else:
                self.location = newLocation
            return self
        
        def Zip(self, newZip):
            if (newZip == ""):
                self.zip = "TBD"
            else:
                self.zip = newZip
            return self

        def Tags(self, newTags):
            if (newTags == []):
                self.tags = ["No Tags"]
            else:
                self.tags = newTags
            return self
        
        def RSVP(self, newRSVP):
            self.rsvp = newRSVP
            return self

        def Summary(self, newSummary):
            self.summary = newSummary
            return self
        
if __name__=="__main__":
    Event1 = EventData.EventBuilder("Event1", "2021-01-01", "user1").build()
    Event1.printAllData()

    Event2 = (EventData.EventBuilder("Event2", "2021-03-31", "user2")
              .Time("10:30")
              .Location("Town Hall")
              .Tags(["tag1", "tag2"])
              .RSVP(["user1", "user3"])
              .build()
              )
    Event2.printAllData()