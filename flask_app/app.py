from flask import Flask, request, url_for, session, redirect, render_template, Response
import spotipy
import requests
from spotipy.oauth2 import SpotifyOAuth
import time
import io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import os
import logging
from datetime import datetime
import webbrowser
import random

# have random datasets to select
playlists = ['37i9dQZF1DXcBWIGoYBM5M', '37i9dQZEVXbMDoHDwVN2tF', '37i9dQZF1DX0XUsuxWHRQd', '37i9dQZF1DX10zKzsJ2jva', '37i9dQZF1DWY7IeIP1cdjF', '37i9dQZF1DWXRqgorJj26U', '37i9dQZF1DWWMOmoXKqHTD', '37i9dQZF1DX4o1oenSJRJd', '37i9dQZF1DX4UtSsGT1Sbe', '37i9dQZF1DX76Wlfdnj7AP', '37i9dQZF1DXbTxeAdrVG2l', '37i9dQZF1DX4WYpdgoIcn6', '37i9dQZF1DX3rxVfibe1L0', '37i9dQZF1DX1lVhptIYRda', '37i9dQZF1DWSqmBTGDYngZ', '37i9dQZF1DX186v583rmzp', '37i9dQZF1DX4sWSpwq3LiO', '0vvXsWCC9xrXsKd4FyS8kM', '37i9dQZF1DXdSjVZQzv2tl', '37i9dQZF1DX08mhnhv6g9b', '37i9dQZF1DWY4xHQp97fN6', '37i9dQZF1DXdxcBWuJkbcy', '37i9dQZF1DX4dyzvuaRJ0n', '37i9dQZF1DXdPec7aLTmlC', '37i9dQZF1DX6aTaZa0K6VA', '37i9dQZF1DX7KNKjOK0o75', '37i9dQZF1DX0Yxoavh5qJV', '37i9dQZF1DXaXB8fQg7xif', '37i9dQZF1DX1rVvRgjX59F', '37i9dQZF1DXcF6B6QPhFDv', '37i9dQZF1DX70RN3TfWWJh', '37i9dQZF1DWTJ7xPn4vNaz', '37i9dQZF1DX9wC1KY45plY', '37i9dQZF1DWWQRwui0ExPn', '37i9dQZF1DWZd79rJ6a7lp', '37i9dQZF1DXcZQSjptOQtk', '37i9dQZF1DWTyiBJ6yEqeu', '37i9dQZF1DX6ziVCJnEm59', '37i9dQZF1DWUVpAXiEPK8P', '37i9dQZF1DX4JAvHpjipBk', '37i9dQZF1DWXmlLSKkfdAk', '37i9dQZF1DWUH2AzNQzWua', '37i9dQZF1DWZeKCadgRdKQ', '37i9dQZF1DX4fpCWaHOned', '37i9dQZF1DWXLeA8Omikj7', '37i9dQZF1DX9tPFwDMOaN1', '37i9dQZF1DX0BcQWzuB7ZO', '37i9dQZF1DWSJHnPb1f0X3', '37i9dQZF1DX9XIFQuFvzM4',
             '37i9dQZF1DX3YSRoSdA634', '37i9dQZF1DXcZDD7cfEKhW', '37i9dQZF1DX6VdMW310YC7', '37i9dQZF1DX6xOPeSOGone', '37i9dQZF1DX7F6T2n2fegs', '37i9dQZF1DX4pUKG1kS0Ac', '37i9dQZF1DWWGFQLoP9qlv', '37i9dQZF1DWYBO1MoTDhZI', '37i9dQZF1DWY4lFlS4Pnso', '37i9dQZF1DX5KpP2LN299J', '37i9dQZF1DX6VDO8a6cQME', '37i9dQZF1DWWEJlAGA9gs0', '37i9dQZF1DX843Qf4lrFtZ', '37i9dQZF1DXaMu9xyX1HzK', '37i9dQZF1DX0Uv9tZ47pWo', '37i9dQZF1DXaKIA8E7WcJj', '37i9dQZF1DXaQm3ZVg9Z2X', '37i9dQZF1DX1clOuib1KtQ', '37i9dQZF1DXbSbnqxMTGx9', '37i9dQZF1DX6R7QUWePReA', '37i9dQZF1DWWiDhnQ2IIru', '37i9dQZF1DX3omIq8ziEt6', '37i9dQZF1DXbITWG1ZJKYt', '37i9dQZF1DWUa8ZRTfalHk', '37i9dQZF1DX35oM5SPECmN', '37i9dQZF1DX8SfyqmSFDwe', '37i9dQZF1DXb57FjYWz00c', '37i9dQZF1EQncLwOalG3K7', '37i9dQZF1DX8NTLI2TtZa6', '37i9dQZF1DWVqfgj8NZEp1', '37i9dQZF1DXcRXFNfZr7Tp', '37i9dQZF1DX2TRYkJECvfC', '37i9dQZF1DX6p4TJxzMRDe', '37i9dQZF1DX4eRPd9frC1m', '37i9dQZF1DX7gIoKXt0gmx', '37i9dQZF1DX4jP4eebSWR9', '37i9dQZF1DX889U0CL85jj', '37i9dQZF1DWT1y71ZcMPe5', '37i9dQZF1DWX9VXBLRgDqu', '37i9dQZF1DX5IDTimEWoTd', '37i9dQZF1DX2UgsUIg75Vg', '37i9dQZF1DX9tzt7g58Xlh', '37i9dQZF1DX1spT6G94GFC', '37i9dQZF1DX2Nc3B70tvx0', '37i9dQZF1DXaTIN6XNquoW', '37i9dQZF1DX4olOMiqFeqU', '37i9dQZF1DX6z20IXmBjWI', '37i9dQZF1DX32NsLKyzScr', '37i9dQZF1DX8kP0ioXjxIA', '37i9dQZF1DX6GwdWRQMQpq']

