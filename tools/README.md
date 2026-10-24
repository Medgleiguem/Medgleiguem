# Maintaining the observatory

The profile uses an original dark anime world to introduce eight major systems and two research tracks. Ten linked animated vector cards supply short project identities; the substantive text lives in public engineering briefs. The main page stays visual and concise. Keep those briefs specific about mechanisms, collaboration and current implementation status. Institutional names do not establish deployment, adoption, correctness or scale.

## Build and verify

```sh
python3 tools/generate_assets.py
python3 -m unittest discover -s tools -p 'test_*.py' -v
python3 tools/verify_profile.py
```

Generation uses the Python standard library and is deterministic for the checked-in JPEG exports and sanitized activity snapshot. The [artwork provenance and exact prompts](../assets/artwork/observatory/README.md) document the built-in image-generation process. JPEG exports are embedded as data URIs in the SVG panoramas; signals, light, research marks and camera transforms animate separately. Do not describe still illustration plus vector motion as hand-animated character footage.

The panorama families are `observatory`, `exchange` and `identity`, with `workbench` and `tools-rail` supporting panels. These have desktop/mobile/explicit-static variants. `tools/project_cards.py` supplies ten distinct vector diagrams under `assets/projects/`; each has an explicit static variant. Linked cards have fixed display widths and wrap naturally into rows or a mobile column without custom CSS. Project identities never wait for a carousel; full prose is in the linked briefs. Mobile artwork has its own composition and legible labels. The README's `<picture>` sources select explicit static files for reduced motion, including the combined mobile/reduced case. SVG media rules alone do not reliably establish that the browser selected still imagery.

The verifier checks self-contained JPEGs, SVG identifiers/references, image paths, alternative text, local Markdown/HTML links and the profile's repository-link allowlist. Scripts, foreign objects, event handlers, remote image references and embedded SVG images are rejected. Broken links to unpublished files outside the repository are rejected too. Keep private source evidence, local project paths, customer documents, biometric images and deployment details out of public briefs.

## Activity refresh

`.github/workflows/profile-activity.yml` refreshes at 06:00 UTC, manually, or when its relevant collector/renderer files change. It retains the allowlisted GraphQL collection boundary: aggregate counts/calendar dates and public-repository language bytes only, with no private repository identifiers. The snapshot schema remains compatible, while the profile displays one compact workbench chart.

The chart shows at most 84 calendar days grouped into consecutive buckets of up to seven days. Missing dates contribute zero. A short calendar keeps its actual bounds; the last bucket may be partial. Both layouts use identical counts and proportional bar heights. Bar titles include each date range and count. The chart prints its displayed total, peak bucket count, actual window and UTC snapshot date. Contributions are not hours worked or a project-quality score.

```sh
python3 tools/update_activity.py --input /path/to/saved-graphql-response.json
```

Live refresh uses `GITHUB_TOKEN`. The workflow defaults to GitHub's built-in token; optional `PROFILE_ACTIVITY_TOKEN` changes aggregate visibility. Never store credentials in files, URLs or logs. All outputs are prepared and validated before replacing the previous snapshot. API or input validation failures retain previous artifacts and fail visibly. Only `data/activity.json` and four `workbench*.svg` files are staged by the refresh job. Its concurrency group and normal rebase/push behavior avoid overwriting other profile work.

## Rendering checks

The `Profile checks` workflow uses read-only permissions, runs tests and the verifier, then checks deterministic generation. Before publishing a visual change, inspect the actual GitHub-rendered README at desktop, 390 px and 320 px, normal and reduced motion, and light/dark GitHub themes. Confirm that embedded raster art actually paints, not merely that the SVG wrapper loads. Compare frames to establish normal motion and static fallback behavior; check clipping, text size and every project destination. Local HTML is useful for diagnosis but does not establish GitHub compatibility.

The original scene illustrations are fictional; the landmark geometry and scansion patterns are illustrative methods, not real biometric data or validated research output. Keep technologies tied to their actual projects, distinguish incomplete integrations from implemented workflows, and preserve the user's priority order: substantial systems and research first, minor public experiments last.

Custom HTML anchor IDs receive GitHub’s `user-content-` prefix. The top navigation and brief return links address those sanitized IDs explicitly. The verifier checks the custom profile navigation; verify actual scrolling after changes.
