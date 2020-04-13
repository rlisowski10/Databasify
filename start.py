from flask import Flask, render_template
from flask import request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from model import Base, Album, Artist, Playlist, Song, User, PlaylistItem
import json
app = Flask(__name__)

engine = create_engine('sqlite:///spotify.db',
                       connect_args={'check_same_thread': False}, echo=True)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# welcome page
@app.route('/', methods=['GET'])
def index():
    playlists = session.query(Playlist).all()
    return render_template('index.html', title='Playlists', playlists=playlists)


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
    result = (session.query(PlaylistItem, Playlist, Song)
              .filter(PlaylistItem.song_id == Song.id)
              .filter(PlaylistItem.playlist_id == Playlist.id)
              .filter(PlaylistItem.playlist_id == playlist_id)
              ).all()

    playlists = session.query(Playlist).all()
    playlistName = session.query(Playlist).filter_by(id=playlist_id).one()
    return render_template('playlistSongs.html', title='Songs', playlistName=playlistName, songs=result, playlists=playlists)


@app.route('/playlist/new/', methods=['GET', 'POST'])
def newPlaylist():
    if request.method == 'POST':
        user_id_form = session.query(User).filter_by(
            email=request.form['user_email']).one()
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

# DELETE playlist
@app.route('/playlist/<int:playlist_id>/delete/', methods=['GET', 'POST'])
def deletePlaylist(playlist_id):
    playlists = session.query(Playlist).all()
    deletePlaylist = session.query(Playlist).filter_by(id=playlist_id).one()

    deleteSongs = session.query(PlaylistItem).filter_by(
        playlist_id=playlist_id).all()

    if request.method == 'POST':
        for row in deleteSongs:
            session.delete(row)
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
        orderByParam = request.form['orderByParam'].lower().replace(' ', '_')
        orderByOrder = request.form['orderByOrder']

        # Gets the artist attribute based on the attribute string from the UI.
        if orderByParam == '':
            filterAttribute = getattr(Artist, filterAttribute)
            if filterOperator == '>':
                artists = session.query(Artist).filter(
                    filterAttribute > userText).all()
            elif filterOperator == '<':
                artists = session.query(Artist).filter(
                    filterAttribute < userText).all()
            else:
                artists = session.query(Artist).filter(
                    filterAttribute == userText).all()
        elif orderByOrder == 'ascending':
            filterAttribute = getattr(Artist, filterAttribute)
            orderByParam = getattr(Artist, orderByParam)
            if filterOperator == '>':
                artists = session.query(Artist).filter(
                    filterAttribute > userText).order_by(orderByParam).all()
            elif filterOperator == '<':
                artists = session.query(Artist).filter(
                    filterAttribute < userText).order_by(orderByParam).all()
            else:
                artists = session.query(Artist).filter(
                    filterAttribute == userText).order_by(orderByParam).all()
        else:
            filterAttribute = getattr(Artist, filterAttribute)
            orderByParam = getattr(Artist, orderByParam)
            if filterOperator == '>':
                artists = session.query(Artist).filter(
                    filterAttribute > userText).order_by(desc(orderByParam)).all()
            elif filterOperator == '<':
                artists = session.query(Artist).filter(
                    filterAttribute < userText).order_by(desc(orderByParam)).all()
            else:
                artists = session.query(Artist).filter(
                    filterAttribute == userText).order_by(desc(orderByParam)).all()

        songCounts = {}
        for artist in artists:
            #songCount = Song.query.filter_by(Song.album.artist.id == artist.id ).count()
            result = (session.query(Song, Album, Artist)
              .filter(Artist.id == Album.artist_id)
              .filter(Song.album_id == Album.id)
              .filter(Artist.id== artist.id)
              ).all()
            songCount = len(result)

            songCounts[artist.id] = songCount

        return render_template(
            'searchArtist.html',
            title='Search Artist',
            playlists=playlists, artists=artists, songCounts=songCounts)

    else:
        artists = session.query(Artist).all()
        songCounts = {}
        for artist in artists:
            #songCount = Song.query.filter_by(Song.album.artist.id == artist.id ).count()
            result = (session.query(Song, Album, Artist)
              .filter(Artist.id == Album.artist_id)
              .filter(Song.album_id == Album.id)
              .filter(Artist.id== artist.id)
              ).all()
            songCount = len(result)

            songCounts[artist.id] = songCount

        return render_template(
        'searchArtist.html',
        title='Search Artist',
        playlists=playlists, artists=artists, songCounts=songCounts)



