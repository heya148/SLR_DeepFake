"""AI-proposed full-text decisions (pending human confirmation)."""
INC = [1,2,3,5,6,11,17,30,39,40,43,52,57,60,62,64,71,76,82,84,86,95,102,103,105,188,
       7,8,10,13,14,19,20,21,23,33,34,42,45,55,63,72,75,78,92,106,114,115,117,126,137,145,152,175,194]
EXC = {
 "E4: no evaluation on unseen dataset/manipulation": [4,15,18,22,24,26,29,44,54,74,91,93,97,100,108,131,136,165,185,195],
 "E3: frequency not part of the detector": [16,28,98,148,113,118,121,122,124,129,144,166,171,174,182,186],
 "E2: generic synthetic-image detection, no face benchmark": [36,38,53,69,81,83,123,151,187,200],
 "I1: not a deepfake detector (provenance tracing)": [89],
}
NOTES = {
 4:"F3-Net reports FF++ only (no cross-dataset table)", 105:"weak title-page match (55.9): PDF confirmed by content (CAFRL, negative result); human to re-check",
 20:"borderline: noise clue = low-frequency suppression (high-pass)", 34:"borderline: frequency used only as degradation augmentation",
 75:"borderline: adversarial high-frequency blurring", 106:"borderline: MLLM with high-frequency module", 129:"graph-spectral, not image frequency",
 144:"'spectral' = SVD of weights", 171:"'spectral' = SVD of weights", 124:"Saab/PixelHop 'spectral', not Fourier",
 148:"implicit neural representation heatmaps, not a frequency transform",
 63:"cross-method transfer across 7 Celeb-DF++ talking-face methods",
}
