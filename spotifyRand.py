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
token = util.prompt_for_user_token( scope='user-library-read user-modify-playback-state', 
                                    client_id=conf['client_id'], 
                                    client_secret=conf['client_secret'], 
                                    redirect_uri=conf['redirect_uri'])

if token:
    sp = spotipy.Spotify(auth=token)

    # Fetch album range and get a random index
    totalAlbums = sp.current_user_saved_albums(1,0)["total"]
    rAlbumIndex = random.randrange(1, totalAlbums)

    # debug values
    # rAlbumIndex = 250
    # rAlbumIndex = 252
    # rAlbumIndex = 3
    # rAlbumIndex = 11

    # Request Album information
    randomAlbum = sp.current_user_saved_albums(1,rAlbumIndex)["items"][0]["album"]    
    
    # Play album if autoplay is enabled
    if 'autoplay' not in conf or conf['autoplay'] == True:
        sp.start_playback(context_uri=randomAlbum["external_urls"]["spotify"])

    # Draw album art if enabled
    if 'draw_art' in conf and conf['draw_art'] == True:
        # Get image data from URL
        mipImageUrl = randomAlbum["images"][2]["url"]   # index 2 = 64x64 mipmap level
        data = BytesIO(requests.get(mipImageUrl).content)
        img = Image.open(data)

        if 'art_res' in conf:
            artres = conf['art_res']
        else:
            artres = 24

        asciify.do(img, artres)

    # Print status messages
    print("Now playing \033[92m%s\033[0m by \033[92m%s\033[0m" % (randomAlbum["name"], randomAlbum["artists"][0]["name"]))
    print("URL: \033[94m%s\033[0m" % randomAlbum["external_urls"]["spotify"])

else:
    print("token failed")

