import spotipy
import spotipy.util as util
import random
import json
import requests
import asciify
import colorama
from io import BytesIO
from PIL import Image

# Load config
with open('conf.json') as json_file:
    conf = json.load(json_file)

# Windows ANSI color compat
colorama.init()

# Load token
token = util.prompt_for_user_token(username=conf['username'], 
                                    scope='user-library-read user-modify-playback-state', 
                                    client_id=conf['client_id'], 
                                    client_secret=conf['client_secret'], 
                                    redirect_uri='http://localhost/')

if token:
    sp = spotipy.Spotify(auth=token)

    # Fetch playlist range and get a random index
    totalPlaylists = sp.current_user_playlists(1,0)["total"]
    rPlaylistIndex = random.randrange(1, totalPlaylists)

    # Request Playlist information
    randomPlaylist = sp.current_user_playlists(1,rPlaylistIndex)["items"][0]   
    
    # Play playlist if autoplay is enabled
    if 'autoplay' not in conf or conf['autoplay'] == True:
        sp.start_playback(context_uri=randomPlaylist["external_urls"]["spotify"])

    # Draw playlist art if enabled
    if 'draw_art' in conf and conf['draw_art'] == True:
        # Get image data from URL
        playlistId = randomPlaylist["id"]
        playlistImageInfo = sp.playlist_cover_image(playlistId)
        mipImageUrl = playlistImageInfo[0]["url"]
        data = BytesIO(requests.get(mipImageUrl).content)
        img = Image.open(data)

        if 'art_res' in conf:
            artres = conf['art_res']
        else:
            artres = 24

        asciify.do(img, artres)

    # Print status messages
    print("Now playing \033[92m%s\033[0m" % (randomPlaylist["name"]))
    print("URL: \033[94m%s\033[0m" % randomPlaylist["external_urls"]["spotify"])

else:
    print("token failed")

