import os
import json
import requests

BASE_URL = "https://retroachievements.org/API/"

def _get_auth_params():
    api_key = os.environ.get("RETROACHIEVEMENTS_API_KEY")
    username = os.environ.get("RETROACHIEVEMENTS_USERNAME")
    if not api_key or not username:
        raise ValueError("Missing RETROACHIEVEMENTS_API_KEY or RETROACHIEVEMENTS_USERNAME environment variable.")
    return {"y": api_key, "z": username, "u": username}

def get_recent_achievements(params, **kwargs):
    try:
        auth = _get_auth_params()
        payload = {**auth, "m": params.get("minutes", 60)}

        response = requests.get(BASE_URL + "API_GetUserRecentAchievements.php", params=payload).json()

        achievements = []
        for a in response:
            achievements.append({
                "achievement": a.get("Title"),
                "description": a.get("Description"),
                "game": a.get("GameTitle"),
                "console": a.get("ConsoleName"),
                "points": a.get("Points"),
                "hardcore": a.get("HardcoreMode") == "1",
                "date": a.get("Date")
            })

        return json.dumps({"success": True, "achievements": achievements})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

def get_recently_played_games(params, **kwargs):
    try:
        auth = _get_auth_params()
        payload = {**auth, "c": params.get("count", 10)}

        response = requests.get(BASE_URL + "API_GetUserRecentlyPlayedGames.php", params=payload).json()

        games = []
        for g in response:
            games.append({
                "game": g.get("Title"),
                "console": g.get("ConsoleName"),
                "game_id": g.get("GameID"),
                "achievements_total": g.get("AchievementsTotal"),
                "last_played": g.get("LastPlayed")
            })

        return json.dumps({"success": True, "games": games})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

def get_game_progress(params, **kwargs):
    try:
        auth = _get_auth_params()
        game_id = params.get("game_id")
        if not game_id:
            raise ValueError("Missing required parameter: game_id")

        payload = {**auth, "g": game_id}
        response = requests.get(BASE_URL + "API_GetGameInfoAndUserProgress.php", params=payload).json()

        achievements_raw = response.get("Achievements", {})
        earned = sum(1 for a in achievements_raw.values() if a.get("DateEarned"))

        return json.dumps({
            "success": True,
            "game": response.get("Title"),
            "console": response.get("ConsoleName"),
            "num_achievements": response.get("NumAchievements"),
            "num_awarded": response.get("NumAwardedToUser"),
            "num_awarded_hardcore": response.get("NumAwardedToUserHardcore"),
            "completion": response.get("UserCompletion"),
            "completion_hardcore": response.get("UserCompletionHardcore"),
            "achievements_earned": earned
        })
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

def get_game_details(params, **kwargs):
    try:
        auth = _get_auth_params()
        game_id = params.get("game_id")
        if not game_id:
            raise ValueError("Missing required parameter: game_id")

        payload = {**auth, "i": game_id}
        response = requests.get(BASE_URL + "API_GetGameExtended.php", params=payload).json()

        achievements_raw = response.get("Achievements", {})
        achievements = []
        for a in achievements_raw.values():
            achievements.append({
                "title": a.get("Title"),
                "description": a.get("Description"),
                "points": a.get("Points")
            })

        return json.dumps({
            "success": True,
            "game": response.get("Title"),
            "console": response.get("ConsoleName"),
            "developer": response.get("Developer"),
            "publisher": response.get("Publisher"),
            "genre": response.get("Genre"),
            "released": response.get("Released"),
            "num_achievements": response.get("NumAchievements"),
            "achievements": achievements
        })
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})
