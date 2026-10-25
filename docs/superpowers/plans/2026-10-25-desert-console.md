# Desert Console Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver the approved dark Mauritanian desert GitHub profile with prominent coordinated animation, a clear personal identity and truthful daily activity.

**Architecture:** Original optimized environment artwork plus self-contained SVG motion, responsive picture sources, and native Markdown links. Keep the sanitized activity collector and its four workbench outputs, changing their renderer to a contribution calendar with an animated decorative signal field. Move the project catalogue into one linked work index.

**Tech Stack:** Python standard library, SVG/CSS/SMIL, GitHub Markdown and Actions; Chromium for real image/GitHub checks.

**Spec:** `docs/superpowers/specs/2026-10-25-console-design.md`

## Global Constraints

- No portrait. Mauritanian/desert influence in artwork, icons and frames, without origin claims or slogans.
- Dark theme; large readable identity; substantial motion; concise profile with subordinate project links.
- No JavaScript, foreignObject, external SVG dependencies, fake telemetry, invented counts or private identifiers.
- Separate desktop/mobile/static compositions; useful native links and alternative text.
- Under 3 MB initially loaded per viewport and under 2 MB per SVG; verify real sizes.
- Reuse collector validation, privacy and failure behavior. Preserve all ten public engineering briefs.

## Review Focus

- Sparse, partial or zero activity: calendar cells, dates and displayed totals must agree.
- Mobile image scaling: essential text must be readable at 320 px, with no overflow.
- Reduced motion and image proxy behavior: selected static files must actually remain still.
- Activity refresh: full generation and collector generation must produce identical output.
- Existing brief return links: all profile fragment targets must survive the new layout and GitHub sanitization.

### Task 1: Original environment and visual renderer

**Files:** new `assets/artwork/desert/` original export/provenance, new `tools/desert_console.py`, modify `tools/generate_assets.py`, relevant `tools/test_profile_assets.py` assertions.

**Interfaces:** `desert_console.hero(mobile=False)`, `tools_panel(mobile=False)`, `footer(mobile=False)` return complete animated SVG strings. `render_workbench(data, mobile=False, animated=True)` remains the collector interface. Existing `static_svg` retains its tested contract.

- [ ] Generate a clean art-only night desert master from the approved study, with no character, type or interface.
- [ ] Optimize a deterministic checked-in JPEG; document exact built-in prompts and reference provenance.
- [ ] Implement sparse warm geometric frames, large name, dune wisps, sky routes and contour motion. Implement recognizable tools and atmospheric contact divider.
- [ ] Reuse the tested static serializer and four-variant writer. Remove obsolete panoramas/card outputs and old generator only after replacing all references.
- [ ] Inspect desktop/mobile image rendering and actual motion before proceeding.

### Task 2: Truthful calendar and refresh compatibility

**Files:** `tools/desert_console.py`, `tools/generate_assets.py`, `tools/test_activity.py`, `.github/workflows/profile-activity.yml`.

**Interfaces:** `calendar_days(data) -> list[tuple[date,int]]` fills the most recent at most 140 days, inclusive of actual bounds; `render_workbench` serializes the same values in desktop/mobile/static assets. Calendar date/count attributes allow semantic verification; metric labels describe the actual displayed window.

- [ ] Write meaningful tests for sparse dates, a short window, zero counts, exact cell/date mapping, identical variant data and explicit static output. Observe failure first.
- [ ] Implement a fixed, readable calendar with a separate moving signal field. Zero-valued dates remain zero; decorative motion never changes actual counts or cell colors.
- [ ] Show displayed-window contributions and active days, actual range, and UTC snapshot date; retain raw snapshot separately. Use a labeled discrete color scale. Existing collector aggregates are not relabeled as displayed-window metrics.
- [ ] Update the workflow trigger for the new renderer, preserving staged paths and least privilege. Run all collector/privacy/error-preservation/integration tests.

### Task 3: README, index, verification and release

**Files:** `README.md`, new `work/README.md`, `tools/README.md`, SVG verifier if required; generated asset families `desert`, `workbench`, `tools-rail`, `desert-footer`.

- [ ] Replace the main gallery with hero, real activity, compact tools/research/work links and contact. Keep native `systems`, `research`, `workbench` targets for existing return links. Index all ten briefs at `work/README.md`.
- [ ] Check links, privacy, static assets and deterministic generation with existing meaningful tests and verifier. Document maintenance and art provenance.
- [ ] Inspect actual GitHub-rendered review-branch README in desktop and 390/320 px, normal/reduced motion; measure loaded assets, compare motion frames and inspect native links.
- [ ] Obtain a fresh whole-branch review, resolve material findings, commit and publish with a normal push under existing authorization. Verify CI and live profile before reporting success.

## Execution decisions

Continue the already-selected inline execution method from the prior approved profile plan. No additional execution-method or publication approval round: this is the same authorized profile task with explicit new design steering. A fresh final reviewer checks the branch. The visual concept's generated calendar and annotations must never ship as real data or finished content.
