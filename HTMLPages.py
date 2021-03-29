# HTML Pages: Functions that return the specific HTML pages
import os
from flask import render_template, session, request, url_for
from typing import List
from dataClasses.EventData import EventData
from dataClasses.UserData import UserData
from dataClasses.extras import VALID_TAGS, DISPLAY_TAGS, NUM_TAGS, DATABASE_PATH, USER_IMAGES, EVENT_IMAGES

class HTMLPages:
    # Wraps input HTML string with common header and footer
    def _wrapHTML(self, inHTML: bool):
        return (render_template("header.html", loggedIn=("Username" in session)) 
                + inHTML 
                + render_template("footer.html"))

    def indexHTML(self, popularEvents):
        retHTML = render_template("pages/index.html")
        retHTML = retHTML + render_template("sections/popularEvents.html")
        retHTML = retHTML + self._eventShortHTML(popularEvents)
        retHTML = retHTML + render_template("sections/endSection.html")
        return self._wrapHTML(retHTML)


    def loginHTML(self, attemptedLogin: bool=False):
        return self._wrapHTML(render_template("pages/login.html", failedLogin=attemptedLogin))
    
    def accountHTML(self, user: UserData, userEvents: List[EventData], isUser: bool=False, userRSVPEvents: List[EventData]=[]):
        retHTML = render_template("sections/accountEventOrganizer.html", isUser=isUser)
        retHTML = retHTML + self._eventShortHTML(userEvents)
        retHTML = retHTML + render_template("sections/endSection.html")
        imageName = self._getCurrentUserImgName(user.getUsername())
        imageName = USER_IMAGES + imageName
        if (isUser):
            retHTML = render_template("pages/accountPrivate.html", username=user.getUsername(), phone=user.getPhone(), email=user.getEmail(), image=imageName, hasImage=os.path.isfile(DATABASE_PATH + imageName)) + retHTML
            retHTML = retHTML + render_template("sections/accountEventRSVP.html")
            retHTML = retHTML + self._eventShortHTML(userRSVPEvents)
            retHTML = retHTML + render_template("sections/endSection.html")
        else:
            retHTML = render_template("pages/accountPublic.html", username=user.getUsername(), image=imageName, hasImage=os.path.isfile(DATABASE_PATH + imageName)) + retHTML
        return self._wrapHTML(retHTML)

    def newAccountHTML(self, badName: bool=False, badImage: bool=False):
        return self._wrapHTML(render_template("pages/accountNew.html", badName=badName, badImage=badImage))

    def editAccountHTML(self, badImage: bool=False):
        return self._wrapHTML(render_template("pages/accountEdit.html", badImage=badImage))

    def accountDNEHTML(self, accountName: str):
        return self._wrapHTML(render_template("pages/accountDNE.html", username=accountName))

    def eventsHTML(self, eventList: List[EventData], searching: str="all"):
        if (request.args):
            searchType = request.args.get("searchType")
            date = request.args.get("searchDate")
            text = request.args.get("searchValue")
            tags = request.args.getlist("tags")
            retHTML = render_template("pages/events.html", tagList=VALID_TAGS, tagDisplay=DISPLAY_TAGS, numTags=NUM_TAGS,
                    searchType=searchType, searchDate=date, searchValue=text, tags=tags)
        else:
            retHTML = render_template("pages/events.html", tagList=VALID_TAGS, tagDisplay=DISPLAY_TAGS, numTags=NUM_TAGS,
                    searchType="", searchDate="", searchValue="", tags=[])
        retHTML = retHTML + self._eventShortHTML(eventList)
        return self._wrapHTML(retHTML)

    def _eventShortHTML(self, eventList: List[EventData]):
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

    def eventArchiveHTML(self, eventList: List[EventData]):
        retHTML = render_template("pages/eventArchive.html")
        retHTML = retHTML + self._eventShortArchivedHTML(eventList)
        return self._wrapHTML(retHTML)
    
    def _eventShortArchivedHTML(self, eventList: List[EventData]):
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

    def eventDetailedHTML(self, event: EventData, trueRSVP: List[UserData]):
        if ("Username" in session):
            username = session["Username"]
        else:
            username = ""
        isOrganizer = (event.isOrganizerName(username))
        imageName = self._getCurrentEventImgName(event.getName())
        imageName = EVENT_IMAGES + imageName
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
                                loggedIn=("Username" in session),
                                image=imageName,
                                hasImage=os.path.isfile(DATABASE_PATH + imageName)
                                )
        if (isOrganizer):
            retHTML = retHTML + self._RSVPHTML(trueRSVP)
            retHTML = retHTML + render_template("sections/endSection.html")
        return self._wrapHTML(retHTML)
    
    def eventDetailedArchivedHTML(self, event: EventData, trueRSVP: List[UserData]):
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
    
    def _RSVPHTML(self, RSVP: List[UserData]):
        retHTML = ""
        for user in RSVP:
            retHTML = retHTML + render_template("sections/userRSVP.html", username=user.getUsername(), phone=user.getPhone(), email=user.getEmail())
        return retHTML
    
    def newEventHTML(self, todayStr: str, badName: bool=False, badImage: bool=False):
        if (request.form):
            name = request.form.get("name")
            date = request.form.get("date")
            time = request.form.get("time")
            location = request.form.get("location")
            zip = request.form.get("zip")
            tags = request.form.getlist("tags")
            summary = request.form.get("summary", "")
            recurring = request.form.get("recurring")
            day = int(date[-2:])

            return self._wrapHTML(render_template("pages/eventNew.html", today=todayStr, tagList=VALID_TAGS, tagDisplay=DISPLAY_TAGS, numTags=NUM_TAGS,
                    name=name, date=date, time=time, location=location, zip=zip, tags=tags, summary=summary, recurring=recurring, day=day, badName=badName, badImage=badImage))
        return self._wrapHTML(render_template("pages/eventNew.html", today=todayStr, tagList=VALID_TAGS, tagDisplay=DISPLAY_TAGS, numTags=NUM_TAGS,
                    name="", date="", time="", location="", zip="", tags="", summary=""))
    
    def editEventHTML(self, event: EventData, badImage: bool=False):
        return self._wrapHTML(render_template("pages/eventEdit.html", name=event.getName(), tagList=VALID_TAGS, tagDisplay=DISPLAY_TAGS, numTags=NUM_TAGS, badImage=badImage))
    
    def _getCurrentEventImgName(self, eventName: str) -> str:
        eventPath = DATABASE_PATH + EVENT_IMAGES
        version = 0
        baseName = eventName + ".jpg"
        imageName = baseName + str(version)
        while(os.path.isfile(eventPath + imageName)):
            version = version + 1
            imageName = baseName + str(version)
        version = version - 1
        imageName = baseName + str(version)
        return imageName

    def _getCurrentUserImgName(self, username: str) -> str:
        userPath = DATABASE_PATH + USER_IMAGES
        version = 0
        baseName = username + ".jpg"
        imageName = baseName + str(version)
        while(os.path.isfile(userPath + imageName)):
            version = version + 1
            imageName = baseName + str(version)
        version = version - 1
        imageName = baseName + str(version)
        return imageName