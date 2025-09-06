#config.py

import os
# Spotify API Credentials
CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID', '11127bd4602e428db0820da88c44c6a9')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET', '113c0a85a83b448fb1ed374885048b57')

# The redirect URI as registered in your Spotify Developer Dashboard
REDIRECT_URI = os.environ.get('SPOTIFY_REDIRECT_URI', 'http://localhost:5000/callback') # FOR DEVELOPMENT ONLY.

# Spotify API URLs
AUTH_BASE_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1'

# Scopes required for this application (reading and modifying playlists)
SCOPES = 'playlist-read-private playlist-modify-public playlist-modify-private'

# ---------- Database Configuration ----------
DB_HOST = os.environ.get("DB_HOST", "db.cs.dal.ca")
DB_USER = os.environ.get("DB_USER", "nbeaulieu")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "tGdHxxEqL5pn9YwkHCea9eV9K")
DB_NAME = os.environ.get("DB_NAME", "nbeaulieu")