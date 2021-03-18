# Event IO: Store and retrieve event data from file
# Child of DataIO class

from DataIO import DataIO
from EventData import EventData

# Data is stored as a list of EventData objects
class EventIO(DataIO):
    # Load Event data from file to memory in object
    def loadData(self):
        with open(self.databasePath + self.eventFilename, 'r') as file:
            for line in file:
                line = line.strip().split()

                # Replace any '_' with ' '
                line = [entry.replace('_', ' ') for entry in line]

                # Separate the line into relevant categories
                eventName = line.pop(0)
                eventTime = line.pop(0)
                eventDate = line.pop(0)
                eventLocation = line.pop(0)
                eventTags = line
                
                # Get next line of organizer and RSVPs
                line = next(file).strip().split()
                eventOrganizer = line.pop(0)
                eventRSVP = line
                
                # Add new EventData object to this object's data list
                self.data.append[EventData(eventName, eventTime, eventDate, 
                                 eventLocation, eventTags, eventOrganizer, 
                                 eventRSVP)]

    # Save Event data to file from memory in object
    def saveData(self):
        pass