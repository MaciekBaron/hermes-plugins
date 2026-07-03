"""RetroAchievements Hermes plugin initialization."""
from . import schemas, tools

def register(ctx):
    # Register Recent Achievements Tool
    ctx.register_tool(
        name="retroachievements_get_recent_achievements",
        toolset="retroachievements",
        schema=schemas.GET_RECENT_ACHIEVEMENTS_SCHEMA,
        handler=tools.get_recent_achievements,
        description="Get the achievements the user has recently unlocked."
    )

    # Register Recently Played Games Tool
    ctx.register_tool(
        name="retroachievements_get_recently_played_games",
        toolset="retroachievements",
        schema=schemas.GET_RECENTLY_PLAYED_GAMES_SCHEMA,
        handler=tools.get_recently_played_games,
        description="Get the games the user has recently played."
    )

    # Register Game Progress Tool
    ctx.register_tool(
        name="retroachievements_get_game_progress",
        toolset="retroachievements",
        schema=schemas.GET_GAME_PROGRESS_SCHEMA,
        handler=tools.get_game_progress,
        description="Get the user's achievement progress for a specific game."
    )

    # Register Game Details Tool
    ctx.register_tool(
        name="retroachievements_get_game_details",
        toolset="retroachievements",
        schema=schemas.GET_GAME_DETAILS_SCHEMA,
        handler=tools.get_game_details,
        description="Get extended details about a game, including its achievement list."
    )
