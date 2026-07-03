import os
import json
import requests

BASE_URL = "http://ws.audioscrobbler.com/2.0/"

def _get_auth_params():
    api_key = os.environ.get("LASTFM_API_KEY")
    username = os.environ.get("LASTFM_USERNAME")
    if not api_key or not username:
        raise ValueError("Missing LASTFM_API_KEY or LASTFM_USERNAME environment variable.")
    return {"api_key": api_key, "user": username, "format": "json"}

def _get_top_payload(params, method):
    return {
        **_get_auth_params(),
        "method": method,
        "period": params.get("period", "overall"),
        "limit": params.get("limit", 10)
    }

def get_current_track(params, **kwargs):
    try:
        auth = _get_auth_params()
        payload = {**auth, "method": "user.getrecenttracks", "limit": 1}
        response = requests.get(BASE_URL, params=payload).json()

        tracks = response.get("recenttracks", {}).get("track", [])
        if not tracks:
            return json.dumps({"success": True, "message": "No history found."})

        # Last.fm returns a list or a single object if there's only 1 track
        latest_track = tracks[0] if isinstance(tracks, list) else tracks

        # Check if it is currently playing
        is_now_playing = latest_track.get("@attr", {}).get("nowplaying") == "true"

        return json.dumps({
            "success": True,
            "now_playing": is_now_playing,
            "track": latest_track.get("name"),
            "artist": latest_track.get("artist", {}).get("#text"),
            "album": latest_track.get("album", {}).get("#text")
        })
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

def get_recent_tracks(params, **kwargs):
    try:
        auth = _get_auth_params()
        payload = {
            **auth,
            "method": "user.getrecenttracks",
            "limit": params.get("limit", 10)
        }

        if "from_timestamp" in params:
            payload["from"] = params["from_timestamp"]
        if "to_timestamp" in params:
            payload["to"] = params["to_timestamp"]

        response = requests.get(BASE_URL, params=payload).json()
        tracks_raw = response.get("recenttracks", {}).get("track", [])

        if not isinstance(tracks_raw, list):
            tracks_raw = [tracks_raw]

        tracks = []
        for t in tracks_raw:
            tracks.append({
                "track": t.get("name"),
                "artist": t.get("artist", {}).get("#text"),
                "album": t.get("album", {}).get("#text"),
                "date": t.get("date", {}).get("#text", "Now Playing")
            })

        return json.dumps({"success": True, "tracks": tracks})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

def get_top_tracks(params, **kwargs):
    try:
        payload = _get_top_payload(params, "user.gettoptracks")
        response = requests.get(BASE_URL, params=payload).json()
        tracks_raw = response.get("toptracks", {}).get("track", [])

        if not isinstance(tracks_raw, list):
            tracks_raw = [tracks_raw]

        tracks = []
        for t in tracks_raw:
            tracks.append({
                "rank": t.get("@attr", {}).get("rank"),
                "track": t.get("name"),
                "artist": t.get("artist", {}).get("name"),
                "playcount": t.get("playcount")
            })

        return json.dumps({"success": True, "period": payload["period"], "top_tracks": tracks})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

def get_top_artists(params, **kwargs):
    try:
        payload = _get_top_payload(params, "user.gettopartists")
        response = requests.get(BASE_URL, params=payload).json()
        artists_raw = response.get("topartists", {}).get("artist", [])

        if not isinstance(artists_raw, list):
            artists_raw = [artists_raw]

        artists = []
        for a in artists_raw:
            artists.append({
                "rank": a.get("@attr", {}).get("rank"),
                "artist": a.get("name"),
                "playcount": a.get("playcount")
            })

        return json.dumps({"success": True, "period": payload["period"], "top_artists": artists})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

def get_top_albums(params, **kwargs):
    try:
        payload = _get_top_payload(params, "user.gettopalbums")
        response = requests.get(BASE_URL, params=payload).json()
        albums_raw = response.get("topalbums", {}).get("album", [])

        if not isinstance(albums_raw, list):
            albums_raw = [albums_raw]

        albums = []
        for a in albums_raw:
            albums.append({
                "rank": a.get("@attr", {}).get("rank"),
                "album": a.get("name"),
                "artist": a.get("artist", {}).get("name"),
                "playcount": a.get("playcount")
            })

        return json.dumps({"success": True, "period": payload["period"], "top_albums": albums})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

def get_artist_info(params, **kwargs):
    try:
        auth = _get_auth_params()
        artist = params.get("artist")
        if not artist:
            raise ValueError("Missing required parameter: artist")

        payload = {**auth, "method": "artist.getinfo", "artist": artist}
        response = requests.get(BASE_URL, params=payload).json()
        info = response.get("artist")

        if not info:
            return json.dumps({"success": False, "error": response.get("message", "Artist not found.")})

        bio = info.get("bio", {})
        tags_raw = info.get("tags", {}).get("tag", [])
        if not isinstance(tags_raw, list):
            tags_raw = [tags_raw]

        return json.dumps({
            "success": True,
            "artist": info.get("name"),
            "listeners": info.get("stats", {}).get("listeners"),
            "playcount": info.get("stats", {}).get("playcount"),
            "tags": [t.get("name") for t in tags_raw],
            "summary": bio.get("summary")
        })
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})
