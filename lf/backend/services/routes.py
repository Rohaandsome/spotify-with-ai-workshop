from flask import Blueprint, request, jsonify, redirect
import os
import base64
import secrets
import tempfile
import requests
from PIL import Image
from playlist_generator import CoverGenerator, DescriptionGenerator, description_prompt

from clients.blob_storage_client import BlobStorageClient
from clients.table_storage_client import TableStorageClient
from clients.spotify_token_client import SpotifyTokenClient
from io import BytesIO
routes = Blueprint('routes', __name__)

cover_generator = CoverGenerator()
description_generator = DescriptionGenerator()
blob_storage = BlobStorageClient()
table_storage = TableStorageClient()
spotify_token = SpotifyTokenClient()

REDIRECT_URI = "http://127.0.0.1:5000/callback"
SCOPES = "playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private ugc-image-upload user-read-private user-top-read"
_state_store: set = set()


@routes.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "API is working"}), 200


@routes.route('/auth-status', methods=['GET'])
def auth_status():
    """Frontend polls this to check if Spotify login has been completed."""
    return jsonify({"authorized": spotify_token.is_authorized()}), 200

@routes.route('/login', methods=['GET'])
def login():
    """Redirect the user to Spotify's authorization page."""
    state = secrets.token_urlsafe(16)
    _state_store.add(state)
    params = {
        "response_type": "code",
        "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
        "scope": SCOPES,
        "redirect_uri": REDIRECT_URI,
        "state": state,
    }
    query = "&".join(f"{k}={requests.utils.quote(str(v))}" for k, v in params.items())
    return redirect(f"https://accounts.spotify.com/authorize?{query}")


@routes.route('/callback', methods=['GET'])
def callback():
    """Exchange the Spotify authorization code for access + refresh tokens."""
    error = request.args.get("error")
    if error:
        return jsonify({"error": f"Spotify authorization denied: {error}"}), 400

    state = request.args.get("state")
    if state not in _state_store:
        return jsonify({"error": "Invalid state parameter"}), 403
    _state_store.discard(state)

    code = request.args.get("code")
    resp = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
            "client_secret": os.getenv("SPOTIFY_CLIENT_SECRET"),
        },
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    spotify_token.set_user_tokens(
        data["access_token"], data["refresh_token"], data["expires_in"]
    )
    print("Spotify user authorized successfully.")
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    return redirect(frontend_url)  # redirect back to frontend


@routes.route('/get-playlist', methods=['GET'])
def get_playlist():
    playlists = get_playlists()
    play_list = []
    for playlist in playlists:
        print(f"Playlist: {playlist['name']} (ID: {playlist['id']})")
        play_list.append({
            'name': playlist['name'],
            'id': playlist['id']
        })
    return jsonify(play_list), 200


@routes.route('/get-tracks', methods=['GET'])
def get_tracks_of_playlist():
    playlist_id = request.args.get('playlist_id')
    if not playlist_id:
        return jsonify({"error": "Missing 'playlist_id' parameter"}), 400

    tracks = get_playlist_tracks(playlist_id)
    for item in tracks:
        track = item['item']
        print(f"Track: {track['name']} by {', '.join(artist['name'] for artist in track['artists'])}")
    return jsonify(tracks), 200


