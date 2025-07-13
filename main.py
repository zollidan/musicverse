from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests

from schema import AlbumSchema
from models import Album
from utils import get_album_cover, get_album_info
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from models import Base
from database import engine

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index_page(request: Request):
    
    albums = get_albums()
    
    return templates.TemplateResponse(
        request=request, name="index.html", context={"albums": albums}
    )
    

@app.get("/api/albums", response_model=list[AlbumSchema])
def get_albums():
    with Session(engine) as session:
        stmt = select(Album)
        albums = session.scalars(stmt).all()
        return albums


@app.post("/api/album/add", response_model=AlbumSchema, status_code=201)
def add_album(album_body: AlbumSchema):
    with Session(engine) as session:
        stmt = select(Album).where(
            Album.name == album_body.name,
            Album.artist == album_body.artist
        )
        existing_album = session.scalar(stmt)
        if existing_album:
            raise HTTPException(status_code=400, detail="Альбом уже существует у этого автора!")

        cover_url = get_album_cover(album_body.name)

        album = Album(
            name=album_body.name,
            artist=album_body.artist,
            cover_url=cover_url
        )

        session.add(album)
        session.commit()
        session.refresh(album)

        return album
