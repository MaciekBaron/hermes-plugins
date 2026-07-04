GET_RECENTLY_PLAYED_GAMES_SCHEMA = {
    "name": "psn_get_recently_played_games",
    "description": "Get the games the user has recently played on PlayStation Network.",
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

GET_GAME_TROPHIES_SCHEMA = {
    "name": "psn_get_game_trophies",
    "description": "Get all trophies (and earned status) for a specific game title.",
    "parameters": {
        "type": "object",
        "properties": {
            "np_communication_id": {
                "type": "string",
                "description": "The game's NP communication ID (e.g. 'NPWR22810_00').",
            },
            "platform": {
                "type": "string",
                "description": "The platform the title belongs to: PS3, PS4, PS5, PSVITA, or PSPC.",
            },
        },
        "required": ["np_communication_id", "platform"],
    },
}

GET_RECENT_TROPHIES_SCHEMA = {
    "name": "psn_get_recent_trophies",
    "description": "Get the trophies the user has most recently earned across all games.",
    "parameters": {
        "type": "object",
        "properties": {
            "count": {
                "type": "integer",
                "description": "Number of recent trophies to return (default: 10).",
                "default": 10,
            },
            "titles_to_scan": {
                "type": "integer",
                "description": "Number of most recently updated game titles to scan for trophies (default: 5).",
                "default": 5,
            },
        },
    },
}

LIST_OWNED_GAMES_SCHEMA = {
    "name": "psn_list_owned_games",
    "description": "List the games owned by the user (PS4 and PS5 only).",
    "parameters": {
        "type": "object",
        "properties": {
            "count": {
                "type": "integer",
                "description": "Number of owned games to return (default: 50).",
                "default": 50,
            },
        },
    },
}

CHECK_GAME_OWNED_SCHEMA = {
    "name": "psn_check_game_owned",
    "description": "Check whether the user owns a specific game, by title ID or by name (by name is slower).",
    "parameters": {
        "type": "object",
        "properties": {
            "title_id": {
                "type": "string",
                "description": "The game's title ID (e.g. 'CUSA00265_00').",
            },
            "name": {
                "type": "string",
                "description": "The game's name to search for, if title_id is not known (slower).",
            },
        },
    },
}

GET_ONLINE_FRIENDS_SCHEMA = {
    "name": "psn_get_online_friends",
    "description": "Get the user's friends who are currently online on PlayStation Network.",
    "parameters": {
        "type": "object",
        "properties": {},
    },
}
