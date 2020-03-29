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
from sqlalchemy import Table, Column, ForeignKey, Integer, String, DateTime, Text, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, Album, Artist, Playlist, Song, User
import datetime

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

    #Initial dummy  data. #TO BE REPLACED with spotify API json

    user1= User(email="kaan@kaan.ca", password="1234")
    user2= User(email="ryan@ryan.ca", password="1234")
    user3= User(email="paul@paul.ca", password="1234")
    session.add(user1)
    session.add(user2)
    session.add(user3)
    session.commit()

    artist1 = Artist(name="Purity Ring", uri="dummy", followers=1)
    session.add(artist1)
    session.commit()

    album1 = Album(name="Another Eternity",
                    uri = "dummyuri",
                    release_date=datetime.datetime.utcnow(),
                    artist_id=artist1.id, artist=artist1)
    session.add(album1)
    session.commit()

    # song1 = Song(uri="dummyuri",track_number=1,name="Heartsigh", popularity=100, duration=189000, danceability=1.0, explicit=False, tempo=1.0, energy=1.0, instrumentalness=1.0,time_signature=100,valence=1.0, album_id=album1.id, album=album1, playlist_id=0)
    # session.add(song1)
    # session.commit()

    plist1=Playlist(name="kaans playlist", user_id=user1.id, user=user1)
    session.add(plist1)
    session.commit()

    song_objects = [
        Song(uri="dummyuri",track_number=1,name="Heartsigh", popularity=100, duration=189000, danceability=1.0, explicit=False, tempo=1.0, energy=1.0, instrumentalness=1.0,time_signature=100,valence=1.0, album_id=album1.id, album=album1, playlist_id=0),
        Song(uri="dummyuri",track_number=2,name="Bodyache", popularity=100, duration=179000, danceability=1.0, explicit=False, tempo=1.0, energy=1.0, instrumentalness=1.0,time_signature=100,valence=1.0, album_id=album1.id, album=album1, playlist_id=0),
        Song(uri="dummyuri",track_number=3,name="Push Pull", popularity=100, duration=169000, danceability=1.0, explicit=False, tempo=1.0, energy=1.0, instrumentalness=1.0,time_signature=100,valence=1.0, album_id=album1.id, album=album1, playlist_id=0),
        Song(uri="dummyuri",track_number=4,name="Repetition", popularity=100, duration=159000, danceability=1.0, explicit=False, tempo=1.0, energy=1.0, instrumentalness=1.0,time_signature=100,valence=1.0, album_id=album1.id, album=album1, playlist_id=0),
        Song(uri="dummyuri",track_number=5,name="Stranger than Earth", popularity=100, duration=149000, danceability=1.0, explicit=False, tempo=1.0, energy=1.0, instrumentalness=1.0,time_signature=100,valence=1.0, album_id=album1.id, album=album1, playlist_id=0),
        Song(uri="dummyuri",track_number=6,name="Begin Again", popularity=100, duration=139000, danceability=1.0, explicit=False, tempo=1.0, energy=1.0, instrumentalness=1.0,time_signature=100,valence=1.0, album_id=album1.id, album=album1, playlist_id=0),
        Song(uri="dummyuri",track_number=7,name="Dust Hymn", popularity=100, duration=129000, danceability=1.0, explicit=False, tempo=1.0, energy=1.0, instrumentalness=1.0,time_signature=100,valence=1.0, album_id=album1.id, album=album1, playlist_id=1),
        Song(uri="dummyuri",track_number=8,name="Flood on the Floor", popularity=100, duration=119000, danceability=1.0, explicit=False, tempo=1.0, energy=1.0, instrumentalness=1.0,time_signature=100,valence=1.0, album_id=album1.id, album=album1, playlist_id=0),
        Song(uri="dummyuri",track_number=9,name="Sea Castle", popularity=100, duration=144000, danceability=1.0, explicit=False, tempo=1.0, energy=1.0, instrumentalness=1.0,time_signature=100,valence=1.0, album_id=album1.id, album=album1, playlist_id=0),
        Song(uri="dummyuri",track_number=10,name="Stillness in Woe", popularity=100, duration=155000, danceability=1.0, explicit=False, tempo=1.0, energy=1.0, instrumentalness=1.0,time_signature=100,valence=1.0, album_id=album1.id, album=album1, playlist_id=0)      
    ]
    session.add_all(song_objects)
    session.commit()


# If the script is directly executed, populate data in tables
if __name__ == '__main__':
    populateData()