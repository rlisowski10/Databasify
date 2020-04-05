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

#welcome page
@app.route('/', methods=['GET'])
def index():
    playlists = session.query(Playlist).all()
    return render_template('index.html', title='Playlists', playlists=playlists)

@app.route('/artist', methods=['GET'])
def showArtists():
    artists = session.query(Artist).all()
    playlists = session.query(Playlist).all()
    return render_template('artists.html', title='Artists', artists=artists, playlists=playlists)

@app.route('/album', methods=['GET'])
def showAlbums():
    albums = session.query(Album).all()
    playlists = session.query(Playlist).all()
    return render_template('albums.html', title='Albums', albums=albums, playlists=playlists)


@app.route('/album/<int:album_id>/', methods=['GET'])
def showSongs(album_id):
    albumName = session.query(Album).filter_by(id=album_id).one()
    songs = session.query(Song).filter_by(album_id=album_id)
    playlists = session.query(Playlist).all()
    return render_template(
        'albumSongs.html',
        title='Songs',
        songs=songs,
        albumName=albumName, playlists=playlists)

@app.route('/artist/<int:artist_id>/', methods=['GET'])
def showAlbum(artist_id):
    artistName = session.query(Artist).filter_by(id=artist_id).one()
    albums = session.query(Album).filter_by(artist_id=artist_id)
    playlists = session.query(Playlist).all()
    return render_template(
        'artistAlbums.html',
        title='Albums',
        albums=albums,
        artistName=artistName, playlists=playlists)

@app.route('/playlist/<int:playlist_id>/', methods=['GET'])
def showPlayListsSongs(playlist_id):
    #songs = session.query(Playlist).join(PlaylistItem).filter(id == playlist_id)
    playlists = session.query(Playlist).all()
    playlistName = session.query(Playlist).filter_by(id=playlist_id).one()
    return render_template('playlistSongs.html', title='Songs', playlistName=playlistName, playlists=playlists)

@app.route('/playlist/<int:playlist_id>/new/', methods=['GET', 'POST'])
def addSongToPlaylist(playlist_id):
    if request.method == 'POST':
        #newSong = assign the song object
        #session.add(newSong)
        #session.commit()
        flash("New song added to the playlist!")
        return redirect(url_for('index'))
    else:
        playlists = session.query(Playlist).all()
        playlistName = session.query(Playlist).filter_by(id=playlist_id).one()
        return render_template(
            'addSongToPlaylist.html',
            title='Playlists',
            playlists=playlists, playlistName=playlistName)

@app.route('/playlist/new/', methods=['GET', 'POST'])
def newPlaylist():
    if request.method == 'POST':
        user_id_form = session.query(User).filter_by(email=request.form['user_email']).one()
        print("HELOOOO", user_id_form.id)
        newPlaylistName = Playlist(
            name=request.form['name'],
            user_id=user_id_form.id)
        session.add(newPlaylistName)
        session.commit()
        flash("New playlist was created!")
        return redirect(url_for('index'))
    else:
        playlists = session.query(Playlist).all()
        users = session.query(User).all()
        return render_template(
            'createNewPlaylist.html',
            title='Create a playlist',
            playlists=playlists, users=users)

if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'SECRET KEY'
    app.run(host='127.0.0.1', port=5001)
