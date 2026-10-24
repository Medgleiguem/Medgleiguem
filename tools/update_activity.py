#!/usr/bin/env python3
"""Fetch aggregate GitHub activity and render self-contained profile SVGs.

Offline: python3 tools/update_activity.py --input /path/to/graphql.json
Live: GITHUB_TOKEN=... python3 tools/update_activity.py --user Medgleiguem
Only aggregate counts, calendar dates, and public-repository languages are saved.
"""
import argparse
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from html import escape
import json
import math
import os
from pathlib import Path
import re
import sys
import tempfile
import urllib.error
import urllib.request


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
COLORS = ["#22d3ee", "#a78bfa", "#34d399", "#fbbf24"]


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


def text(x, y, value, size=20, fill="#eef2ff", weight=400, extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" {extra}>{escape(str(value))}</text>'


def panel(x, y, width, height, radius=20, fill="#111a2e"):
    return f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" fill="{fill}" stroke="#26334e"/>'


def render_svg(data, mobile=False, animated=True):
    """Render the same verified snapshot in two layouts and motion preferences."""
    width, height = (600, 1450) if mobile else (1000, 880)
    margin = 32 if mobile else 40
    label_size = 24 if mobile else 20
    output = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
              '<title id="title">Medgleiguem · GitHub activity</title>',
              '<desc id="desc">' + escape(
                  f"{data['stats']['total_contributions']:,} GitHub-visible contributions; "
                  f"{data['stats']['active_days']} active days; current streak {data['stats']['current_streak']} days; "
                  f"longest streak {data['stats']['longest_streak']} days. "
                  f"Calendar window {data['window']['start']} to {data['window']['end']}. "
                  "Language shares cover public repositories only. "
                  f"Updated {data['updated_at']}.") + '</desc>',
              '<defs><linearGradient id="accent"><stop stop-color="#22d3ee"/><stop offset="1" stop-color="#a78bfa"/></linearGradient></defs>',
              '<style>text{font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}']
    if animated:
        output.append('@keyframes breathe{0%,100%{opacity:.6}50%{opacity:1}}@keyframes grow{from{transform:scaleX(.15)}to{transform:scaleX(1)}}.beacon{animation:breathe 4s ease-in-out infinite}.language-fill{transform-box:fill-box;transform-origin:left;animation:grow 1.8s ease-out both}@media(prefers-reduced-motion:reduce){.beacon,.language-fill{animation:none}}')
    output.extend(['</style>', f'<rect width="{width}" height="{height}" rx="28" fill="#0b1020"/>',
                   f'<rect x="{margin}" y="0" width="{width-2*margin}" height="3" fill="url(#accent)"/>'])
    output.append(text(margin, 57, "ACTIVITY / UTC", label_size, "#a78bfa", 650))
    output.append(f'<circle class="beacon" cx="{width-margin-7}" cy="49" r="6" fill="#34d399"/>')
    output.append(text(margin, 111, "The work, in motion.", 35 if mobile else 40, weight=700))
    output.append(text(margin, 148 if mobile else 147, "A daily GitHub snapshot.", 24 if mobile else 22, "#b7c3dc"))
    stats = data["stats"]
    cards = [("total_contributions", ["GitHub-visible", "contributions"], "#22d3ee"),
             ("active_days", ["Active days", "in this window"], "#34d399"),
             ("current_streak", ["Current streak", "days"], "#a78bfa"),
             ("longest_streak", ["Longest streak", "days in window"], "#22d3ee")]
    card_width = 256 if mobile else 217
    for index, (key, labels, color) in enumerate(cards):
        x = margin + (index % 2) * 280 if mobile else margin + index * 234
        y = 183 + (index // 2) * 164 if mobile else 185
        output.append(panel(x, y, card_width, 148 if mobile else 150))
        output.append(text(x+20, y+58, f"{stats[key]:,}", 44 if mobile else 43, color, 750))
        output.append(text(x+20, y+98, labels[0], label_size, weight=550))
        output.append(text(x+20, y+128, labels[1], label_size, "#b7c3dc"))
    detail_y = 538 if mobile else 377
    output.append(text(margin, detail_y, f"{stats['last_30_days']:,} contributions in the last 30 days", 24 if mobile else 22, "#b7c3dc"))
    output.append(text(margin, 589 if mobile else 426, "Contribution calendar", 28 if mobile else 25, weight=650))
    dates = {date.fromisoformat(day["date"]): day["count"] for day in data["calendar"]}
    first = min(dates)
    sunday = first - timedelta(days=(first.weekday()+1) % 7)
    weeks = math.ceil(((max(dates)-sunday).days+1)/7)
    groups = [(0, min(27, weeks)), (27, weeks)] if mobile and weeks > 27 else [(0, weeks)]
    maximum = max(dates.values(), default=0)
    for group_index, (start_week, end_week) in enumerate(groups):
        base_y = 654 + group_index * 230 if mobile else 478
        cell, gap = (15, 4) if mobile else (13, 4)
        pitch = cell + gap
        month_positions = []
        last_month = None
        for column in range(start_week, end_week):
            label_day = max(sunday + timedelta(days=column*7), first)
            month = label_day.strftime("%b")
            if month != last_month:
                month_positions.append((column, month))
                last_month = month
        # Omit a partial month label when it would collide with the next month.
        labels = {}
        for index, (column, month) in enumerate(month_positions):
            next_column = month_positions[index+1][0] if index+1 < len(month_positions) else end_week
            if next_column-column >= 3:
                labels[column] = month
        for column in range(start_week, end_week):
            week_start = sunday + timedelta(days=column*7)
            if column in labels:
                output.append(text(margin+(column-start_week)*pitch, base_y-17, labels[column], label_size, "#b7c3dc"))
            for row in range(7):
                day = week_start + timedelta(days=row)
                if day not in dates:
                    continue
                count = dates[day]
                level = 0 if not count else min(4, max(1, math.ceil(4 * math.sqrt(count / maximum))))
                color = ["#1c2941", "#154c63", "#177e91", "#22b2c3", "#47e5d0"][level]
                x, y = margin+(column-start_week)*pitch, base_y+row*pitch
                output.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{color}"><title>{day.isoformat()}: {count} contributions</title></rect>')
        if mobile:
            block_start = max(sunday+timedelta(days=start_week*7), first)
            block_end = min(sunday+timedelta(days=end_week*7-1), max(dates))
            output.append(text(margin, base_y+164, f"{block_start:%d %b %Y} – {block_end:%d %b %Y}", 24, "#b7c3dc"))
    legend_y = 1081 if mobile else 625
    output.append(text(margin, legend_y, "Less", label_size, "#b7c3dc"))
    for index, color in enumerate(["#1c2941", "#154c63", "#177e91", "#22b2c3", "#47e5d0"]):
        output.append(f'<rect x="{margin+69+index*25}" y="{legend_y-18}" width="18" height="18" rx="3" fill="{color}"/>')
    output.append(text(margin+208, legend_y, "More", label_size, "#b7c3dc"))
    language_y = 1140 if mobile else 684
    output.append(text(margin, language_y, "Public-repository languages", 27 if mobile else 25, weight=650))
    languages = list(data["public_languages"][:3])
    remaining = data["public_languages"][3:]
    if remaining:
        languages.append({"name": "Other", "percent": sum(item["percent"] for item in remaining)})
    if not languages:
        output.append(text(margin, language_y+45, "No public language data available.", label_size, "#b7c3dc"))
    for index, item in enumerate(languages):
        x = margin if mobile else margin + (index % 2) * 480
        y = language_y+43+index*43 if mobile else language_y+43+(index//2)*48
        name = item["name"] if len(item["name"]) <= 20 else item["name"][:19]+"…"
        output.append(f'<circle cx="{x+6}" cy="{y-7}" r="5" fill="{COLORS[index]}"/>')
        output.append(text(x+21, y, name, label_size))
        output.append(text(x+(530 if mobile else 438), y, f"{item['percent']:.1f}%", label_size, "#b7c3dc", extra='text-anchor="end"'))
        output.append(f'<rect x="{x+21}" y="{y+9}" width="{max(1, item["percent"] / 100 * (490 if mobile else 415)):.1f}" height="3" rx="1.5" fill="{COLORS[index]}" class="language-fill"/>')
    footer_y = 1370 if mobile else 823
    if mobile:
        output.append(text(margin, footer_y-26, "Public language bytes · aggregate activity", 24, "#b7c3dc"))
        output.append(text(margin, footer_y+10, f"Updated {data['updated_at'][:10]} · UTC", 24, "#b7c3dc"))
        output.append(text(margin, footer_y+46, f"Window {data['window']['start']} → {data['window']['end']}", 24, "#b7c3dc"))
    else:
        output.append(text(margin, footer_y, "Public language bytes · aggregate activity only", 20, "#b7c3dc"))
        output.append(text(margin, footer_y+33, f"Window {data['window']['start']} → {data['window']['end']} · Updated {data['updated_at'][:10]} UTC", 20, "#b7c3dc"))
    output.append('</svg>')
    return "\n".join(output)+"\n"


def render_skyline(data, mobile=False, animated=True):
    """Weekly columns use linear heights; mobile shows the most recent 27 weeks."""
    days = {date.fromisoformat(item["date"]): item["count"] for item in data["calendar"]}
    first, last = min(days), max(days)
    first_sunday = first - timedelta(days=(first.weekday()+1) % 7)
    week_count = ((last-first_sunday).days // 7)+1
    start_index = max(0, week_count-27) if mobile else 0
    weeks = []
    for index in range(start_index, week_count):
        sunday = first_sunday + timedelta(days=index*7)
        count = sum(days.get(sunday+timedelta(days=offset), 0) for offset in range(7))
        weeks.append((sunday, count))
    maximum = max((count for _, count in weeks), default=0)
    width, height = (600, 600) if mobile else (1000, 500)
    margin, font = (32, 24) if mobile else (40, 20)
    baseline, max_height = (421, 214) if mobile else (355, 190)
    chart_width = width-2*margin-8
    pitch = chart_width/len(weeks)
    bar_width = min(pitch*.58, 38)
    depth = min(pitch*.25, 7)
    window_start = max(first, weeks[0][0])
    window_end = last
    scope = "Last 27 weeks" if mobile and start_index else f"{len(weeks)} weeks in this window"
    output = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="skyline-title skyline-desc">',
              '<title id="skyline-title">Medgleiguem · contribution skyline</title>',
              '<desc id="skyline-desc">'+escape(
                  f"{scope}. {sum(count for _, count in weeks):,} GitHub-visible contributions "
                  f"from {window_start.isoformat()} to {window_end.isoformat()}. "
                  f"Each column is one Sunday-starting week; height is proportional to its actual contribution count. "
                  f"The tallest week has {maximum:,} contributions. Updated {data['updated_at']}.")+'</desc>',
              '<defs><linearGradient id="skyline-face" x1="0" y1="1" x2="0" y2="0"><stop stop-color="#126179"/><stop offset="1" stop-color="#22d3ee"/></linearGradient><linearGradient id="skyline-accent"><stop stop-color="#a78bfa"/><stop offset="1" stop-color="#22d3ee"/></linearGradient></defs>',
              '<style>text{font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}.skyline-column{transform-box:fill-box;transform-origin:center bottom}.skyline-scan{opacity:0}']
    if animated:
        output.append('@keyframes skyline-rise{from{transform:scaleY(.08);opacity:.5}to{transform:scaleY(1);opacity:1}}@keyframes skyline-shine{0%,100%{opacity:0}35%,55%{opacity:.72}}.skyline-column{animation:skyline-rise 1.2s cubic-bezier(.18,.7,.25,1) both;animation-delay:var(--rise-delay)}.skyline-scan{animation:skyline-shine 6s ease-in-out infinite;animation-delay:var(--scan-delay)}@media(prefers-reduced-motion:reduce){.skyline-column,.skyline-scan{animation:none}}')
    output.extend(['</style>', f'<rect width="{width}" height="{height}" rx="28" fill="#0b1020"/>',
                   f'<rect x="{margin}" width="{width-2*margin}" height="3" fill="url(#skyline-accent)"/>',
                   text(margin, 48, "CONTRIBUTION SKYLINE", font, "#a78bfa", 650),
                   text(margin, 98, "Built one week at a time.", 32 if mobile else 35, weight=700),
                   text(margin, 137, "Weekly GitHub-visible contributions", 24 if mobile else 22, "#b7c3dc")])
    if mobile:
        output.append(text(margin, 176, scope, 24, "#34d399", 550))
    # Ground plane and guides give depth without altering contribution heights.
    for fraction in (.25, .5, .75, 1):
        y = baseline-max_height*fraction
        output.append(f'<path d="M {margin} {y:.2f} H {width-margin}" stroke="#1b2940" stroke-width="1" stroke-dasharray="3 8"/>')
    output.append(f'<path d="M {margin} {baseline} L {width-margin-7} {baseline} L {width-margin} {baseline-7}" stroke="#3d506e" fill="none"/>')
    month_positions = []
    previous_month = None
    for index, (week, count) in enumerate(weeks):
        x = margin+index*pitch
        bar_height = max_height*count/maximum if maximum else 0
        y = baseline-bar_height
        title = f"Week of {week.isoformat()}: {count:,} contributions"
        output.append(f'<g class="skyline-column" data-week="{week.isoformat()}" data-count="{count}" style="--rise-delay:{index*.018:.3f}s"><title>{escape(title)}</title>')
        output.append(f'<rect data-face="front" x="{x:.2f}" y="{y:.2f}" width="{bar_width:.2f}" height="{bar_height:.4f}" fill="url(#skyline-face)"/>')
        if count:
            output.append(f'<path d="M {x+bar_width:.2f} {y:.2f} l {depth:.2f} {-depth:.2f} v {bar_height:.4f} l {-depth:.2f} {depth:.2f} Z" fill="#296785"/>')
            output.append(f'<path d="M {x:.2f} {y:.2f} l {depth:.2f} {-depth:.2f} h {bar_width:.2f} l {-depth:.2f} {depth:.2f} Z" fill="#84f1de"/>')
            if animated:
                output.append(f'<rect class="skyline-scan" x="{x:.2f}" y="{y:.2f}" width="{bar_width:.2f}" height="{bar_height:.4f}" fill="#a78bfa" style="--scan-delay:{index*.085:.3f}s"/>')
        else:
            output.append(f'<path d="M {x:.2f} {baseline} h {bar_width:.2f}" stroke="#33435f" stroke-width="2"/>')
        output.append('</g>')
        label_date = max(first, week)
        if label_date.month != previous_month:
            month_positions.append((index, label_date.strftime("%b")))
            previous_month = label_date.month
    minimum_label_spacing = 3 if mobile else 4
    for index, (column, month) in enumerate(month_positions):
        next_column = month_positions[index+1][0] if index+1 < len(month_positions) else len(weeks)
        if next_column-column >= minimum_label_spacing:
            output.append(text(round(margin+column*pitch, 2), baseline+36, month, font, "#b7c3dc"))
    summary_y = 503 if mobile else 428
    output.append(text(margin, summary_y, f"{sum(count for _, count in weeks):,} contributions · peak week {maximum:,}", font, "#eef2ff", 550))
    if not mobile:
        output.append(text(margin, summary_y+30, f"{scope} · bar height = actual weekly total", 20, "#b7c3dc"))
    output.append(text(margin, 548 if mobile else 484, f"{window_start.isoformat()} → {window_end.isoformat()}", font, "#b7c3dc"))
    if mobile:
        output.append(text(margin, 582, f"Updated {data['updated_at'][:10]} UTC", 24, "#b7c3dc"))
    output.append('</svg>')
    return "\n".join(output)+"\n"


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
                name = "assets/activity"+("-mobile" if mobile else "")+("" if animated else "-static")+".svg"
                outputs[name] = render_svg(snapshot, mobile, animated)
                name = "assets/skyline"+("-mobile" if mobile else "")+("" if animated else "-static")+".svg"
                outputs[name] = render_skyline(snapshot, mobile, animated)
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
    print("Refreshed aggregate activity snapshot and eight SVG variants.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
