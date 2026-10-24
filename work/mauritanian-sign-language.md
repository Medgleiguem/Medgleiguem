# Mauritanian Sign Language

This university research direction works toward a corpus and recognition tools for Mauritanian signs. The current engineering focus is dataset preparation: making image inputs traceable, inspectable and suitable for meaningful experiments.

Lighting, blur, hand visibility and framing vary, so labeled files are not automatically a useful training set. Evaluation can also become misleading when related images or the same participants appear across training and test data. Preparation and splitting are therefore part of the research method.

The documented pipeline combines three mechanisms:

- Incremental ingestion records image identity and processing state in SQLite. Originals are retained, and configuration versions identify the settings associated with each processing result.
- MediaPipe hand detection feeds quality checks and cropping. Cached landmarks support reprocessing when crop settings change; rejection reasons and HTML before/after reports make the effects inspectable.
- Perceptual duplicate checks and subject-aware train, validation and test manifests address different sources of repeated evidence, providing a foundation for evaluation on held-out participants.

Dataset preparation is the current focus; Mauritania-specific label validation and recognition evaluation remain ongoing research.

Work undertaken in a university research context, connecting corpus preparation with the longer-term recognition direction.

**Technology:** Python, SQLite, MediaPipe, perceptual hashing and generated HTML reports.

**Code: private**

---

[← Back to the observatory](../README.md#research)
