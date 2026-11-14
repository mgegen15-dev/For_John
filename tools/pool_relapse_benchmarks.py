"""Pool 4-month event-free / progression-free rates in measurable relapsed
osteosarcoma by drug class, across the three benchmark files in data/
(registry, published papers, basket trials). One hand-picked row per trial arm
(see `sel`), weighted by patients. Requires pandas.

Usage: python3 tools/pool_relapse_benchmarks.py (run from the repo root)
"""
import pandas as pd, math
D='data/'
reg=pd.read_csv(D+'osteosarcoma_relapse_benchmarks.csv'); reg['src']='registry'
pub=pd.read_csv(D+'osteosarcoma_relapse_benchmarks_published.csv'); pub['src']='published'
bas=pd.read_csv(D+'osteosarcoma_relapse_benchmarks_basket.csv'); bas['src']='basket'
a=pd.concat([reg,pub,bas],ignore_index=True)
# select one row per arm: (src, trial substring, agent substring, measure substring, time_frame substring)
sel={
 'Older cytotoxics (single agents/doublets)':[
   ('published','COG pooled','pooled','event-free','4 months'),
   ('registry','AOST1322','eribulin','disease control','4 months'),
   ('published','NPCF','gemcitabine','progression-free survival','4 months')],
 'Antibodies, ADC, DNA-repair (non-IGF-1R)':[
   ('registry','AOST1321','denosumab','disease control','4 months'),
   ('registry','AOST1521','glembatumumab','disease control','6 cycles'),
   ('registry','Dana-Farber','olaparib','event-free','4 months')],
 'IGF-1R antibody (R1507, basket)':[
   ('basket','R1507','R1507','progression-free rate','18 weeks')],
 'Non-VEGFR kinase inhibitor (imatinib, adult basket)':[
   ('basket','imatinib','imatinib','clinical benefit','4 months')],
 'VEGFR TKI alone':[
   ('published','sorafenib phase 2','sorafenib','progression-free survival (KM)','4 months'),
   ('published','apatinib phase 2','apatinib','progression-free survival (KM)','4 months'),
   ('published','ITCC-050','lenvatinib','progression-free rate (binomial)','4 months','2B'),
   ('published','CABONE','cabozantinib','progression-free survival (KM)','4 months')],
 'VEGFR TKI + IE':[
   ('published','ITCC-050','ifosfamide','progression-free rate','4 months','3A'),
   ('published','OLIE','lenvatinib','progression-free survival (KM)','4 months'),
   ('published','OAIE','apatinib','progression-free survival (KM)','4 months')],
 'VEGFR TKI + PD-1 (APFAO)':[
   ('published','APFAO','camrelizumab','progression-free survival (KM)','4 months')],
 'IE alone (randomized controls)':[
   ('published','OLIE','ifosfamide + etoposide','progression-free survival (KM)','4 months','Arm B'),
   ('published','OAIE','ifosfamide + etoposide','progression-free survival (KM)','4 months','IE control')],
}
sens={
 'VEGFR TKI alone + ADVL1622 (35%, endpoint = response or disease control, definition not seen)':('basket','ADVL1622','cabozantinib','response + disease control',''),
 'VEGFR TKI + topotecan (PAZOTOP, 12-week rate)':('basket','PAZOTOP','pazopanib','progression-free rate','12 weeks'),
}
def pick(k):
    s,tr,ag,me,tf=k[:5]; armk=k[5] if len(k)>5 else ''
    m=a[a.arm.str.contains(armk,regex=False)&(a.src==s)&a.trial.str.contains(tr,regex=False)&a.agent.str.contains(ag,regex=False)&a.measure.str.contains(me,regex=False)&a.time_frame.fillna('').str.contains(tf,regex=False)]
    assert len(m)==1,(k,len(m))
    return m.iloc[0]
def summ(rows):
    n=sum(r.n for r in rows); p=sum(r.n*r.percent for r in rows)/n
    se=math.sqrt(p/100*(1-p/100)/n)*100
    return n,p,max(0,p-1.96*se),min(100,p+1.96*se),min(r.percent for r in rows),max(r.percent for r in rows)
out=[]
for c,ks in sel.items():
    rows=[pick(k) for k in ks]
    n,p,lo,hi,mn,mx=summ(rows)
    out.append((c,len(rows),n,p,lo,hi,mn,mx))
    print(f'| {c} | {len(rows)} | {n} | {p:.1f}% (about {lo:.0f}-{hi:.0f}%) | {mn:g}-{mx:g}% |')
    for r in rows: print('     ',r.trial,'|',r.agent,'|',r.n,r.percent)
print('sensitivity:')
base=[pick(k) for k in sel['VEGFR TKI alone']]
r=pick(sens['VEGFR TKI alone + ADVL1622 (35%, endpoint = response or disease control, definition not seen)'])
n,p,lo,hi,mn,mx=summ(base+[r]); print(f'TKI alone + ADVL1622: arms {len(base)+1} n {n} {p:.1f}% ({lo:.0f}-{hi:.0f}) range {mn}-{mx}')
r=pick(sens['VEGFR TKI + topotecan (PAZOTOP, 12-week rate)']); print('PAZOTOP',r.n,r.percent)
bio=[pick(k) for k in sel['Antibodies, ADC, DNA-repair (non-IGF-1R)']]+[pick(sel['IGF-1R antibody (R1507, basket)'][0])]
n,p,lo,hi,mn,mx=summ(bio); print(f'all antibodies/ADC/DNA-repair incl R1507: arms 4 n {n} {p:.1f}% ({lo:.0f}-{hi:.0f}) range {mn}-{mx}')
old=[pick(k) for k in sel['Older cytotoxics (single agents/doublets)']]+[pick(sel['Non-VEGFR kinase inhibitor (imatinib, adult basket)'][0])]
n,p,lo,hi,mn,mx=summ(old); print(f'older + imatinib: arms 4 n {n} {p:.1f}% ({lo:.0f}-{hi:.0f}) range {mn}-{mx}')
nonT=old+bio
n,p,lo,hi,mn,mx=summ(nonT); print(f'ALL non-VEGFR single-agent-type arms: arms {len(nonT)} n {n} {p:.1f}% ({lo:.0f}-{hi:.0f}) range {mn}-{mx}')
# CABONE framing check (audit 2026-11-14): the main table uses CABONE's KM PFS at
# 4 months (71.4%). The trial's own primary endpoint, crude 6-month
# non-progression, was 33.3% (14/42), the same in paper and registry.
cab_crude=pick(('registry','CABONE','cabozantinib','non-progression','6 months'))
alt=[r for r in base if 'CABONE' not in r.trial]+[cab_crude]
n,p,lo,hi,mn,mx=summ(alt); print(f'TKI alone with CABONE crude 6-month primary endpoint (33.3%) instead of KM 4-month: arms {len(alt)} n {n} {p:.1f}% ({lo:.0f}-{hi:.0f}) range {mn}-{mx}')
