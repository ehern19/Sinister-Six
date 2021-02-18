# Data IO

class DataIO:
    def __init__(self):
        self.userData = {}
        self.eventData = {}

    # Load event names from .txt
    def loadEventNames(self):
        return ["event1", "event2"]

    # Load event times from .txt
    def loadEventTimes(self):
        return {"event1":"10:00", "event2":"13:00"}

    # Load event tags from .txt
    def loadEventTags(self):
        return {"event1":["construction", "physical labor"], "event2":["tag1", "tag2"]}

    # Load RSVPLists from .txt
    def loadRSVPLists(self):
        return {"event1":["user1", "user2"], "event2":["user3", "user2"]}

    # Load user data from .txt
    def loadUsers(self):
        return {"user1":"pw1", "user2":"pw2", "user3":"pw3"}

  # Save all data to .txt files
    def save(self):
        # TODO
        return