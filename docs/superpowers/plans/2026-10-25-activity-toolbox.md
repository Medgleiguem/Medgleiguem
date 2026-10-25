# Activity and toolbox implementation plan

> **For agentic workers:** Use superpowers:executing-plans. Existing inline execution and publication authorization retained.

**Goal:** Complete the screenshot's activity section with meaningful annual/recent data and a visible contextual toolbox.

**Architecture:** Separate data derivation/native summary from SVG composition. Keep the stable collector renderer interface, six workbench variants and existing static serializer. Add six toolbox variants without changing header/domain assets.

**Tech Stack:** Python standard library, self-contained SVG, local icon geometry, GitHub Markdown/Actions.

**Spec:** docs/superpowers/specs/2026-10-25-activity-toolbox-design.md

## Global constraints

No private identifiers/event payloads, fabricated metrics, animated data geometry or external card services. Preserve existing header/domains/project routes, failure retention and deterministic generation. Missing type fields mean unavailable; zero means zero. Calendar sums and independently scoped API counters remain separate. Public language shares are source-byte proportions, not expertise ratings.

## Review focus

- Full calendars can require54 columns; phone strips must preserve every actual day exactly once.
- Sparse, short, stale, zero or unavailable data needs truthful display and sensible dates.
- API collection counts and calendar totals can disagree without either being overwritten.
- Public language tails/zero bytes must not yield false percentages or malformed SVG.
- Actual GitHub must retain picture media sources/native links and readable phone spacing.

### Task 1: Complete the activity model, renderer and refresh

**Files:** activity_data.py, activity_dashboard.py, desert_console.py, generate_assets.py, update_activity.py, test_activity.py, new test_activity_data.py, six workbench assets, data/activity.json, work/activity.md, workflow.

**Interfaces:** calendar_days(data), calendar_stats(data), weekly_totals(days), language_shares(data), activity_summary(data). render_workbench(data,mobile=False,animated=True,compact=False) stays re-exported from generate_assets.

- [ ] Write failing tests for full366-day bounds/short gaps; actual weekly bins/30-day/current+longest streaks; missing/zero/invalid type fields and timestamps; language grouping/normalization/empty states.
- [ ] Implement data helpers and expanded aggregate collector fields after observing failures.
- [ ] Compose the annual dashboard using four metrics, responsive calendar, weekly trend, separate collection-type counters and public-code shares. Preserve data-date/count/fill and data-metric hooks.
- [ ] Update meaningful existing tests from140-day crop to full window and integration fixture dependencies. Require all six SVGs and native summary to match refresh/full generation exactly.
- [ ] Run suite/verifier/deterministic generation; refresh actual aggregate data without publishing raw API payloads; commit.

### Task 2: Toolbox and profile integration

**Files:** expertise.py, generate_assets.py, local icon paths, six toolbox SVGs, README.md, maintenance/provenance.

**Interfaces:** toolbox(mobile=False,compact=False) renders grouped languages/providers/additional services/editor-platform tools from existing evidence. Three sizes/static equivalents.

- [ ] Compose the original visible toolbox with local icons, grouped labels and restrained actual animation; retain native text equivalent.
- [ ] Replace plain language/disclosure block, add board after activity, link activity.md and raw JSON; keep domain links and contact navigation.
- [ ] Browser-check320/390/1024/1440, light/reduced modes, text bounds/overlap, correct data charts, normal motion/static equivalents and hosted branch markup.
- [ ] Fresh final review; resolve material findings with regression tests; publish, wait for CI and verify ordinary live profile/cache freshness.
