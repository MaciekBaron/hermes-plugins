GET_RECENT_ACHIEVEMENTS_SCHEMA = {
    "name": "retroachievements_get_recent_achievements",
    "description": "Get the achievements the user has recently unlocked on RetroAchievements.",
    "parameters": {
        "type": "object",
        "properties": {
            "minutes": {
                "type": "integer",
                "description": "How far back to look for achievements, in minutes (default: 60).",
                "default": 60,
            },
        },
    },
}

GET_RECENTLY_PLAYED_GAMES_SCHEMA = {
    "name": "retroachievements_get_recently_played_games",
    "description": "Get the games the user has recently played on RetroAchievements.",
    "parameters": {
        "type": "object",
        "properties": {
            "count": {
                "type": "integer",
                "description": "Number of recently played games to return (default: 10).",
                "default": 10,
            },
        },
    },
}

GET_GAME_PROGRESS_SCHEMA = {
    "name": "retroachievements_get_game_progress",
    "description": "Get the user's achievement progress for a specific game.",
    "parameters": {
        "type": "object",
        "properties": {
            "game_id": {
                "type": "integer",
                "description": "The RetroAchievements game ID.",
            },
        },
        "required": ["game_id"],
    },
}

GET_GAME_DETAILS_SCHEMA = {
    "name": "retroachievements_get_game_details",
    "description": "Get extended details about a game, including its full achievement list.",
    "parameters": {
        "type": "object",
        "properties": {
            "game_id": {
                "type": "integer",
                "description": "The RetroAchievements game ID.",
            },
        },
        "required": ["game_id"],
    },
}
