# Event Data: Stores the data for one event
from datetime import date, datetime, timedelta
from dateutil import relativedelta
from pytz import timezone
from typing import List

# Calculates offset between Central Time and UTC
# Time is stored as a datetime object in UTC
# This is done to prevent errors due to daylight savings
def setOffset() -> timedelta:
    centralTime = datetime.now()
    centralTime = centralTime.astimezone(timezone("US/Central"))
    return centralTime.utcoffset()

class EventData:
    # For use converting Central Time to UTC
    CentralOffset = setOffset()
    
    # Get methods for data stored in object
    def getName(self) -> str:
        return self.name

    def getTimeStr(self) -> str:
        if (self.time == "TBD"):
            return self.time
        else:
            time = self.time + self.CentralOffset
            return time.strftime("%H:%M")

    def getDateStr(self) -> str:
        return self.date.strftime("%Y-%m-%d")

    def getLocation(self) -> str:
        return self.location
    
    def getZip(self) -> str:
        return self.zip
        
    def getTagStrs(self) -> List[str]:
        tags = [entry.replace('_', ' ') for entry in self.tags]
        return tags

    def getOrganizer(self) -> str:
        return self.organizer

    def getRSVP(self) -> List[str]:
        return self.RSVP

    def getSummary(self) -> str:
        return self.summary
    
    def getRecurring(self) -> str:
        return self.recurring
    
    # Set methods for optional data stored in object
    # Used when editing events
    # Cannot change required fields (name, date, organizer)
    def setTime(self, newCentralTime: str) -> None:
        centralTime = datetime.strptime(newCentralTime, "%H:%M")
        self.time = centralTime - self.CentralOffset

    def setLocation(self, newLocation: str) -> None:
        self.location = newLocation

    def setZip(self, newZip: str) -> None:
        self.zip = newZip

    def setTags(self, newTags: str) -> None:
        self.tags = newTags

    def setSummary(self, newSummary: str) -> None:
        self.summary = newSummary
    
    def resetOptional(self) -> None:
        self.time = "TBD"
        self.location = "TBD"
        self.zip = "TBD"
        self.tags = ["No Tags"]
        self.summary = "No Summary"
    
    # Returns True if given event name matches the object's name
    def isEventname(self, otherName: str) -> bool:
        return otherName.lower() == self.name.lower()

    # Returns True if given user name matches the object's organizer name
    def isOrganizerName(self, username: str) -> bool:
        return username.lower() == self.organizer.lower()

    # Returns True if given zip code matches the object's zip code
    def inZipCode(self, zip: str) -> bool:
        return self.zip == zip
    
    # Returns True if given date matches the object's date
    def isOnDate(self, date: date) -> bool:
        return self.date == date
        
    # Returns True if given username is in the object's RSVP list
    def hasUserRSVP(self, username: str) -> bool:
        return username in self.RSVP

    # Returns True if given tag list is in the object's tag list 
    # (Has all tags, can have more)
    def hasTags(self, tags: List[str]) -> bool:
        for tag in tags:
            if (tag not in self.tags):
                return False
        return True

    # Returns True if the object's date is on or after the current date and time
    def isActive(self) -> bool:
        now = datetime.now() - self.CentralOffset
        today = now.date()
        if (today < self.date):
            return True
        else:
            return self.time.time() < now.time()
    
    # Returns True if the object is a recurring event
    def isRecurring(self):
        return not self.recurring == "none"

    # Returns True if the object is a valid monthly recurring event or is not a monthly recurring event
    def isValidRecurring(self):
        if (self.recurring == "monthly"):
            return self.date.day <= 28
        else:
            return True

    # Add user to RSVP list (Returns True if successful)
    def addRSVP(self, username: str) -> bool:
        if username in self.RSVP:
            return False
        else:
            self.RSVP.append(username)
            return True
    
    # Remove user from RSVP list (Returns True if successful)
    def removeRSVP(self, user: str) -> bool:
        if not user in self.RSVP:
            return False
        else:
            self.RSVP.remove(user)
            return True

    # Printing for debugging
    def printAllData(self) -> None:
        print(f"Event: {self.name}\n  Date: {self.getDateStr()}\n  Time: {self.getTimeStr()}\n  Location: {self.location}\n  Tags: {self.tags}\n  Organizer: {self.organizer}\n  RSVP List: {self.RSVP}\n")
    
    def printName(self) -> None:
        print(f"Event: {self.name}")

    class EventBuilder:
        pass

