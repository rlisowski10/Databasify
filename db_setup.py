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
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Date, Text, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, Album, Artist, Playlist, Song, User, PlaylistItem
from datetime import date
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# Note that Spotify credentials (Client ID and Client Secret) should be added as System Variables.
# Client ID as SPOTIPY_CLIENT_ID and Client Secret as SPOTIPY_CLIENT_SECRET

# Configuration: Create the database and tables
engine = create_engine('sqlite:///spotify.db')
Base.metadata.create_all(engine)

# Create a Spotify object using Spotify developer credentials.
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


def spotifyAPITest():
    """Tests against the spotify API to confirm connection.
    """
    print(os.environ.get('SPOTIPY_CLIENT_ID'))
    results = sp.search(q='weezer', limit=20)

    for idx, track in enumerate(results['tracks']['items']):
        print(idx, track['name'])


def populateArtist(session, artist_name, album_name):
    """Populates the artist database table with data from the Spotify API.

    Keyword arguments:
    session -- the database session.
    artist_name -- the name of the artist to search for.
    album_name -- the name of the album to search for.
    """
    album_result = sp.search(q='artist:' + artist_name + ' album:'
                             + album_name, type='album')
    album = sp.album(album_result['albums']['items'][0]['uri'])
    artist = sp.artist(album['artists'][0]['uri'])

    # Populate artist information based on the album search.
    # TODO: Implement code to deal with an existing artist.
    artist_db_obj = Artist(name=artist['name'],
                           uri=artist['uri'],
                           popularity=artist['popularity'],
                           followers=artist['followers']['total'])
    session.add(artist_db_obj)
    session.commit()

    populateAlbum(session, artist_db_obj, album)


def determineReleaseDate(release_date):
    """Returns a release date in python format, with the month and/or
    day set to '1' if missing.

    Keyword arguments:
    release_date -- the release date of the album in string format.
                    i.e. 2019-05-23
    """
    release_date = release_date.split('-')
    if len(release_date) == 3:
        release_date = date(
            int(release_date[0]), int(release_date[1]), int(release_date[2]))
    elif len(release_date) == 2:
        release_date = date(
            int(release_date[0]), int(release_date[1]), 1)
    elif len(release_date) == 1:
        release_date = date(int(release_date[0]), 1, 1)
    else:
        release_date = date(1900, 1, 1)

    return release_date


def populateAlbum(session, artist_db_obj, album):
    """Populates the album database table with data from the Spotify API.

    Keyword arguments:
    session -- the database session.
    artist_db_obj -- the artist database object.
    album -- the album object containing Spotify data.
    """
    # Populate album information based on the album search.
    album_db_obj = Album(name=album['name'],
                         uri=album['uri'],
                         release_date=determineReleaseDate(
        album['release_date']),
        artist_id=artist_db_obj.id, artist=artist_db_obj)
    session.add(album_db_obj)
    session.commit()

    populateSongs(session, album_db_obj, album)


def populateSongs(session, album_db_obj, album):
    """Populates the song database table with data from the Spotify API.

    Keyword arguments:
    session -- the database session.
    album_db_obj -- the album database object.
    album -- the album object containing Spotify data.
    """
    song_objects = []

    # Populate album information based on the album search.
    for track in album['tracks']['items']:
        track_info = sp.track(track['uri'])
        track_features = sp.audio_features(track['id'])[0]

        song = Song(uri=track_info['uri'],
                    track_number=track_info['track_number'],
                    name=track_info['name'],
                    popularity=track_info['popularity'],
                    duration=track_info['duration_ms'],
                    explicit=track_info['explicit'],
                    danceability=track_features['danceability'],
                    tempo=track_features['tempo'],
                    energy=track_features['energy'],
                    instrumentalness=track_features['instrumentalness'],
                    time_signature=track_features['time_signature'],
                    valence=track_features['valence'],
                    album_id=album_db_obj.id,
                    album=album_db_obj)
        song_objects.append(song)

    session.add_all(song_objects)
    session.commit()


