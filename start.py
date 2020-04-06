from flask import Flask, render_template
from flask import request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, Album, Artist, Playlist, Song, User, PlaylistItem
import json
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

# @app.route('/artist', methods=['GET'])
# def showArtists():
#     artists = session.query(Artist).all()
#     playlists = session.query(Playlist).all()
#     return render_template('searchArtist.html', title='Artists', artists=artists, playlists=playlists)

# @app.route('/album', methods=['GET'])
# def showAlbums():
#     albums = session.query(Album).all()
#     playlists = session.query(Playlist).all()
#     return render_template('searchAlbum.html', title='Albums', albums=albums, playlists=playlists)


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
    result = (session.query(PlaylistItem, Playlist, Song)
        .filter(PlaylistItem.song_id == Song.id)
        .filter(PlaylistItem.playlist_id == Playlist.id)
        .filter(PlaylistItem.playlist_id==playlist_id)
        # .order_by(Group.number)
        ).all()
    # for row in result:
    #     print(row.Song.name)

    playlists = session.query(Playlist).all()
    playlistName = session.query(Playlist).filter_by(id=playlist_id).one()
    return render_template('playlistSongs.html', title='Songs', playlistName=playlistName, songs=result, playlists=playlists)

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
            'searchSong.html',
            title='Playlists',
            playlists=playlists, playlistName=playlistName)

@app.route('/playlist/new/', methods=['GET', 'POST'])
def newPlaylist():
    if request.method == 'POST':
        user_id_form = session.query(User).filter_by(email=request.form['user_email']).one()
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

#DELETE playlist
@app.route('/playlist/<int:playlist_id>/delete/', methods=['GET', 'POST'])
def deletePlaylist(playlist_id):
    playlists = session.query(Playlist).all()
    deletePlaylist = session.query(Playlist).filter_by(id=playlist_id).one()

    deleteSongs = session.query(PlaylistItem).filter_by(playlist_id=playlist_id).all()

    if request.method == 'POST':
        for row in deleteSongs:
            session.delete(row)
        #session.delete(deletePlaylist)
        session.delete(deletePlaylist)
        session.commit()
        flash("Playlist {} is deleted".format(deletePlaylist.name))
        return redirect(url_for('index', playlist_id=playlist_id))
    else:
        playlistName = session.query(Playlist).filter_by(id=playlist_id).one()
        return render_template(
            'deletePlaylist.html',
            playlist_id=playlist_id,
            playlistName=playlistName,
            deletePlaylist=deletePlaylist,
            playlists=playlists)

@app.route('/artist', methods=['GET', 'POST'])
def searchArtist():
    artists = session.query(Artist).all()
    playlists = session.query(Playlist).all()

    if request.method == 'POST':
        # Get all user-provided values from the UI.
        filterAttribute = request.form['attribute'].lower().replace(' ', '_')
        filterOperator = request.form['operator']
        userText = request.form['usrText']

        # Gets the artist attribute based on the attribute string from the UI.
        filterAttribute = getattr(Artist, filterAttribute)
        if filterOperator == '>':
            artists = session.query(Artist).filter(filterAttribute > userText).all()
        elif filterOperator == '<':
            artists = session.query(Artist).filter(filterAttribute < userText).all()
        else:
            artists = session.query(Artist).filter(filterAttribute == userText).all()
    
    return render_template(
        'searchArtist.html',
        title='Search Artist',
        playlists=playlists, artists=artists)

@app.route('/album', methods=['GET', 'POST'])
def searchAlbum():
    albums = session.query(Album).all()
    playlists = session.query(Playlist).all()

    if request.method == 'POST':
        # Get all user-provided values from the UI.
        filterAttribute = request.form['attribute'].lower().replace(' ', '_')
        filterOperator = request.form['operator']
        userText = request.form['usrText']

        # Gets the album attribute based on the attribute string from the UI.
        filterAttribute = getattr(Album, filterAttribute)
        if filterOperator == '>':
            albums = session.query(Album).filter(filterAttribute > userText).all()
        elif filterOperator == '<':
            albums = session.query(Album).filter(filterAttribute < userText).all()
        else:
            albums = session.query(Album).filter(filterAttribute == userText).all()


    return render_template(
        'searchAlbum.html',
        title='Search Albums',
        playlists=playlists, albums=albums)

@app.route('/playlist/<int:playlist_id>/new/searchsong', methods=['GET', 'POST'])
def searchSong(playlist_id):
    songs = None
    if request.method == 'POST':
        # Get all user-provided values from the UI.
        filterAttribute = request.form['attribute'].lower().replace(' ', '_')
        filterOperator = request.form['operator']
        userText = request.form['usrText']

        # Gets the song attribute based on the attribute string from the UI.
        # if filterAttribute == 'artist':
        #     songs = session.query(Song).filter(Song.album == userText).all()
        # else:
        filterAttribute = getattr(Song, filterAttribute)
        if filterOperator == '>':
            songs = session.query(Song).filter(filterAttribute > userText).all()
        elif filterOperator == '<':
            songs = session.query(Song).filter(filterAttribute < userText).all()
        else:
            songs = session.query(Song).filter(filterAttribute == userText).all()

    playlists = session.query(Playlist).all()
    playlistName = session.query(Playlist).filter_by(id=playlist_id).one()

    return render_template( 
        'searchSong.html',
        title='Search Songs',
        playlists=playlists, playlistName=playlistName, songs=songs)

# xport playlist
@app.route('/playlist/<int:playlist_id>/export/', methods=['GET', 'POST'])
def exportPlaylist(playlist_id):
    if request.method == 'POST':
        return "This page will create a playlist on Spotify for playlist id: %s" % playlist_id
    else:
        uris = []
        strOut = ""
        songURIS = (session.query(PlaylistItem, Playlist, Song)
        .filter(PlaylistItem.song_id == Song.id)
        .filter(PlaylistItem.playlist_id == Playlist.id)
        .filter(PlaylistItem.playlist_id==playlist_id)
        ).all()

        for row in songURIS:
            strOut = strOut + row.Song.uri + ","
            #print(row.Song.uri)
            uris.append(row.Song.uri)
        # USE uris LIST VARIABLE TO PASS TO SPOTIFY
        return "This page will create a playlist on Spotify with these uris: %s" % strOut

# Route for UPDATE playlist
@app.route('/playlist/<int:playlist_id>/edit/', methods=['GET', 'POST'])
def editPlaylist(playlist_id):
    playlists = session.query(Playlist).all()
    playlistName = session.query(Playlist).filter_by(id=playlist_id).one()

    editedPlaylist = session.query(Playlist).filter_by(id=playlist_id).one()

    if request.method == 'POST':
        if request.form['name']:
            editedPlaylist.name = request.form['name']
        session.commit()
        flash("Playlist has been updated!")
        return redirect(url_for('showPlayListsSongs', playlists=playlists, playlist_id=playlistName.id))
    else:
        playlists = session.query(Playlist).all()
        playlistName = session.query(Playlist).filter_by(id=playlist_id).one()

        return render_template(
            'editPlaylist.html',
            playlist_id=playlist_id,
            playlists=playlists,
            editedPlaylist=editedPlaylist,
            playlistName=playlistName)

# JSON API endpoint for getting all albums
@app.route('/album/JSON')
def albumsJSON():
    results = session.query(Album).all()
    return jsonify(Albums=[
        result.serialize for result in results]
        )

if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'SECRET KEY'
    app.run(host='127.0.0.1', port=5001)
