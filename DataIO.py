# Data IO: Store and retrieve data from files
# Abstract Class

class DataIO:
    # File path/names to read/write data from/to
    databasePath = "database\\"
    eventFilename = "Events.txt"
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