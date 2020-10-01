'''
This code defines the object relational model classes that sqlalchemy uses.
Each class maps to a table in the database.
'''

# Create the sqlite database and map python objects
# Configuration: import all modules needed

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float, Boolean


# Configuration: Create instance of declarative base (class code will inherit this)
Base = declarative_base()


# Representation of the user database table as a python class.
class User(Base):
    __tablename__ = 'user'

    # id is auto-incremented.
    id = Column(Integer, primary_key=True)
    email = Column(String(150), nullable=False)
    password = Column(String(150), nullable=False)


# Representation of the playlist table and relationship as a python class.
class Playlist(Base):
    __tablename__ = 'playlist'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    user = relationship(User)


# Representation of the artist table as a python class.
class Artist(Base):
    __tablename__ = 'artist'

    id = Column(Integer, primary_key=True)
    uri = Column(String(50), nullable=False)
    name = Column(String(150), nullable=False)
    popularity = Column(Integer, nullable=False)
    followers = Column(Integer, nullable=False)


# Representation of the album table and relationship as a python class.
class Album(Base):
    __tablename__ = 'album'

    id = Column(Integer, primary_key=True)
    uri = Column(String(50), nullable=False)
    name = Column(String(150), nullable=False)
    release_date = Column(Date, nullable=False)
    artist_id = Column(Integer, ForeignKey('artist.id'), nullable=False)

    artist = relationship(Artist, backref="artist")

    # JSON objects in a serializable format
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'uri': self.uri,
            'release_date': self.release_date,
            'artist_id': self.artist_id,
        }


# Representation of the playlist item table and relationship as a python class.
class PlaylistItem(Base):
    __tablename__ = 'playlist_item'

    id = Column(Integer, primary_key=True)
    playlist_id = Column(Integer, ForeignKey('playlist.id'), nullable=False)
    song_id = Column(Integer, ForeignKey('song.id'), nullable=False)

    playlist = relationship(Playlist, backref="playlist")


# Representation of the featuring item table and relationship as a python class.
class FeaturingItem(Base):
    __tablename__ = 'featuring_item'

    id = Column(Integer, primary_key=True)
    artist_id = Column(Integer, ForeignKey('artist.id'), nullable=False)
    song_id = Column(Integer, ForeignKey('song.id'), nullable=False)

    featuringArtist = relationship(Artist, backref="featuringArtist")


# Representation of the song item table and relationship as a python class.
class Song(Base):
    __tablename__ = 'song'

    id = Column(Integer, primary_key=True)
    uri = Column(String(50), nullable=False)
    track_number = Column(Integer, nullable=True)
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

    album = relationship(Album, backref="album")
