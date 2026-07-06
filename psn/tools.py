import os
import json

from psnawp_api import PSNAWP
from psnawp_api.models.search import SearchDomain
from psnawp_api.models.trophies import PlatformType

_psnawp = None
_client = None


def _get_client():
    global _psnawp, _client
    if _client is None:
        npsso = os.environ.get("PSN_NPSSO")
        if not npsso:
            raise ValueError("Missing PSN_NPSSO environment variable.")
        _psnawp = PSNAWP(npsso)
        _client = _psnawp.me()
    return _client


def _get_psnawp():
    _get_client()
    return _psnawp


def _dt(value):
    return value.isoformat() if value is not None else None


def _duration_seconds(value):
    return value.total_seconds() if value is not None else None


def _platform_type(platform):
    if not platform:
        raise ValueError("Missing required parameter: platform")
    try:
        return PlatformType[platform.upper()]
    except KeyError:
        raise ValueError(
            f"Unknown platform '{platform}'. Expected one of: PS3, PS4, PS5, PSVITA, PSPC."
        )


_PLATFORM_PRIORITY = [PlatformType.PS5, PlatformType.PS4, PlatformType.PS3, PlatformType.PS_VITA, PlatformType.PSPC]


def _sorted_platforms(platforms):
    platforms = set(platforms)
    ordered = [p for p in _PLATFORM_PRIORITY if p in platforms]
    ordered += [p for p in platforms if p not in ordered]
    return ordered


def _resolve_trophy_title(client, title_id):
    matches = list(client.trophy_titles_for_title([title_id]))
    if not matches:
        raise ValueError(f"No trophy title found for title_id '{title_id}'.")
    match = matches[0]
    if not match.np_communication_id or not match.title_platform:
        raise ValueError(f"Could not resolve trophy info for title_id '{title_id}'.")
    return match.np_communication_id, match.title_platform


def _fetch_trophies_any_platform(client, np_communication_id, platforms, **kwargs):
    last_error = None
    for platform in _sorted_platforms(platforms):
        try:
            return list(client.trophies(np_communication_id, platform, **kwargs)), platform
        except Exception as e:
            last_error = e
            continue
    raise last_error or ValueError("No trophies found for any platform.")


def get_recently_played_games(params, **kwargs):
    try:
        client = _get_client()
        count = params.get("count", 10)

        games = []
        for title in client.title_stats(limit=count):
            games.append({
                "title_id": title.title_id,
                "name": title.name,
                "platform": title.category.value if title.category else None,
                "play_count": title.play_count,
                "play_duration_seconds": _duration_seconds(title.play_duration),
                "first_played": _dt(title.first_played_date_time),
                "last_played": _dt(title.last_played_date_time),
            })

        return json.dumps({"success": True, "games": games})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


def get_game_trophies(params, **kwargs):
    try:
        client = _get_client()
        np_communication_id = params.get("np_communication_id")
        title_id = params.get("title_id")
        platform = params.get("platform")

        if not np_communication_id and not title_id:
            raise ValueError("Provide either np_communication_id (with platform) or title_id.")

        if np_communication_id:
            if not platform:
                raise ValueError(
                    "platform is required when np_communication_id is provided directly; "
                    "provide title_id instead to auto-detect it."
                )
            trophies_iter = client.trophies(np_communication_id, _platform_type(platform), include_progress=True)
        else:
            np_communication_id, platforms = _resolve_trophy_title(client, title_id)
            if platform:
                trophies_iter = client.trophies(np_communication_id, _platform_type(platform), include_progress=True)
            else:
                trophies_iter, _ = _fetch_trophies_any_platform(client, np_communication_id, platforms, include_progress=True)

        trophies = []
        earned_count = 0
        platinum_earned = False
        for trophy in trophies_iter:
            earned = bool(trophy.earned)
            if earned:
                earned_count += 1
            trophy_type = trophy.trophy_type.value if trophy.trophy_type else None
            if earned and trophy_type == "platinum":
                platinum_earned = True

            trophies.append({
                "trophy_id": trophy.trophy_id,
                "name": trophy.trophy_name,
                "detail": trophy.trophy_detail,
                "type": trophy_type,
                "hidden": trophy.trophy_hidden,
                "earned": trophy.earned,
                "earned_date": _dt(trophy.earned_date_time),
                "rarity": trophy.trophy_rarity.name if trophy.trophy_rarity else None,
                "earn_rate": trophy.trophy_earn_rate,
            })

        total = len(trophies)
        summary = {
            "total": total,
            "earned": earned_count,
            "unearned": total - earned_count,
            "completion_pct": round(earned_count / total * 100, 1) if total else 0.0,
            "platinum_earned": platinum_earned,
        }

        return json.dumps({"success": True, "summary": summary, "trophies": trophies})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


