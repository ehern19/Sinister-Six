#                                        Summary:
#
# This class handles our project's interaction with the flask application. It allows
# our backend logic and classes to translate into webpages, in conjinction with the
# HTML templates also contained in our project.
#
#
#
#                                        Data Members:
#
# dateObj, popularEvents, username, password, phone, email, eventList, searchType,
# searchTags, searchDate, searchValue, eventName, rsvp
#
#
#
#                                         Methods:
#
# "index": Sets up our homepage.
#
# "login": The login page, in which the user enters their info. If the user is already
# logged in, it redirects to the "account" page.
#
# "account": The page that displays the user info, including what events they have RSVP'd
# for.
#
# "newAccount": This page allows the user to create a new account. If the user is already
# logged in, it will redirect to the "account" page.
#
# "events": Displays every event by default, along with a search function
# that will allow users to search availible events.
#
# "eventArchive": Shows archived events, ones that have passed.
#
# "eventDetails:" Webpage that shows the details for each event, along with
# allowing users to add or remove themselves from events.
#
# "eventsDetailsArchived": Page that shows details for events that have been 
# archived. This page does not allow editing of any kind, since the event has 
# passed.
#
# "newEvent": Webpage that allows the user to create a new event, of which they will be the
# organizer of.
#
# "editEvent": Allows the user to edit events they organized/has edit privilages for.
#
# "setTasks": Sets up a program to call and run the "checkActive" method every 12 hours.
#
# "checkActive": Checks to see if events are still active and removes out of date
# events.
#
# "updateNotificationsSent": Passes a list of active events to the emailHandler
# class and updates the notification list.
#
# "oneDayNotification": Examines every event and sends out email notifications for those starting
# within 24 hours.

# Flask Website: "Main"
import os
from flask import Flask, request, session, redirect, url_for
from flask_apscheduler import APScheduler, scheduler
from datetime import date
from ProcessManager import ProcessManager
from HTMLPages import HTMLPages
from EmailHandler import EmailHandler
from dataClasses.extras import DATABASE_PATH, USER_IMAGES, EVENT_IMAGES

app = Flask(__name__)
app.secret_key = "secure"

# For automatic timed scripts (removing out-of-date events)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

PManager = ProcessManager()
pages = HTMLPages()
EmHandler = EmailHandler()

dateObj = date

# Index/Home Page
@app.route("/", methods=["GET", "POST"])
def index():
    popularEvents = PManager.getPopularEvents()
    return pages.indexHTML(popularEvents)

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
        if (not account):
            session.pop("Username", None)
            return redirect(url_for("login"))
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
        zip = request.form.get("zip", "")
        if ("image" in request.files):
            imageFile = request.files["image"]
            if (PManager.allowedImageFile(imageFile.filename)):
                imageName = PManager.getNextUserImgName(username)
                imageFile.save(DATABASE_PATH + USER_IMAGES + imageName)
            else:
                return pages.newAccountHTML(badImage=True)
        
        if (PManager.passNewUser(username, password, phone, email, zip)):
            session["Username"] = username
            return redirect(url_for("account", user=username))
        else:
            return pages.newAccountHTML(badName=True)

    return pages.newAccountHTML()

# Edit Account: Form a user fills out to edit their account
@app.route("/editAccount/", methods=["GET", "POST"])
def editAccount():
    pass
    if (not "Username" in session):
        return redirect(url_for("login"))
    elif (request.method == "POST"):
        username = session["Username"]
        phone = request.form.get("phone", None)
        email = request.form.get("email", None)
        if ("image" in request.files):
            imageFile = request.files["image"]
            if (imageFile):
                if (PManager.allowedImageFile(imageFile.filename)):
                    imageName = PManager.getNextUserImgName(username)
                    imageFile.save(DATABASE_PATH + USER_IMAGES + imageName)
                else:
                    return pages.editAccountHTML(badImage=True)
        
        if (PManager.passEditUser(username, phone, email)):
            return redirect(url_for("account", user=username))

    return pages.editAccountHTML()

