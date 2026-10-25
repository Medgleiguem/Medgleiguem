# Maintaining the expertise profile

The main profile shows eight domains with methods, contextual tools and representative work. The domain index in `work/README.md` provides native text and individual project links. The CV supports broad toolkit/practice claims; the ten source-reviewed briefs describe actual implementations and current boundaries. Do not turn tool lists into claims that every tool is used in every example. Keep institutional source code, private identifiers and unsupported adoption/scale claims out of public content.

## Build

```sh
python3 tools/generate_assets.py
python3 -m unittest discover -s tools -p 'test_*.py' -v
python3 tools/verify_profile.py
```

`tools/expertise.py` owns the eight domain definitions, short vector header, bespoke animated method sketches and contextual tool marks. `tools/desert_console.py` supplies shared SVG primitives, the tested static serializer and the real contribution-calendar renderer. `tools/generate_assets.py` emits four variants of `desert`, six variants of each `domains/<slug>` row, and six `workbench` variants. Domain rows have phone, compact tablet and desktop compositions, each with a static counterpart. All generation uses the Python standard library and locally vendored inputs. The old generated landscape is archived; it is no longer served in the main profile. Artwork/icon provenance is in `assets/artwork/desert/README.md`.

Domain rows are ordinary linked GitHub pictures, not webpage-only interactive components. Keep each linked picture inside its own `<p>` HTML block: GitHub's Markdown parser otherwise separates the leading inline anchor from later image markup. Verify that the rendered image's nearest link is the intended domain route, not GitHub's automatic raw-image link. Each leads to an explicit native anchor in the work index. The main images have useful alternative text; the index supplies searchable/readable content. Main `systems`, `research` and `workbench` anchors remain for brief return links. GitHub prefixes custom IDs with `user-content-`; use those sanitized names in fragment targets.

Each domain has distinct illustrative motion, without implying a successful real payment, verified biometric or measured research result. Main content stays visible throughout a loop. Explicit static assets serve reduced-motion users. The 400-unit mobile layouts are composed independently from the 1000-unit desktop rows. The calendar preserves its compact 601–1279 px layout, in addition to mobile and desktop. Check actual GitHub column sizes, text clipping/overlap, meaningful links, normal motion, static behavior and overflow at desktop, tablet, 390 and 320 px before publishing.

## Activity refresh

The collector's allowlisted GraphQL boundary is unchanged: aggregate counts, calendar dates and public-repository language bytes only. It does not request private repository identifiers or event messages. Preserve validation, streak calculations, failure behavior and prepare-before-replacement semantics.

The calendar displays the most recent at most 140 actual window days, filling missing dates with zero. It aligns Sunday-first weeks and prints displayed-window totals/active days, actual range, UTC snapshot date and fixed color buckets: 0, 1–4, 5–19, 20–49, 50+. Data cells never animate or change values; the branch signals are a separate decorative layer. Contributions are not work hours or a project-quality score. Raw data stays linked.

The workflow refreshes at 06:00 UTC, manually or on relevant renderer/collector changes. Its stable collector interface remains `generate_assets.render_workbench(data, mobile=False, animated=True, compact=False)`. It stages only `data/activity.json` and six `workbench*.svg` files, using the existing shared concurrency and normal rebase/push. `PROFILE_ACTIVITY_TOKEN` is optional; never store credentials or log failed API payloads. Refresh/full-generation equivalence is covered by the integration test; copy every renderer dependency into its fixture.

```sh
python3 tools/update_activity.py --input /path/to/saved-graphql-response.json
```

The read-only checks workflow runs tests, verifies safe self-contained SVG/local links and checks deterministic generation. Keep all project briefs reachable from the domain index. There are no fake proficiency meters, invented releases or fabricated public security projects.