def get_recent_trophies(params, **kwargs):
    try:
        client = _get_client()
        count = params.get("count", 10)
        titles_to_scan = params.get("titles_to_scan", 10)

        earned = []
        for title in client.trophy_titles(limit=titles_to_scan):
            if not title.np_communication_id or not title.title_platform:
                continue
            try:
                trophies, _ = _fetch_trophies_any_platform(
                    client, title.np_communication_id, title.title_platform, include_progress=True
                )
            except Exception:
                continue

            for trophy in trophies:
                if trophy.earned and trophy.earned_date_time:
                    earned.append({
                        "game": title.title_name,
                        "trophy_id": trophy.trophy_id,
                        "name": trophy.trophy_name,
                        "type": trophy.trophy_type.value if trophy.trophy_type else None,
                        "earned_date": _dt(trophy.earned_date_time),
                        "_sort_key": trophy.earned_date_time,
                    })

        earned.sort(key=lambda t: t["_sort_key"], reverse=True)
        for t in earned:
            del t["_sort_key"]

        return json.dumps({"success": True, "trophies": earned[:count]})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


def list_owned_games(params, **kwargs):
    try:
        client = _get_client()
        count = params.get("count", 50)
        games_only = params.get("games_only", True)

        games = []
        for entitlement in client.game_entitlements(page_size=100):
            if games_only and entitlement.get("isGame") is False:
                continue

            title_meta = entitlement.get("titleMeta") or {}
            game_meta = entitlement.get("gameMeta") or {}
            games.append({
                "title_id": title_meta.get("titleId"),
                "name": title_meta.get("name") or game_meta.get("name"),
                "active": entitlement.get("activeFlag"),
                "active_date": entitlement.get("activeDate"),
            })

            if len(games) >= count:
                break

        return json.dumps({"success": True, "games": games})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


def check_game_owned(params, **kwargs):
    try:
        client = _get_client()
        title_id = params.get("title_id")
        name = params.get("name")
        if not title_id and not name:
            raise ValueError("Provide either title_id or name.")

        if title_id:
            matches = list(client.game_entitlements(title_ids=[title_id]))
        else:
            matches = [
                e for e in client.game_entitlements(page_size=500)
                if name.lower() in ((e.get("titleMeta") or {}).get("name") or "").lower()
            ]

        owned = len(matches) > 0
        matched_games = [
            {
                "title_id": (m.get("titleMeta") or {}).get("titleId"),
                "name": (m.get("titleMeta") or {}).get("name"),
            }
            for m in matches
        ]

        return json.dumps({"success": True, "owned": owned, "matches": matched_games})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


def get_online_friends(params, **kwargs):
    try:
        client = _get_client()

        friends = list(client.friends_list(limit=1000))
        online_id_by_account_id = {f.account_id: f.online_id for f in friends}
        account_ids = list(online_id_by_account_id.keys())

        online_friends = []
        for i in range(0, len(account_ids), 100):
            chunk = account_ids[i:i + 100]
            presences = client.get_presences(chunk).get("basicPresences", [])
            for presence in presences:
                platform_info = presence.get("primaryPlatformInfo") or {}
                if platform_info.get("onlineStatus") != "online":
                    continue

                games = presence.get("gameTitleInfoList") or []
                online_friends.append({
                    "online_id": online_id_by_account_id.get(presence.get("accountId")),
                    "account_id": presence.get("accountId"),
                    "platform": platform_info.get("platform"),
                    "availability": presence.get("availability"),
                    "playing": games[0].get("titleName") if games else None,
                })

        return json.dumps({"success": True, "friends": online_friends})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


def search_games(params, **kwargs):
    try:
        psnawp = _get_psnawp()
        query = params.get("query")
        if not query:
            raise ValueError("Missing required parameter: query")
        count = params.get("count", 10)

        results = []
        for item in psnawp.search(query, SearchDomain.FULL_GAMES, limit=count):
            result = item.get("result") or {}
            price = result.get("price") or {}
            results.append({
                "concept_id": item.get("id"),
                "name": result.get("name"),
                "invariant_name": result.get("invariantName"),
                "type": result.get("itemType"),
                "platforms": result.get("platforms"),
                "classification": result.get("storeDisplayClassification"),
                "price": price.get("basePrice"),
                "discounted_price": price.get("discountedPrice"),
                "is_free": price.get("isFree"),
            })

        return json.dumps({"success": True, "results": results})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})
