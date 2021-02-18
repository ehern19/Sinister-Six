# RSVP Handler

class RSVPHandler:
    def __init__(self):
        self.RSVPLists = {}
        
    def setLists(self, listData):
        self.RSVPLists = listData
        return
    
    def loadList(self, eventName):
        return self.RSVPLists[eventName]