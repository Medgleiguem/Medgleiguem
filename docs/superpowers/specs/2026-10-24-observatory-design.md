# The Observatory — art-led anime GitHub profile

Approved design, 24 October 2026. Selected approach: the user chose “Art-led anime world — immersive illustration and project-themed animation.” This choice supersedes the earlier recommendation of an editorial engineering studio.

## Intent

Create an immersive, polished GitHub profile whose visual world is original and whose project content demonstrates substantial engineering work. Readers should remember the author, recognize the important systems, and find meaningful technical detail. Dark theme, visible coordinated animation, anime character, and a high-tech identity are required. The existing profile's composition, art, palette and wording are not constraints.

The intended audience is engineers, collaborators and people evaluating the work. This is a profile and project showcase, with no CV timeline, education or awards wall. Institutional names do not establish scale, adoption, deployment or individual subsystem ownership.

## Approaches and selection

The reference board compared an editorial engineering studio, an illustrated anime world, and a technical publication. The user selected the illustrated world. It gives the strongest atmosphere, while requiring deliberate space for readable project explanations. The implementation must preserve that choice; it must not quietly converge on a generic dashboard or text-only engineering page.

## Visual world

An original fictional coastal observatory at night, with Atlantic Saharan architectural influences. It is a metaphor for connecting evidence, signals and human judgment, not a depiction of actual institutional facilities. Three complementary panoramas have been generated as concept art using the built-in image-generation tool:

1. **The observatory:** an open coastal terrace, a circular precision instrument, suspended source fragments and a small engineer giving human scale. This establishes the world and the evidence chapter.
2. **The exchange hall:** three distinct luminous channels and an ordered central lattice, expressing heterogeneous data becoming analytical structure.
3. **The identity atelier:** separate synthetic landmark, credential and signal instruments, expressing distinct verification and hand-off operations.

The selected visual language is drawn 2D anime with crisp ink contours, cel-shaded architectural forms, midnight blue, charcoal, silver signal light and warm brass. A small adult figure is fictional and does not claim to be a portrait of the user. No existing anime characters or third-party artwork are incorporated.

These are art-direction concepts. Final artwork optimization and motion alignment happen during implementation. The selected images are preserved in the concept's `art/` folder, with exact generation prompts in `art/README.md`.

## Composition and content

### Opening

A wide, animated panorama fills the profile column. Med Gleiguem's name and one plain description of the work appear in the dark left portion. Small chapter markers suggest a designed archive. Introductory text and links remain readable immediately. The art establishes identity; the text names the work.

### Chapter 01 — Evidence into decisions

The observatory introduces the four institutional AI/evidence systems. Each name and project link is continuously visible:

- Health Ministry AI: ministry/domain-scoped retrieval, dossiers, human decisions and follow-up.
- Central Bank / RKF: document identity and version context, review boundaries and hybrid retrieval.
- ARE Intelligence: regulatory evidence, obligations and decision views. Current search is lexical; generated answers are disabled.
- National Knowledge Base: imports, private staff previews and initial dataset review. Publication and customer retrieval remain later increments.

Each entry has a concise purpose, one distinctive mechanism and a useful link to an approximately 200-word public engineering brief. Text is native Markdown in the shipped profile. Briefs describe collaboration and current status precisely, without institutional source documents, internal endpoints or customer data.

### Chapter 02 — Data with a destination

The exchange hall introduces ANRPTS / BI Houwiyeti as a larger single feature: heterogeneous inputs, source contracts, incremental acquisition, analytical models and a read-only dashboard boundary. Current dbt placeholders are described accurately in its brief. Do not claim complete domain coverage or measured throughput without evidence.

### Chapter 03 — Identity and payment journeys

The identity atelier introduces three separate project entries:

- KYC Identity: capture, liveness and matching remain distinct operations. The original platform and v2 effort remain distinct implementation tracks.
- Taazour Aoun: household/beneficiary eligibility through OTP/eKYC and wallet-transfer states. It is a beneficiary disbursement journey.
- Taazour Pay: provider adapters and a durable household payment lock. Mocked or pending integrations remain identified in its brief.

No animated scene implies a real successful biometric or payment operation. All depicted landmarks and signals are synthetic visual metaphors.

### Chapter 04 — Language, gesture, structure

Two equally visible research entries use the visual world's precise marks and warm framing:

- Hassaniya Laghn: corpus preparation, explicit metre/rhyme rules and testable violations. No completed trained generation model is claimed.
- Mauritanian Sign Language: traceable image processing, quality checks, deduplication and subject-aware evaluation splits. No delivered live translator is claimed.

The methods receive bespoke vector animation: a scansion pattern and synthetic hand-landmark sequence. Text names the actual method rather than presenting the animation as measured research output.

### Chapter 05 — At the workbench

