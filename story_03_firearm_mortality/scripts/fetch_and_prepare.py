from __future__ import annotations

import io
import json
import pathlib
import urllib.parse
import urllib.request
from datetime import datetime, timezone

import pandas as pd
from scipy.stats import spearmanr


ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / 'data' / 'raw'
PROCESSED = ROOT / 'data' / 'processed'
for p in [RAW, PROCESSED, ROOT/'figures', ROOT/'notebooks', ROOT/'presentation', ROOT/'submission', ROOT/'sources', ROOT/'scripts']:
    p.mkdir(parents=True, exist_ok=True)

STATE_ABBR = {
    'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR','California':'CA','Colorado':'CO','Connecticut':'CT','Delaware':'DE','Florida':'FL','Georgia':'GA','Hawaii':'HI','Idaho':'ID','Illinois':'IL','Indiana':'IN','Iowa':'IA','Kansas':'KS','Kentucky':'KY','Louisiana':'LA','Maine':'ME','Maryland':'MD','Massachusetts':'MA','Michigan':'MI','Minnesota':'MN','Mississippi':'MS','Missouri':'MO','Montana':'MT','Nebraska':'NE','Nevada':'NV','New Hampshire':'NH','New Jersey':'NJ','New Mexico':'NM','New York':'NY','North Carolina':'NC','North Dakota':'ND','Ohio':'OH','Oklahoma':'OK','Oregon':'OR','Pennsylvania':'PA','Rhode Island':'RI','South Carolina':'SC','South Dakota':'SD','Tennessee':'TN','Texas':'TX','Utah':'UT','Vermont':'VT','Virginia':'VA','Washington':'WA','West Virginia':'WV','Wisconsin':'WI','Wyoming':'WY'}

def get(url: str) -> bytes:
    return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 DATA608 coursework analysis'}), timeout=45).read()

query = {'$where': "year_and_quarter='2024 Q4' and time_period='12 months ending with quarter' and cause_of_death='Firearm-related injury' and rate_type='Age-adjusted'", '$limit':'10'}
api_url = 'https://data.cdc.gov/resource/489q-934x.json?' + urllib.parse.urlencode(query)
data = json.loads(get(api_url))
assert len(data) == 1, f'Expected one matched CDC record, got {len(data)}'
row = data[0]
(RAW/'CDC_API_2024_firearm_age_adjusted.json').write_text(json.dumps({'request_url':api_url,'retrieved_utc':datetime.now(timezone.utc).isoformat(),'response':data},indent=2)+'\n',encoding='utf-8')
meta_url = 'https://data.cdc.gov/api/views/489q-934x.json'
meta = json.loads(get(meta_url))
(RAW/'CDC_API_dataset_metadata.json').write_text(json.dumps({'name':meta['name'],'description':meta.get('description'),'columns':[{'fieldName':c['fieldName'],'name':c['name']} for c in meta['columns']],'source_url':meta_url},indent=2)+'\n',encoding='utf-8')

scores_url = 'https://giffords.org/resources/scorecard2024/'
html = get(scores_url)
(RAW/'GIFFORDS_2024_scorecard_source.html').write_bytes(html)
t = pd.read_html(io.BytesIO(html))[0]
t = t[t['State'].isin(STATE_ABBR)].copy()
t = t.rename(columns={'Gun Law Strength  (Ranked)':'gun_law_strength_rank','State':'state','Grade':'gun_law_grade'})
t['gun_law_strength_rank'] = pd.to_numeric(t['gun_law_strength_rank'])
t['law_level'] = t.gun_law_grade.str[0].map({'F':1,'D':2,'C':3,'B':4,'A':5})
t['law_label'] = t.law_level.map({1:'1  Most lax (F)',2:'2  Lax (D)',3:'3  Middle (C)',4:'4  Strict (B)',5:'5  Strictest (A)'})
t['abbr'] = t.state.map(STATE_ABBR)
assert len(t)==50 and set(t.state)==set(STATE_ABBR) and t.law_level.notna().all()
t[['state','abbr','gun_law_grade','gun_law_strength_rank','law_level','law_label']].sort_values('state').to_csv(PROCESSED/'law_scale_50_states.csv',index=False)

rates = []
for state, abbr in STATE_ABBR.items():
    key='rate_'+state.lower().replace(' ','_')
    rates.append({'state':state,'abbr':abbr,'firearm_death_rate_2024':float(row[key]),'year':2024,'rate_type':'age-adjusted','period':'12 months ending 2024 Q4'})
rates=pd.DataFrame(rates)
rates.sort_values('state').to_csv(PROCESSED/'cdc_2024_age_adjusted_rates_50_states.csv',index=False)
v=t[['state','abbr','gun_law_grade','gun_law_strength_rank','law_level','law_label']].merge(rates,on=['state','abbr'],validate='one_to_one').sort_values(['law_level','firearm_death_rate_2024'],ascending=[False,True])
v.to_csv(PROCESSED/'state_analysis_2024.csv',index=False)
summary=v.groupby(['law_level','law_label'],as_index=False).agg(states=('state','size'),mean_rate=('firearm_death_rate_2024','mean'),median_rate=('firearm_death_rate_2024','median'),min_rate=('firearm_death_rate_2024','min'),max_rate=('firearm_death_rate_2024','max'))
summary.to_csv(PROCESSED/'five_level_summary.csv',index=False,float_format='%.3f')
rho,p=spearmanr(v.law_level,v.firearm_death_rate_2024)
payload={'count':len(v),'spearman_rho':float(rho),'spearman_p_two_sided':float(p),'five_level_summary':summary.round(3).to_dict(orient='records'),'lowest_rate_states':v.nsmallest(5,'firearm_death_rate_2024')[['state','gun_law_grade','firearm_death_rate_2024']].to_dict(orient='records'),'highest_rate_states':v.nlargest(5,'firearm_death_rate_2024')[['state','gun_law_grade','firearm_death_rate_2024']].to_dict(orient='records')}
(PROCESSED/'analysis_summary.json').write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
print('CDC API:',api_url)
print('50-state join:',len(v),'Spearman rho:',round(rho,3),'p:',round(p,5))
print(summary.to_string(index=False))
