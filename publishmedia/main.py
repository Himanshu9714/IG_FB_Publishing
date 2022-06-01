from flask import Flask, render_template, redirect, request, session, url_for
import requests
from oauthlib.oauth2 import WebApplicationClient
import os
from dotenv import load_dotenv
from .posting_content import get_user_media_edge
from .posting_content import upload_image
from .posting_content import get_media_with_media_id
from .utils import setCreds

load_dotenv()


# Configuration
INSTAGRAM_CLIENT_ID = os.environ.get("IG_APP_ID", None)
INSTAGRAM_CLIENT_SECRET = os.environ.get("IG_SECRET_KEY", None)

FB_ACCESS_TOKEN = None

# OAuth 2 client setup
client = WebApplicationClient(INSTAGRAM_CLIENT_ID)

app = Flask(__name__)
app.config["USER_ACCESS_TOKEN"] = None


@app.route("/")
def index():
    code = request.args.get("code")
    if code:
        data = {
            "client_id": INSTAGRAM_CLIENT_ID,
            "client_secret": INSTAGRAM_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "redirect_uri": os.environ.get("REDIRECT_URL"),
            "code": code,
        }
        print("\n\n\nCookie: ", request.cookies.get("sessionid"), "\n\n")
        session = requests.session()
        response_data = session.post(os.environ.get("IG_ACCESS_TOKEN_URL"), data)
        json_data = response_data.json()
        app.config["USER_ACCESS_TOKEN"] = json_data["access_token"]
        app.config["USER_IG_ID"] = str(json_data["user_id"])
        return redirect(url_for("ig_media"))

    return render_template("index.html")


@app.route("/ig-media")
def ig_media():
    print("Setting Credentials...", FB_ACCESS_TOKEN)
    app.config.update(USER_ACCESS_TOKEN=FB_ACCESS_TOKEN)
    print(app.config["USER_ACCESS_TOKEN"], "17841453260604057")
    setCreds(app.config["USER_ACCESS_TOKEN"], "17841453260604057")             
    upload_image()
    return render_template("media.html", response={"success": "uploaded successfully!"})


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
        scope=["user_profile", "user_media", "instagram_content_publish"],
    )
    print("\n\n\n", request.cookies.get("sessionid"))
    print("*" * 20)
    print(request_uri, "\n", request.base_url)
    print("*" * 20)
    return redirect(request_uri)


@app.route("/publish-media")
def publish_media():
    upload_image()
    return "You're on the publish media page!"


@app.route("/get-token", methods=['POST'])
def get_token():
    jsdata = request.get_json()
    access_token = jsdata["authResponse"]["accessToken"]
    global FB_ACCESS_TOKEN
    FB_ACCESS_TOKEN = access_token
    print("Access Token", FB_ACCESS_TOKEN)
    return redirect(url_for("ig_media"))