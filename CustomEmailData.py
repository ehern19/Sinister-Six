import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from pathlib import Path
from flask import Flask, render_template, url_for
from typing import List
from dataClasses.EventData import EventData
from EmailHandler import EmailHandler

databasePath = "database\\"
emailFilename = "CustomEmails.txt"
oldEventFilename = "OldEvents.txt"
userdataFilename = "Userdata.txt"

def __init__(self):
    self.email = EmailIO(self)

def content():