@app.route('/album', methods=['GET', 'POST'])
def searchAlbum():
    albums = session.query(Album).all()
    playlists = session.query(Playlist).all()

    if request.method == 'POST':
        # Get all user-provided values from the UI.
        filterAttribute = request.form['attribute'].lower().replace(' ', '_')
        filterOperator = request.form['operator']
        userText = request.form['usrText']
        orderByParam = request.form['orderByParam'].lower().replace(' ', '_')
        orderByOrder = request.form['orderByOrder']

        # Gets the album attribute based on the attribute string from the UI.
        if orderByParam == '':
            if filterAttribute == 'artist':
                albums = session.query(Album).join(
                    Artist).filter(Artist.name == userText).all()
            else:
                filterAttribute = getattr(Album, filterAttribute)
                if filterOperator == '>':
                    albums = session.query(Album).filter(
                        filterAttribute > userText).all()
                elif filterOperator == '<':
                    albums = session.query(Album).filter(
                        filterAttribute < userText).all()
                else:
                    albums = session.query(Album).filter(
                        filterAttribute == userText).all()
        elif orderByOrder == 'ascending':
            orderByParam = getattr(Album, orderByParam)
            if filterAttribute == 'artist':
                albums = session.query(Album).join(Artist).filter(
                    Artist.name == userText).order_by(orderByParam).all()
            else:
                filterAttribute = getattr(Album, filterAttribute)
                if filterOperator == '>':
                    albums = session.query(Album).filter(
                        filterAttribute > userText).order_by(orderByParam).all()
                elif filterOperator == '<':
                    albums = session.query(Album).filter(
                        filterAttribute < userText).order_by(orderByParam).all()
                else:
                    albums = session.query(Album).filter(
                        filterAttribute == userText).order_by(orderByParam).all()
        else:
            orderByParam = getattr(Album, orderByParam)
            if filterAttribute == 'artist':
                albums = session.query(Album).join(Artist).filter(
                    Artist.name == userText).order_by(desc(orderByParam)).all()
            else:
                filterAttribute = getattr(Album, filterAttribute)
                if filterOperator == '>':
                    albums = session.query(Album).filter(
                        filterAttribute > userText).order_by(desc(orderByParam)).all()
                elif filterOperator == '<':
                    albums = session.query(Album).filter(
                        filterAttribute < userText).order_by(desc(orderByParam)).all()
                else:
                    albums = session.query(Album).filter(
                        filterAttribute == userText).order_by(desc(orderByParam)).all()

    return render_template(
        'searchAlbum.html',
        title='Search Albums',
        playlists=playlists, albums=albums)


@app.route('/playlist/<int:playlist_id>/new/searchsong/<song_id_list>', methods=['GET', 'POST'])
def addSongsToPlaylist(playlist_id, song_id_list):
    playlists = session.query(Playlist).all()
    playlistName = session.query(Playlist).filter_by(id=playlist_id).one()

    if request.method == 'POST':
        songidToBeAdded = request.form.getlist('mycheckbox')
        for s in songidToBeAdded:
            pitem = PlaylistItem(playlist_id=playlist_id, song_id=s)
            session.add(pitem)
        session.commit()

        flash("Songs added to the playlist")
        return redirect(url_for('showPlayListsSongs', playlist_id=playlistName.id))
    else:
        song_id_list = song_id_list.replace(
            "[", "").replace("]", "").replace(" ", "")
        song_id_list = song_id_list.split(",")

        songs = []
        for song_id in song_id_list:
            result = session.query(Song).filter(Song.id == song_id).all()
            for song in result:
                songs.append(song)

        return render_template(
            'addSongToPlaylist.html',
            title='Add songs to playlist',
            playlistName=playlistName, playlists=playlists, songs=songs)


