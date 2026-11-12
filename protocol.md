# SLR Protocol (Stage 1) — frozen before the first search

**Review title:** Frequency-domain cues for generalizable deepfake detection: a systematic literature review
**Reviewer:** Mst. Fatema Nusrat (DIU SWE). AI-assisted proposals by Claude; every decision confirmed by the human reviewer.
**Method:** PRISMA 2020 + Kitchenham & Charters (2007), using the `systematic-review-pipeline` toolkit (Hossain, 2026).
**Protocol date:** 2026-11-12

## PICOC

| Element | Definition |
|---|---|
| Population | Face deepfakes in images and videos: face swap, face reenactment and face editing. |
| Intervention | Detection methods that use frequency-domain information (DCT, FFT, wavelet, phase spectrum, high-frequency filters) as an input stream, a feature, an attention cue or an augmentation. |
| Comparison | RGB-only (spatial) detectors, where the study reports one. |
| Outcome | Cross-dataset or cross-manipulation performance (AUC, accuracy, EER) on data not used in training, plus ablations of frequency components. |
| Context | Peer-reviewed papers and arXiv preprints, 2019 to 2026, English, computer vision / machine learning / security venues. |

## Research questions (each traces to a PICOC cell)

- **RQ1 (Intervention):** Which frequency representations (transform, band split, fusion point) do deepfake detectors use?
- **RQ2 (Context/Outcome):** Which datasets, protocols and metrics are used to test generalization?
- **RQ3 (Comparison/Outcome):** Do studies show a cross-dataset gain over an RGB-only baseline trained the same way?
- **RQ4 (Intervention/Outcome):** Which frequency bands are reported as informative, and is band importance tested on unseen data?
- **RQ5 (cross-cutting):** What reproducibility gaps and limitations do these studies report?

## Inclusion criteria

- I1. Primary study that proposes or evaluates a face deepfake / face forgery detector.
- I2. The method uses frequency-domain information as input, feature, attention or augmentation.
- I3. Reports at least one evaluation on a dataset or manipulation type not used in training.
- I4. Published 2019 to 2026, in English, as a peer-reviewed paper or arXiv preprint.

## Exclusion criteria

- E1. Audio-only, text or speech deepfakes.
- E2. Generic synthetic image detection (whole-image GAN or diffusion images) with no face forgery benchmark.
- E3. No frequency component in the method.
- E4. Only within-dataset evaluation (checked at full-text stage).
- E5. Surveys, theses, book chapters, blogs, vendor pages (surveys are kept as background only).
- E6. Proactive defenses (watermarking, adversarial perturbation against generators) and attacks on detectors.
- E7. Non-English, or full text not available.

Grey literature (blogs, vendor pages) is excluded to keep a peer-review / preprint quality floor (PRISMA item 14). No meta-analysis is planned, so reporting-bias assessment (item 21) is scoped out.

## Search strategy (Stage 2)

Two concept blocks, synonyms ORed inside a block, blocks ANDed:

- Block 1 (task): deepfake, "face forgery", "face manipulation", "face swap", "forgery detection"
- Block 2 (frequency): frequency, DCT, "discrete cosine", Fourier, spectral, spectrum, wavelet, "high-frequency"

Sources (no key needed): OpenAlex, arXiv, Crossref, Semantic Scholar.
Years: 2019 to 2026. Plus backward and forward citation snowballing from the included set (OpenAlex).

## Screening (Stage 3)

Deduplication by exact DOI, then fuzzy title + shared author (`dedup.py`). Title/abstract screening, then full-text screening. AI proposes include / exclude / maybe with the criterion code. The human reviewer confirms or changes every decision and the final sheet records `decision_source`.

## Extraction and quality (Stages 4–5)

Fixed schema from `extract.py`. Quality rated with R/A/T/C (Rigor, Artifact availability, Threat model, Currency), L/S/H per dimension, tiers A/B/C by the repo's published formula. Dybå & Dingsøyr (2008) used as the external appraisal instrument.

## Synthesis and reporting (Stages 6–7)

Narrative synthesis by RQ (no meta-analysis, because datasets, splits and metrics differ). PRISMA 2020 flow diagram from `figures.py`.
