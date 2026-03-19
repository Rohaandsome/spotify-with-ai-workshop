import os
import time
import requests

_TOKEN_FILE = os.path.join(os.path.dirname(__file__), ".spotify_refresh_token")


class SpotifyTokenClient:
    def __init__(self):
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self._access_token = os.getenv("SPOTIFY_ACCESS_TOKEN") if os.getenv("SPOTIFY_ACCESS_TOKEN") else None # Check env var on startup for manual token
        self._refresh_token = None
        self._expires_at = 0
        self._load_persisted_token()

    def _load_persisted_token(self):
        """Restore refresh token from disk if available (survives server reloads)."""
        if os.path.exists(_TOKEN_FILE):
            with open(_TOKEN_FILE, "r") as f:
                token = f.read().strip()
                if token:
                    self._refresh_token = token
                    print("Spotify refresh token loaded from disk.")

    def _persist_token(self):
        """Write refresh token to disk so it survives process restarts."""
        with open(_TOKEN_FILE, "w") as f:
            f.write(self._refresh_token)

    # ------------------------------------------------------------------ #
    # Called by the /callback route after the user authorizes             #
    # ------------------------------------------------------------------ #
    def set_user_tokens(self, access_token: str, refresh_token: str, expires_in: int):
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._expires_at = time.time() + expires_in - 30
        self._persist_token()

    def is_authorized(self) -> bool:
        """True if OAuth refresh token is stored, or a manual env token is set."""
        if self._refresh_token or bool(os.getenv("SPOTIFY_ACCESS_TOKEN")):
            return True
        # Re-check file in case another process wrote it after startup
        self._load_persisted_token()
        return self._refresh_token is not None

    # ------------------------------------------------------------------ #
    # Used by fetch_web_api                                               #
    # Priority: OAuth access/refresh token > SPOTIFY_ACCESS_TOKEN env var #
    # ------------------------------------------------------------------ #
    def get_token(self) -> str:
        # 1. Valid cached OAuth access token
        if self._access_token and time.time() < self._expires_at:
            return self._access_token
        # 2. If no refresh token in memory, check file (handles multi-process Flask reloader)
        if not self._refresh_token:
            self._load_persisted_token()
        # 3. Silently refresh via stored refresh token
        if self._refresh_token:
            return self._refresh()
        # 4. Fall back to manually set env var token
        env_token = os.getenv("SPOTIFY_ACCESS_TOKEN")
        if env_token:
            return env_token
        raise Exception("No Spotify token available. Visit /login to authorize.")

    def _refresh(self) -> str:
        response = requests.post(
            "https://accounts.spotify.com/api/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "refresh_token",
                "refresh_token": self._refresh_token,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        self._access_token = data["access_token"]
        self._expires_at = time.time() + data["expires_in"] - 30
        print(f"Spotify token refreshed, expires in {data['expires_in']}s")
        return self._access_token


