#!/usr/bin/env python
# app.py

import os
import csv
import json
import requests
from flask import Flask, redirect, request, session, jsonify
from urllib.parse import urlencode
import logging
from flask_cors import CORS
import config
import math
from db import UserAuth

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = os.urandom(24)  # FOR DEVELOPMENT ONLY. In production, use a fixed secure secret key.

# Define file paths
ACCOUNTS_FILE = os.path.join(os.path.dirname(__file__), "accounts.json")
CSV_FILE = os.path.join(os.path.dirname(__file__), "../data", "track_data.csv")


##############################
# Helper Functions
##############################
## JSON Development Helper Functions
# def load_accounts():
#     if os.path.exists(ACCOUNTS_FILE):
#         with open(ACCOUNTS_FILE, "r") as f:
#             try:
#                 accounts = json.load(f)
#                 return accounts
#             except json.JSONDecodeError:
#                 return []
#     return []

# def save_accounts(accounts):
#     with open(ACCOUNTS_FILE, "w") as f:
#         json.dump(accounts, f)

def get_playlist_duration(playlist_id, headers):
    url = f"{config.API_BASE_URL}/playlists/{playlist_id}/tracks?limit=100"
    total_duration = 0
    while url:
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            break
        data = r.json()
        for item in data.get("items", []):
            track = item.get("track")
            if track and track.get("duration_ms"):
                total_duration += track.get("duration_ms")
        url = data.get("next")
    return total_duration

##############################
# Spotify OAuth Endpoints
##############################

@app.route('/auth')
def auth():
    # Build query parameters required by Spotify
    query_params = {
        "client_id": config.CLIENT_ID,
        "response_type": "code",
        "redirect_uri": config.REDIRECT_URI,
        "scope": config.SCOPES
    }
    # Construct the Spotify authorization URL
    auth_url = config.AUTH_BASE_URL + "?" + urlencode(query_params)
    return redirect(auth_url)

@app.route('/callback')
def callback():
    error = request.args.get('error')
    if error:
        return jsonify({"error": error})
    code = request.args.get('code')
    if not code:
        return jsonify({"error": "No authorization code provided."})
    
    # Exchange the authorization code for an access token and refresh token
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": config.REDIRECT_URI,
        "client_id": config.CLIENT_ID,
        "client_secret": config.CLIENT_SECRET
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    token_resp = requests.post(config.TOKEN_URL, data=payload, headers=headers)
    if token_resp.status_code != 200:
        return jsonify({"error": "Token exchange failed", "details": token_resp.json()})
    token_info = token_resp.json()
    session['access_token'] = token_info.get('access_token')
    session['refresh_token'] = token_info.get('refresh_token')
    # Redirect user to the frontend Create Run page
    return redirect("http://localhost:3000/create-run")

##############################
# Account Management Endpoints
##############################

# @app.route('/create-account', methods=["POST"])
# def create_account():
#     data = request.get_json()
#     email = data.get("email")
#     password = data.get("password")
#     if not email or not password:
#         return jsonify({"success": False, "message": "Email and password required."})
#     accounts = load_accounts()
#     if any(acc.get("email") == email for acc in accounts):
#         return jsonify({"success": False, "message": "Account already exists."})
#     accounts.append({"email": email, "password": password})
#     save_accounts(accounts)
#     return jsonify({"success": True, "message": "Account Created"})

# @app.route('/login', methods=["POST"])
# def login_endpoint():
#     data = request.get_json()
#     email = data.get("email")
#     password = data.get("password")
#     accounts = load_accounts()
#     for acc in accounts:
#         if acc.get("email") == email and acc.get("password") == password:
#             return jsonify({"success": True})
#     return jsonify({"success": False, "message": "Invalid credentials."})

@app.route('/create-account', methods=["POST"])
def create_account():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"success": False, "message": "Email and password required."})
    
    # Use the database to register the user
    user_auth = UserAuth()
    success, message = user_auth.register_user(email, password)
    user_auth.close()
    return jsonify({"success": success, "message": message})

@app.route('/login', methods=["POST"])
def login_endpoint():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"success": False, "message": "Email and password required."})
    
    # Use the database to authenticate the user
    user_auth = UserAuth()
    success, message = user_auth.login_user(email, password)
    user_auth.close()
    return jsonify({"success": success, "message": message})

##############################
# Playlists Endpoint
##############################

@app.route('/playlists', methods=["GET"])
def playlists():
    access_token = session.get("access_token")
    if not access_token:
        return jsonify({"error": "User not authenticated."}), 401
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(config.API_BASE_URL + "/me/playlists", headers=headers)
    if resp.status_code != 200:
        return jsonify({"error": "Failed to fetch playlists", "details": resp.json()}), 400
    data = resp.json()
    playlists_list = []
    for item in data.get("items", []):
        playlist_id = item.get("id")
        total_tracks = item.get("tracks", {}).get("total", 0)
        duration_ms = 0
        if playlist_id:
            duration_ms = get_playlist_duration(playlist_id, headers)
        playlists_list.append({
            "id": playlist_id,
            "name": item.get("name"),
            "images": item.get("images"),
            "total_tracks": total_tracks,
            "duration_ms": duration_ms
        })
    return jsonify({"playlists": playlists_list})

