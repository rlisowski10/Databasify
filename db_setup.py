'''
This code creates the  database  by completing the tasks below;
- Creates the sqlite database and its tables/columns
- Maps python objects to those columns for CRUD operations
- Populates some data within those tables.

'''

# Create the sqlite database and map python objects
# Configuration: import all modules needed
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, Album, Artist

# Configuration: Create the database and tables
engine = create_engine('sqlite:///spotify.db')
Base.metadata.create_all(engine)


def populateData():
    # Populate starter data in the database
    # Bind the engine to the metadata of the Base class (enables declaratives to be accessed through a DBSession instance)
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)

    # A DBSession() instance establishes all conversations with the database and represents a "staging zone"
    # for all the objects loaded into the database session object. Any change made against the objects in the
    # session won't be persisted into the database until you call session.commit(). If you're not happy about the changes,
    # you can revert all of them back to the last commit by calling session.rollback()
    session = DBSession()

    # Initial artists and albums. #TO BE REPLACED with spotify API json

    artist1 = Artist(name="Lana Del Rey")

    session.add(artist1)
    session.commit()

    album1 = Album(name="Ultraviolence",
                   date=2014,
                   artist_id=artist1.id, artist=artist1)

    session.add(album1)
    session.commit()

    album2 = Album(name="Honeymoon",
                   date=2015,
                   artist_id=artist1.id, artist=artist1)

    session.add(album2)
    session.commit()

    album3 = Album(name="Norman Fucking Rockwell!",
                   date=2019,
                   artist_id=artist1.id, artist=artist1)

    session.add(album3)
    session.commit()

    artist2 = Artist(name="Aurora")

    session.add(artist1)
    session.commit()

    album4 = Album(name="A Different Kind of Human (Step 2)",
                   date=2018,
                   artist_id=artist2.id, artist=artist2)

    session.add(album4)
    session.commit()

    album5 = Album(name="Infections of a Different Kind (Step 1)",
                   date=2019,
                   artist_id=artist2.id, artist=artist2)

    session.add(album5)
    session.commit()

    album6 = Album(name="All My Demons Greeting Me as a Friend",
                   date=2016,
                   artist_id=artist2.id, artist=artist2)

    session.add(album6)
    session.commit()


# If the script is directly executed, populate data in tables
if __name__ == '__main__':
    populateData()
