# Header refinement implementation plan

> **For agentic workers:** Use superpowers:executing-plans, retaining the existing inline execution and publication workflow.

**Goal:** Improve the specific pictured header's artwork, typography balance and integrated animation.

**Architecture:** Replace only hero(mobile=False)'s composition and its four generated outputs. Use a locally embedded optimized artwork layer with live SVG text and motion. No new runtime dependency.

**Tech Stack:** Python standard library, self-contained SVG and optimized JPEG.

**Spec:** docs/superpowers/specs/2026-10-25-header-refinement-design.md

## Global constraints

Keep the eight domains, content, native links and actual activity intact. No portrait/origin claims. Keep separate phone/static variants, local-only assets and meaningful alt text.

## Review focus

- Phone crop retains the scene's architectural focal point.
- Title remains readable and does not overlap busy artwork.
- Reduced-motion header remains still and visually complete.
- Embedded image stays within existing payload/security boundary.
- All fifty-four non-header SVGs remain identical.

### Task 1: Refine and verify header

**Files:** tools/expertise.py, four assets/desert*.svg, assets/artwork/desert/ksar-night-v2.jpg, provenance, README alt text and tools/README.md.

**Interfaces:** Keep hero(mobile=False) and four current output filenames.

- [ ] Save optimized artwork and exact generation prompt/provenance.
- [ ] Recompose header text, original motif and integrated dune/constellation motion for desktop and phone.
- [ ] Generate and verify all assets; existing26 tests, verifier58, deterministic generation and byte equality for non-header outputs.
- [ ] Browser-check text bounds, image payload, full artwork, phone readability and normal/static motion in local and hosted GitHub layouts.
- [ ] Fresh final review, resolve material findings, publish and verify live result.
