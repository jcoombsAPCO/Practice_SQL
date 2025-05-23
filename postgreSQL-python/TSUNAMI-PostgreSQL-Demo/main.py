from fastapi import FastAPI, Depends
import psycopg2
from sqlmodel import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Album, Song, newAlbum, newSong, Base

# The following 4 lines are necessary for developing a connection to the database - NECESSARY
# DATABASE_URL includes a password (in this case jencena317) which can be changed and included in a KEYS file
DATABASE_URL = "postgresql://postgres:jencena317@localhost/Beatles"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)       # Base must be created with declarative_base() elsewhere

app = FastAPI()         # Initializing the FastAPI app - used in all fastapi programs

# Creating a function to initialize a session that enters the database - NECESSARY
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST Request to send a new Album to the database
@app.post("/Albums/", response_model=newAlbum)         # The request creates an output with the
async def create_album(                                # Pydantic formed newAlbum structure
    album_data: newAlbum,                              # Input should be in the Pydantic BaseModel structure
    session: Session = Depends(get_session)            
):                                                     
    album = Album(                          # Clarifies the entry is going to the Album table;
        id = album_data.id,                 # This is why the SQL models are essential to create
        title = album_data.title,           
        release = album_data.release,       # The entries are filled according to the SQLmodel schema
        songs = [],
        numberOne = album_data.numberOne 
    )

    song_objects = album_data.songs
    if song_objects:
        for songs in song_objects:
            added_song = Song(
                id = songs.id,              # This line/any input is unnecessary due to Field() call in the Pydantic model
                title = songs.title,
                album_id = album.id         # A foreign key exists, but this ensures the correct album id is assigned
            )
            album.songs.append(added_song)
    
    session.add(album)
    session.commit()
    session.refresh(album)                  # For things like id where input is not necessary, "refresh" updates and
    return(album)                           # returns the actual data in the database (for debugging purposes)
    


# POST Request to send a new song to the database
@app.post("/songs/", response_model=newSong)
async def create_song(
    song_data: newSong,
    session: Session = Depends(get_session)         # Any request that utilizes the database must initialize
):                                                  # a session parameter with the Depends() command
    if song_data.id:
        song_data.id = None
    
    song = Song(
        id = song_data.id,
        title = song_data.title,
        album_id = song_data.album_id
    )

    session.add(song)
    session.commit()
    session.refresh(song)
    return(song)

# GET Request to see all the Albums in the database
@app.get("/albums/")
async def see_albums(
    session: Session = Depends(get_session)
):
    albums = session.query(Album).all()             # Queries all the entries in the Albums table that is defined
    return(albums)                                  # by the "Album" SQLmodel Base object

# GET Request to see all the Songs in the database
@app.get("/songs/")
async def see_songs(
    session: Session = Depends(get_session)
):
    songs = session.query(Song).all()
    return(songs)

# DELETE Request to remove a song from the database
@app.delete("/songs/")
async def delete_song(
    song_id: int,
    session: Session = Depends(get_session)
):
    song = session.query(Song).filter(Song.id == song_id).first()   # Song.id searches through the table defined by the 
                                                                    # Song SQLmodel Base and finds the matching id
    session.delete(song)
    session.commit()
    return {f"Song with id {song_id} has been deleted"}

