# ANRPTS / BI Houwiyeti

BI Houwiyeti connects operational data sources to an analytics workspace for ANRPTS. The engineering problem is to create a useful analytical view without making dashboard code reconcile every source or asking operational systems to behave like a warehouse.

Inputs span MongoDB, PostgreSQL and MySQL, with different structures and extraction behavior. Analytical access also needs a boundary from operational changes: a dashboard runtime should not acquire unnecessary warehouse write authority.

Three choices organize the pipeline:

- Source definitions establish extraction contracts. Source-specific connectors and a hybrid incremental loading approach feed a raw landing layer, separating acquisition from business interpretation.
- The transformation design separates staging, cross-source harmonization and dimensional marts. Each layer has a different responsibility, keeping source normalization apart from the models intended for analysis.
- The Next.js dashboard consumes analytical data through a read-only database role. Raw-data inspection is an explicit diagnostic capability, rather than the default route for business analytics.

Airflow and dbt establish the pipeline backbone; dbt currently contains minimal placeholder models, with full domain modeling developed incrementally.

Work undertaken within IBTIKAR Technologies’ engineering team, connecting data pipelines with the application used to explore their results.

**Technology:** Python, Airflow, PostgreSQL, dbt, Next.js, React and TypeScript.

**Code: private**

---

[← Back to profile](../README.md#user-content-systems)
