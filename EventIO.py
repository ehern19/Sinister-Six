# Event IO: Store and retrieve event data from file
# Child of DataIO class

from DataIO import DataIO
from EventData import EventData

# Data is stored as a list of EventData objects
class EventIO(DataIO):
    filePath = DataIO.databasePath + DataIO.eventFilename
    filePathOld = DataIO.databasePath + DataIO.oldEventFilename

    def __init__(self):
        super().__init__()
        self.oldData = []
    
    # Get method for data stored in OldData (inactive events)
    def getOldData(self):
        return self.oldData

    # Set method for data stored in oldData (inactive events)
    def setOldData(self, newData):
        self.oldData = newData

    # Load Event data from file to memory in object
    def loadData(self):
        self._readData(self.filePath, self.data)
        self._readData(self.filePathOld, self.oldData)

    # Open file and read data to list
    def _readData(self, filePath, appendList):
        with open(filePath, 'r') as inFile:
            for line in inFile:
                line = line.strip().split()

                # Replace any '_' with ' '
                line = [entry.replace('_', ' ') for entry in line]

                # Separate the line into relevant categories
                eventName = line.pop(0)
                eventTime = line.pop(0)
                eventDate = line.pop(0)
                eventLocation = line.pop(0)
                eventZip = line.pop(0)
                eventTags = line
                
                # Get next line of organizer and RSVPs
                eventRSVP = next(inFile).strip().split()

                # Get next line of Summary
                eventSummary = next(inFile).strip()
                
                # Add new EventData object to this object's data list
                # appendList.append(EventData(eventName, eventTime, eventDate, eventLocation, eventZip, eventTags, eventRSVP, eventSummary))
                event = EventData.EventBuilder(eventName, eventDate, eventRSVP[0]).Time(eventTime).Location(eventLocation).Zip(eventZip).Summary(eventSummary)
                if (not eventTags == "No Tags"):
                    event.Tags(eventTags)
                if (not eventRSVP[1:] == []):
                    event.RSVP(eventRSVP[1:])
                event = event.build()
                appendList.append(event)

    # Save Event data to file from memory in object
    def saveData(self):
        self._writeData(self.filePath, self.data)
        self._writeData(self.filePathOld, self.oldData)
        
    def _writeData(self, filePath, outList):
        with open(filePath, 'w') as outFile:
            for event in outList:
                # Create a list with name, time, date, location, and tags
                line = []
                line.append(event.getName())
                line.append(event.getTimeStr())
                line.append(event.getDateStr())
                line.append(event.getLocation())
                line.append(event.getZip())
                tags = event.getTags()
                if (not tags == []):
                    for tag in event.getTags():
                        line.append(tag)
                
                # Replace any ' ' with '_'
                line = [entry.replace(' ', '_') for entry in line]

                # Convert to single line string
                line = ' '.join(line)

                # Print line to file
                print(line, file=outFile)

                # Repeat with organizer and RSVP
                line = []
                line.append(event.getOrganizer())
                eventRSVP = event.getRSVP()
                if (not eventRSVP == []):
                    for user in eventRSVP:
                        line.append(user)
                line = ' '.join(line)
                print(line, file=outFile)

                # Print summary directly to file
                print(event.getSummary(), file=outFile)

if __name__=="__main__":
    events = EventIO()
    events.loadData()
    for event in events.getData():
        event.printAllData()
    events.saveData()