##############################
# Generate Playlist Endpoint
##############################

@app.route('/generate-playlist', methods=["POST"])
def generate_playlist():
    access_token = session.get("access_token")
    if not access_token:
        return jsonify({"success": False, "message": "User not authenticated."}), 401

    data = request.get_json()
    playlist_title = data.get("playlistTitle")
    try:
        run_distance = float(data.get("runDistance"))
        run_time = float(data.get("runTime"))
        height = float(data.get("height"))
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Invalid numerical input."}), 400
    sex = data.get("sex", "").lower()
    selected_playlists = data.get("selectedPlaylists", [])
    if not playlist_title or not run_distance or not run_time or not height or not sex or not selected_playlists:
        return jsonify({"success": False, "message": "Missing required fields."}), 400

    # Calculate desired cadence.
    # Running speed (v) in m/min
    v = run_distance / run_time
    # Step length multiplier based on sex
    if sex == "male":
        c = 0.70
    elif sex == "female":
        c = 0.65
    else:
        c = 0.675  # default for unspecified/other
    desired_cadence = v / (c * height)
    app.logger.debug(f"Calculated desired cadence: {desired_cadence}")

    # Fetch tracks from each selected Spotify playlist (include duration_ms).
    headers = {"Authorization": f"Bearer {access_token}"}
    combined_tracks = []
    for playlist in selected_playlists:
        playlist_id = playlist.get("id")
        if not playlist_id:
            continue
        tracks_url = f"{config.API_BASE_URL}/playlists/{playlist_id}/tracks"
        resp = requests.get(tracks_url, headers=headers)
        if resp.status_code != 200:
            app.logger.error("Failed to fetch tracks for playlist %s: %s", playlist_id, resp.json())
            continue
        tracks_data = resp.json()
        for item in tracks_data.get("items", []):
            track = item.get("track")
            if track and track.get("id"):
                track_info = {
                    "id": track.get("id"),
                    "title": track.get("name"),
                    "artist": ", ".join([artist.get("name") for artist in track.get("artists", [])]),
                    "uri": track.get("uri"),
                    "duration_ms": track.get("duration_ms"),
                    "image": (track.get("album", {}).get("images", [{}])[0].get("url")
                            if track.get("album") and track.get("album").get("images") else "https://via.placeholder.com/120")
                }
                combined_tracks.append(track_info)
    if not combined_tracks:
        return jsonify({"success": False, "message": "No tracks found in selected playlists."}), 400

    # Read the CSV file to build a mapping of track id to tempo (BPM).
    tempo_map = {}
    try:
        with open(CSV_FILE, newline='', encoding='utf-8', errors='replace') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                tid = row.get('id')
                if tid:
                    try:
                        tempo_map[tid] = float(row.get('tempo', 0))
                    except (ValueError, TypeError):
                        tempo_map[tid] = 0
    except Exception as e:
        app.logger.error("Failed to read CSV file: %s", e)
        return jsonify({"success": False, "message": "Internal error reading track data."}), 500

    # Add tempo (BPM) to each track and filter for valid tempo values.
    tracks_with_tempo = []
    for track in combined_tracks:
        tempo = tempo_map.get(track["id"], 0)
        if tempo > 0:
            track["tempo"] = tempo
            tracks_with_tempo.append(track)
    if not tracks_with_tempo:
        return jsonify({"success": False, "message": "No tracks with tempo data found."}), 400

    # Sort tracks by tempo (ascending order).
    sorted_tracks = sorted(tracks_with_tempo, key=lambda x: x["tempo"])

    # --- Song Selection Algorithm Based on Cadence ---
    # Find the seed song with tempo closest to desired_cadence.
    seed_index = 0
    min_diff = float('inf')
    for i, t in enumerate(sorted_tracks):
        diff = abs(t["tempo"] - desired_cadence)
        if diff < min_diff:
            min_diff = diff
            seed_index = i

    # Initialize selection.
    selected_tracks = [sorted_tracks[seed_index]]
    total_duration_ms = sorted_tracks[seed_index].get("duration_ms", 0)
    sum_tempos = sorted_tracks[seed_index]["tempo"]

    # Initialize two pointers for lower and higher relative to seed.
    lower_ptr = seed_index - 1
    higher_ptr = seed_index + 1
    required_duration_ms = run_time * 60000  # convert minutes to milliseconds

    # Iteratively add songs based on current average tempo.
    while total_duration_ms < required_duration_ms and (lower_ptr >= 0 or higher_ptr < len(sorted_tracks)):
        current_avg = sum_tempos / len(selected_tracks)
        candidate = None

        if current_avg <= desired_cadence:
            # Prefer the next higher tempo candidate.
            if higher_ptr < len(sorted_tracks):
                candidate = sorted_tracks[higher_ptr]
                higher_ptr += 1
            elif lower_ptr >= 0:
                candidate = sorted_tracks[lower_ptr]
                lower_ptr -= 1
        else:
            # Prefer the next lower tempo candidate.
            if lower_ptr >= 0:
                candidate = sorted_tracks[lower_ptr]
                lower_ptr -= 1
            elif higher_ptr < len(sorted_tracks):
                candidate = sorted_tracks[higher_ptr]
                higher_ptr += 1

        if candidate is None:
            break

        selected_tracks.append(candidate)
        total_duration_ms += candidate.get("duration_ms", 0)
        sum_tempos += candidate["tempo"]

    # --- Post-Selection Reordering ---
    # First, sort the selected songs in ascending order by tempo.
    sorted_selected = sorted(selected_tracks, key=lambda x: x["tempo"])
    n = len(sorted_selected)
    # Determine the lower segment (20% of selected songs; using ceil to ensure at least one song).
    lower_count = math.ceil(n * 0.2) if n > 0 else 0
    lower_segment = sorted_selected[:lower_count]
    upper_segment = sorted_selected[lower_count:]

    # For the upper 80%, re-order them by taking:
    #  - the songs at odd indices (in order) and
    #  - then the songs at even indices in reverse order.
    new_upper = []
    if upper_segment:
        part1 = upper_segment[1::2]
        part2 = upper_segment[0::2]
        new_upper = part1 + part2[::-1]

    final_order = lower_segment + new_upper

    # Compute the average tempo of the final ordered playlist.
    avg_tempo = sum(t["tempo"] for t in final_order) / len(final_order) if final_order else 0

    if sex == "male":
        c = 0.70
    elif sex == "female":
        c = 0.65
    else:
        c = 0.675
    actual_distance = avg_tempo * c * height * run_time

    # Build the playlist preview.
    playlist_preview = {
        "title": playlist_title,
        "actualDuration": round(total_duration_ms / 60000, 2),  # in minutes
        "actualDistance": round(actual_distance, 2),  # computed value
        "avgTempo": round(avg_tempo, 2),
        "songs": [
            {
                "title": t["title"],
                "artist": t["artist"],
                "tempo": t["tempo"],
                "uri": t["uri"],
                "duration_ms": t["duration_ms"],
                "image": t["image"]
            } for t in final_order
        ]
    }
    return jsonify({"success": True, "playlist": playlist_preview})

