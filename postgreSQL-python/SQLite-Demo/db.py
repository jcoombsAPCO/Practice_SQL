from sqlmodel import create_engine, SQLModel, Session

DATABASE_URL = 'sqlite:///db.sqlite'                # Where the database is stored ***This is SQLite, but others can be used

engine = create_engine(DATABASE_URL, echo=True)     

def init_db():                                      # This function makes it so that all the objects with 'Table=True'
    SQLModel.metadata.create_all(engine)            # will automatically be converted into tables in the database

def get_session():                                  # Each 'Session' object indicates some type of access to the database,
    with Session(engine) as session:                # and will be called in each of the CRUD requests
        yield session