def populateDataFromSpotify():
    """Populates the database tables with data from the Spotify API.
    """
    # Connects to SQLite Database
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    # Add all albums to be included in the database instance.
    # Currently, adding more than one album from the same artist creates
    # duplicate artists. This will have to be dealt with.
    populate_albums = []
    # Ryan
    populate_albums.append(('st vincent', 'masseduction'))
    populate_albums.append(('air', 'moon safari'))
    populate_albums.append(('wilco', 'yankee hotel foxtrot'))
    populate_albums.append(('stone roses', 'stone roses'))
    populate_albums.append(('run the jewels', 'run the jewels 2'))
    populate_albums.append(('lana del rey', 'norman fucking rockwell!'))
    populate_albums.append(('caribou', 'andorra'))
    populate_albums.append(('daft punk', 'random access memories'))
    populate_albums.append(('dan deacon', 'mystic familiar'))
    populate_albums.append(('cut copy', 'in ghost colours'))
    # Kaan
    populate_albums.append(('iamx', 'metanoia'))
    populate_albums.append(('kim petras', 'turn off the light'))
    populate_albums.append(('allie x', 'cape god'))
    populate_albums.append(('ionnalee', 'everyone afraid to be forgotten'))
    populate_albums.append(('janelle monae', 'dirty computer'))
    populate_albums.append(('goldfrapp', 'supernature'))
    populate_albums.append(('austra', 'future politics'))
    populate_albums.append(('marina', 'love + fear'))
    populate_albums.append(('morcheeba', 'blood like lemonade'))
    populate_albums.append(('purity ring', 'another eternity'))
    # Paul
    populate_albums.append(('still woozy', 'lately ep'))
    populate_albums.append(('vampire weekend', 'vampire weekend'))
    populate_albums.append(('fleet foxes', 'fleet foxes'))
    populate_albums.append(('alvvays', 'antisocialites'))
    populate_albums.append(('cage the elephant', 'melophobia'))
    populate_albums.append(('the arcs', 'yours, dreamily,'))
    populate_albums.append(('tame impala', 'lonerism'))
    populate_albums.append(('mild high club', 'skiptracing'))
    populate_albums.append(('arctic monkeys', 'am'))
    populate_albums.append(('the beatles', 'abbey road (remastered)'))

    for album in populate_albums:
        # Sleeps for two seconds between albums to not overwhelm the Spotify API.
        time.sleep(1)
        populateArtist(session, album[0], album[1])
        print(f"Populated to DB: {album[1]}")


def populateDataManually():
    """Populates the database tables with dummy data.
    """
    # Populate starter data in the database
    # Bind the engine to the metadata of the Base class (enables declaratives to be accessed through a DBSession instance)
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)

    # A DBSession() instance establishes all conversations with the database and represents a "staging zone"
    # for all the objects loaded into the database session object. Any change made against the objects in the
    # session won't be persisted into the database until you call session.commit(). If you're not happy about the changes,
    # you can revert all of them back to the last commit by calling session.rollback()
    session = DBSession()

    # Initial dummy  data. #TO BE REPLACED with spotify API json

    user1 = User(email="kaan@kaan.ca", password="1234")
    user2 = User(email="ryan@ryan.ca", password="1234")
    user3 = User(email="paul@paul.ca", password="1234")
    session.add(user1)
    session.add(user2)
    session.add(user3)
    session.commit()

    artist1 = Artist(name="Purity Ring", uri="dummy", followers=1)
    session.add(artist1)
    session.commit()

    album1 = Album(name="Another Eternity",
                   uri="dummyuri",
                   release_date=date.today,
                   artist_id=artist1.id, artist=artist1)
    session.add(album1)
    session.commit()

    # song1 = Song(uri="dummyuri",track_number=1,name="Heartsigh", popularity=100, duration=189000, danceability=1.0, explicit=False, tempo=1.0, energy=1.0, instrumentalness=1.0,time_signature=100,valence=1.0, album_id=album1.id, album=album1, playlist_id=0)
    # session.add(song1)
    # session.commit()

