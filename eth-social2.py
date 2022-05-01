import requests
import os
import json


# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='blah blah blah blah'
bearer_token = os.environ.get("BEARER_TOKEN")


def create_url():
    tweet_fields = "tweet.fields=lang,author_id,created_at,conversation_id,entities,geo,id,source,text"

    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld

    #author_id = "whale_alert"

    ids = "ids=1507256051892113427"
    #ids = "ids=1507256051892113427,1505953365892685827"
    #https://twitter.com/whale_alert/status/1507256051892113427
    #https://twitter.com/whale_alert/status/1505953365892685827

    # You can adjust ids to include a single Tweets.
    # Or you can add to up to 100 comma-separated IDs
    url = "https://api.twitter.com/2/tweets?{}&{}".format(ids, tweet_fields)
    return url


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2TweetLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main():
    url = create_url()
    json_response = connect_to_endpoint(url)
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()


# check:
# https://github.com/twitterdev/search-tweets-python

# lib:
# https://developer.twitter.com/en/docs/twitter-api/tools-and-libraries/v2

# https://twython.readthedocs.io/en/latest/