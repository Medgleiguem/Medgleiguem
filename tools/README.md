# Profile maintenance

The profile is a personal hacker/anime workspace centered on the owner’s major private systems, language research, tools and real GitHub activity. Career timelines, business-impact metrics and awards are deliberately absent. Keep the copy short, specific and project-led.

## Build and checks

```sh
python3 tools/generate_assets.py
python3 -m unittest discover -s tools -p 'test_*.py' -v
python3 tools/verify_profile.py
```

The generator uses only the Python standard library. The entrance combines [original anime artwork](../assets/artwork/README.md) with SVG rain, a CRT sweep and restrained glitch layers. The two project consoles cover eight selected private systems through animated engineering scope maps. Their index and active diagram share one animation clock. The research panel covers Hassaniya Laghn and Mauritanian Sign Language. Smaller public side projects stay in a disclosure at the bottom. The terminal cycles and types interest lines; the loadout uses vendored [Simple Icons](https://github.com/simple-icons/simple-icons) with the included [CC0 license](../assets/icons/LICENSE.md). The illustration, typography, motion and accent palette belong to one visual system.

SVGs may embed local JPEG bytes as data URIs; remote image references, embedded SVG images, scripts, foreign objects and event handlers are rejected by the verifier. All images and source artwork live in the repository. There are no remote stats widgets, downloaded fonts or JavaScript embeds. Desktop and phone compositions are separate; reduced-motion preferences stop all animation and select static contribution visuals.

## Activity automation

`.github/workflows/profile-activity.yml` refreshes at 06:00 UTC or manually. It requests aggregate calendar/count data and public-repository language bytes through GitHub GraphQL. It never requests private repository identifiers. Language shares cover public repositories only. The dashboard prints its actual date window and freshness. Weekly skyline heights use real counts; the phone view explicitly shows the latest 27 weeks. A failed API request leaves the last successful snapshot intact and fails the workflow visibly.

The default workflow uses GitHub's built-in token. The optional `PROFILE_ACTIVITY_TOKEN` secret can change account visibility; never store credentials in files, image URLs or logs. Raw API responses are not committed. Only allowlisted `data/activity.json` and eight rendered variants are published. `python3 tools/update_activity.py --input /path/to/response.json` supports offline rendering.

The contribution snake refreshes every 12 hours. `tools/style_snake.py` applies the background and creates a matching static fallback. Both writing workflows share a concurrency group, stage only their own outputs, rebase before normal pushes and use path filters to avoid loops. The separate `Profile checks` workflow uses read-only permissions and checks tests, assets and deterministic artwork generation.

## Publishing

Check the actual GitHub-rendered README on desktop, 320px/390px phones, light/dark themes and reduced motion. Confirm that bitmap art inside SVGs really paints, not merely that the SVG wrapper loads. Check typing transitions, character framing, text clipping and project links. Do not manufacture activity, online status or tool authorship. Preserve history with normal pushes. Major private projects stay visible with concise descriptions, source-grounded technologies and simplified workflow diagrams. Never copy internal customer data, credentials or deployment details into public cards. Repository documentation may describe design targets or incomplete integrations: avoid unverified rollout, adoption or correctness guarantees. Public availability is not a proxy for project importance.
