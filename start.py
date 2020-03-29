from flask import Flask, render_template
from flask import request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, Album, Artist, Playlist, Song, User

app = Flask(__name__)

engine = create_engine('sqlite:///spotify.db',
                       connect_args={'check_same_thread': False}, echo=True)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/', methods=['GET'])
def index():
    albums = session.query(Album).all()
    return render_template('index.html', title='Albums', albums=albums)

@app.route('/albums/<int:album_id>/', methods=['GET'])
def showSong(album_id):
    albumName = session.query(Album).filter_by(id=album_id).one()
    songs = session.query(Song).filter_by(album_id=album_id)
    return render_template(
        'songs.html',
        title='Songs',
        songs=songs,
        albumName=albumName)

@app.route('/artists/<int:artist_id>/', methods=['GET'])
def showAlbums(artist_id):
    artistName = session.query(Artist).filter_by(id=artist_id).one()
    albums = session.query(Album).filter_by(artist_id=artist_id)
    return render_template(
        'albums.html',
        title='Albums',
        albums=albums,
        artistName=artistName)

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5001)
