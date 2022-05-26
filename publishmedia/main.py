from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return "Jay Shree Ram"

@app.route("/privacy-policy")
def privacy_policy():
    return render_template("privacy_policy.html")