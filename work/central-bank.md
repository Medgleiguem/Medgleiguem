# Central Bank RAG / Richat Knowledge Foundation

The Richat Knowledge Foundation organizes legal texts, central-bank material and financial-program documents for source-cited retrieval in the Banque Centrale de Mauritanie scope. Its central problem is preserving document identity, provenance and version context as material moves from acquisition to retrieval.

One document may have several language or historical versions without becoming several unrelated records. Material being processed by staff must also remain distinct from independently validated evidence.

Three mechanisms structure the foundation:

- A canonical document registry separates identity from versions and retains provenance for metadata and source material. Legal status and review status are represented separately.
- Preview and validated retrieval use separate corpus boundaries. Expert review and independent audit form part of the validation route; automated processing prepares candidates instead of approving its own output.
- Hybrid retrieval combines PostgreSQL lexical search and pgvector rankings, then applies collection, confidentiality and legal-status filters. Answers retain source references, with citation-marker checks providing an additional mechanical safeguard.

The current retrieval baseline uses document-level status filters and citation checks; provision-level legal-time reasoning and stronger claim verification remain development work.

A collaborative Richat Partners project spanning engineering, product and institutional expertise.

**Technology:** Python, FastAPI, SQLAlchemy, PostgreSQL/pgvector and React.

**Code: private**

---

[← Back to the observatory](../README.md#systems)
