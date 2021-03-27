# HTML Pages: Functions that return the specific HTML pages
from flask import render_template, session
from dataClasses.EventData import EventData
from dataClasses.UserData import UserData
from dataClasses.tags import VALID_TAGS, DISPLAY_TAGS, NUM_TAGS

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
            retHTML = render_template("pages/accountPrivate.html", username=user.getUsername(), phone=user.getPhone(), email=user.getEmail()) + retHTML
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
        retHTML = render_template("pages/events.html", tagList=VALID_TAGS, tagDisplay=DISPLAY_TAGS, numTags=NUM_TAGS)
        retHTML = retHTML + self._eventShortHTML(eventList)
        return self._wrapHTML(retHTML)

    def _eventShortHTML(self, eventList):
        retHTML = ""
        for event in eventList:
            retHTML = retHTML + render_template("sections/eventShort.html", 
                                                 name=event.getName(), 
                                                 date=event.getDateStr(), 
                                                 time=event.getTimeStr(), 
                                                 location=event.getLocation(), 
                                                 tags=event.getTagStrs()
                                                 )
        return retHTML

    def eventArchiveHTML(self, eventList):
        retHTML = render_template("pages/eventArchive.html")
        retHTML = retHTML + self._eventShortArchivedHTML(eventList)
        return self._wrapHTML(retHTML)
    
    def _eventShortArchivedHTML(self, eventList):
        retHTML = ""
        for event in eventList:
            retHTML = retHTML + render_template("sections/eventShortArchived.html", 
                                                 name=event.getName(), 
                                                 date=event.getDateStr(), 
                                                 time=event.getTimeStr(), 
                                                 location=event.getLocation(), 
                                                 tags=event.getTagStrs()
                                                 )
        return retHTML

    def eventDetailedHTML(self, event, trueRSVP):
        if ("Username" in session):
            username = session["Username"]
        else:
            username = ""
        isOrganizer = (event.isOrganizerName(username))
        retHTML = render_template("pages/eventDetails.html", 
                                name=event.getName(), 
                                date=event.getDateStr(), 
                                time=event.getTimeStr(), 
                                location=event.getLocation(), 
                                organizer=event.getOrganizer(),
                                tags=event.getTagStrs(),
                                summary=event.getSummary(),
                                isOrganizer=isOrganizer,
                                inEvent=(username in event.getRSVP()),
                                loggedIn=("Username" in session)
                                )
        if (isOrganizer):
            retHTML = retHTML + self._RSVPHTML(trueRSVP)
            retHTML = retHTML + render_template("sections/endSection.html")
        return self._wrapHTML(retHTML)
    
    def eventDetailedArchivedHTML(self, event, trueRSVP):
        if ("Username" in session):
            username = session["Username"]
        else:
            username = ""
        isOrganizer = (event.isOrganizerName(username))
        retHTML = render_template("pages/eventDetailsArchived.html", 
                                name=event.getName(), 
                                date=event.getDateStr(), 
                                time=event.getTimeStr(), 
                                location=event.getLocation(), 
                                organizer=event.getOrganizer(),
                                tags=event.getTagStrs(),
                                summary=event.getSummary(),
                                isOrganizer=isOrganizer,
                                )
        if (isOrganizer):
            retHTML = retHTML + self._RSVPHTML(trueRSVP)
            retHTML = retHTML + render_template("sections/endSection.html")
        return self._wrapHTML(retHTML)
    
    def _RSVPHTML(self, RSVP):
        retHTML = ""
        for user in RSVP:
            retHTML = retHTML + render_template("sections/userRSVP.html", username=user.getUsername(), phone=user.getPhone(), email=user.getEmail())
        return retHTML
    
    def newEventHTML(self, todayStr):
        return self._wrapHTML(render_template("pages/newEvent.html", today=todayStr, tagList=VALID_TAGS, tagDisplay=DISPLAY_TAGS, numTags=NUM_TAGS))
    
    def editEventHTML(self, event):
        return self._wrapHTML(render_template("pages/editEvent.html", name=event.getName(), tagList=VALID_TAGS, tagDisplay=DISPLAY_TAGS, numTags=NUM_TAGS))