@app.route('/playlist/<int:playlist_id>/new', methods=['GET', 'POST'])
def searchSong(playlist_id):
    songs = None
    playlists = session.query(Playlist).all()
    playlistName = session.query(Playlist).filter_by(id=playlist_id).one()

    if request.method == 'POST':
        # Get all user-provided values from the UI.
        filterAttribute = request.form['attribute'].lower().replace(' ', '_')
        filterOperator = request.form['operator']
        userText = request.form['usrText']
        orderByParam = request.form['orderByParam'].lower().replace(' ', '_')
        orderByOrder = request.form['orderByOrder']

        # Gets the song attribute based on the attribute string from the UI.
        if orderByParam == '':
            if filterAttribute == 'artist':
                songs = session.query(Song).join(Album).join(
                    Artist).filter(Artist.name == userText).all()
            elif filterAttribute == 'album':
                songs = session.query(Song).join(
                    Album).filter(Album.name == userText).all()
            else:
                filterAttribute = getattr(Song, filterAttribute)
                if filterOperator == '>':
                    songs = session.query(Song).filter(
                        filterAttribute > userText).all()
                elif filterOperator == '<':
                    songs = session.query(Song).filter(
                        filterAttribute < userText).all()
                else:
                    songs = session.query(Song).filter(
                        filterAttribute == userText).all()
        elif orderByOrder == 'ascending':
            orderByParam = getattr(Song, orderByParam)
            if filterAttribute == 'artist':
                songs = session.query(Song).join(Album).join(Artist).filter(
                    Artist.name == userText).order_by(orderByParam).all()
            elif filterAttribute == 'album':
                songs = session.query(Song).join(Album).filter(
                    Album.name == userText).order_by(orderByParam).all()
            else:
                filterAttribute = getattr(Song, filterAttribute)
                if filterOperator == '>':
                    songs = session.query(Song).filter(
                        filterAttribute > userText).order_by(orderByParam).all()
                elif filterOperator == '<':
                    songs = session.query(Song).filter(
                        filterAttribute < userText).order_by(orderByParam).all()
                else:
                    songs = session.query(Song).filter(
                        filterAttribute == userText).order_by(orderByParam).all()
        else:
            orderByParam = getattr(Song, orderByParam)
            if filterAttribute == 'artist':
                songs = session.query(Song).join(Album).join(Artist).filter(
                    Artist.name == userText).order_by(desc(orderByParam)).all()
            elif filterAttribute == 'album':
                songs = session.query(Song).join(Album).filter(
                    Album.name == userText).order_by(desc(orderByParam)).all()
            else:
                filterAttribute = getattr(Song, filterAttribute)
                if filterOperator == '>':
                    songs = session.query(Song).filter(
                        filterAttribute > userText).order_by(desc(orderByParam)).all()
                elif filterOperator == '<':
                    songs = session.query(Song).filter(
                        filterAttribute < userText).order_by(desc(orderByParam)).all()
                else:
                    songs = session.query(Song).filter(
                        filterAttribute == userText).order_by(desc(orderByParam)).all()

        song_id_list = []
        for s in songs:
            song_id_list.append(s.id)

        return redirect(url_for('addSongsToPlaylist', playlist_id=playlist_id, song_id_list=song_id_list))
    else:
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
                    .filter(PlaylistItem.playlist_id == playlist_id)
                    ).all()

        for row in songURIS:
            strOut = strOut + row.Song.uri + ","
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


@app.route('/ta', methods=['GET', 'POST'])
def ta():
    if request.method == 'POST':
        playlists = session.query(Playlist).all()
        #songs = session.query(Song).filter_by(album_id=1)
        #with engine.connect() as con:

        if request.form.get("name"):
            taQuery = request.form.get("name")
            results = {}

            qsongs = session.execute(taQuery)
            # for row in songs:
            #     #row = (8, 'spotify:track:5IXTT9RvcVupmzLTFqIInj', 8, 'New York', 56, 154960, 0.373, 1, 137.866, 0.449, 1.26e-05, 4, 0.327, 1)
            #     results[row[0]] = [row[1], row[2], row[3],row[4]] 
            

            song_id_list = []
            songs = []

            for s in qsongs:
                song_id_list.append(s[0])
            
            for song_id in song_id_list:
                result = session.query(Song).filter(Song.id == song_id).all()
                for song in result:
                    songs.append(song)

            return render_template(
                'taresults.html',
                title='query results',
                playlists=playlists, songs=songs)
    else:
        playlists = session.query(Playlist).all()
        return render_template(
            'ta.html',
            title='query options',
            playlists=playlists)


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'SECRET KEY'
    app.run(host='127.0.0.1', port=5001)