featVals = []

app = Flask(__name__, template_folder='templateFiles',
            static_folder='staticFiles')

logging.basicConfig(level=logging.DEBUG)

app.secret_key = "adjh37g3qwbd8ad"
app.config['SESSION_COCKIE_NAME'] = 'ursession'
TOKEN_INFO = "token_info"


@app.route('/')  # shows the home page on flask
def login():
    # connect to spotify with oauth
    sp_oauth = create_spotify_oauth()
    # get the return link to go to
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)
# id 07fcd214c3184ca6988249ae0a6ac952
# secret dbbd27a235724e4c9f77153379014b4d

# function that gets the access token


@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)  # saving the token
    session[TOKEN_INFO] = token_info
    return redirect(url_for('AnalyseTracks', _external=True))

# function used to get the song data from playlists


@app.route('/AnalyseTracks')
def AnalyseTracks():
    try:
        token_info = get_token()
    except:
        print('user not logged in')
        return redirect("/")

    sp = spotipy.Spotify(auth=token_info['access_token'])
    # sp = spotipy.Spotify(auth=token_info['access_token'])
    all_songs = []
    all_songs_id = []
    all_songs_audio_features = []
    global playlist_id
    playlist_id = (random.choices(playlists, k=1))[0]
    iteration = 0
    while True:
        # items = sp.current_user_saved_tracks(
        #    limit=50, offset=iteration*50)['items']
        items = sp.playlist_tracks(playlist_id=playlist_id, limit=40, offset=iteration*40)[
            'items']  # [0]['track']['id']
        iteration += 1
        all_songs += items
        if (len(items) < 40):  # 50 for current_user_saved_tracks
            break

    number_of_songs = len(all_songs)

    for song in all_songs:  # all_songs
        songid = song['track']['id']
        all_songs_id.append(songid)
        all_songs_audio_features.append(sp.audio_features(songid))

    # get the average values for acousticness, danceability, energy, instrumentalness, valence.
    acousticness = 0
    danceability = 0
    energy = 0
    instrumentalness = 0
    valence = 0
    for features in all_songs_audio_features:
        acousticness += features[0]['acousticness']
        danceability += features[0]['danceability']
        energy += features[0]['energy']
        instrumentalness += features[0]['instrumentalness']
        valence += features[0]['valence']
    acousticness = acousticness/number_of_songs
    danceability = danceability/number_of_songs
    energy = energy/number_of_songs
    instrumentalness = instrumentalness/number_of_songs
    valence = valence/number_of_songs

    featVals = [acousticness, danceability, energy, instrumentalness, valence]

    output = "acousticness: " + str(acousticness) + " " + "danceability: " + str(danceability) + " " + \
        "energy: " + str(energy) + " " + "instrumentalness: " + \
        str(instrumentalness) + " " + "valence: " + str(valence)

    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    feat = ['acousticness', 'danceability',
            'energy', 'instrumentalness', 'valence']
    # example: [0.23272203816631132, 0.6673049040511725, 0.6631820895522385, 0.0836214930063965, 0.46053283582089544]
    global val  # global so that it is accessible from a different function
    val = [round(acousticness, 2),  round(danceability, 2), round(
        energy, 2), round(instrumentalness, 2), round(valence, 2)]

    # there is an option to output the a bar graph
    ax.bar(feat, val)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    # output the graph
    # return Response(output.getvalue(), mimetype='image/png')

    log_data()

    # return the data for strings
    return str(number_of_songs) + str(val)  # only returns strings

# function to get access token


def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise 'exception'
    now = int(time.time())

    is_expired = token_info['expires_at'] - now < 60

    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info


# function creates the spotify oauth
def create_spotify_oauth():
    return SpotifyOAuth(
        client_id="07fcd214c3184ca6988249ae0a6ac952",
        client_secret="dbbd27a235724e4c9f77153379014b4d",
        # redirect to /redirect
        redirect_uri=url_for('redirectPage', _external=True),
        scope="user-library-read"
    )

# logs data to a text file


def log_data():
    filename = r"M:\UAL\SpotifyApp\flask_app\data.txt"
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S:%D")
    data = "Program ran at: " + current_time

    if os.path.isfile(filename):
        with open(filename, "a") as f:
            f.write('\n' + data)
            f.write(str('\n' + "Playlist ID: " + str(playlist_id)))
            f.write(str('\n' + "Features: " + str(val)))
    else:
        with open(filename, "a") as f:
            f.write('\n' + data)
            f.write(str('\n' + "Playlist ID: " + str(playlist_id)))
            f.write(str('\n' + "Features: " + str(val)))


def main():
    # opens the server to run the flask application
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        webbrowser.open_new('http://127.0.0.1:5000/')

    app.run()


# runs the main function
if __name__ == '__main__':
    main()
