from pydantic import BaseModel


class AlbumSchema(BaseModel):
    name: str
    artist: str
    cover_url: str = ""

    class Config:
        orm_mode = True
