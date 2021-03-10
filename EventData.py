# Event Data
class EventData:
    def __init__(self, name, time, tags):
        self.name = name
        self.time = time
        self.tags = tags
        self.RSVPList = []
    
    def getName(self):
        return self.name
    
    def getTime(self):
        return self.time
    
    def getTags(self):
        return self.tags

    def getRSVPList(self):
        return self.RSVPList
    
    def loadRSVPList(self, RSVPList):
        self.RSVPList = RSVPList
    
    def addRSVP(self, username):
        if username in self.RSVPList:
            print("Already in event")
            return False
        else:
            self.RSVPList.append(username)
            print(f"Successfully joined {self.name}")
            return True
    
    def removeRSVP(self, username):
        if not username in self.RSVPList:
            print("Not in event")
            return False
        else:
            self.RSVPList.remove(username)
            print(f"Successfully left {self.name}")
            return True

    # Printing for debugging
    def printAllData(self):
        print(f"Event: {self.name}\n\tTime: {self.time}\n\tTags: {self.tags}\n\tRSVP List: {self.RSVPList}\n")