# Email Handler: Sends email notifications out
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

    def __init__(self) -> None:
        load_dotenv(dotenv_path=self.envPath)
        self.senderEmail = os.getenv("SENDER_EMAIL")
        self.password = os.getenv("PASSWORD")
        self.port = 465
        self.context = ssl.create_default_context()
        self.notifiedList: List[List[str]] = []
    
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
    def removeNotified(self, events: List[EventData]) -> None:
        for event in events:
            eventName = event.getName()
            for notified in self.notifiedList:
                if (notified[0] == eventName):
                    self.notifiedList.remove(notified)
        self._saveNotifiedList()

    # Send email notifications for an event that happens the next day
    def oneDayNotification(self, event: EventData, rsvps: List[UserData]) -> None:
        for entry in self.notifiedList:
            if (event.isEventname(entry[0])):
                if (entry[1] == "one day"):
                    return
        with smtplib.SMTP_SSL("smtp.gmail.com", self.port, context=self.context) as server:
            server.login(self.senderEmail, self.password)
            for user in rsvps:
                receiverEmail = user.getEmail()
                message = self._oneDayNotificationMsg(event, user)
                server.sendmail(self.senderEmail, receiverEmail, message.as_string())
        self.notifiedList.append([event.getName(), "one day"])

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
            with smtplib.SMTP_SSL("smtp.gmail.com", self.port, context=self.context) as server:
                server.login(self.senderEmail, self.password)
                receiverEmail = user.getEmail()
                message = self._oneDayNotificationMsg(event, user)
                server.sendmail(self.senderEmail, receiverEmail, message.as_string())

    # Returns MIMEMultipart for email notification for an event that happens the next day
    def _oneDayNotificationMsg(self, event: EventData, user: UserData) -> MIMEMultipart:
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Reminder: {event.getName()} Tomorrow!"
        message["From"] = self.senderEmail
        message["To"] = user.getEmail()

        app = Flask("tempForSendingEmails")
        with app.app_context():
            textMsg = render_template("emails/oneDayNotification.txt", eventName=event.getName(), username=user.getUsername(), date=event.getDateStr())
            htmlMsg = render_template("emails/oneDayNotification.html", eventName=event.getName(), username=user.getUsername(), date=event.getDateStr())

        textPart = MIMEText(textMsg, "plain")
        htmlPart = MIMEText(htmlMsg, "html")

        message.attach(textPart)
        message.attach(htmlPart)
        return message

if __name__=="__main__":
    testEvent = EventData.EventBuilder("Event0", "2021-03-30", "user0", "none").RSVP(["user1", "user2"]).build()
    testUsers = [UserData("user1", "pw1", "111-111-1111", "csc3380.receive+user1@gmail.com"),
                 UserData("user2", "pw2", "222-222-2222", "csc3380.receive+user2@gmail.com")]

    app = Flask(__name__)    
    EmHandler = EmailHandler()
    
    with app.app_context():
        EmHandler.oneDayNotification(testEvent, testUsers)
        # textMsg = render_template("emails/oneDayNotification.txt", eventName="event1", username="user1", date="2021-01-01")
        # htmlMsg = render_template("emails/oneDayNotification.html", eventName="event1", username="user1", date="2021-01-01")
