GET_CURRENT_TRACK_SCHEMA = {
    "name": "lastfm_get_current_track",
    "description": "Get the track the user is currently listening to on Last.fm.",
    "parameters": {
        "type": "object",
        "properties": {},
    },
}

GET_RECENT_TRACKS_SCHEMA = {
    "name": "lastfm_get_recent_tracks",
    "description": "Retrieve the user's recent tracks or scrobbles from a specific time period.",
    "parameters": {
        "type": "object",
        "properties": {
            "from_timestamp": {
                "type": "integer",
                "description": "Beginning of the time period as a Unix timestamp.",
            },
            "to_timestamp": {
                "type": "integer",
                "description": "End of the time period as a Unix timestamp.",
            },
            "limit": {
                "type": "integer",
                "description": "The number of results to fetch (default: 10, max: 200).",
                "default": 10,
            },
        },
    },
}

GET_TOP_TRACKS_SCHEMA = {
    "name": "lastfm_get_top_tracks",
    "description": "Get basic stats about the user's most listened to tracks over a given period.",
    "parameters": {
        "type": "object",
        "properties": {
            "period": {
                "type": "string",
                "description": "The time period over which to retrieve top tracks.",
                "enum": ["overall", "7day", "1month", "3month", "6month", "12month"],
                "default": "overall",
            },
            "limit": {
                "type": "integer",
                "description": "Number of top tracks to return.",
                "default": 10,
            },
        },
    },
}

GET_TOP_ARTISTS_SCHEMA = {
    "name": "lastfm_get_top_artists",
    "description": "Get the user's most listened to artists over a given period.",
    "parameters": {
        "type": "object",
        "properties": {
            "period": {
                "type": "string",
                "description": "The time period over which to retrieve top artists.",
                "enum": ["overall", "7day", "1month", "3month", "6month", "12month"],
                "default": "overall",
            },
            "limit": {
                "type": "integer",
                "description": "Number of top artists to return.",
                "default": 10,
            },
        },
    },
}

GET_TOP_ALBUMS_SCHEMA = {
    "name": "lastfm_get_top_albums",
    "description": "Get the user's most listened to albums over a given period.",
    "parameters": {
        "type": "object",
        "properties": {
            "period": {
                "type": "string",
                "description": "The time period over which to retrieve top albums.",
                "enum": ["overall", "7day", "1month", "3month", "6month", "12month"],
                "default": "overall",
            },
            "limit": {
                "type": "integer",
                "description": "Number of top albums to return.",
                "default": 10,
            },
        },
    },
}

GET_ARTIST_INFO_SCHEMA = {
    "name": "lastfm_get_artist_info",
    "description": "Get biography, tags, and listener stats for an artist on Last.fm.",
    "parameters": {
        "type": "object",
        "properties": {
            "artist": {
                "type": "string",
                "description": "Name of the artist.",
            },
        },
        "required": ["artist"],
    },
}