One compact, generated activity strip uses the actual public aggregate contribution data and labels its capture date/time window. It fits the new palette and replaces the need to stack several visualizations of the same activity. Keep existing daily data-refresh capabilities where suitable; appearance is redesigned. Do not expose private repository names, events or messages.

Technology is tied to the systems using it, plus a compact text index if useful. Existing minor public side projects are available as small secondary links. Do not fabricate releases or an engineering-note publishing history.

## Motion choreography

| Scene | Motion | Timing and limits |
| --- | --- | --- |
| Opening | restrained slow camera drift, thin signal paths, small light points and instrument highlights | 12–18 second loop; name and introduction never disappear |
| Evidence | source-to-citation path with a clear human-review stopping point | 7–10 seconds; no simulated legal correctness or approvals |
| Data | three separately phased batches traverse distinct lanes | 6–9 seconds; no throughput counters |
| Identity | synthetic landmarks, credential outline and hand-off signal appear in separate stages | 8–12 seconds; no implied real verification result |
| Research | alternating scansion marks and hand-landmark traces | 7–11 seconds; labels remain visible |
| Activity | one introductory reveal of actual data, then a stable readable view | no fake live telemetry |

The profile should visibly animate in several places, with coordinated rhythm and no rapid flashes. The raster illustration is static art; animated vector paths and image transforms provide scene motion. Do not describe it as hand-animated character footage. Stagger emphasis rather than making every element flash at once.

## GitHub implementation constraints

The final deliverable is a GitHub profile README with normal text, links, supported disclosure elements and self-contained SVG/image assets. GitHub does not provide an arbitrary interactive webpage canvas. No custom JavaScript, hover-only project navigation, full-page CSS or unsupported HTML is promised in the profile.

The local concept HTML is a **throwaway visual study**, not the final implementation. It may offer motion controls for review. Those controls are explicitly excluded from the GitHub deliverable. The study must not depend on scrolling to reveal project information or use interaction as evidence that the shipped profile will support it.

Its responsive grids are a composition study. The final README uses native project headings, concise descriptions and links; pairings are retained only if actual GitHub mobile rendering remains readable. It does not promise a custom CSS grid or an identical browser-page layout inside GitHub.

Implementation approach proposed by the builder:

- Optimize the chosen PNG artwork to appropriate web dimensions and JPEG quality while retaining the original masters.
- Embed the optimized raster in self-contained SVG scene assets, with native vector motion and no scripts or remote resources. Keep each scene below the existing verifier's 2 MB safety limit; target below 700 KB per panorama and below 3 MB total profile assets where feasible. Measure the results before claiming the target is met.
- Produce explicit static counterparts selected by `<picture>` for reduced-motion users. A CSS rule inside an SVG alone is not sufficient evidence that reduced motion works when the asset is loaded as an image.
- Avoid long image-baked paragraphs. Names, descriptions and links are native Markdown; names within art are duplicated by useful alt text and native context.
- Use a single-column sequence with paired project entries only where GitHub rendering remains readable. At 390 px, art may crop or simplify but must not shrink essential paragraph text to illegibility.
- Preserve the existing audited privacy and activity collection logic where its behavior is still appropriate. Styling and information layout are redesigned. Do not disturb unrelated workspace changes.

## Public content and links

The profile includes eight project briefs and two research briefs in public Markdown files inside the profile repository. All ten names and routes remain visible. No entry depends on watching a carousel. Private-source buttons are not presented as public demos. Side projects remain visually subordinate.

The ten drafts and private source-evidence notes are in the research folder. Evidence notes, source paths and internal documents are not published. A final disclosure and factual review checks that public briefs contain only the CV-level project context and general engineering mechanisms already selected for this profile.

## Verification before publication

- Run existing meaningful activity and SVG-verifier tests; update tests only for genuinely changed behavior.
- Inspect deterministic generation, file sizes, local references, alt text and public links.
- Inspect actual SVG files as images in a real browser, desktop and 390 px, normal and reduced motion.
- Confirm visible motion from frame differences and confirm static behavior under explicit reduced-motion selection.
- Inspect actual GitHub rendering before claiming the final profile works there. A local HTML study is insufficient evidence.
- Confirm all ten project links are continuously visible, useful and public-safe.
- Run the profile repository's checks before publishing. Publishing authority follows the user's existing authorization for this profile; do not ask again for a permission already granted.

## Decisions left to the builder

Precise typography, crop positions, motion path coordinates, compression settings and generator organization are routine design/implementation decisions. Settle them through rendering checks. They do not require another preference question. Retain the chosen art-led hierarchy, project importance and factual boundaries.

## Approval boundary

The user selected the art-led approach and approved this design and its moving study with “yes” on 24 October 2026. Implementation and publication proceed under that approval and the existing profile task authorization.

## Review evidence

A fresh-context designer/engineer reviewed the written design for planning gaps and reported “nothing important left.” The local browser study is checked at 1440 px and 390 px with normal and reduced motion. These checks are evidence about the concept only; they do not establish the final GitHub rendering.