@routes.route('/generate-cover', methods=['GET'])
def generate_cover_image_for_playlist():
    playlist_id = request.args.get('playlist_id')
    user_id = request.args.get('userId')

    if not playlist_id:
        return jsonify({"error": "Missing 'playlist_id' parameter"}), 400
    
    if not user_id:
        return jsonify({"error": "Missing 'userId' parameter"}), 400

    try:
        tracks = get_playlist_tracks(playlist_id)
        track_names = [item['item']['name'] for item in tracks]
        
        # Use the CoverGenerator to create the cover image (returns base64 data URL)
        dalle_image_url = cover_generator.generate_cover_image(track_names)
        
        if not dalle_image_url:
            return jsonify({"error": "Failed to generate cover image"}), 500
        
        # Upload the image to blob storage and get permanent URL
        blob_image_url = blob_storage.upload_image_from_url(dalle_image_url, user_id, playlist_id)
        
        if blob_image_url:
            return jsonify({"image_url": blob_image_url}), 200
        else:
            return jsonify({"error": "Failed to upload image to storage"}), 500
            
    except Exception as e:
        error_msg = str(e)
        # Truncate error message if it contains base64 data
        if len(error_msg) > 200:
            error_msg = error_msg[:200] + "... (truncated)"
        print(f"ERROR in generate_cover_image_for_playlist: {error_msg}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Failed to process request"}), 500


@routes.route('/generate-description', methods=['GET'])
def generate_description_for_playlist():
    playlist_id = request.args.get('playlist_id')
    user_id = request.args.get('userId')

    if not playlist_id:
        return jsonify({"error": "Missing 'playlist_id' parameter"}), 400
    
    if not user_id:
        return jsonify({"error": "Missing 'userId' parameter"}), 400

    try:
        tracks = get_playlist_tracks(playlist_id)
        track_names = [item['item']['name'] for item in tracks]
        description = description_generator.generate_description(track_names)
        
        if description:
            # Get playlist name for table storage record
            try:
                playlists = get_playlists()
                playlist_name = next((p['name'] for p in playlists if p['id'] == playlist_id), 'Unknown Playlist')
            except Exception as e:
                print(f"WARNING: Could not fetch playlist name: {str(e)}")
                playlist_name = 'Unknown Playlist'
            
            # Save description record to table storage
            try:
                prompt = description_prompt(track_names)
                table_storage.save_description_record(playlist_id, playlist_name, description, prompt)
            except Exception as e:
                print(f"WARNING: Could not save to table storage: {str(e)}")
                # Don't fail the request if table storage fails
            
            return jsonify({"description": description}), 200
        else:
            return jsonify({"error": "Failed to generate description"}), 500
    except Exception as e:
        print(f"ERROR in generate_description_for_playlist: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Failed to process request: {str(e)}"}), 500


@routes.route('/recomendations', methods=['GET'])
def get_recomendations():
    playlist_id = request.args.get('playlist_id')

    if not playlist_id:
        return jsonify({"error": "Missing 'playlist_id' parameter"}), 400

    try:
        genre_seeds = get_genre_seeds()
        print(f"Available genre seeds: {genre_seeds}")

    except Exception as e:
        print(f"ERROR in get_recomendations: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Failed to process request: {str(e)}"}), 500

@routes.route('/set-cover', methods=['PUT'])
def set_cover_image_for_playlist():
    playlist_id = request.args.get('playlist_id')
    user_id = request.args.get('userId')
    ai_cover_image = request.json.get('image_url')

    if not playlist_id:
        return jsonify({"error": "Missing 'playlist_id' parameter"}), 400
    
    if not user_id:
        return jsonify({"error": "Missing 'userId' parameter"}), 400

    if not ai_cover_image:
        return jsonify({"error": "Missing 'image_url' in request body"}), 400

    try:
        # Download image from blob storage URL
        img_response = requests.get(ai_cover_image, timeout=30)
        img_response.raise_for_status()

        # Convert to JPEG and compress until base64-encoded size is under 256 KB (Spotify limit)
        # Base64 adds ~33% overhead, so raw JPEG must stay under 192 KB
        image = Image.open(BytesIO(img_response.content)).convert('RGB')
        quality = 85
        buffer = BytesIO()
        while quality >= 10:
            buffer = BytesIO()
            image.save(buffer, format='JPEG', quality=quality)
            if buffer.tell() <= 192 * 1024:
                break
            quality -= 10

        jpeg_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        # PUT to Spotify API — body must be base64-encoded JPEG string
        token = spotify_token.get_token()
        res = requests.put(
            f'https://api.spotify.com/v1/playlists/{playlist_id}/images',
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'image/jpeg'
            },
            data=jpeg_b64,
            timeout=30
        )

        if res.status_code not in (200, 202):
            print(f"Spotify API Error: {res.status_code} - {res.text}")
            return jsonify({"error": f"Spotify API returned {res.status_code}"}), 500

        return jsonify({"message": "Cover image updated successfully"}), 200

    except Exception as e:
        print(f"ERROR in set_cover_image_for_playlist: {str(e)}")
        return jsonify({"error": f"Failed to set cover image: {str(e)}"}), 500


