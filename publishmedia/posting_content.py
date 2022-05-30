import time
from .utils import getCreds, makeApiCall
from dotenv import load_dotenv
import os

load_dotenv()


def createMediaObject(params):
    """Create media object

    Args:
            params: dictionary of params

    API Endpoint:
            https://graph.facebook.com/v13.0/{ig-user-id}/media?image_url={image-url}&caption={caption}&access_token={access-token}
            https://graph.facebook.com/v13.0/{ig-user-id}/media?video_url={video-url}&caption={caption}&access_token={access-token}

    Returns:
            object: data from the endpoint

    """

    print("\nParameters: ", params)
    url = params["endpoint_base"] + params["instagram_account_id"] + "/media"

    endpointParams = dict()
    endpointParams["caption"] = params["caption"]
    endpointParams["access_token"] = params["access_token"]

    # IMAGE Media Type
    if "IMAGE" == params["media_type"]:
        endpointParams["image_url"] = params["media_url"]
    # VIDEO Media Type
    else:
        endpointParams["media_type"] = params["media_type"]
        endpointParams["video_url"] = params["media_url"]

    return makeApiCall(url, endpointParams, "POST")


def getMediaObjectStatus(mediaObjectId, params):
    """Check the status of a media object

    Args:
            mediaObjectId: id of the media object
            params: dictionary of params

    API Endpoint:
            https://graph.facebook.com/v5.0/{ig-container-id}?fields=status_code

    Returns:
            object: data from the endpoint

    """

    url = params["endpoint_base"] + "/" + mediaObjectId

    endpointParams = dict()
    endpointParams["fields"] = "status_code"
    endpointParams["access_token"] = params["access_token"]

    return makeApiCall(url, endpointParams, "GET")  # make the api call


def publishMedia(mediaObjectId, params):
    """Publish content

    Args:
            mediaObjectId: id of the media object
            params: dictionary of params

    API Endpoint:
            https://graph.facebook.com/v5.0/{ig-user-id}/media_publish?creation_id={creation-id}&access_token={access-token}

    Returns:
            object: data from the endpoint

    """

    url = (
        params["endpoint_base"] + params["instagram_account_id"] + "/media_publish"
    )  # endpoint url

    endpointParams = dict()
    endpointParams["creation_id"] = mediaObjectId
    endpointParams["access_token"] = params["access_token"]

    return makeApiCall(url, endpointParams, "POST")


def getContentPublishingLimit(params):
    """Get the api limit for the user

    Args:
            params: dictionary of params

    API Endpoint:
            https://graph.facebook.com/v5.0/{ig-user-id}/content_publishing_limit?fields=config,quota_usage

    Returns:
            object: data from the endpoint

    """

    url = (
        params["endpoint_base"]
        + params["instagram_account_id"]
        + "/content_publishing_limit"
    )

    endpointParams = dict()
    endpointParams["fields"] = "config,quota_usage"
    endpointParams["access_token"] = params["access_token"]

    return makeApiCall(url, endpointParams, "GET")


def upload_image():
    params = getCreds()
    print("\n\nParams:", params)
    params["media_type"] = os.environ.get("MEDIA_TYPE")
    params["media_url"] = os.environ.get("MEDIA_URL")
    params["caption"] = os.environ.get("CAPTION")

    # create a media object through the api
    imageMediaObjectResponse = createMediaObject(params)
    # id of the media object that was created
    print(imageMediaObjectResponse)
    imageMediaObjectId = imageMediaObjectResponse["json_data"]["id"]
    imageMediaStatusCode = "IN_PROGRESS"

    print(f"\n---- IMAGE MEDIA OBJECT -----\n\tID:\t {imageMediaObjectId}")

    while (
        imageMediaStatusCode != "FINISHED"
    ):  # keep checking until the object status is finished
        imageMediaObjectStatusResponse = getMediaObjectStatus(
            imageMediaObjectId, params
        )
        imageMediaStatusCode = imageMediaObjectStatusResponse["json_data"][
            "status_code"
        ]

        print(
            f"\n---- IMAGE MEDIA OBJECT STATUS -----\n\tStatus Code:\t{imageMediaStatusCode}"
        )

        # wait 5 seconds if the media object is still being processed
        time.sleep(5)

    # publish the post to instagram
    publishImageResponse = publishMedia(imageMediaObjectId, params)
    # json response from ig api
    print(
        f'\n---- PUBLISHED IMAGE RESPONSE -----\n\tResponse:{publishImageResponse["json_data_pretty"]}'
    )


def get_user_media_edge():
    """
    API Endpoint: 
        https://graph.instagram.com/me/media?fields={fields}&access_token={access_token}
    """

    params = getCreds()
    endpointParams = dict()
    endpointParams["fields"] = ["id", "caption"]
    endpointParams["access_token"] = params["access_token"]
    url = "https://graph.instagram.com/me/media"
    
    return makeApiCall(url, endpointParams, "GET")


def get_media_with_media_id(media_id):
    """
    API Endpoint:
        https://graph.instagram.com/{media_id}?fields=id,media_type,media_url,username,timestamp&access_token={access_token}
    """
    params = getCreds()
    endpointParams = dict()
    endpointParams["access_token"] = params["access_token"]
    url = f"https://graph.instagram.com/{media_id}?fields=id,media_type,media_url,username,timestamp"
    
    return makeApiCall(url, endpointParams, "GET")
