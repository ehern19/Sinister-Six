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
    
    def loadRSVPList(self, RSVPList):
        self.RSVPList = RSVPList
    
    def addRSVP(self, username):
        if (username in self.RSVPList):
            return False
        else:
            self.RSVPList.append(username)
            return True
    
    def removeRSVP(self, username):
        # TODO
        return True