#     plist1 = Playlist(name="kaans playlist", user_id=user1.id, user=user1)
#     session.add(plist1)
#     session.commit()

    song_objects = [
        Song(uri="dummyuri", track_number=1, name="Heartsigh", popularity=100, duration=189000, danceability=1.0, explicit=False,
             tempo=1.0, energy=1.0, instrumentalness=1.0, time_signature=100, valence=1.0, album_id=album1.id, album=album1),
        Song(uri="dummyuri", track_number=2, name="Bodyache", popularity=100, duration=179000, danceability=1.0, explicit=False,
             tempo=1.0, energy=1.0, instrumentalness=1.0, time_signature=100, valence=1.0, album_id=album1.id, album=album1),
        Song(uri="dummyuri", track_number=3, name="Push Pull", popularity=100, duration=169000, danceability=1.0, explicit=False,
             tempo=1.0, energy=1.0, instrumentalness=1.0, time_signature=100, valence=1.0, album_id=album1.id, album=album1),
        Song(uri="dummyuri", track_number=4, name="Repetition", popularity=100, duration=159000, danceability=1.0, explicit=False,
             tempo=1.0, energy=1.0, instrumentalness=1.0, time_signature=100, valence=1.0, album_id=album1.id, album=album1),
        Song(uri="dummyuri", track_number=5, name="Stranger than Earth", popularity=100, duration=149000, danceability=1.0, explicit=False,
             tempo=1.0, energy=1.0, instrumentalness=1.0, time_signature=100, valence=1.0, album_id=album1.id, album=album1),
        Song(uri="dummyuri", track_number=6, name="Begin Again", popularity=100, duration=139000, danceability=1.0, explicit=False,
             tempo=1.0, energy=1.0, instrumentalness=1.0, time_signature=100, valence=1.0, album_id=album1.id, album=album1),
        Song(uri="dummyuri", track_number=7, name="Dust Hymn", popularity=100, duration=129000, danceability=1.0, explicit=False,
             tempo=1.0, energy=1.0, instrumentalness=1.0, time_signature=100, valence=1.0, album_id=album1.id, album=album1),
        Song(uri="dummyuri", track_number=8, name="Flood on the Floor", popularity=100, duration=119000, danceability=1.0, explicit=False,
             tempo=1.0, energy=1.0, instrumentalness=1.0, time_signature=100, valence=1.0, album_id=album1.id, album=album1),
        Song(uri="dummyuri", track_number=9, name="Sea Castle", popularity=100, duration=144000, danceability=1.0, explicit=False,
             tempo=1.0, energy=1.0, instrumentalness=1.0, time_signature=100, valence=1.0, album_id=album1.id, album=album1),
        Song(uri="dummyuri", track_number=10, name="Stillness in Woe", popularity=100, duration=155000, danceability=1.0, explicit=False,
             tempo=1.0, energy=1.0, instrumentalness=1.0, time_signature=100, valence=1.0, album_id=album1.id, album=album1)
    ]
    session.add_all(song_objects)
    session.commit()


def populatePlaylists():
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    user1 = User(email="kaan@kaan.ca", password="1234")
    user2 = User(email="ryan@ryan.ca", password="1234")
    user3 = User(email="paul@paul.ca", password="1234")

    session.add(user1)
    session.add(user2)
    session.add(user3)

    p1 = Playlist(name="Kaan's list", user_id=user1.id, user=user1)
    p2 = Playlist(name="Ryan's list", user_id=user1.id, user=user2)
    p3 = Playlist(name="Paul's list", user_id=user1.id, user=user3)

    session.add(p1)
    session.add(p2)
    session.add(p3)
    session.commit()


def populatePlaylistItems():
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # ryan
    pi1 = PlaylistItem(playlist_id=2, song_id=2)
    pi2 = PlaylistItem(playlist_id=2, song_id=15)
    pi3 = PlaylistItem(playlist_id=2, song_id=30)
    # kaan
    pi4 = PlaylistItem(playlist_id=1, song_id=153)
    pi5 = PlaylistItem(playlist_id=1, song_id=162)
    pi6 = PlaylistItem(playlist_id=1, song_id=171)
    # paul
    pi7 = PlaylistItem(playlist_id=3, song_id=265)
    pi8 = PlaylistItem(playlist_id=3, song_id=301)
    pi9 = PlaylistItem(playlist_id=3, song_id=250)

    session.add(pi1)
    session.add(pi2)
    session.add(pi3)
    session.add(pi4)
    session.add(pi5)
    session.add(pi6)
    session.add(pi7)
    session.add(pi8)
    session.add(pi9)

    session.commit()


# If the script is directly executed, populate data in tables
if __name__ == '__main__':
    # populateDataManually()
    # spotifyAPITest()
    populateDataFromSpotify()
    populatePlaylists()
    populatePlaylistItems()

    print("Database populated successfully")