##############################
# Save Playlist Endpoint
##############################

@app.route('/save-playlist', methods=["POST"])
def save_playlist():
    access_token = session.get("access_token")
    if not access_token:
        return jsonify({"success": False, "message": "User not authenticated."}), 401

    data = request.get_json()
    playlist = data.get("playlist")
    if not playlist:
        return jsonify({"success": False, "message": "Missing playlist data."}), 400

    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    # Get user profile to determine the user ID
    user_resp = requests.get(config.API_BASE_URL + "/me", headers=headers)
    if user_resp.status_code != 200:
        return jsonify({"success": False, "message": "Failed to fetch user profile", "details": user_resp.json()}), 400
    user_id = user_resp.json().get("id")
    if not user_id:
        return jsonify({"success": False, "message": "User ID not found in profile."}), 400

    # Create a new playlist in the user's Spotify account
    create_playlist_url = f"{config.API_BASE_URL}/users/{user_id}/playlists"
    payload = {
        "name": playlist.get("title") + " (Runify)",
        "description": "Runify generated running playlist.",
        "public": False
    }
    create_resp = requests.post(create_playlist_url, headers=headers, json=payload)
    if create_resp.status_code not in [200, 201]:
        return jsonify({"success": False, "message": "Failed to create new playlist", "details": create_resp.json()}), 400
    new_playlist_data = create_resp.json()
    new_playlist_id = new_playlist_data.get("id")

    # Add tracks to the newly created playlist using their URIs
    track_uris = [song["uri"] for song in playlist.get("songs", []) if song.get("uri")]
    add_tracks_url = f"{config.API_BASE_URL}/playlists/{new_playlist_id}/tracks"
    add_resp = requests.post(add_tracks_url, headers=headers, json={"uris": track_uris})
    if add_resp.status_code not in [200, 201]:
        return jsonify({"success": False, "message": "Failed to add tracks", "details": add_resp.json()}), 400

    return jsonify({"success": True, "message": "Playlist saved", "new_playlist_id": new_playlist_id})

##############################
# Main
##############################

if __name__ == '__main__':
    app.run(debug=True, port=5000)