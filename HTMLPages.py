# HTML Pages: Functions that return the specific HTML pages
from flask import render_template
from UserData import UserData

class HTMLPages:
    def __init__(self):
        self.validLogin = False

    # Switches validLogin
    def switchLogin(self):
        self.validLogin = not self.validLogin

    # Wraps input HTML string with common header and footer
    def wrapHTML(self, inHTML):
        return (render_template("header.html", loggedIn=self.validLogin) 
                + inHTML 
                + render_template("footer.html"))

    def indexHTML(self):
        return self.wrapHTML(render_template("pages/index.html"))

    def loginHTML(self, attemptedLogin=False):
        return self.wrapHTML(render_template("pages/login.html", failedLogin=attemptedLogin))
    
    def accountHTML(self, user, isUser=False):
        if (isUser):
            return self.wrapHTML(render_template("pages/accountPrivate.html", username=user.getUsername()))
        else:
            return self.wrapHTML(render_template("pages/accountPublic.html", username=user.getUsername()))

    def eventsHTML(self):
        return self.wrapHTML(render_template("pages/events.html"))