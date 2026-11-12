import pandas as pd, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from collections import Counter
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
BLUE,ORANGE,GREEN,GREY='#2b6cb0','#dd6b20','#2f855a','#718096'
# PRISMA
fig,ax=plt.subplots(figsize=(8.6,9.2)); ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,12)
def box(x,y,w,h,t,fc,ec):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.05',fc=fc,ec=ec,lw=1.4))
    ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=9.2)
def arr(x1,y1,x2,y2): ax.annotate('',(x2,y2),(x1,y1),arrowprops=dict(arrowstyle='-|>',color='#333',lw=1.2))
L,W,SX,SW=0.4,4.3,5.2,4.75
rows=[(10.3,1.3,"Records identified (n = 300)\narXiv API (n = 200)\nCrossref API (n = 100)", "Duplicates removed (n = 10)\nOpenAlex, Semantic Scholar: rate-limited,\nnot searched (see Deviations)"),
      (8.1,1.0,"Records screened\n(title/abstract) (n = 290)","Records excluded (n = 121)\nE1 audio/text 49; E2 generic images 22\nE5 not primary 17; E6 attacks/proactive 14\nI4 year/language 7; E3 no frequency 6; I1 6"),
      (5.9,1.0,"Reports sought for retrieval\n(n = 169)","Reports not retrieved (n = 67)\nno open-access full text"),
      (3.7,1.0,"Reports assessed for eligibility\n(full text) (n = 102)","Reports excluded (n = 47)\nE4 no unseen-data test 20\nE3 frequency not in detector 15\nE2 no face benchmark 10; I1 1"),
      (1.5,1.0,"Studies included in review\n(n = 55)",None)]
for k,(y,h,m,s) in enumerate(rows):
    box(L,y,W,h,m,'#ebf4ff' if k<4 else '#e6fffa',BLUE if k<4 else GREEN)
    if s: 
        sh=1.3 if k in (1,3) else h; sy=y+h/2-sh/2
        box(SX,sy,SW,sh,s,'#fffaf0',ORANGE); arr(L+W+0.05,y+h/2,SX-0.05,y+h/2)
    if k<4: arr(L+W/2,y-0.02,L+W/2,rows[k+1][0]+rows[k+1][1]+0.08)
for y,t in [(10.95,'Identification'),(6.9,'Screening'),(2.0,'Included')]:
    ax.text(0.05,y,t,rotation=90,ha='center',va='center',fontsize=10,color=BLUE,weight='bold')
plt.savefig('figs/prisma.png',dpi=220,bbox_inches='tight'); plt.close()
X=pd.read_csv('output/extraction.csv')
def barh(cnt,fn,title,color,xl='Number of studies'):
    items=sorted(cnt.items(),key=lambda x:x[1])
    fig,ax=plt.subplots(figsize=(7,0.42*len(items)+1.1))
    ax.barh([a for a,_ in items],[b for _,b in items],color=color)
    for i,(_,b) in enumerate(items): ax.text(b+0.3,i,str(b),va='center',fontsize=9)
    ax.set_xlabel(xl); ax.set_title(title,loc='left',weight='bold'); ax.spines[['top','right']].set_visible(False)
    plt.tight_layout(); plt.savefig(f'figs/{fn}.png',dpi=220); plt.close()
barh(Counter(t for s in X.freq_repr for t in s.split(';')),'freq_repr','Frequency representations used (n = 55, multi-label)',BLUE)
barh(Counter(t for s in X.unseen_test.fillna('') for t in s.split(';') if t),'datasets','Unseen test datasets reported (n = 55, multi-label)',ORANGE)
yc=X.year.astype(int).value_counts().sort_index()
fig,ax=plt.subplots(figsize=(7,3)); ax.bar(yc.index.astype(str),yc.values,color=GREEN)
for i,v in enumerate(yc.values): ax.text(i,v+0.3,str(v),ha='center',fontsize=9)
ax.set_title('Included studies by year',loc='left',weight='bold'); ax.spines[['top','right']].set_visible(False); ax.set_ylabel('Studies')
plt.tight_layout(); plt.savefig('figs/years.png',dpi=220); plt.close()
# evidence gaps
g={'Test on unseen dataset':int(X.cross_dataset.sum()),'Test on unseen manipulation':int(X.cross_manip.sum()),'Robustness test (compression/noise)':int(X.robustness_test.sum()),
   'Frequency vs RGB-only ablation':int(X.rgb_ablation.sum()),'Band-level analysis':int(X.band_analysis.sum()),'Own code released':int(X.code_available.sum()),
   'RGB ablation and band analysis together':int((X.rgb_ablation&X.band_analysis).sum())}
items=list(g.items())[::-1]
fig,ax=plt.subplots(figsize=(7.4,3.6)); cols=[GREY if v<20 else BLUE for _,v in items]
ax.barh([a for a,_ in items],[55]*len(items),color='#edf2f7'); ax.barh([a for a,_ in items],[v for _,v in items],color=[ORANGE if v<20 else BLUE for _,v in items])
for i,(_,v) in enumerate(items): ax.text(v+0.6,i,f'{v}/55',va='center',fontsize=9)
ax.set_xlim(0,60); ax.set_title('What the included studies report',loc='left',weight='bold'); ax.spines[['top','right']].set_visible(False)
plt.tight_layout(); plt.savefig('figs/gaps.png',dpi=220); plt.close()
q=X.quality_tier.value_counts().reindex(['A','B','C']).fillna(0)
fig,ax=plt.subplots(figsize=(5,2.8)); ax.bar(q.index,q.values,color=[GREEN,BLUE,ORANGE])
for i,v in enumerate(q.values): ax.text(i,v+0.5,str(int(v)),ha='center')
ax.set_title('Quality tier (R/A/T/C)',loc='left',weight='bold'); ax.spines[['top','right']].set_visible(False)
plt.tight_layout(); plt.savefig('figs/quality.png',dpi=220); plt.close()
print('ok')
