# Data IO

class DataIO:
    # File paths/names to read/write data from/to
    databasePath = "database\\"
    eventNameFile = "EventNames.txt"
    eventTimeFile = "EventTimes.txt"
    eventTagsFile = "EventTags.txt"
    eventRSVPsFile = "EventRSVPLists.txt"
    userDataFile = "UserData.txt"

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
        with open(self.databasePath + self.eventNameFile, 'r') as nameFile:
            for event in nameFile:
                event = event.strip()

                # Check if event is in file more than once
                if event in self.eventNames:
                    print(f"Error: {event} is duplicated in {self.eventNameFile}")
                    return False
                self.eventNames.append(event)

        # self.eventNames = ["Event1", "Event2"] # Example data
        return self.eventNames

    # Load event times from .txt
    def _loadEventTimes(self):
        with open(self.databasePath + self.eventTimeFile, 'r') as timeFile:
            for line in timeFile:
                line = line.split()
                event = line[0]
                time = line[1]

                # Check if event is in file more than once
                if event in self.eventTimes:
                    print(f"Error: {event} is duplicated in {self.eventTimeFile}")
                    return False
                self.eventTimes.update({event:time})

        # self.eventTimes =  {"Event1":"10:00", "Event2":"13:00"} # Example data
        return self.eventTimes

    # Load event tags from .txt
    def _loadEventTags(self):
        with open(self.databasePath + self.eventTagsFile, 'r') as tagFile:
            for line in tagFile:
                line = line.split()
                event = line[0]

                # Check if event is in file more than once
                if event in self.eventTags:
                    print(f"Error: {event} is duplicated in {self.eventTagsFile}")
                    return False

                rawTags = line[1:]
                editTags = []
                # Replace "_" with " " ("_" is in the file so that tags with " " are still read as one tag)
                for tag in rawTags:
                    tag = tag.replace('_', ' ')
                    # Check if a tag is duplicated for the event
                    if tag in editTags:
                        print(f"Error: {event} has duplicate tag \"{tag}\" in {self.eventTagsFile}")
                        return False
                    editTags.append(tag)

                self.eventTags.update({event:editTags})

        # self.eventTags = {"Event1":["construction", "physical labor"], "Event2":["tag1", "tag2"]} # Example data
        return self.eventTags

    # Load RSVPLists from .txt
    def _loadRSVPLists(self):
        with open(self.databasePath + self.eventRSVPsFile, 'r') as listFile:
            for line in listFile:
                line = line.split()
                event = line[0]

                # Check if event is in file more than once
                if event in self.eventRSVPs:
                    print(f"Error: {event} is duplicated in {self.eventRSVPsFile}")
                    return False

                rawList = line[1:]
                editList = []
                # Check if a user is duplicated for the event
                for user in rawList:
                    if user in editList:
                        print(f"Error: {event} has duplicate user \"{user}\" in {self.eventRSVPsFile}")
                        return False
                    editList.append(user)

                self.eventRSVPs.update({event:editList})

        # self.eventRSVPs = {"Event1":["user1", "user2"], "Event2":["user3", "user2"]} # Example data
        return self.eventRSVPs

    # Load user data from .txt
    def _loadUsers(self):
        with open(self.databasePath + self.userDataFile, 'r') as userFile:
            for line in userFile:
                line = line.split()
                user = line[0]
                password = line[1]

                # Check if a user is duplicated
                if user in self.userData:
                    print(f"Error: {user} has a duplicate in {self.userDataFile}")
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

    # Save event names to .txt
    def _saveEventNames(self):
        nameFile = open(self.databasePath + self.eventNameFile, 'w')
        for event in self.eventNames:
            print(event, file=nameFile)
        return True

    # Save event times to .txt
    def _saveEventTimes(self):
        timeFile = open(self.databasePath + self.eventTimeFile, 'w')
        for event in self.eventTimes:
            print(f"{event} {self.eventTimes[event]}", file=timeFile)
        return True

    # Save event tags to .txt
    def _saveEventTags(self):
        tagFile = open(self.databasePath + self.eventTagsFile, 'w')
        for event in self.eventTags:
            print(event, end='', file=tagFile)
            for tag in self.eventTags[event]:
                # Replace " " with "_" ("_" is in the file so that tags with " " are still read as one tag)
                tag = tag.replace(' ', '_')
                print(f" {tag}", end='', file=tagFile)
            print('', file=tagFile)
        return True

    # Save RSVPLists to .txt
    def _saveRSVPLists(self):
        RSVPFile = open(self.databasePath + self.eventRSVPsFile, 'w')
        for event in self.eventRSVPs:
            print(event, end='', file=RSVPFile)
            for user in self.eventRSVPs[event]:
                print(f" {user}", end='', file=RSVPFile)
            print('', file=RSVPFile)
        return True

    # Save user data to .txt
    def _saveUsers(self):
        userFile = open(self.databasePath + self.userDataFile, 'w')
        for user in self.userData:
            print(f"{user} {self.userData[user]}", file=userFile)
        return True

    # Save all data to .txt files
    def saveAll(self):
        self._saveEventNames()
        self._saveEventTimes()
        self._saveEventTags()
        self._saveRSVPLists()
        self._saveUsers()
        return True

# For testing the methods of DataIO
if __name__=="__main__":
    dataIO = DataIO()
    
    # Load Methods ==================================================================================

    print(dataIO.loadAll()) # Test load method (All load methods in one)

    # Individual load method tests ------------------------------------------------------------------
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

    # Save Methods ==================================================================================

    print(dataIO.saveAll()) # Test save method (All save methods in one)
    
    # Individual save method tests ------------------------------------------------------------------
    # dataIO._saveEventNames()
    # dataIO._saveEventTimes()
    # dataIO._saveEventTags()
    # dataIO._saveRSVPLists()
    # dataIO._saveUsers()