# Events Page: Displays all events by default
# Search at top of page: Changes what events get displayed
@app.route("/events/", methods=["GET", "POST"])
def events():
    if ("searchValue" not in request.args):
        eventList = PManager.getAllEvents()
    elif (request.method == "GET"):
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
                if (PManager.passRSVP(username, eventName)):
                    if (event.isNextDay()):
                        currentUser = PManager.passUsername(session["Username"])
                        EmHandler.oneUserOneDayNotification(event, currentUser)
            elif ("leave" in request.form):
                PManager.passLeaveRSVP(username, eventName)
            elif ("remove" in request.form):
                if (PManager.passRemEvent(event)):
                    EmHandler.removeNotified([event])
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
        recurring = request.form.get("recurring")
        if ("image" in request.files):
            imageFile = request.files["image"]
            if (PManager.allowedImageFile(imageFile.filename)):
                imageName = PManager.getNextEventImgName(name)
                imageFile.save(DATABASE_PATH + EVENT_IMAGES + imageName)
            else:
                todayStr = dateObj.today().strftime("%Y-%m-%d")
                return pages.newEventHTML(todayStr, badImage=True)

        if (PManager.passNewEvent(name, date, session["Username"], recurring, time, location, zip, tags, summary)):
            return redirect(url_for("eventDetails", name=name))
        else:
            todayStr = dateObj.today().strftime("%Y-%m-%d")
            return pages.newEventHTML(todayStr, badName=True)

    todayStr = dateObj.today().strftime("%Y-%m-%d")
    return pages.newEventHTML(todayStr)

# Edit Event: Form that a user fills out to edit an event
@app.route("/editEvent/", methods=["GET", "POST"])
def editEvent():
    eventName = request.args.get("name")
    if (not eventName):
        return redirect(url_for("events"))
    if (not "Username" in session):
        return redirect(url_for("login"))
    event = PManager.getEvent(eventName)
    if (not event.isOrganizerName(session["Username"])):
        return redirect(url_for("events"))

    if (request.method == "POST"):
        reset = "reset" in request.form
        time = request.form.get("time")
        location = request.form.get("location")
        zip = request.form.get("zip")
        tags = request.form.getlist("tags")
        summary = request.form.get("summary")
        if ("image" in request.files):
            imageFile = request.files["image"]
            if (PManager.allowedImageFile(imageFile.filename)):
                imageName = PManager.getNextEventImgName(eventName)
                imageFile.save(DATABASE_PATH + EVENT_IMAGES + imageName)
            else:
                return pages.editEventHTML(event, badImage=True)
        if (PManager.passEditEvent(eventName, reset, time, location, zip, tags, summary)):
            return redirect(url_for("eventDetails", name=eventName))
        else:
            return redirect(url_for("events"))
    return pages.editEventHTML(event)
    

# Sets up APScheduler to run checkActive() every 12 hours
def setTasks():
    # app.apscheduler.add_job(func=checkActive, trigger="interval", hours=12, id="checkActiveTask") # For actual use, 12 hour intervals
    app.apscheduler.add_job(func=checkActive, trigger="interval", seconds=10, id="checkActiveTask") # For debug use, 10 second intervals
    # app.apscheduler.add_job(func=oneDayNotifications, trigger="interval", hours=12, id="sendOneDayNotificationTask") # For debug use, 12 hour intervals
    app.apscheduler.add_job(func=oneDayNotifications, trigger="interval", seconds=10, id="sendOneDayNotificationTask") # For debug use, 10 second intervals

# Checks all events and removes out-of-date events
def checkActive() -> None:
    retiredEvents = PManager.passCheckActive()
    EmHandler.removeNotified(retiredEvents)

# Sends active events to EmailHandler to update the notifications sent list
def updateNotificationsSent() -> None:
    activeEvents = PManager.getAllEvents()
    EmHandler.loadNotifiedList(activeEvents)

# Checks all events and sends notifications for those starting within 1 day
def oneDayNotifications() -> None:
    events = PManager.getOneDayEvents()
    for event in events:
        rsvp = PManager.passGetRSVP(event)
        EmHandler.oneDayNotification(event, rsvp)

if __name__=="__main__":
    updateNotificationsSent()
    setTasks()
    checkActive()
    oneDayNotifications()
    app.run(host="127.0.0.1", port=8080, debug=True)