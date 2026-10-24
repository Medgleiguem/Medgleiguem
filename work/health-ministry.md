# Health Ministry AI

Ministerial work moves between documents, questions, decisions and actions. Health Ministry AI brings those activities into a shared workspace for the Ministry of Health, connecting source-grounded assistance with dossier review and follow-up.

Information must remain within the appropriate ministry and domain, even when people share an assistant. Human authority is a separate boundary: generated text can support a decision, but cannot replace an instruction, approval or evidence of execution.

Three engineering choices connect the workflow:

- Ministry and domain scope travel through document indexing and retrieval. Information boundaries belong in the application and search logic, rather than relying on a prompt alone.
- Retrieved passages retain document and page context. Generation uses those passages as evidence, and the application does not call the answer provider when there are no excerpts to support a response.
- A defined dossier circuit connects review, decision and follow-up. Supporting material stays alongside the case, while responsibility and subsequent actions remain visible to the people handling it.

The platform combines document assistance with a unified dossier workflow; assisted drafting remains subject to human review.

Developed collaboratively within Richat Partners’ AI and software team, with product and domain contributors.

**Technology:** Python, FastAPI, PostgreSQL/pgvector, MinIO, Next.js and React.

**Code: private**

---

[← Back to the observatory](../README.md#systems)
