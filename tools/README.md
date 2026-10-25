# Maintaining the profile

The profile shows eight domains with methods, contextual tools and representative work, followed by the annual GitHub board and a grouped toolbox. The illustrated header, domain briefs and CV support different kinds of evidence: a toolkit entry is broader practice, not proof that every tool was used in every listed project. Keep private source code, identifiers and unsupported adoption/scale claims out of public content.

## Generate and verify

```sh
python3 tools/generate_assets.py
python3 -m unittest discover -s tools -p 'test_*.py' -v
python3 tools/verify_profile.py
```

Generation is standard-library Python with local inputs only. It emits64 SVGs: four header,48 domain, six activity and six toolbox variants, plus the native `work/activity.md` summary. `expertise.py` owns domain/toolbox content and original vector marks; the header embeds an optimized local illustration. `desert_console.py` supplies shared SVG primitives and the tested static serializer. `activity_data.py` derives metrics and native tables; `activity_dashboard.py` composes responsive charts. The generator re-exports `render_workbench(data,mobile=False,animated=True,compact=False)` for the collector's stable interface. Copy all renderer dependencies into integration fixtures.

Keep linked domain pictures within individual raw `<p>` blocks: GitHub's Markdown parser otherwise separates the image from its intended link. Domain routes address explicit `user-content-` anchors in `work/README.md`; all10 project briefs remain accessible. Main `systems`, `research` and `workbench` anchors are stable. Main pictures have meaningful alt text; the linked native activity tables and toolbox disclosure provide text equivalents.

## Activity semantics

Calendar cells cover the full returned window, capped at366 days. Missing dates inside that window are zero; no days outside it are invented. The headline total, active days, longest streak and recent weekly bins derive from those exact cells. Current streak ends at `as_of` or yesterday and is zero for an older stale window. Last30 days is inclusive of `as_of` and the prior29 days. Weeks begin Sunday and edge weeks may be partial. Phone calendars split at18 weeks per strip to preserve day-cell size. Calendar colors have fixed buckets:0,1–4,5–19,20–49,50+.

API contribution types are separate counters: commits, pull requests opened, issues opened and pull request reviews. Their collection timestamps are shown separately. They reflect accessible API records; they are not a partition of the calendar total, which can differ. Preserve unavailable fields as null and real zero as zero. Public language bars recompute source-byte proportions; more than five languages become four plus Other. Public-code composition is not a proficiency score or a representation of private/institutional projects. The native summary prints full scopes, values and source definitions.

The live query follows GitHub's official [ContributionsCollection reference](https://docs.github.com/en/graphql/reference/users#contributionscollection). It requests only calendar dates/counts, four aggregate counters/collection dates, follower count and public-repository language/star aggregates. No private repository identifiers, issue titles, messages, branch names or event streams are requested or saved. Never log credentials or API error bodies. Bad responses retain all previous artifacts; validate/render all outputs before replacement.

Data cells, bar heights, numeric labels and language proportions never animate. Original header/architectural traces and toolbox dividers supply motion separately. Explicit static sources serve reduced-motion users. Check actual GitHub at320/390/1024/1440, normal/reduced motion and light mode, including text overlaps, image-link routes, keyboard navigation, snapshot freshness and horizontal overflow. Raw images can remain cached briefly after publication; confirm fresh dimensions/content before declaring live verification complete.

## Refresh automation

The workflow refreshes at06:00 UTC, manually and after relevant collector/renderer changes. It stages only `data/activity.json`, six `workbench*.svg` files and `work/activity.md`. The shared concurrency, ordinary rebase/push and optional `PROFILE_ACTIVITY_TOKEN` remain. No credentials belong in files. The read-only checks run the full suite, SVG/local-link verification and deterministic generation for assets plus the native summary.

```sh
python3 tools/update_activity.py --input /path/to/saved-graphql-response.json
```

Artwork and locally vendored icon provenance is in `assets/artwork/desert/README.md`. Groq uses an original processor mark because an official path was unavailable; SQL/storage/queue/transformation marks are original role symbols. Brand marks identify tools without implying endorsement. No fake proficiency meters, invented security projects or fabricated releases.
