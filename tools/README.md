# Maintaining the profile

The README is a GitHub-native animated portfolio. Self-hosted SVGs contain custom artwork and CSS motion; substantive project notes and links also exist as native Markdown. Desktop and mobile compositions are separate, and all animation respects reduced motion. It uses no JavaScript embeds, remote statistics widgets or external font services.

## Commands

```sh
python3 tools/generate_assets.py
python3 -m unittest discover -s tools -p 'test_*.py' -v
python3 tools/verify_profile.py
```

The asset generator uses only the Python standard library. Technology paths are vendored from [Simple Icons](https://github.com/simple-icons/simple-icons) under the included [CC0 license](../assets/icons/LICENSE.md); brand names and logos remain their owners’ trademarks. `tools/icons.json` lists the chosen icons. Keep generated files and their source in the same change.

## Daily activity

`.github/workflows/profile-activity.yml` refreshes activity at 06:00 UTC and can be run manually. It requests aggregate calendar/count data and public-repository language bytes through GitHub GraphQL. It never requests or stores private repository identifiers. GitHub-visible totals may include private contribution aggregates when the token and profile settings make them available; public language shares do not describe private repositories. No private access token is required for the default workflow.

An optional `PROFILE_ACTIVITY_TOKEN` repository secret can be used if the owner wants different account visibility. Never put tokens in files, README URLs or logs. The output prints its actual calendar window and last successful update date. A failed API request leaves the previous successful data and images intact and fails the workflow visibly.

Offline development can use `python3 tools/update_activity.py --input /path/to/graphql-response.json`. Raw API responses are not committed. Only the allowlisted `data/activity.json` and eight dashboard/skyline variants are published. The skyline uses real weekly totals and labels the shorter phone window. Tests cover streaks, missing days, empty today, the last-30-days boundary, failed API responses, privacy filtering and proportional skyline heights.

## Contribution animation

`.github/workflows/snake.yml` refreshes the Platane/snk animation every 12 hours. `tools/style_snake.py` applies the profile background and generates its matching static fallback. The two writing workflows share a concurrency group, stage only their own outputs and pull with rebase before normal pushes. Push path filters avoid regeneration loops. `Profile checks` uses read-only permissions and validates tests, assets, image references and deterministic artwork generation.

## Content and verification

Institutional figures and career details are based on the owner’s supplied CV; project descriptions also use project documentation. Ongoing research and in-design work are labeled accordingly. Do not imply authorship of third-party tools or link to private repository backups. Do not publish credentials or internal documents.

Before publishing, run the commands above, check the GitHub-rendered README at phone and desktop widths, inspect light/dark themes, verify animation and reduced motion, and open public project links signed out. Preserve history with normal fast-forward pushes. Workflows display failures rather than silently publishing fabricated or zeroed statistics.
