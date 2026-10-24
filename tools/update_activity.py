#!/usr/bin/env python3
"""Fetch aggregate GitHub activity and render self-contained profile SVGs.

Offline: python3 tools/update_activity.py --input /path/to/graphql.json
Live: GITHUB_TOKEN=... python3 tools/update_activity.py --user Medgleiguem
Only aggregate counts, calendar dates, and public-repository languages are saved.
"""
import argparse
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import urllib.error
import urllib.request

from generate_assets import render_workbench


REPOSITORIES = """repositories(first: 100, after: $cursor, privacy: PUBLIC, ownerAffiliations: OWNER) {
  pageInfo { hasNextPage endCursor }
  nodes { stargazerCount languages(first: 100) { edges { size node { name color } } } }
}"""
QUERY = """query($login: String!, $cursor: String) {
  user(login: $login) {
    login followers { totalCount }
    contributionsCollection {
      contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
    }
    """ + REPOSITORIES + """
  }
}"""
REPOSITORIES_QUERY = "query($login: String!, $cursor: String) { user(login: $login) { " + REPOSITORIES + " } }"


class ActivityError(ValueError):
    """A credential-free error message safe to show in workflow logs."""


def checked_count(value):
    if type(value) is not int or value < 0:
        raise ActivityError("GitHub returned an invalid aggregate count")
    return value


def fetch_activity(login):
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise ActivityError("Set GITHUB_TOKEN for a live refresh, or use --input")

    def request(query, cursor=None):
        body = json.dumps({"query": query, "variables": {"login": login, "cursor": cursor}}).encode()
        req = urllib.request.Request("https://api.github.com/graphql", data=body, headers={
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json", "User-Agent": "profile-activity-generator",
        })
        try:
            with urllib.request.urlopen(req, timeout=45) as response:
                result = json.load(response)
        except (urllib.error.URLError, json.JSONDecodeError):
            raise ActivityError("GitHub activity request failed; previous snapshot retained") from None
        if result.get("errors") or not result.get("data", {}).get("user"):
            raise ActivityError("GitHub did not return complete activity data; previous snapshot retained")
        return result

    result = request(QUERY)
    repositories = result["data"]["user"]["repositories"]
    page = repositories
    cursors = set()
    while page["pageInfo"]["hasNextPage"]:
        cursor = page["pageInfo"]["endCursor"]
        if not cursor or cursor in cursors:
            raise ActivityError("GitHub repository pagination failed; previous snapshot retained")
        cursors.add(cursor)
        page = request(REPOSITORIES_QUERY, cursor)["data"]["user"]["repositories"]
        repositories["nodes"].extend(page["nodes"])
    return result


def summarize(payload, login, today):
    """Allowlist the response and derive date-based statistics without repo identifiers."""
    if payload.get("errors") or not payload.get("data", {}).get("user"):
        raise ActivityError("GitHub did not return complete activity data; previous snapshot retained")
    user = payload["data"]["user"]
    if user["login"].lower() != login.lower():
        raise ActivityError("GitHub returned a different profile; previous snapshot retained")
    collection = user["contributionsCollection"]
    calendar = collection["contributionCalendar"]
    days = {}
    for week in calendar["weeks"]:
        for item in week["contributionDays"]:
            day = date.fromisoformat(item["date"])
            if day in days:
                raise ActivityError("GitHub returned duplicate calendar dates")
            count = checked_count(item["contributionCount"])
            if day > today:
                if count:
                    raise ActivityError("GitHub returned contributions dated in the future")
                continue
            days[day] = count
    if not days:
        raise ActivityError("GitHub returned an empty contribution calendar")
    ordered = sorted(days)
    longest = run = 0
    previous = None
    for day in ordered:
        if days[day] > 0:
            run = run + 1 if previous == day - timedelta(days=1) else 1
            longest = max(longest, run)
        else:
            run = 0
        previous = day
    anchor = today if days.get(today, 0) else today - timedelta(days=1)
    current = 0
    while days.get(anchor, 0):
        current += 1
        anchor -= timedelta(days=1)
    language_bytes = defaultdict(int)
    stars = 0
    for repository in user["repositories"]["nodes"]:
        stars += checked_count(repository["stargazerCount"])
        for edge in repository["languages"]["edges"]:
            name = edge["node"]["name"]
            if not isinstance(name, str) or not name:
                raise ActivityError("GitHub returned an invalid language name")
            language_bytes[name] += checked_count(edge["size"])
    total_bytes = sum(language_bytes.values())
    languages = [{"name": name, "bytes": size, "percent": round(100 * size / total_bytes, 2)}
                 for name, size in sorted(language_bytes.items(), key=lambda item: (-item[1], item[0])) if size]
    return {
        "schema_version": 1, "login": user["login"], "as_of": today.isoformat(),
        "updated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "window": {"start": ordered[0].isoformat(), "end": ordered[-1].isoformat()},
        "stats": {
            "total_contributions": checked_count(calendar["totalContributions"]),
            "active_days": sum(count > 0 for count in days.values()),
            "current_streak": current, "longest_streak": longest,
            "last_30_days": sum(count for day, count in days.items()
                                if today - timedelta(days=29) <= day <= today),
            "followers": checked_count(user["followers"]["totalCount"]), "public_stars": stars,
        },
        "calendar": [{"date": day.isoformat(), "count": days[day]} for day in ordered],
        "public_languages": languages,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--user", default="Medgleiguem")
    parser.add_argument("--input", type=Path, help="Use a saved GraphQL response instead of the network")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--today", type=date.fromisoformat, default=datetime.now(timezone.utc).date(), help="UTC date override for reproducible tests")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?", args.user):
        parser.error("--user must be a valid GitHub login")
    try:
        raw = json.loads(args.input.read_text()) if args.input else fetch_activity(args.user)
        snapshot = summarize(raw, args.user, args.today)
        outputs = {"data/activity.json": json.dumps(snapshot, indent=2, ensure_ascii=False)+"\n"}
        for mobile in (False, True):
            for animated in (True, False):
                name = "assets/workbench"+("-mobile" if mobile else "")+("" if animated else "-static")+".svg"
                outputs[name] = render_workbench(snapshot, mobile, animated)+'\n'
        # Prepare and validate every output before replacing any previous snapshot.
        import xml.etree.ElementTree as ET
        for name, content in outputs.items():
            if name.endswith(".svg"):
                ET.fromstring(content)
        staged = []
        try:
            for name, content in outputs.items():
                target = args.output_dir / name
                target.parent.mkdir(parents=True, exist_ok=True)
                with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=target.parent, delete=False) as temporary:
                    temporary.write(content)
                    staged.append((Path(temporary.name), target))
            for temporary, target in staged:
                temporary.replace(target)
        finally:
            for temporary, _ in staged:
                temporary.unlink(missing_ok=True)
    except (ValueError, KeyError, TypeError, OSError) as error:
        # Never print response bodies, credentials, or arbitrary server error messages.
        message = str(error) if isinstance(error, ActivityError) else "Activity refresh failed validation; previous snapshot retained"
        print(message, file=sys.stderr)
        return 1
    print("Refreshed aggregate activity snapshot and four workbench variants.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
