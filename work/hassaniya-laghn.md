# Hassaniya Laghn

Laghn is independent research on Hassaniya poetry: building a usable corpus and a computational account of metre and rhyme. The immediate goal is to make poetic structure inspectable and testable, creating a foundation for later generation experiments.

Written Hassaniya varies, so cleaning text for comparison can erase information needed for poetic interpretation. Many texts also lack diacritics, leaving metrical distinctions unresolved; classical Arabic scansion conventions cannot simply be assumed to describe every Laghn rule.

The implementation explores three mechanisms:

- Conservative normalization separates text preparation from original material, with optional spelling normalization and diacritic handling. A normalized form supports comparison without replacing the source.
- A configuration-driven metre registry supplies rules to a checker that reports concrete violations, including movement counts and silence constraints. Metrical assumptions can be revised without burying every rule in application code.
- A scoring interface distinguishes rule checking from uncertain inference on undiacritized text. Exploratory rhyme analysis provides another inspectable structural signal alongside the metrical checks.

Rule checking and exploratory rhyme logic are implemented; linguistic validation remains ongoing, while generation and fine-tuning are research directions.

An independent project combining corpus engineering with reviewable linguistic hypotheses and expert validation.

**Technology:** Python, Pydantic, YAML configuration and Arabic text-processing tools.

**Code: private**

---

[← Back to the observatory](../README.md#user-content-research)
