#                                       Summary:
#
# This class handles and regulates the sending of emails to each user out from our program.
# It allows for sending emails, tracking what has been sent, eliminating events from notification lists,
# and preventing spam.
#
#
#
#                                      Data members:
#
# notifiedList, password, senderEmail, eventName, notificationType
#
#
#
#                                       Methods:
#
# "init": The "constructor" class, it initializes each one.
#
# "loadNotifiedList": It creates and loads a list of notifications that have already
# been sent out, along with handling events that are no longer active.
#
# "saveNotifiedList": It saves the notified list.
#
# "removeNotified": If an event does not need notifications sent out,
# it removes the event from the list
#
# "oneDayNotification": Will send out event information for events happening 
# the next day.
#
# "oneDayUserNotification": Specifically sends an email to the user about an upcoming event,
# provided that one has already been sent for that event.
#
# "oneDayNotificationMsg": Returns a value for messages sent out for the one day
# notification.

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from pathlib import Path
from flask import Flask, render_template, url_for
from typing import List


from dataClasses.EventData import EventData
from dataClasses.UserData import UserData

class EmailHandler:
    envPath = Path("database/.env")
    emailTemplatePath = "emails\\"
    notifiedListPath = "database\\NotifiedList.txt"
    invitedListPath = "database\\InvitedList.txt"

    def __init__(self, newHostName) -> None:
        load_dotenv(dotenv_path=self.envPath)
        self.senderEmail = os.getenv("SENDER_EMAIL")
        self.password = os.getenv("PASSWORD")
        self.emailPort = 465
        self.hostName = newHostName
        self.context = ssl.create_default_context()
        # [[eventName, notificationType], ...]
        self.notifiedList: List[List[str]] = []
        # [[eventName, [userName, ...]], ...]
        self.invitedList: List[List[str, List[str]]] = []
        self.onStartup()
    
    # Check if files exist, make them if not
    def onStartup(self):
        if (not os.path.exists(self.notifiedListPath)):
            newFile = open(self.notifiedListPath, 'w')
            newFile.close()
        if (not os.path.exists(self.invitedListPath)):
            newFile = open(self.invitedListPath, 'w')
            newFile.close()
    
    # Call load methods
    def load(self, activeEvents: List[EventData]) -> None:
        self.loadNotifiedList(activeEvents)
        self.loadInvitedList(activeEvents)

    # Load list of event notifications already sent out
    def loadNotifiedList(self, activeEvents: List[EventData]) -> None:
        self.notifiedList = []
        with open(self.notifiedListPath, 'r') as inFile:
            for line in inFile:
                line = line.strip().split()
                line = [entry.replace('_', ' ') for entry in line]
                eventName = line.pop(0)
                notificationType = line.pop(0)
                
                # Ignore events that are not active anymore
                activeEventNames = [event.getName() for event in activeEvents]
                if (eventName in activeEventNames):
                    self.notifiedList.append([eventName, notificationType])
        self._saveNotifiedList()
    
    # Save notified list
    def _saveNotifiedList(self) -> None:
        with open(self.notifiedListPath, 'w') as outFile:
            for entry in self.notifiedList:
                line = entry
                line = [entry.replace(' ', '_') for entry in line]
                line = ' '.join(line)
                print(line, file=outFile)

    # Remove a list of retired events from the notified list
    # Removes all mentions of each event in list
    def removeNotified(self, events: List[EventData]) -> None:
        for event in events:
            eventName = event.getName()
            for notified in self.notifiedList:
                if (notified[0] == eventName):
                    self.notifiedList.remove(notified)
        self._saveNotifiedList()
    
    # Load list of event invitations already sent out
    def loadInvitedList(self, activeEvents: List[EventData]) -> None:
        self.invitedList = []
        with open(self.invitedListPath, 'r') as inFile:
            for line in inFile:
                line = line.strip().split()
                eventName = line[0]

                # Ignore events that are not active anymore
                activeEventNames = [event.getName() for event in activeEvents]
                if (eventName in activeEventNames):
                    self.invitedList.append(line)
        self._saveInvitedList()
    
    # Save notified list
    def _saveInvitedList(self) -> None:
        with open(self.invitedListPath, 'w') as outFile:
            for entry in self.invitedList:
                line = []
                line.extend(entry)
                line = ' '.join(line)
                print(line, file=outFile)

    # Remove a list of retired events from the invited list
    # Removes all mentions of each event in list
    def removeInvited(self, events: List[EventData]) -> None:
        for event in events:
            eventName = event.getName()
            for invited in self.invitedList:
                if (invited[0] == eventName):
                    self.invitedList.remove(invited)
        self._saveInvitedList()
    
    # Returns list of usernames already invited to given event
    # Returns empty list if event is not in invitedList
    def getInvited(self, eventName: str) -> List[str]:
        for entry in self.invitedList:
            if (eventName == entry[0]):
                return entry[1:]
        return []

    # Send email notifications for an event that happens the next day
    def oneDayNotification(self, event: EventData, rsvps: List[UserData]) -> None:
        for entry in self.notifiedList:
            if (event.isEventname(entry[0])):
                if (entry[1] == "one day"):
                    return
        with smtplib.SMTP_SSL("smtp.gmail.com", self.emailPort, context=self.context) as server:
            server.login(self.senderEmail, self.password)
            for user in rsvps:
                receiverEmail = user.getEmail()
                message = self._oneDayNotificationMsg(event, user)
                server.sendmail(self.senderEmail, receiverEmail, message.as_string())
            self.notifiedList.append([event.getName(), "one day"])
            self._saveNotifiedList()

    # Send email notification to one user for an event that happens the next day
    # Will only send if a notification has already been sent for the event
    def oneUserOneDayNotification(self, event: EventData, user: UserData) -> None:
        alreadyNotified = False
        for entry in self.notifiedList:
            if (event.isEventname(entry[0])):
                if (entry[1] == "one day"):
                    alreadyNotified = True
        if (not alreadyNotified):
            return
        else:
            with smtplib.SMTP_SSL("smtp.gmail.com", self.emailPort, context=self.context) as server:
                server.login(self.senderEmail, self.password)
                receiverEmail = user.getEmail()
                message = self._oneDayNotificationMsg(event, user)
                server.sendmail(self.senderEmail, receiverEmail, message.as_string())

    # Returns MIMEMultipart for email notification for an event that happens the next day
    def _oneDayNotificationMsg(self, event: EventData, user: UserData) -> MIMEMultipart:
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Reminder: {event.getName()} Soon!"
        message["From"] = self.senderEmail
        message["To"] = user.getEmail()

        app = Flask("tempForSendingEmails")
        with app.app_context():
            textMsg = render_template("emails/oneDayNotification.txt", eventName=event.getName(), username=user.getUsername(), date=event.getDateStr(), host=self.hostName)
            htmlMsg = render_template("emails/oneDayNotification.html", eventName=event.getName(), username=user.getUsername(), date=event.getDateStr(), host=self.hostName)

        textPart = MIMEText(textMsg, "plain")
        htmlPart = MIMEText(htmlMsg, "html")

        message.attach(textPart)
        message.attach(htmlPart)
        return message
    
    # Send email notifications for an event that happens the next week
    def oneWeekNotification(self, event: EventData, rsvps: List[UserData]) -> None:
        for entry in self.notifiedList:
            if (event.isEventname(entry[0])):
                if (entry[1] == "one week"):
                    return
        with smtplib.SMTP_SSL("smtp.gmail.com", self.emailPort, context=self.context) as server:
            server.login(self.senderEmail, self.password)
            for user in rsvps:
                receiverEmail = user.getEmail()
                message = self._oneWeekNotificationMsg(event, user)
                server.sendmail(self.senderEmail, receiverEmail, message.as_string())
            self.notifiedList.append([event.getName(), "one week"])
            self._saveNotifiedList()

    # Returns MIMEMultipart for email notification for an event that happens the next day
    def _oneWeekNotificationMsg(self, event: EventData, user: UserData) -> MIMEMultipart:
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Reminder: {event.getName()} Tomorrow!"
        message["From"] = self.senderEmail
        message["To"] = user.getEmail()

        app = Flask("tempForSendingEmails")
        with app.app_context():
            textMsg = render_template("emails/oneWeekNotification.txt", eventName=event.getName(), username=user.getUsername(), date=event.getDateStr(), host=self.hostName)
            htmlMsg = render_template("emails/oneWeekNotification.html", eventName=event.getName(), username=user.getUsername(), date=event.getDateStr(), host=self.hostName)

        textPart = MIMEText(textMsg, "plain")
        htmlPart = MIMEText(htmlMsg, "html")

        message.attach(textPart)
        message.attach(htmlPart)
        return message
    
    # Send email invite with link to event page to a list of users
    # Ignores users that have received an invite for that event
    def sendInvitation(self, event: EventData, users: List[UserData]) -> None:
        tempEventInvites = [event.getName()]
        for entry in self.invitedList:
            if (event.isEventname(entry[0])):
                remList = []
                for user in users:
                    if user.getUsername() in entry[1:]:
                        remList.append(user)
                for user in remList:
                    users.remove(user)
                
                if len(users) == 0:
                    return
                else:
                    tempEventInvites = entry
                    self.invitedList.remove(entry)

        with smtplib.SMTP_SSL("smtp.gmail.com", self.emailPort, context=self.context) as server:
            server.login(self.senderEmail, self.password)
            for user in users:
                receiverEmail = user.getEmail()
                message = self._sendInvitationMsg(event, user)
                tempEventInvites.append(user.getUsername())
                server.sendmail(self.senderEmail, receiverEmail, message.as_string())
            self.invitedList.append(tempEventInvites)
            self._saveInvitedList()

    # Returns MIMEMultipart for email invitation to an event
    def _sendInvitationMsg(self, event: EventData, user: UserData) -> MIMEMultipart:
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Notification: You're Invited!"
        message["From"] = self.senderEmail
        message["To"] = user.getEmail()

        app = Flask("tempForSendingEmails")
        with app.app_context():
            textMsg = render_template("emails/sendInvitation.txt", eventName=event.getName(), username=user.getUsername(), organizer=event.getOrganizer(), host=self.hostName)
            htmlMsg = render_template("emails/sendInvitation.html", eventName=event.getName(), username=user.getUsername(), organizer=event.getOrganizer(), host=self.hostName)

        textPart = MIMEText(textMsg, "plain")
        htmlPart = MIMEText(htmlMsg, "html")

        message.attach(textPart)
        message.attach(htmlPart)
        return message

if __name__=="__main__":
    testEvent = EventData.EventBuilder("Event0", "2021-03-30", "user0", "none").RSVP(["user1", "user2"]).build()
    testUsers = [UserData("user1", "pw1", "111-111-1111", "csc3380.receive+user1@gmail.com", "12345"),
                 UserData("user2", "pw2", "222-222-2222", "csc3380.receive+user2@gmail.com", "12345")]

    app = Flask(__name__)    
    EmHandler = EmailHandler("localhost")
    EmHandler.load([testEvent])
    
    EmHandler.oneDayNotification(testEvent, testUsers)
    EmHandler.sendInvitation(testEvent, testUsers)