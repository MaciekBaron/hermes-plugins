# hermes-plugins

Hermes plugins for interacting with third-party APIs.

## Plugins

### lastfm

Interact with the Last.fm API to fetch scrobbles, top tracks/artists/albums, and artist info.

Requires: `LASTFM_API_KEY`, `LASTFM_USERNAME`

Tools:
- `lastfm_get_current_track`
- `lastfm_get_recent_tracks`
- `lastfm_get_top_tracks`
- `lastfm_get_top_artists`
- `lastfm_get_top_albums`
- `lastfm_get_artist_info`

### retroachievements

Interact with the RetroAchievements API to fetch recent achievements, game progress, and game details.

Requires: `RETROACHIEVEMENTS_API_KEY`, `RETROACHIEVEMENTS_USERNAME`

Tools:
- `retroachievements_get_recent_achievements`
- `retroachievements_get_recently_played_games`
- `retroachievements_get_game_progress`
- `retroachievements_get_game_details`

### psn

Interact with the PlayStation Network (via PSNAWP) to fetch recently played games, trophies, and owned games.

Requires: `PSN_NPSSO` (expires roughly every two months and needs to be refreshed)

Tools:
- `psn_get_recently_played_games`
- `psn_get_game_trophies`
- `psn_get_recent_trophies`
- `psn_list_owned_games`
- `psn_check_game_owned`
- `psn_get_online_friends`
