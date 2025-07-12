from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from utils import get_album_info
from sqlalchemy import create_engine
from models import Base


# "sqlite://" for inmemory db and "sqlite:///database.db" for file db
engine = create_engine("sqlite://", echo=True)

Base.metadata.create_all(engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request,):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )


@app.get("/api/album")
def get_album(artist: str, album: str):
    info = get_album_info(artist, album)
    return info
