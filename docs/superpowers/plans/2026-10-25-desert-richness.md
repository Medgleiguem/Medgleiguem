# Desert richness implementation plan

> **For agentic workers:** Use superpowers:executing-plans. Continue the previously selected inline execution and publication workflow.

**Goal:** Restore substantial desert-tech atmosphere and distinct animations without removing expertise breadth.

**Architecture:** Extend the existing original vector renderer and keep the same 58 asset interfaces, Markdown routes, activity collector and static serializer.

**Tech Stack:** Python standard library, self-contained animated SVG, GitHub Markdown.

**Spec:** docs/superpowers/specs/2026-10-25-desert-richness-design.md

## Global constraints

Keep existing domains, claims, native project routes and activity semantics. No portrait, origin slogans, external rendering dependencies or fake telemetry. Retain phone/compact/desktop variants and reduced-motion equivalents.

## Review focus

- All long domain/tool labels fit in every composition.
- Linked pictures remain wrapped in raw paragraph blocks on actual GitHub.
- Large illustrations never overlap text or tool labels.
- Static variants preserve essential artwork and contain no motion.
- Phone rendering stays legible without horizontal overflow.

### Task 1: Enrich existing visual assets

**Files:** tools/expertise.py, generated assets, README.md, tools/README.md.

**Interfaces:** Keep hero(mobile=False), domain_row(slug, mobile=False, compact=False) and DOMAINS intact. Keep asset filenames and routes unchanged.

- [ ] Replace the sparse header with an original layered vector skyline/dunes composition.
- [ ] Add eight larger animated method illustrations and alternating desktop layouts with dedicated compact/phone composition.
- [ ] Regenerate assets and update image descriptions/maintenance notes.
- [ ] Run existing 26 tests, SVG verifier and deterministic generation check. Decorative coordinates are verified visually rather than mirrored by unit tests.
- [ ] Browser-check text bounds, 320/390/1024/1440 layouts, ten animated/static images and eight native routes.
- [ ] Obtain fresh final review; resolve material findings, commit and publish; verify hosted output.
