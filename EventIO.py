# Event IO: Store and retrieve event data from file
# Child of DataIO class

from DataIO import DataIO
from EventData import EventData

# Data is stored as a list of EventData objects
class EventIO(DataIO):
    filePath = DataIO.databasePath + DataIO.eventFilename
    # Load Event data from file to memory in object
    def loadData(self):
        with open(self.filePath, 'r') as inFile:
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
                
                # Add new EventData object to this object's data list
                self.data.append(EventData(eventName, eventTime, eventDate, eventLocation, eventZip, eventTags, eventRSVP))

    # Save Event data to file from memory in object
    def saveData(self):
        with open(self.filePath, 'w') as outFile:
            for event in self.data:
                # Create a list with name, time, date, location, and tags
                line = []
                line.append(event.getName())
                line.append(event.getTime())
                line.append(event.getDate())
                line.append(event.getLocation())
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
                for user in event.getRSVP():
                    line.append(user)
                line = ' '.join(line)
                print(line, file=outFile)

if __name__=="__main__":
    events = EventIO()
    events.loadData()
    for event in events.getData():
        event.printAllData()
    events.saveData()
