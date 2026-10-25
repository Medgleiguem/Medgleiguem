# Maintaining the desert console

The profile centers on personal identity, original night-desert artwork, actual GitHub activity and a compact tool dock. The [selected work index](../work/README.md) links the ten existing engineering briefs. Keep detailed project descriptions there. Do not add origin slogans, a CV chronology, a portrait or an oversized main-page project catalogue.

## Build and verify

```sh
python3 tools/generate_assets.py
python3 -m unittest discover -s tools -p 'test_*.py' -v
python3 tools/verify_profile.py
```

`tools/desert_console.py` owns the original SVG composition and motion. `tools/generate_assets.py` writes the `desert`, `workbench`, `tools-rail` and `desert-footer` families: desktop, mobile, desktop static and mobile static. Generation uses the Python standard library and checked-in local inputs. The [artwork provenance and exact prompt](../assets/artwork/desert/README.md) record the separate clean illustration and locally vendored CC0 icon paths. No image or font is fetched at render time.

The original illustration is still art. Vector paths, sand highlights, contours and signal traces provide genuine browser animation. Do not describe the result as animated character footage. All names, metrics and essential content have visible base states. The README uses native clickable links for contact, work and research; no fake terminal controls or JavaScript.

Every picture selects explicit static files for reduced motion, including the combined mobile/reduced case. Mobile assets have their own layouts rather than shrinking a full desktop canvas. Inspect desktop, 390 px and 320 px in actual GitHub rendering; a local HTML mockup is insufficient evidence. Check normal/static motion using captured frames, embedded art painting, clipping, link behavior and the served file budget. Targets: under 2 MB per SVG and under 3 MB loaded per viewport.

## Activity and privacy

The existing allowlisted GraphQL collector saves aggregate counts, calendar dates and public-repository language bytes. It never asks for private repository identifiers, messages or events. Keep its validation, streak calculations, error handling and prepare-before-replacement behavior intact. The UI's contribution/active-day metrics are computed from the displayed calendar, rather than relabeling the collector's broader aggregate totals.

The custom calendar displays at most the most recent 140 days, inclusive of the actual snapshot window. Missing calendar dates are zero. A short window keeps its own bounds. Dates align into Sunday-first weeks. Zero cells remain zero; data cells never animate or change color. The moving branch signals are a separate decorative layer. Each cell includes its date and count in SVG metadata/title, while the panel prints actual range and UTC snapshot date. Colors use fixed buckets: 0, 1–4, 5–19, 20–49, 50+. Contributions are neither work hours nor a quality score. Raw data remains linked from the main profile.

`.github/workflows/profile-activity.yml` refreshes at 06:00 UTC, on manual dispatch and on relevant renderer/collector changes. The collector's stable interface remains `generate_assets.render_workbench(data, mobile=False, animated=True)`. It writes only `data/activity.json` and four `workbench*.svg` outputs. The workflow preserves scoped staging, shared concurrency and normal rebase/push. `PROFILE_ACTIVITY_TOKEN` is optional; never publish credentials or log payloads from failed API responses.

```sh
python3 tools/update_activity.py --input /path/to/saved-graphql-response.json
```

The checks workflow uses read-only permissions and verifies tests, safe assets/links and deterministic generation. The refresh/full-generation integration test ensures both paths produce identical workbench files.

## Links and factual boundaries

Keep the `systems`, `research` and `workbench` custom anchors for existing brief return links. GitHub prefixes them with `user-content-`; fragment links use that sanitized name. All ten briefs remain public and reachable from the work index. Do not publish internal paths, customer documents, private source links, biometric examples or unverified deployment/scale claims. Institutional names alone do not establish adoption or correctness.
