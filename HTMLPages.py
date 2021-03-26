# HTML Pages: Functions that return the specific HTML pages
from flask import render_template, session
from EventData import EventData
from UserData import UserData

class HTMLPages:
    # Wraps input HTML string with common header and footer
    def _wrapHTML(self, inHTML):
        return (render_template("header.html", loggedIn=("Username" in session)) 
                + inHTML 
                + render_template("footer.html"))

    def indexHTML(self):
        return self._wrapHTML(render_template("pages/index.html"))

    def loginHTML(self, attemptedLogin=False):
        return self._wrapHTML(render_template("pages/login.html", failedLogin=attemptedLogin))
    
    def accountHTML(self, user, userEvents, isUser=False, userRSVPEvents=[]):
        retHTML = render_template("sections/accountEventOrganizer.html", isUser=isUser)
        retHTML = retHTML + self._eventShortHTML(userEvents)
        retHTML = retHTML + render_template("sections/endSection.html")
        if (isUser):
            retHTML = render_template("pages/accountPrivate.html", username=user.getUsername()) + retHTML
            retHTML = retHTML + render_template("sections/accountEventRSVP.html")
            retHTML = retHTML + self._eventShortHTML(userRSVPEvents)
            retHTML = retHTML + render_template("sections/endSection.html")
        else:
            retHTML = render_template("pages/accountPublic.html", username=user.getUsername()) + retHTML
        return self._wrapHTML(retHTML)

    def newAccountHTML(self):
        return self._wrapHTML(render_template("pages/accountNew.html"))

    def accountDNEHTML(self, accountName):
        return self._wrapHTML(render_template("pages/accountDNE.html", username=accountName))

    def eventsHTML(self, eventList, searching="all"):
        retHTML = render_template("pages/events.html", searchParamaters=searching)
        retHTML = retHTML + self._eventShortHTML(eventList)
        return self._wrapHTML(retHTML)

    def _eventShortHTML(self, eventList):
        retHTML = ""
        for event in eventList:
            retHTML = retHTML + render_template("sections/eventShort.html", 
                                                 name=event.getName(), 
                                                 date=event.getDate(), 
                                                 time=event.getTime(), 
                                                 location=event.getLocation(), 
                                                 tags=event.getTags()
                                                 )
        return retHTML

    def eventDetailedHTML(self, event):
        if ("Username" in session):
            username = session["Username"]
        else:
            username = ""
        retHTML = render_template("pages/eventDetails.html", 
                                name=event.getName(), 
                                date=event.getDate(), 
                                time=event.getTime(), 
                                location=event.getLocation(), 
                                organizer=event.getOrganizer(),
                                tags=event.getTags(),
                                summary=event.getSummary(),
                                isOrganizer=(event.isOrganizerName(username)),
                                inEvent=(username in event.getRSVP()),
                                loggedIn=("Username" in session)
                                )
        return self._wrapHTML(retHTML)
    
    def newEventHTML(self, todayStr):
        return self._wrapHTML(render_template("pages/newEvent.html", today=todayStr))