# Flask Website: "Main"
from EventHandler import EventHandler
from flask import Flask, request, session, redirect, url_for
from flask_apscheduler import APScheduler, scheduler
from datetime import date
from ProcessManager import ProcessManager
from HTMLPages import HTMLPages

app = Flask(__name__)
app.secret_key = "secure"

# For automatic timed scripts (removing out-of-date events)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

PManager = ProcessManager()
pages = HTMLPages()

dateObj = date

# Index/Home Page
@app.route("/", methods=["GET", "POST"])
def index():
    return pages.indexHTML()

# Login Page: Enter username+Password to log in
# If a user is already logged in, redirects to their account page
@app.route("/login/", methods=["GET", "POST"])
def login():
    if ("Username" in session):
        return redirect(url_for("account", user=session["Username"]))
    elif (request.method == "POST"):
        username = request.form.get("username", "null")
        password = request.form.get("password", "null")
        if (PManager.passLogin(username, password)):
            session["Username"] = username
            return redirect(url_for("account", user=username))
        else:
            return pages.loginHTML(True)
    return pages.loginHTML()

# Account Page: Displays information about a user's events
# If the user is currently logged in, also shows what events they RSVP'd for
@app.route("/account/", methods=["GET", "POST"])
def account():
    if (request.method == "POST"):
        if ("logout" in request.form):
            session.pop("Username", None)
            return redirect(url_for("index"))

    accountName = request.args.get("user")
    if (accountName):
        account = PManager.passUsername(accountName)
        userOrganizedEvents = PManager.searchEvents("organizer", account.getUsername())
        if (account == None):
            return pages.accountDNEHTML(accountName)
        elif ("Username" in session):
            user = PManager.passUsername(session["Username"])
            userRSVPEvents = PManager.searchEventsRSVP(user)
            return pages.accountHTML(account, userOrganizedEvents, user.isUser(account), userRSVPEvents)
        else:
            return pages.accountHTML(account, userOrganizedEvents)
    elif ("Username" in session):
        return redirect(url_for("account", user=session["Username"]))
    else:
        return redirect(url_for("index"))

# New Account Page: Displays form to create a new account
# If the user is currently logged in, redirects to their account page
@app.route("/newAccount/", methods=["GET", "POST"])
def newAccount():
    if ("Username" in session):
        return redirect(url_for("account", user=session["Username"]))
    elif (request.method == "POST"):
        username = request.form.get("username")
        password = request.form.get("password")
        phone = request.form.get("phone")
        email = request.form.get("email")
        if (PManager.passNewUser(username, password, phone, email)):
            session["Username"] = username
            return redirect(url_for("account", user=username))

    return pages.newAccountHTML()

# Events Page: Displays all events by default
# Search at top of page: Changes what events get displayed
@app.route("/events/", methods=["GET", "POST"])
def events():
    if ("searchValue" not in request.args):
        eventList = PManager.getAllEvents()
    else:
        searchType = request.args.get("searchType")
        searchValue = request.args.get("searchValue", "")
        searchDate = request.args.get("searchDate")
        searchTags = request.args.getlist("tags")
        eventList = PManager.searchEvents(searchType, searchValue, searchDate, searchTags)

    return pages.eventsHTML(eventList)

# Event Archive: Displays out-of-date events
@app.route("/eventArchive/", methods=["GET", "POST"])
def eventArchive():
    eventList = PManager.getOldEvents()
    return pages.eventArchiveHTML(eventList)

# Event Details: Displays a single event's details
# Allows joining/leaving an event
@app.route("/eventDetails/", methods=["GET", "POST"])
def eventDetails():
    eventName = request.args.get("name")
    event = PManager.getEvent(eventName)
    if (request.method == "POST" and eventName):
        if ("Username" in session):
            username = session["Username"]
            if ("join" in request.form):
                PManager.passRSVP(username, eventName)
            elif ("leave" in request.form):
                PManager.passLeaveRSVP(username, eventName)
            elif ("remove" in request.form):
                if (PManager.passRemEvent(event)):
                    return redirect(url_for("events"))
    trueRSVP = PManager.passGetRSVP(event)
    return pages.eventDetailedHTML(event, trueRSVP)

# Event Details Archived: Displays an archived event's details
# Does not allow editing event in any way (join/leave/delete)
@app.route("/eventDetailsArchived/", methods=["GET", "POST"])
def eventDetailsArchived():
    eventName = request.args.get("name")
    event = PManager.getOldEvent(eventName)
    trueRSVP = PManager.passGetRSVP(event)
    return pages.eventDetailedArchivedHTML(event, trueRSVP)

# New Event: Form that a user fills out to create a new event
# Current user is organizer
@app.route("/newEvent/", methods=["GET", "POST"])
def newEvent():
    if (not "Username" in session):
        return redirect(url_for("login"))
    elif (request.method == "POST"):
        name = request.form.get("name")
        date = request.form.get("date")
        time = request.form.get("time")
        location = request.form.get("location")
        zip = request.form.get("zip")
        tags = request.form.getlist("tags")
        summary = request.form.get("summary", "")
        # if (summary == ""):
        #     summary = "None"
        if (PManager.passNewEvent(name, time, date, location, zip, tags, session["Username"], summary)):
            return redirect(url_for("eventDetails", name=name))

    todayStr = dateObj.today().strftime("%Y-%m-%d")
    return pages.newEventHTML(todayStr)

# Sets up APScheduler to run checkActive() every 12 hours
def setTasks():
    # app.apscheduler.add_job(func=checkActive, trigger="interval", hours=12, id="checkActiveTask") # For actual use, 12 hour intervals
    app.apscheduler.add_job(func=checkActive, trigger="interval", seconds=10, id="checkActiveTask") # For debug use, 10 second intervals

# Checks all events and removes out-of-date events
def checkActive():
    PManager.passCheckActive()

if __name__=="__main__":
    setTasks()
    checkActive()
    app.run(host="127.0.0.1", port=8080, debug=True)