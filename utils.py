import os
from typing import Optional
from dotenv import load_dotenv
import requests

load_dotenv(override=True)

API_KEY = os.getenv("LAST_FM_API_KEY")
BASE_URL = os.getenv("BASE_LAST_FM_URL")

def get_album_cover(album_name: str):
    params = {
        "entity": "song",
        "limit": 1,
        "term": album_name
    }

    res = requests.get("https://itunes.apple.com/search", params=params).json()
    cover_url = res["results"][0]["artworkUrl100"] if res.get("results") else ""
    cover_url = cover_url.replace("100x100bb.jpg", "1000x1000bb.jpg")

    return cover_url

def get_album_info(artist: str, album: str):

    params = {
        "method": "album.getinfo",
        "artist": artist,
        "album": album,
        "api_key": API_KEY,
        "format": "json"
    }

    response = requests.get(BASE_URL, params=params)

    return response.json()
