# 🎵 Now Playing — Spotify Web Visualizer

This is a web app that shows your currently playing Spotify track using the Spotify Web API. It displays:

- Album art  
- Track and artist information  
- Playback progress bar  
- Popularity and album details  
- Playlist (if playing from one)  
- Fullscreen display mode  

Built using **Python Flask**, **HTML**, **CSS**, and **JavaScript**.

## 🔧 Features

- 🔗 Connects to your Spotify Premium account
- 🎧 Real-time track updates 
- 🟢 Animated pulse synced to tempo
- 🖥️ Fullscreen toggle button
- 🎨 Responsive and minimal interface

---

## 🛠️ Installation

1. **Clone the repo**

2. Create a virtual environment
3. python -m venv venv
4. On Windows: venv\Scripts\activate

5. Install dependencies ->
pip install flask requests

6. Set up your Spotify API credentials
https://developer.spotify.com/dashboard
Create an app -> Set the Redirect URI to:
http://127.0.0.1:5000/callback

7. Fill the .env file with ID ->
CLIENT_ID = "your_client_id_from_spotify" +
CLIENT_SECRET = "your_client_secret_from_spotify"

8. In terminal -> pip install -r requirements.txt

9. Run the app
flask run -
then open http://127.0.0.1:5000 in your browser.

## Requirements
Spotify Premium account -
Python 3.7+ -
Internet connection


## Testing
1. In terminal -> pip install flask requests python-dotenv
2. Run tests -> python -m unittest test_app

