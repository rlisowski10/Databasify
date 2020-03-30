# Create the sqlite database and map python objects
# Configuration: import all modules needed
import os
import sys
from sqlalchemy import Table, Column, ForeignKey, Integer, String, DateTime, Text, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime


# Configuration: Create instance of declarative base (class code will inherit this)
Base = declarative_base()

# #association tables
# playlist_association = Table('playlist_item', Base.metadata,
#     Column('playlist_id', Integer, ForeignKey('song.playlist_id')),
#     Column('id', Integer, ForeignKey('playlist.id'))
# )

# # featuring_association = Table('featuring_item', Base.metadata,
# #     Column('song_id', Integer, ForeignKey('song.id')),
# #     Column('artist_id', Integer, ForeignKey('artist.id'))
# # )


# Class: Representation of table as a python class, extends the Base class

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(150), nullable=False)
    password = Column(String(150), nullable=False)

class Playlist(Base):
    __tablename__ = 'playlist'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    user = relationship(User)

class Artist(Base):
    __tablename__ = 'artist'  # Table in the database

    # Mapper: Maps python objects to columns in the database
    id = Column(Integer, primary_key=True)  # auto incremented
    uri = Column(String(50), nullable=False) #spotify:artist:6rqhFgbbKwnb9MLmUQDhG6
    name = Column(String(150), nullable=False)
    followers = Column(Integer, nullable=False) #of people following them (spotify)

class Album(Base):
    __tablename__ = 'album'

    id = Column(Integer, primary_key=True)  # auto incremented
    uri = Column(String(50), nullable=False)# spotify:album:6rqhFgbbKwnb9MLmUQDhG6
    name = Column(String(150), nullable=False)
    release_date = Column(DateTime, nullable=False)
    artist_id = Column(Integer, ForeignKey('artist.id'), nullable=False)

    artist = relationship(Artist, backref="artist") 

class PlaylistItem(Base):
    __tablename__ = 'playlist_item'
    id = Column(Integer, primary_key=True)  # auto incremented
    playlist_id = Column(Integer, ForeignKey('playlist.id'), nullable=False)
    song_id = Column(Integer, ForeignKey('song.id'), nullable=False)

    playlist = relationship(Playlist, backref="playlist")

class FeaturingItem(Base):
    __tablename__ = 'featuring_item'
    id = Column(Integer, primary_key=True)  # auto incremented
    artist_id = Column(Integer, ForeignKey('artist.id'), nullable=False)
    song_id = Column(Integer, ForeignKey('song.id'), nullable=False)

    featuringArtist = relationship(Artist, backref="featuringArtist")


class Song(Base):
    __tablename__ = 'song'

    id = Column(Integer, primary_key=True)
    uri = Column(String(50), nullable=False) #spotify:track:6rqhFgbbKwnb9MLmUQDhG6
    track_number = Column(Integer, nullable=True) #order it appears on the album
    name = Column(String(250), nullable=False)
    popularity = Column(Integer, nullable=True)
    duration = Column(Integer, nullable=False)
    danceability = Column(Float, nullable=True)
    explicit = Column(Boolean, nullable=True)
    tempo = Column(Float, nullable=True)
    energy = Column(Float, nullable=True)
    instrumentalness = Column(Float, nullable=True)
    time_signature = Column(Integer, nullable=True)
    valence = Column(Float, nullable=True)
    album_id = Column(Integer, ForeignKey('album.id'), nullable=False)
    #playlist_id = Column(Integer, ForeignKey(Playlist.id), nullable=True)

    album = relationship(Album, backref="album")

    #playlists = relationship(Playlist, backref="playlist")
    #artists = relationship(Artist, secondary=featuring_association, backref="featuring")
