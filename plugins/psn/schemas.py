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
    "description": (
        "Get all trophies (and earned status) for a specific game title, plus a completion summary. "
        "Provide title_id (recommended, e.g. from psn_check_game_owned/psn_list_owned_games) to auto-detect "
        "the np_communication_id, or np_communication_id directly. The platform is auto-detected by trying "
        "every platform if not given or if the given/detected one doesn't have trophy data — platform is "
        "only a hint to try first, never required."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "title_id": {
                "type": "string",
                "description": "The game's title ID (e.g. 'CUSA00265_00' or 'PPSA13956_00'). Used to auto-detect np_communication_id.",
            },
            "np_communication_id": {
                "type": "string",
                "description": "The game's NP communication ID (e.g. 'NPWR22810_00'), if already known.",
            },
            "platform": {
                "type": "string",
                "description": "Optional hint for the platform to try first: PS3, PS4, PS5, PSVITA, or PSPC. Every platform is tried regardless if this doesn't pan out.",
            },
        },
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
                "description": "Number of most recently updated game titles to scan for trophies (default: 10).",
                "default": 10,
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
            "games_only": {
                "type": "boolean",
                "description": "Exclude non-game entitlements (streaming apps, etc.) when the API flags them as such (default: true).",
                "default": True,
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

SEARCH_GAMES_SCHEMA = {
    "name": "psn_search_games",
    "description": (
        "Search the PlayStation Store catalog for games and add-ons by name. "
        "This searches the whole store, not just games the user owns — use psn_check_game_owned "
        "or psn_list_owned_games to check ownership. Useful to get a game's price."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query (game name).",
            },
            "count": {
                "type": "integer",
                "description": "Number of results to return (default: 10).",
                "default": 10,
            },
        },
        "required": ["query"],
    },
}
