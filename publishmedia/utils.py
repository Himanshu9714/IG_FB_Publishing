import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def setCreds(access_token, instagram_id):
    if access_token is not None and instagram_id is not None:
        os.environ["USER_ACCESS_TOKEN"] = access_token
        os.environ["USER_INSTAGRAM_ID"] = instagram_id


def getCreds():
    """Get creds required for use in the applications

    Returns:
            dictonary: credentials needed globally

    """
    creds = dict()
    creds["access_token"] = os.environ.get("USER_ACCESS_TOKEN")
    creds["graph_domain"] = os.environ.get("GRAPH_DOMAIN")
    creds["graph_version"] = os.environ.get("GRAPH_VERSION")
    creds["endpoint_base"] = creds["graph_domain"] + creds["graph_version"] + "/"
    creds["instagram_account_id"] = os.environ.get("USER_INSTAGRAM_ID")

    return creds


def makeApiCall(url, endpointParams, type):
    """Request data from endpoint with params

    Args:
            url: string of the url endpoint to make request from
            endpointParams: dictionary keyed by the names of the url parameters


    Returns:
            object: data from the endpoint

    """

    if type == "POST":
        if "CAROUSEL" in url:
            data = requests.post(url)
        else:
            data = requests.post(url, endpointParams)
    else:
        data = requests.get(url, endpointParams)

    response = dict()
    response["url"] = url
    response["endpoint_params"] = endpointParams
    response["endpoint_params_pretty"] = json.dumps(endpointParams, indent=4)
    response["json_data"] = json.loads(data.content)
    response["json_data_pretty"] = json.dumps(response["json_data"], indent=4)

    return response
