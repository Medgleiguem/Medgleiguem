# KYC Identity

KYC Identity connects partner applications to journeys involving national identity services, document capture and biometric checks. The engineering problem is orchestration: the appropriate route depends on the evidence available, and a partner needs a meaningful verification outcome rather than unrelated image-processing responses.

A person with a digital identity account needs a different path from someone requiring document and face checks. Capture, liveness and identity matching are also distinct signals; success in one operation must not imply success in all of them.

Three mechanisms organize the original platform:

- Verification branches between national digital-identity OTP and document or biometric journeys. The selected evidence route remains explicit throughout the case.
- Browser capture feeds liveness and face-matching services, with document OCR as another evidence path. Application casework connects the results and supports manual review where a decision is not automatic.
- Partner API access and result callbacks connect verification to the consuming application. Staff use a backoffice workflow for case management.

The original platform and Identity v2 are separate implementation tracks; v2 matching and SDK components still include scaffolding and placeholders.

Developed within IBTIKAR Technologies’ engineering team.

**Technology:** original platform: Next.js/TypeScript, MongoDB, object storage and Python vision services; v2: NestJS and hosted Next.js.

**Code: private**

---

[← Back to the observatory](../README.md#user-content-systems)
