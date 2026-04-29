import requests

MY_DECKS_ENDPOINT = "https://decksofkeyforge.com/public-api/v1/my-decks"


def get_decks(api_key):
    r = requests.get(MY_DECKS_ENDPOINT, headers={"Api-Key": api_key})
    return r.json()
