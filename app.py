from flask import Flask, redirect, request, session, render_template, jsonify
import requests, os
from dotenv import load_dotenv
from urllib.parse import urlencode

load_dotenv()
app = Flask(__name__)
app.secret_key = os.urandom(24)

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1"

SCOPE = "user-read-currently-playing user-read-playback-state user-modify-playback-state"



@app.route("/")
def index():
    if 'access_token' in session:
        return render_template("index.html", access_token=session['access_token'])
    else:
        auth_url = SPOTIFY_AUTH_URL + '?' + urlencode({
            'client_id': CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'scope': SCOPE
        })
        return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get('code')
    response = requests.post(SPOTIFY_TOKEN_URL, data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    })
    response_data = response.json()
    session['access_token'] = response_data['access_token']
    return redirect("/")

def get_auth_headers():
    return {
        "Authorization": f"Bearer {session['access_token']}"
    }

def get_current_playback(headers):
    res = requests.get(f"{SPOTIFY_API_BASE_URL}/me/player/currently-playing", headers=headers)
    if res.status_code == 204:
        return None  
    if res.status_code != 200:
        raise Exception(f"Failed to fetch playback: {res.status_code}")
    return res.json()

def get_playlist_name(context, headers):
    if context and context.get("type") == "playlist":
        playlist_id = context["uri"].split(":")[-1]
        res = requests.get(f"{SPOTIFY_API_BASE_URL}/playlists/{playlist_id}", headers=headers)
        if res.status_code == 200:
            return res.json().get("name")
    return None

def format_track_data(playback_data, playlist_name):
    item = playback_data["item"]
    return {
        "name": item["name"],
        "artists": ", ".join([artist["name"] for artist in item["artists"]]),
        "album_image": item["album"]["images"][0]["url"],
        "progress_ms": playback_data["progress_ms"],
        "duration_ms": item["duration_ms"],
        "popularity": item["popularity"],
        "album": item["album"]["name"],
        "playlist": playlist_name,
    }

@app.route("/current")
def current_track():
    if "access_token" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    headers = get_auth_headers()

    try:
        playback_data = get_current_playback(headers)
        if not playback_data:
            return jsonify({"playing": False})

        playlist_name = get_playlist_name(playback_data.get("context"), headers)
        response = format_track_data(playback_data, playlist_name)

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/play", methods=["PUT"])
def play():
    headers = get_auth_headers()
    res = requests.put(f"{SPOTIFY_API_BASE_URL}/me/player/play", headers=headers)
    return jsonify(res.json() if res.content else {"status": res.status_code})

@app.route("/pause", methods=["PUT"])
def pause():
    headers = get_auth_headers()
    res = requests.put(f"{SPOTIFY_API_BASE_URL}/me/player/pause", headers=headers)
    return jsonify(res.json() if res.content else {"status": res.status_code})

@app.route("/next", methods=["POST"])
def next_track():
    headers = get_auth_headers()
    res = requests.post(f"{SPOTIFY_API_BASE_URL}/me/player/next", headers=headers)
    return jsonify(res.json() if res.content else {"status": res.status_code})

@app.route("/previous", methods=["POST"])
def prev_track():
    headers = get_auth_headers()
    res = requests.post(f"{SPOTIFY_API_BASE_URL}/me/player/previous", headers=headers)
    return jsonify(res.json() if res.content else {"status": res.status_code})
