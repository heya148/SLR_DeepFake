"""Full-text evidence collector for AI-assisted full-text screening.
For every downloaded PDF: verify the title page, then count criterion evidence.
Output is a PROPOSAL only; the human reviewer confirms each decision."""
import re, subprocess, sys, os
import pandas as pd
from rapidfuzz import fuzz

OUT = sys.argv[1]  # output dir
log = pd.read_csv(f"{OUT}/download_log.csv")
cand = pd.read_csv(f"{OUT}/ft_sought.csv")
T = {
    "face": r"\bface|facial",
    "forgery": r"deepfake|deep fake|forger|manipulat|face swap|faceswap",
    "freq": r"\bDCT\b|discrete cosine|Fourier|\bFFT\b|wavelet|\bDWT\b|frequency domain|frequency-domain|high[- ]frequency|low[- ]frequency|spectrum|spectral|phase spectrum|frequency band|frequency-aware|frequency information|frequency feature",
    "xdata": r"Celeb-?DF|DFDC|\bDFD\b|DeeperForensics|WildDeepfake|Wild ?Deepfake|FFIW|DF-?1\.0|UADFV|DFDCP|DF40|DiffusionFace|cross-dataset|cross dataset|cross-domain|cross-manipulation|unseen",
    "rgbabl": r"w/o frequency|without frequency|RGB[- ]only|spatial[- ]only|only (?:the )?(?:RGB|spatial)|frequency branch|frequency stream|ablation",
    "code": r"github\.com/[\w\-]+/[\w\-\.]+",
    "vit": r"Vision Transformer|\bViT\b|transformer|Swin",
    "clip": r"\bCLIP\b",
}
DS = ["FaceForensics++", "Celeb-DF", "DFDC", "DFDCP", "DFD", "DeeperForensics", "WildDeepfake", "FFIW", "DF40", "UADFV", "DiffusionFace", "GenImage", "ForgeryNet"]
rows = []
for r in log.itertuples():
    p = getattr(r, "saved_path", None)
    if not isinstance(p, str):
        continue
    p = os.path.normpath(os.path.join(OUT, p))
    if not os.path.exists(p):
        continue
    try:
        txt = subprocess.run(["pdftotext", "-q", p, "-"], capture_output=True, text=True, timeout=60).stdout
    except Exception:
        txt = ""
    title = cand.loc[cand.id == r.id, "title"].values[0]
    head = " ".join(txt[:3000].split())
    tmatch = fuzz.partial_ratio(title.lower(), head.lower()) if head else 0
    body = re.split(r"\n\s*References\s*\n|\nREFERENCES\n", txt)[0]
    c = {k: len(re.findall(v, body, flags=re.I)) for k, v in T.items()}
    ds = [d for d in DS if re.search(re.escape(d) if d != "DFD" else r"\bDFD\b", body)]
    gh = re.findall(T["code"], body)
    rows.append(dict(id=r.id, title=title, title_match=tmatch, words=len(body.split()), datasets=";".join(ds), code=";".join(sorted(set(gh)))[:120], **{f"n_{k}": v for k, v in c.items()}))
df = pd.DataFrame(rows)
df.to_csv(f"{OUT}/ft_evidence.csv", index=False)
print(len(df), "PDFs analysed;", (df.title_match < 80).sum(), "with weak title match")
