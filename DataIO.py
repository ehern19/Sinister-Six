# Data IO

class DataIO:
    databasePath = "database\\"

    def __init__(self):
        self.eventNames = []
        self.eventTimes = {}
        self.eventTags = {}
        self.eventRSVPs = {}
        self.userData = {}

    # Get methods for data stored in DataIO object
    def getEventNames(self):
        return self.eventNames

    def getEventTimes(self):
        return self.eventTimes

    def getEventTags(self):
        return self.eventTags

    def getEventRSVPs(self):
        return self.eventRSVPs

    def getUserData(self):
        return self.userData

    # Load event names from .txt
    def _loadEventNames(self):
        with open(self.databasePath + "EventNames.txt", 'r') as nameFile:
            for event in nameFile:
                event = event.strip()

                # Check if event is in file more than once
                if event in self.eventNames:
                    print(f"Error: {event} is duplicated in EventNames.txt")
                    return False
                self.eventNames.append(event)

        # self.eventNames = ["event1", "event2"] # Example data
        return self.eventNames

    # Load event times from .txt
    def _loadEventTimes(self):
        with open(self.databasePath + "EventTimes.txt", 'r') as timeFile:
            for event in timeFile:
                event = event.strip()
                time = timeFile.readline().strip()

                # Check if event is in file more than once
                if event in self.eventTimes:
                    print(f"Error: {event} is duplicated in EventTimes.txt")
                    return False
                self.eventTimes.update({event:time})

        # self.eventTimes =  {"event1":"10:00", "event2":"13:00"} # Example data
        return self.eventTimes

    # Load event tags from .txt
    def _loadEventTags(self):
        with open(self.databasePath + "EventTags.txt", 'r') as tagFile:
            for line in tagFile:
                line = line.split()
                event = line[0]

                # Check if event is in file more than once
                if event in self.eventTags:
                    print(f"Error: {event} is duplicated in EventTags.txt")
                    return False

                rawTags = line[1:]
                editTags = []
                # Replace "_" with " " ("_" is in the file so that tags with " " are still read as one tag)
                for tag in rawTags:
                    tag = tag.replace('_', ' ')
                    # Check if a tag is duplicated for the event
                    if tag in editTags:
                        print(f"Error: {event} has duplicate tag \"{tag}\"")
                        return False
                    editTags.append(tag)

                self.eventTags.update({event:editTags})

        # self.eventTags = {"event1":["construction", "physical labor"], "event2":["tag1", "tag2"]} # Example data
        return self.eventTags

    # Load RSVPLists from .txt
    def _loadRSVPLists(self):
        with open(self.databasePath + "EventRSVPLists.txt", 'r') as listFile:
            for line in listFile:
                line = line.split()
                event = line[0]

                # Check if event is in file more than once
                if event in self.eventRSVPs:
                    print(f"Error: {event} is duplicated in EventRSVPLists.txt")
                    return False

                rawList = line[1:]
                editList = []
                # Check if a user is duplicated for the event
                for user in rawList:
                    if user in editList:
                        print(f"Error: {event} has duplicate user \"{user}\" in EventRSVPLists.txt")
                        return False
                    editList.append(user)

                self.eventRSVPs.update({event:editList})

        # self.eventRSVPs = {"event1":["user1", "user2"], "event2":["user3", "user2"]} # Example data
        return self.eventRSVPs

    # Load user data from .txt
    def _loadUsers(self):
        with open(self.databasePath + "UserData.txt", 'r') as userFile:
            for line in userFile:
                line = line.split()
                user = line[0]
                password = line[1]

                # Check if a user is duplicated
                if user in self.userData:
                    print(f"Error: {user} has a duplicate in \"UserData.txt\"")
                    return False
                
                self.userData.update({user:password})

        # self.userData = {"user1":"pw1", "user2":"pw2", "user3":"pw3"} # Example data
        return self.userData

    # Validate loaded data (Check if each event has data for each of time, tags, and RSVP list)
    def _validateLoad(self):
        # TODO
        return True

    # Call all load methods
    def loadAll(self):
        names = self._loadEventNames()
        times = self._loadEventTimes()
        tags = self._loadEventTags()
        RSVPs = self._loadRSVPLists()
        users = self._loadUsers()

        # Check if any of the loads returned False (Error occurred)
        if not (names or times or tags or RSVPs or users):
            print("An error occurred while loading data")
            return False

        return self._validateLoad()

    # Save all data to .txt files
    def save(self):
        # TODO
        return

# For testing the methods of DataIO
if __name__=="__main__":
    dataIO = DataIO()
    
    print(dataIO.loadAll()) # Test load method (All load methods in one)

    # Individual method tests
    # dataIO._loadEventNames()
    # print("Event Names:")
    # print(dataIO.eventNames)
    # print()

    # dataIO._loadEventTimes()
    # print("Event Times:")
    # print(dataIO.eventTimes)
    # print()

    # dataIO._loadEventTags()
    # print("Event Tags:")
    # print(dataIO.eventTags)
    # print()

    # dataIO._loadRSVPLists()
    # print("Event RSVP Lists:")
    # print(dataIO.eventRSVPs)
    # print()

    # dataIO._loadUsers()
    # print("User Data:")
    # print(dataIO.userData)
    # print()