import unittest
from unittest.mock import patch, MagicMock
from app import app, format_track_data

class SpotifyAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_index_redirects_to_auth_if_no_token(self):
        with self.client.session_transaction() as sess:
            sess.pop("access_token", None)
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("accounts.spotify.com", response.headers["Location"])

    def test_index_renders_template_if_authenticated(self):
        with self.client.session_transaction() as sess:
            sess["access_token"] = "dummy_token"
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<!DOCTYPE html>", response.data)

    @patch("app.requests.get")
    def test_current_track_returns_playing_false_on_204(self, mock_get):
        with self.client.session_transaction() as sess:
            sess["access_token"] = "dummy_token"
        mock_get.return_value.status_code = 204
        response = self.client.get("/current")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"playing": False})

    @patch("app.requests.get")
    def test_current_track_returns_error_on_failure(self, mock_get):
        with self.client.session_transaction() as sess:
            sess["access_token"] = "dummy_token"
        mock_get.return_value.status_code = 400
        response = self.client.get("/current")
        self.assertEqual(response.status_code, 500)
        self.assertIn("error", response.get_json())

    def test_format_track_data(self):
        dummy_playback = {
            "item": {
                "name": "Test Song",
                "artists": [{"name": "Test Artist"}],
                "album": {
                    "images": [{"url": "http://image"}],
                    "name": "Test Album"
                },
                "duration_ms": 200000,
                "popularity": 80
            },
            "progress_ms": 50000
        }
        result = format_track_data(dummy_playback, "Test Playlist")
        self.assertEqual(result["name"], "Test Song")
        self.assertEqual(result["artists"], "Test Artist")
        self.assertEqual(result["album"], "Test Album")
        self.assertEqual(result["playlist"], "Test Playlist")

if __name__ == "__main__":
    unittest.main()
