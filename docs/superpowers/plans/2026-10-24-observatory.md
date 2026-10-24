# Anime Observatory Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the approved original anime world as a readable, animated GitHub profile centered on eight major systems and two research tracks.

**Architecture:** Self-contained SVG panoramas embed optimized original JPEG artwork and add vector animation. Native Markdown supplies project summaries and links to public engineering briefs. The existing privacy-filtered activity collector feeds one compact workbench chart.

**Tech Stack:** Python standard library, SVG/CSS animation, GitHub Markdown and Actions; isolated Chromium for visual verification.

**Spec:** `docs/superpowers/specs/2026-10-24-observatory-design.md`

## Global Constraints

- Dark art-led anime hierarchy, midnight blue/silver/brass; no reuse of the former layout or illustration.
- Eight systems and two research tracks have continuously visible names and useful public brief links.
- No private repository identifiers, source documents, deployments, credentials or unverified adoption/readiness claims.
- Native text and links; no profile JavaScript, foreign objects, remote image dependencies or custom full-page CSS.
- Explicit static variants for every animated picture, including combined mobile/reduced-motion selection.
- Each panorama below 2 MB; target below 700 KB per served panorama and below 3 MB of assets loaded per view.
- Preserve the existing collector's allowlist, error behavior and scoped automation writes.

## Review Focus

- SVG wrappers can load while embedded bitmaps fail to paint: visually inspect actual image documents.
- Motion preferences may not propagate into image SVGs: verify selected static URLs and identical frames.
- GitHub strips unsupported HTML: inspect actual GitHub-rendered Markdown and image sources.
- Sparse and short contribution calendars must preserve actual totals, date gaps and truthful bucket labels.
- Generated project text may overstate implementation or ownership: review all public briefs against the approved evidence boundaries.

---

### Task 1: Original art and GitHub-native scene renderer

**Files:** Replace `tools/generate_assets.py`; add three optimized JPEGs and provenance under `assets/artwork/observatory/`; add meaningful coverage in `tools/test_profile_assets.py`.

**Interfaces:** `scene(name: str, mobile: bool=False) -> str`; `research(mobile: bool=False) -> str`; existing `static_svg(source: str) -> str`; deterministic `main()` emits desktop/mobile/explicit-static variants.

- [ ] Add a regression test for static conversion of the new motion classes: remove keyframes/animation, leave paths and labels visible, preserve markup and bitmap validation.
- [ ] Run it and observe failure before updating the static converter.
- [ ] Export the three approved masters to optimized full-resolution JPEGs; preserve original masters in the local review artifacts, and record exact prompts and built-in generation provenance in the repo.
- [ ] Replace the old renderer with the observatory, exchange, identity and research compositions. Keep pixel-critical titles readable on first frame; text paragraphs stay in Markdown.
- [ ] Run SVG boundary tests and inspect generated desktop/mobile scene images in a real browser.
- [ ] Commit the independently reviewable renderer/artwork change.

### Task 2: Workbench chart and daily automation

**Files:** `tools/generate_assets.py`, `tools/update_activity.py`, `tools/test_activity.py`, `.github/workflows/profile-activity.yml`.

**Interfaces:** `render_workbench(data: dict, mobile: bool=False, animated: bool=True) -> str` consumes the existing sanitized snapshot schema and produces four `assets/workbench*.svg` files. Collector output becomes snapshot + those four variants.

- [ ] Replace obsolete dashboard/skyline output assertions with tests for the single workbench: real date buckets/counts, proportional heights, short/sparse calendars and explicit static output.
- [ ] Run tests to observe failure for the absent workbench behavior.
- [ ] Implement at most 84 calendar days, grouped into consecutive seven-day buckets from the displayed window start; fill date gaps with zero and label actual bounds and snapshot date. Retain meaningful `<title>` labels per bar.
- [ ] Remove obsolete activity renderers, preserve fetching/sanitization/streak calculations and atomic validation-before-replacement behavior.
- [ ] Update workflow paths, generation and staged file list to the new four variants. Keep its existing shared concurrency and normal rebase/push behavior.
- [ ] Run the whole suite, including privacy and failed-refresh preservation tests, then commit.

### Task 3: Profile, public briefs and release verification

**Files:** `README.md`, ten `work/*.md` briefs, `tools/verify_profile.py`, `tools/README.md`, generated assets; remove obsolete unreferenced generated SVGs and old scene artwork.

**Interfaces:** README references only the new responsive pictures and native public brief links; each brief links back to the profile. Existing verifier gains broken local Markdown link detection.

- [ ] Add a verifier regression for a missing local Markdown brief and verify failure first.
- [ ] Publish the reviewed project text as ten substantive briefs with precise status and collaborative attribution. Keep source evidence and internal paths outside the repo.
- [ ] Build README in the approved chapter sequence, with native summaries/technologies and ordinary links, compact tools/contact, and minor side projects subordinate.
- [ ] Extend verification to local Markdown/HTML links without treating `mailto:` or fragment anchors as files. Verify the actual ten destination files.
- [ ] Update maintenance docs and remove obsolete generated artwork from the current tree; git history preserves prior versions.
- [ ] Run suite, verifier and deterministic generation; inspect actual rendered GitHub Markdown locally and then in a review branch on GitHub. Check desktop and 390/320 px, normal/reduced motion, loaded bitmaps, useful links and all project names.
- [ ] Obtain a fresh whole-branch review, fix material findings, commit, then publish with a normal fast-forward push under the user's existing authorization. Wait for CI and inspect the live profile before reporting completion.

## Execution decisions

The user approved the art-led design and requested the rebuild. Execute inline without another technical-plan permission round; routine implementation choices are delegated to the builder in the approved spec. One fresh reviewer checks the completed branch. The task ledger is in `/tmp/profile-build-observatory/progress.md`, outside published content.
