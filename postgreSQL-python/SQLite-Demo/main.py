
from fastapi import FastAPI, HTTPException, Query, Depends
import psycopg2
from pydantic import BaseModel
from datetime import date
from sqlmodel import SQLModel, Field, Relationship, Session
from contextlib import asynccontextmanager
from db import init_db, get_session

@asynccontextmanager                
async def lifespan(app: FastAPI):       # A lifespan function is executed before the program is start up
    init_db()                           # The function initializes the database upon startup of the program
    yield

app = FastAPI(lifespan=lifespan)

# Reading root location to check for server existence
# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# Defining classes of objects
class baseSong(SQLModel):          # General object for a song written by a band member
    title: str
    releaseDate: date
    memberId: int | None = Field(foreign_key="member.id")  # Links song to the id of the member who wrote it through member: Member

class Song(baseSong, table=True):             # Class inherited from base, but includes song id
    id: int = Field(default=None,primary_key=True)
    member: "Member" = Relationship(back_populates="songs") # Fills songs in Member with its data; ("") since Member not defined yet

class BandMember(SQLModel):         # General object of a band member
    name: str
    startDate: date
    endDate: date = '1995-07-09'

class Member(BandMember, table=True):               # Class inherited from base, but includes member id
    id: int = Field(default=None,primary_key=True)  
    songs: list[Song] = Relationship(back_populates="member")   # Same as other Relationship() call but reverse order

# Defining initial files of band members
bandMembers = [
    {"name":"Jerry Garcia","startDate":"1965-01-01","endDate":"1995-06-30"}
#   {name='Bob Weir', startDate='1965-01-01'},
#   {name='Phil Lesh', startDate='1965-01-01'}
]

# Reading directory for all band members
@app.get("/members/")
async def see_members(name: str | None = None) -> list[BandMember]:
    queryBandMembers = bandMembers
    if name:
        queryBandMembers = []
        for members in bandMembers:
            if members["name"] == name:
                queryBandMembers.append(members)
    return(queryBandMembers)
 
# Inserting a new band member
@app.post("/members/")
async def new_member(
    member_data: BandMember,                            # POST expects data on a member in the BandMember class format
    session: Session = Depends(get_session)             # Initialize session for database access
) -> Member:
    member = Member(                                    # indexes out the provided information in the Member class format
        name=member_data.name,
        startDate=member_data.startDate,
        endDate=member_data.endDate
    )

    if member.songs:                                       # Logic adds the information for any songs that 
        for song in member.songs:                          # are included with the post request
            song_object = Song(title=song.title,
                               releaseDate=song.releaseDate,
                               memberId=member)
            session.add(song_object)

    session.add(member)             # Adds the data from member into database
    session.commit()                # Commits the changes to the database
    session.refresh(member)         # Refreshes data in member with new database additions (i.e. the primary key index)
    
    return(member)
    