# EventBuilder Methods (Moved to allow defining of arguments/return variables)
def EB__init__(self, newName, newDate, newOrganizer, newRecurring) -> EventData.EventBuilder:
    # Required Fields
    self.name = newName
    self.date = datetime.strptime(newDate, "%Y-%m-%d").date()
    self.organizer = newOrganizer
    self.recurring = newRecurring

    # Optional Fields
    self.time = "TBD"
    self.location = "TBD"
    self.zip = "TBD"
    self.tags = []
    self.rsvp = []
    self.summary = "No Summary"
        
def EB__new__(cls, newName: str, newDate: str, newOrganizer: str, newRecurring: str) -> EventData.EventBuilder:
    return super(EventData.EventBuilder, cls).__new__(cls)

def EBbuild(self) -> EventData.EventBuilder:
    event = EventData(self)
    return event

# Optional Field Constructors
def EBTime(self, newCentralTime: str) -> EventData.EventBuilder:
    if (newCentralTime == "TBD" or newCentralTime == ""):
        self.time = "TBD"
        return self
    else:
        centralTime = datetime.strptime(newCentralTime, "%H:%M")
        self.time = centralTime - EventData.CentralOffset
        return self

def EBLocation(self, newLocation: str) -> EventData.EventBuilder:
    if (newLocation == ""):
        self.location = "TBD"
    else:
        self.location = newLocation
    return self

def EBZip(self, newZip: str) -> EventData.EventBuilder:
    if (newZip == ""):
        self.zip = "TBD"
    else:
        self.zip = newZip
    return self

def EBTags(self, newTags: str) -> EventData.EventBuilder:
    if (newTags == []):
        self.tags = ["No Tags"]
    else:
        self.tags = newTags
    return self

def EBRSVP(self, newRSVP: List[str]) -> EventData.EventBuilder:
    self.rsvp = newRSVP
    return self

def EBSummary(self, newSummary: str) -> EventData.EventBuilder:
    self.summary = newSummary
    return self

EventData.EventBuilder.__init__ = EB__init__
EventData.EventBuilder.__new__ = EB__new__
EventData.EventBuilder.build = EBbuild
EventData.EventBuilder.Time = EBTime
EventData.EventBuilder.Location = EBLocation
EventData.EventBuilder.Zip = EBZip
EventData.EventBuilder.Tags = EBTags
EventData.EventBuilder.RSVP = EBRSVP
EventData.EventBuilder.Summary = EBSummary

# EventData Methods (Moved to allow defining of arguments/return variables)
def ED__init__(self, builder: EventData.EventBuilder) -> None:
    # Required Fields
    self.name = builder.name
    self.date = builder.date
    self.organizer = builder.organizer
    self.recurring = builder.recurring

    # Optional Fields
    self.time = builder.time
    self.location = builder.location
    self.zip = builder.zip
    self.tags = builder.tags
    self.RSVP = builder.rsvp
    self.summary = builder.summary

# Returns True if given event matches the object's name
def EDisEvent(self, otherEvent: EventData) -> bool:
    return otherEvent.getName().lower() == self.name.lower()
        
# Returns a new event with the same data except for date based on recurring
def EDgetNextRecurringEvent(self: EventData) -> EventData:
    if (self.recurring == "none"):
        return None
    elif (self.recurring == "weekly"):
        date = self.date + relativedelta.relativedelta(weeks=1)
    else:
        date = self.date + relativedelta.relativedelta(months=1)

    name = self.name
    date = date.strftime("%Y-%m-%d")
    organizer = self.organizer
    recurring = self.recurring
    time = self.getTimeStr()
    location = self.location
    zip = self.zip
    tags = self.tags
    summary = self.summary

    event = (EventData.EventBuilder(name, date, organizer, recurring)
                .Time(time)
                .Location(location)
                .Zip(zip).Tags(tags)
                .Summary(summary)
                .build()
            )
    return event

# Defines less than operator for EventData objects
# Defined to compare dates first, then times, then names
# Used in sorting list of events
def ED__lt__(self, other: EventData) -> bool:
    return (self.date, self.getTimeStr(), self.name) < (other.date, self.getTimeStr(), other.name)

EventData.__init__ = ED__init__
EventData.getNextRecurringEvent = EDgetNextRecurringEvent
EventData.isEvent = EDisEvent
EventData.__lt__ = ED__lt__

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