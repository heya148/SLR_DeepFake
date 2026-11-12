"""AI-assisted coding of the extraction matrix from full texts.
Every value is a PROPOSAL; human reviewer verifies against the PDF."""
import re, subprocess, pandas as pd
X = pd.read_csv('output/extraction.csv')
SC = pd.read_csv('output/screening.csv')
def text(i):
    t = subprocess.run(['pdftotext','-q',f'pdfs/{i}.pdf','-'],capture_output=True,text=True).stdout
    return re.split(r"\n\s*(?:References|REFERENCES|Bibliography)\s*\n", t)[0]
def has(p,t,n=1): return len(re.findall(p,t,flags=re.I))>=n
TR = {"DCT":r"\bDCT\b|discrete cosine","FFT/Fourier":r"\bFFT\b|Fourier","Wavelet":r"wavelet|\bDWT\b|curvelet",
      "Phase":r"phase spectrum|phase information|phase component|amplitude and phase|phase-aware","High-pass/SRM/LoG":r"\bSRM\b|high[- ]pass|Laplacian of Gaussian|\bLoG\b|noise residual",
      "Learnable filter/band":r"learnable (?:frequency|filter|band|mask)|adaptive(?:ly)? (?:frequency|band)|band[- ]attention|frequency attention",
      "Freq. augmentation":r"frequency[- ](?:domain )?(?:augmentation|blending|masking|perturbation)|FreqBlender|mask(?:ed|ing) frequency|blend(?:ing)? frequency"}
BB = {"Xception":r"Xception","EfficientNet":r"EfficientNet","ResNet":r"ResNet","ViT/Swin":r"\bViT\b|Vision Transformer|\bSwin\b","CLIP":r"\bCLIP\b","Mamba":r"Mamba","MLLM":r"LLaVA|multimodal large language|\bMLLM\b"}
UNSEEN = ["Celeb-DF","DFDC","DFDCP","DFD","DeeperForensics","WildDeepfake","FFIW","DF40","UADFV","DiffusionFace","DiFF","Dolos",r"Celeb-DF\+\+","ForgeryNIR"]
rows=[]
for r in X.itertuples():
    t=text(r.id)
    ab=str(r.title)+' '+str(SC.loc[SC.id==r.id,'abstract'].values[0])
    tr=[k for k,v in TR.items() if re.search(v,ab,re.I)]
    if not tr:
        cnt={k:len(re.findall(v,t,re.I)) for k,v in TR.items()}
        tr=[k for k,c in sorted(cnt.items(),key=lambda x:-x[1])[:1] if c>=3]
    src='abstract' if re.search('|'.join(TR.values()),ab,re.I) else 'body'
    bc={k:len(re.findall(v,t,re.I)) for k,v in BB.items()}
    bb=[k for k,c in sorted(bc.items(),key=lambda x:-x[1])[:1] if c>=3]
    ds=[d.replace('\\','') for d in UNSEEN if len(re.findall(r"\b"+d+r"\b" if d!="DFD" else r"\bDFD\b",t))>=3]
    cross = has(r"cross-dataset|cross dataset|cross-domain|unseen dataset",t)
    crossman = has(r"cross-manipulation|cross manipulation|unseen manipulation|leave-one-out|leave one out|cross-method",t)
    abl = has(r"w/o (?:the )?(?:freq|frequency|FAM|DCT|wavelet|spectral)|without (?:the )?(?:frequency|DCT|wavelet|spectral)|RGB[- ]only|spatial[- ]only|only (?:the )?(?:RGB|spatial)|(?:RGB|spatial) (?:branch|stream) only|single[- ](?:branch|stream)",t)
    band = has(r"low[- ]frequency band|middle[- ]frequency|mid[- ]frequency|high[- ]frequency band|frequency bands?|sub-?bands?",t,3)
    code = bool(re.search(r"(?:code|implementation|models?)[^.]{0,60}(?:available|released|github)",t,re.I) and re.search(r"github\.com",t[:20000]+t[-8000:],re.I))
    robust = has(r"compression|JPEG|Gaussian (?:noise|blur)|perturbation|robustness",t,3)
    limit = has(r"\blimitations?\b",t,1)
    newdata = any(d in ds for d in ["DFDC","WildDeepfake","DF40","DiffusionFace","DiFF","FFIW","DeeperForensics","Celeb-DF++"])
    diffusion = has(r"diffusion",t,3)
    R = 'L' if (cross or crossman) and abl and len(ds)>=2 else ('S' if (cross or crossman or ds) else 'H')
    A = 'L' if code else 'S'
    T = 'L' if robust and limit else ('S' if robust or limit else 'H')
    C = 'L' if (newdata or diffusion) else 'S'
    pts=sum({'L':2,'S':1,'H':0}[v] for v in (R,A,T,C))
    tier='C' if 'H' in (R,T) else ('A' if pts>=7 else 'B' if pts>=5 else 'C')
    rows.append(dict(id=r.id,freq_src=src,freq_repr=";".join(tr) or "other/implicit",backbone=";".join(bb),unseen_test=";".join(ds),
        cross_dataset=cross,cross_manip=crossman,rgb_ablation=abl,band_analysis=band,code_available=code,robustness_test=robust,
        limitations_section=limit,diffusion_mentioned=diffusion,R=R,A=A,T=T,C=C,points=pts,quality_tier=tier))
F=pd.DataFrame(rows)
F.to_csv('output/coding_auto.csv',index=False)
pd.set_option('display.width',250);pd.set_option('display.max_colwidth',45)
print(F.drop(columns=['diffusion_mentioned']).to_string())
print(F.quality_tier.value_counts())
