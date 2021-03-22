# Flask Website: "Main"
from flask import Flask, request, session, redirect, url_for
from ProcessManager import ProcessManager
from HTMLPages import HTMLPages

app = Flask(__name__)
app.secret_key = "secure"

PManager = ProcessManager()
pages = HTMLPages()

@app.route("/", methods=["GET", "POST"])
def index():
    return pages.indexHTML()

@app.route("/login/", methods=["GET", "POST"])
def login():
    if "Username" in session:
        return redirect(url_for("account"))
    if (request.method == "POST"):
        username = request.form.get("username", "null")
        password = request.form.get("password", "null")
        if PManager.passLogin(username, password):
            session["Username"] = username
            pages.switchLogin()
            return redirect(url_for("account"))
        else:
            return pages.loginHTML(True)
    return pages.loginHTML()

@app.route("/account/", methods=["GET", "POST"])
def account():
    if "Username" in session:
        user = PManager.passUsername(session["Username"])
        return pages.accountHTML(user, True)
    else:
        return pages.accountHTML()

@app.route("/events/", methods=["GET", "POST"])
def events():
    return pages.eventsHTML()
        
if __name__=="__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)