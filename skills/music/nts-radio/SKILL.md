---
name: nts-radio
description: Check what's currently playing on NTS Radio and what's coming up next.
version: 0.1.0
metadata:
  hermes:
    tags:
      - Music
      - Radio
---

# NTS Radio

Fetch live now-playing and next-up info for NTS Radio's two channels, using curl and jq against the NTS live API.

NTS Radio is a London-based online radio station with a global audience, broadcasting a wide range of music and talk shows.

## Fetching data

```bash
curl -s https://www.nts.live/api/v2/live
```

No auth required. Response shape:

```json
{
  "results": [
    { "channel_name": "1", "now": { ... }, "next": { ... } },
    { "channel_name": "2", "now": { ... }, "next": { ... } }
  ]
}
```

Each `now`/`next` object has `broadcast_title`, `start_timestamp`, `end_timestamp`, and
`embeds.details` with the show's `name`, `description`, `location_long`, `genres`
(array of `{id, value}`), `moods`, and a `links` array (`rel: "self"` gives the episode API URL).

This endpoint only exposes the current and next broadcast per channel — there is no
further-ahead schedule available from the API.

## Common queries

Now playing on both channels, with time range and genres:

```bash
curl -s https://www.nts.live/api/v2/live | jq -r '
  .results[] |
  "Channel \(.channel_name): \(.now.broadcast_title)
    \(.now.start_timestamp | split("T")[1][0:5])-\(.now.end_timestamp | split("T")[1][0:5])
    Genres: \([.now.embeds.details.genres[].value] | join(", "))"
'
```

Now + next for both channels:

```bash
curl -s https://www.nts.live/api/v2/live | jq -r '
  .results[] |
  "Channel \(.channel_name)\n  Now:  \(.now.broadcast_title)\n  Next: \(.next.broadcast_title)"
'
```

Just one channel (e.g. channel 1):

```bash
curl -s https://www.nts.live/api/v2/live | jq '.results[] | select(.channel_name == "1")'
```

## Notes

- `start_timestamp`/`end_timestamp` include the show's local timezone offset (e.g.
  `2026-07-09T17:00:00+01:00`); render times as-is rather than converting, since that's
  the timezone NTS itself reports the broadcast in.
- `embeds.details` may be missing fields depending on the show (e.g. `genres`/`moods`
  can be empty arrays) — guard jq filters with `// []` or `// "unknown"` where useful.
- (R) in the title indicates a repeat broadcast.
