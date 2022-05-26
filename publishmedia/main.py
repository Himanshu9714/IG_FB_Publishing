from flask import Flask, render_template, redirect, request, session
import requests
from oauthlib.oauth2 import WebApplicationClient
import os
from dotenv import load_dotenv
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

load_dotenv()


# Configuration
INSTAGRAM_CLIENT_ID = os.environ.get("IG_APP_ID", None)
INSTAGRAM_CLIENT_SECRET = os.environ.get("IG_SECRET_KEY", None)

# OAuth 2 client setup
client = WebApplicationClient(INSTAGRAM_CLIENT_ID)

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

@app.route("/")
def index():
    try:
        code = request.args.get("code")
        print("\n\nThis is code", code)
        url = "https://api.instagram.com/oauth/access_token"
        data = {"client_id": os.environ.get("IG_APP_ID"), "client_secret": os.environ.get("IG_CLIENT_SECRET"), "grant_type": "authorization_code", "redirect_url": os.environ.get("REDIRECT_URL"), "code": code}
        json_data = requests.post(url, data=data)
        print(json_data)
        if code:
            return f"Data: {json_data}"
    except:pass
    return '<a class="button" href="/login">IG Login</a>'

@app.route("/privacy-policy")
def privacy_policy():
    return render_template("privacy_policy.html")


# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)

@app.route("/login")
def login():
    authorization_endpoint = os.environ.get("IG_DISCOVERY_URL")

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=os.environ.get("REDIRECT_URL"),
        scope=["user_profile", "user_media"],
    )
    print("*"*20)
    print(request_uri, "\n", request.base_url)
    print("*"*20)
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    """
    https://api.instagram.com/oauth/access_token \
    -F client_id=990602627938098 \
    -F client_secret=eb8c7... \
    -F grant_type=authorization_code \
    -F redirect_uri=https://socialsizzle.herokuapp.com/auth/ \
    -F code=AQBx-hBsH3...
    """
    code = request.args.get("code")
    url = "https://api.instagram.com/oauth/access_token"
    data = {"client_id": os.environ.get("IG_APP_ID"), "client_secret": os.environ.get("IG_CLIENT_SECRET"), "grant_type": "authorization_code", "redirect_url": os.environ.get("REDIRECT_URL")+'/auth/', "code": code}
    json_data = requests.post(url, data=data)
    return json_data
