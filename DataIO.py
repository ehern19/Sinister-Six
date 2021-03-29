#                             Summary:
#
# This class stores the data for each event and initializes the data members.
# the purpose of this is to allow users to add events to the list, along with viewing
# capabilities.
#
#
#
#                             Data members:
#
# newName, newTime, newDate, newLocation, newTags, newRSVP
#
#
#
#                              Methods:
#
# Init: The constructor for the variables, it intializes each one
#
# "get____": Each method returns a variable, which gets the data stored in each object
#
# "is____": Each method checks to see if the given data matches the objects
#
# addRSVP : Allows the user to add themselves to the RSVP list for a certain event.
# The function returns rrue if a user is added to the list for the event, and if not 
# it returns false and adds the user.
#
# removeRSVP : Allows the user to remove themselves to the RSVP list for a certain event.
# The function returns true if a user is removed from the list for the event, and if not 
# it returns false and removes the user.

class DataIO:
    # File path/names to read/write data from/to
    databasePath = "database\\"
    eventFilename = "Events.txt"
    oldEventFilename = "OldEvents.txt"
    userdataFilename = "Userdata.txt"

    def __init__(self):
        self.data = []
    
    # Get method for data stored in object
    def getData(self):
        return self.data
    
    # Set method for data stored in object
    def setData(self, newData):
        self.data = newData
    
    # (Abstract) Load data from file to memory in object
    def loadData(self):
        pass

    # (Abstract) Save data to file from memory in object
    def saveData(self):
        pass