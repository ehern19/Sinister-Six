# Flask Website: "Main"
from flask import Flask, request, session, redirect, url_for
from datetime import date, time
from ProcessManager import ProcessManager
from HTMLPages import HTMLPages

app = Flask(__name__)
app.secret_key = "secure"

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
    print(session)
    if ("Username" in session):
        return redirect(url_for("account", user=session["Username"]))
    if (request.method == "POST"):
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
            redirect(url_for("index"))

    accountName = request.args.get("user")
    if (accountName):
        account = PManager.passUsername(accountName)
        if (account == None):
            return pages.accountDNEHTML(accountName)
        elif ("Username" in session):
            user = PManager.passUsername(session["Username"])
            return pages.accountHTML(account, user.isUser(account))
        else:
            return pages.accountHTML(account, False)
    elif ("Username" in session):
        user = PManager.passUsername(session["Username"])
        return pages.accountHTML(user, True)
    else:
        return redirect(url_for("index"))

# Events Page: Displays all events by default
# TODO: Allow searching events
@app.route("/events/", methods=["GET", "POST"])
def events():
    eventList = PManager.getAllEvents()
    return pages.eventsHTML(eventList)

# Event Details: Displays a single event's details
# Allows joining/leaving an event
@app.route("/eventDetails/", methods=["GET", "POST"])
def eventDetails():
    eventName = request.args.get("name")
    if (request.method == "POST" and eventName):
        if ("Username" in session):
            username = session["Username"]
            if ("join" in request.form):
                PManager.passRSVP(username, eventName)
            elif ("leave" in request.form):
                PManager.passLeaveRSVP(username, eventName)

    event = PManager.getEvent(request.args.get("name"))
    return pages.eventDetailedHTML(event)

@app.route("/newEvent/", methods=["GET", "POST"])
def newEvent():
    if (not "Username" in session):
        return redirect(url_for("login"))
    elif (request.method == "POST"):
        name = request.form.get("name")
        date = request.form.get("date")
        time = request.form.get("time")
        location = request.form.get("location")
        tags = request.form.getlist("tags")
        if (PManager.passNewEvent(name, time, date, location, tags, session["Username"])):
            return redirect(url_for("eventDetails", name=name))

    todayStr = dateObj.today().strftime("%Y-%m-%d")
    return pages.newEventHTML(todayStr)

if __name__=="__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)