"""PSN Hermes plugin initialization."""
from . import schemas, tools

def register(ctx):
    # Register Recently Played Games Tool
    ctx.register_tool(
        name="psn_get_recently_played_games",
        toolset="psn",
        schema=schemas.GET_RECENTLY_PLAYED_GAMES_SCHEMA,
        handler=tools.get_recently_played_games,
        description="Get the games the user has recently played on PlayStation Network."
    )

    # Register Game Trophies Tool
    ctx.register_tool(
        name="psn_get_game_trophies",
        toolset="psn",
        schema=schemas.GET_GAME_TROPHIES_SCHEMA,
        handler=tools.get_game_trophies,
        description="Get all trophies for a specific game title, including earned status."
    )

    # Register Recent Trophies Tool
    ctx.register_tool(
        name="psn_get_recent_trophies",
        toolset="psn",
        schema=schemas.GET_RECENT_TROPHIES_SCHEMA,
        handler=tools.get_recent_trophies,
        description="Get the trophies the user has most recently earned across all games."
    )

    # Register Owned Games Tool
    ctx.register_tool(
        name="psn_list_owned_games",
        toolset="psn",
        schema=schemas.LIST_OWNED_GAMES_SCHEMA,
        handler=tools.list_owned_games,
        description="List the games owned by the user."
    )

    # Register Game Ownership Check Tool
    ctx.register_tool(
        name="psn_check_game_owned",
        toolset="psn",
        schema=schemas.CHECK_GAME_OWNED_SCHEMA,
        handler=tools.check_game_owned,
        description="Check whether the user owns a specific game."
    )

    # Register Online Friends Tool
    ctx.register_tool(
        name="psn_get_online_friends",
        toolset="psn",
        schema=schemas.GET_ONLINE_FRIENDS_SCHEMA,
        handler=tools.get_online_friends,
        description="Get the user's friends who are currently online."
    )
