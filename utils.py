import os
from typing import Optional
from dotenv import load_dotenv
import requests
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import engine
from models import Album

load_dotenv(override=True)

API_KEY = os.getenv("LAST_FM_API_KEY")
BASE_URL = os.getenv("BASE_LAST_FM_URL")


def get_albums():
    with Session(engine) as session:
        stmt = select(Album)
        albums = session.scalars(stmt).all()
        return albums


def get_one_album(id):
    with Session(engine) as session:
        stmt = select(Album).where(Album.id == id)
        album = session.scalars(stmt).first()

        return album


def get_album_cover(album_name: str, country: str = "us"):
    params = {
        "term": album_name,
        "entity": "album",
        "limit": 1,
        "country": country
    }

    res = requests.get("https://itunes.apple.com/search", params=params)
    data = res.json()

    if data.get("results"):
        cover_url = data["results"][0]["artworkUrl100"]
        return cover_url.replace("100x100bb.jpg", "3000x3000.jpg")
    return ""


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
