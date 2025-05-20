from datetime import date
from sqlmodel import Field
from sqlalchemy import Column, String, Date, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

# Base is essential to connecting SQLmodels from SQLalchemy and using alembic to make updates
Base = declarative_base()

# Both the "Album" and "Song" utilize Base in order to construct a class that represents a table in the database
# These objects are referenced in order to determine which table an endpoint request refers to
# These objects are necessary in order to develop database schema that alembic uses to autogenerate SQL code
class Album(Base):
    __tablename__ = 'Albums'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release = Column(Date, nullable=False)
    songs = relationship("Song",back_populates="album")             # "Album" and "Song" in "" to avoid errors if they are not yet defined

class Song(Base):
    __tablename__ = 'Songs'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    album_id = Column(Integer,ForeignKey('Albums.id'))              # The table that contains songs has a foreign key
                                                                    # that connects it to the album which it belongs;
    album = relationship("Album",back_populates="songs")            # back_populates must be present in both tables that
                                                                    # use it, but the foreign key is only necessary in one;

# Both the "newAlbum" and "newSong" objects are pydantic base models that are necessary for validating responses in
# endpoint requests for FastAPI; They can be used 1) to create a schema that makes user input easier to input (although
# this would not likely be necessary in TSUNAMI) and 2) they validate the data in the output is correct - error managing
class newAlbum(BaseModel):                                          
    id: int = Field(default=None,primary_key=True)
    title: str
    release: date
    songs: list["newSong"] = []

class newSong(BaseModel):
    id: int = Field(default=None,primary_key=True)
    title: str
    album_id: int 



