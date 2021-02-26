# Process Manager
# Main controlling script
from DataIO import *
from EventHandler import *
from LoginHandler import *
# from WebsiteUI import *
  
# Instantiate objects
def onStartup():
    global DataIO 
    DataIO = DataIO()
    global EventHandler
    EventHandler = EventHandler()
    global LoginHandler
    LoginHandler = LoginHandler()
    # global WebsiteUI = WebsiteUI()
    loadData()
    return

# Load data into each object as necessary
def loadData():
    EventHandler.loadEvents(DataIO.loadEventNames(), DataIO.loadEventTimes(), DataIO.loadEventTags())
    EventHandler.loadRSVPLists(DataIO.loadRSVPLists())
    LoginHandler.loadUsers(DataIO.loadUsers())

# Save data from each object to .txt files
def saveData():
    #TODO
    return

# Get input from WebsiteUI
def getInput(moreInfo = ""):
    #TODO
    return input(">>"+moreInfo)


if __name__ == "__main__": #Don't really need, but is basically main()
    user = "guest"
    isOnline = True
    onStartup()
    
    # Loop to continuously receive input from WebsiteUI (Currently Terminal/Command Line Interaction)
    print("Welcome to the Volunteer UI")
    while (isOnline):
        option = getInput()
        # User login
        if (option == "login" and user == "guest"):
            username = getInput("Username: ")
            password = getInput("Password: ")
            if LoginHandler.checkLogin([username, password]):
                print(f"Successfully logged in as {username}")
                user = username
            else:
                print("Invalid username or password")
        # Exit Case
        elif (option == "exit"):
            isOnline = False
        
        # Only allow the following if the user is logged in
        elif (user != "guest"):
            # Add user to event RSVPList
            if (option == "joinEvent"):
                eventName = getInput("Event: ")
                if (EventHandler.addRSVP(eventName, user)):
                    # TODO: Display event data and join confirmation
                    i = 0
                else:
                    # TODO: Display join failure
                    i = 0
                
            # Remove user from event RSVPList
            elif (option == "leaveEvent"):
                eventName = getInput("Event: ")
                if (EventHandler.removeRSVP(eventName, user)):
                    # TODO: Display event data and leave confirmation
                    i = 0
                else:
                    # TODO: Display leave failure
                    i = 0

            # Create event
            elif (option == "createEvent"):
                eventName = getInput("Event Name: ")
                eventTime = getInput("Event Time: ")
                eventTags = getInput("Event Tags: ")
                if (EventHandler.addEvent(eventName, eventTime, eventTags)):
                    # TODO: Display event data and creation confirmation
                    i = 0
                else:
                    # TODO: Display creation failure
                    i = 0
        else:
            print("Not a valid option")
        
# end main