import pandas as pd
INC = [1,2,3,4,5,6,11,15,17,18,26,30,39,40,43,52,53,57,60,62,64,71,74,76,82,84,86,93,95,97,102,103,105,148,188,202,204,207,211,244,264,270,279]
EXC = {
 'E1': [37,41,48,50,56,58,67,73,77,94,96,99,101,107,110,111,116,120,127,128,130,132,133,139,140,142,146,147,149,153,155,156,162,163,169,172,173,176,178,179,181,183,191,192,193,196,197,198,199],
 'E2': [27,46,47,49,59,61,65,66,87,109,112,119,138,157,159,160,164,170,177,180,184,189],
 'E3': [25,35,141,143,161,297],
 'E5': [150,203,209,212,213,227,236,246,250,253,254,256,257,262,274,291,298],
 'E6': [9,12,31,32,51,68,80,90,125,134,135,154,167,168],
 'I1': [85,88,104,158,190,266],
 'I4': [70,79,271,277,290,292,295],
}
REASON = {
 'E1': 'E1: audio, speech or text deepfake, not face images',
 'E2': 'E2: generic synthetic or tampered image detection, no face forgery benchmark',
 'E3': 'E3: no frequency-domain component in the method',
 'E5': 'E5: not a primary study (survey, book matter, supplementary file or table)',
 'E6': 'E6: attack on detectors or proactive defense, not a detector',
 'I1': 'I1: not a deepfake detector (generation, face recognition or other task)',
 'I4': 'I4: published before 2019',
}
s = pd.read_csv('screening.csv')
def decide(i, ab):
    if i in INC: return 'include', 'I1-I3 met at title/abstract level: face forgery detector using frequency cues with a generalization focus'
    for k, ids in EXC.items():
        if i in ids: return 'exclude', REASON[k]
    if not isinstance(ab, str) or len(ab.split()) < 20:
        return 'maybe', 'insufficient abstract, decide at full text'
    return 'maybe', 'frequency use or cross-dataset evaluation unclear from abstract'
d = [decide(r.id, r.abstract) for r in s.itertuples()]
s['ta_decision'] = [x[0] for x in d]
s['ta_reason'] = [x[1] for x in d]
s['reviewer'] = 'AI-proposed (Claude); pending human confirmation'
s['decision_source'] = 'ai_assisted'
s['round'] = 1
s.to_csv('screening.csv', index=False)
print(s.ta_decision.value_counts().to_dict())
print(s[s.ta_decision=='exclude'].ta_reason.str[:3].value_counts().to_dict())
