from flask import Flask, render_template, redirect, request, session
import requests
from oauthlib.oauth2 import WebApplicationClient
import os
from dotenv import load_dotenv

load_dotenv()


# Configuration
INSTAGRAM_CLIENT_ID = os.environ.get("IG_APP_ID", None)
INSTAGRAM_CLIENT_SECRET = os.environ.get("IG_SECRET_KEY", None)

# OAuth 2 client setup
client = WebApplicationClient(INSTAGRAM_CLIENT_ID)

app = Flask(__name__)

@app.route("/")
def index():
    code = request.args.get("code")
    print("\n\nThis is code", code)
    if code:
        url = "https://api.instagram.com/oauth/access_token"
        data = {"client_id": INSTAGRAM_CLIENT_ID, "client_secret": INSTAGRAM_CLIENT_SECRET, "grant_type": "authorization_code", "redirect_uri": os.environ.get("REDIRECT_URL"), "code": code}
        # session = requests.Session()
        # json_data = session.post(url, data)
        # print(json_data)
        return f"Data"
    return '<a class="button" href="/login">IG Login</a>'

@app.route("/privacy-policy")
def privacy_policy():
    return render_template("privacy_policy.html")



@app.route("/login")
def login():
    authorization_endpoint = os.environ.get("IG_DISCOVERY_URL")
    print("os.environ.get('REDIRECT_URL') ", os.environ.get("REDIRECT_URL"))
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=os.environ.get("REDIRECT_URL"),
        scope=["user_profile", "user_media"],
    )
    print("*"*20)
    print(request_uri, "\n", request.base_url)
    print("*"*20)
    return redirect(request_uri)