"""Last.fm Hermes plugin initialization."""
from . import schemas, tools

def register(ctx):
    # Register Current Track Tool
    ctx.register_tool(
        name="lastfm_get_current_track",
        toolset="lastfm",
        schema=schemas.GET_CURRENT_TRACK_SCHEMA,
        handler=tools.get_current_track,
        description="Get the track the user is currently listening to on Last.fm."
    )

    # Register Recent Tracks (Time-boxed) Tool
    ctx.register_tool(
        name="lastfm_get_recent_tracks",
        toolset="lastfm",
        schema=schemas.GET_RECENT_TRACKS_SCHEMA,
        handler=tools.get_recent_tracks,
        description="Retrieve history or recent tracks from a given time frame."
    )

    # Register Top Track Stats Tool
    ctx.register_tool(
        name="lastfm_get_top_tracks",
        toolset="lastfm",
        schema=schemas.GET_TOP_TRACKS_SCHEMA,
        handler=tools.get_top_tracks,
        description="Get basic listening metrics like top tracks over a certain period."
    )

    # Register Top Artists Tool
    ctx.register_tool(
        name="lastfm_get_top_artists",
        toolset="lastfm",
        schema=schemas.GET_TOP_ARTISTS_SCHEMA,
        handler=tools.get_top_artists,
        description="Get the user's most listened to artists over a certain period."
    )

    # Register Top Albums Tool
    ctx.register_tool(
        name="lastfm_get_top_albums",
        toolset="lastfm",
        schema=schemas.GET_TOP_ALBUMS_SCHEMA,
        handler=tools.get_top_albums,
        description="Get the user's most listened to albums over a certain period."
    )

    # Register Artist Info Tool
    ctx.register_tool(
        name="lastfm_get_artist_info",
        toolset="lastfm",
        schema=schemas.GET_ARTIST_INFO_SCHEMA,
        handler=tools.get_artist_info,
        description="Get biography, tags, and listener stats for an artist."
    )
