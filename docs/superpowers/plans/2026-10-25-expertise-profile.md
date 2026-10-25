# Expertise Profile Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement inline. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make domains, methods, contextual tools and representative projects the profile's main content, with a smaller original vector header and polished animation.

**Architecture:** Add `tools/expertise.py` for the evidence-based domain definitions and original vector visuals. Reuse the existing SVG serializer, activity renderer/collector and variant writer. Generate eight full-width responsive domain rows; native links lead to sections in `work/README.md`.

**Tech Stack:** Python standard library, self-contained SVG, supported GitHub HTML/Markdown, isolated Chromium.

**Spec:** `docs/superpowers/specs/2026-10-25-expertise-profile-design.md`

## Global Constraints

- Eight explicit domains with knowledge, tools and examples; no CV chronology or project-first gallery.
- Original code-native vector craft; no giant generated image or portrait. Keep dark desert colors, geometric details and visible animation.
- No proficiency claims or fabricated deployments, metrics, engagement history or research completion.
- Real activity collection, privacy, daily refresh and all ten briefs remain intact.
- Supported native links; mobile/static image selection; no horizontal overflow; useful alt text.

## Review Focus

- Broad CV tools must not become claims about implementation in particular projects.
- Long domain/tool/project names must remain readable at actual GitHub column sizes.
- All eight image links must reach the right native section; ten project links remain distinct.
- New renderer imports must be copied into the refresh/full-generation test fixture.
- Every domain needs visible purposeful motion and an explicit static fallback.

### Task 1: Content and original vector design

- [ ] Add `tools/expertise.py`: domain data, bespoke method glyphs, `hero(mobile=False)` and `domain_row(slug, mobile=False)` returning complete SVGs.
- [ ] Vendor needed CC0 Simple Icons paths locally with provenance; use original glyphs for generic concepts.
- [ ] Replace obsolete large-scene renderer/outputs, retaining shared safe serialization and the unchanged calendar logic.
- [ ] Generate four variants per domain and header; inspect actual text and motion in Chromium.

### Task 2: Native profile and domain index

- [ ] Rewrite README around the smaller identity header, eight linked domain rows, visible language foundations, real activity and contact.
- [ ] Expand `work/README.md` into eight native sections with methods, relevant toolkit and individual brief links. Keep reported experience separate from project delivery claims.
- [ ] Update maintenance/art documentation and integration fixture imports; run suite, verifier and reproducibility check.

### Task 3: Review and release

- [ ] Verify GitHub-hosted review branch at desktop/phone/tablet sizes: all domain motion, still variants, text, overflow and all domain routes.
- [ ] Obtain one fresh whole-branch review, resolve material findings and commit.
- [ ] Fast-forward the live profile under existing authorization; verify CI, activity refresh and live rendering before reporting completion.

Continue the existing inline execution and publication method; this is the user's explicit correction to the same profile task.