@routes.route('/cover-images', methods=['GET'])
def get_cover_images():
    user_id = request.args.get('userId')
    
    if not user_id:
        return jsonify({"error": "user_id query parameter is required"}), 400

    try:
        cover_images = blob_storage.list_user_covers(user_id)
        
        # Fetch all playlists to get names
        try:
            playlists = get_playlists()
            playlist_map = {p['id']: p['name'] for p in playlists}
            
            # Add playlist names to cover images
            for cover in cover_images:
                playlist_id = cover.get('playlistId')
                cover['playlistName'] = playlist_map.get(playlist_id, 'Unknown Playlist')
        except Exception as e:
            print(f"WARNING: Could not fetch playlist names: {str(e)}")
            # Continue without playlist names
            for cover in cover_images:
                cover['playlistName'] = 'Unknown Playlist'
        
        return jsonify(cover_images), 200
    except Exception as e:
        print(f"ERROR in get_cover_images: {str(e)}")
        return jsonify({"error": "An error occurred while processing your request."}), 500


@routes.route('/top-artists', methods=['GET'])
def top_artists():
    try:
        artists = get_top_artists()
        return jsonify(artists), 200
    except Exception as e:
        print(f"ERROR in top_artists: {str(e)}")
        return jsonify({"error": str(e)}), 500


@routes.route('/top-tracks', methods=['GET'])
def top_tracks():
    try:
        tracks = get_top_tracks()
        return jsonify(tracks), 200
    except Exception as e:
        print(f"ERROR in top_tracks: {str(e)}")
        return jsonify({"error": str(e)}), 500


def fetch_web_api(endpoint, method, body=None):
    """Fetch from Spotify Web API
    Args:
        endpoint: API endpoint path
        method: HTTP method (GET, POST, etc.)
        body: Optional request body (dict)

    Returns:
        Response JSON as dict
    """
    if not spotify_token.is_authorized():
        raise Exception("User not authorized. Please visit /login first.")
    token = spotify_token.get_token()
    res = requests.request(
        method,
        f'https://api.spotify.com/{endpoint}',
        headers={'Authorization': f'Bearer {token}'},
        json=body
    )
    
    if res.status_code != 200:
        print(f"Spotify API Error: {res.status_code} - {res.text}")
        raise Exception(f"Spotify API returned {res.status_code}: {res.text}")
    
    return res.json()


def get_playlists():
    """Get user's playlists"""
    return fetch_web_api(
        'v1/me/playlists',
        'GET'
    )['items']

def get_genre_seeds():
    """Get available genre seeds for recommendations"""
    return fetch_web_api(
        'v1/recommendations/available-genre-seeds',
        'GET'
    )['genres']

def get_top_artists():
    """Get user's top artists"""
    result = fetch_web_api('v1/me/top/artists', 'GET')
    print("Top artists response:", result)
    return result['items']

def get_top_tracks():
    """Get user's top tracks"""
    result = fetch_web_api('v1/me/top/tracks', 'GET')
    print("Top tracks response:", result)
    return result['items']

def get_playlist_tracks(playlist_id):
    """Get tracks in a playlist
    Args:
        playlist_id: Spotify playlist ID

    Returns:
        List of tracks in the playlist
    """
    return fetch_web_api(
        f'v1/playlists/{playlist_id}/items',
        'GET'
    )['items']
