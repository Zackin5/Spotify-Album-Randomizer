# Spotify-Album-Randomizer
A Python script to randomly play a saved album in your Spotify library

# Required libraries
spotipy, colorama, pillow, numpy

# Configuration
Execution requires an conf.json file to be present in the root directory with the following contents:

```
{
    "username": YOUR_SPOTIFY_USERNAME_HERE,
    "client_id": YOUR_SPOTIFY_API_CLIENT_ID,
    "client_secret": YOUR_SPOTIFY_API_CLIENT_SECRET,
    "redirect_uri": "http://localhost/"
}
```

Other options available are:
- `autoplay`: enable\disable album autoplay
- `draw_art`: enable\disable ascii album artwork
- `art_res`: character resolution for the ascii album artwork
