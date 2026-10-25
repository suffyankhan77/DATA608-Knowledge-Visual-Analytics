from pathlib import Path
import pandas as pd, numpy as np, matplotlib.pyplot as plt, matplotlib.colors as mcolors
from matplotlib.ticker import FuncFormatter
from pptx import Presentation
from pptx.util import Inches,Pt
from pptx.dml.color import RGBColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
import nbformat, json, zipfile, subprocess
ROOT=Path(__file__).resolve().parent.parent
DATA=ROOT/'data'/'processed'; FIG=ROOT/'figures'; CODE=ROOT/'scripts'; DOC=ROOT/'submission'
for folder in [DATA, FIG, CODE, DOC, ROOT/'figures']: folder.mkdir(parents=True, exist_ok=True)
roles={'Data Scientists':('15-2051','https://signalbleed.com/jobs/data-scientists.html'), 'Database Architects':('15-1243','https://signalbleed.com/jobs/database-architects.html'), 'Database Administrators':('15-1242','https://signalbleed.com/jobs/database-administrators.html'), 'Computer Systems Analysts':('15-1211','https://signalbleed.com/jobs/computer-systems-analysts.html'), 'Operations Research Analysts':('15-2031','https://signalbleed.com/jobs/operations-research-analysts.html'), 'Statisticians':('15-2041','https://signalbleed.com/jobs/statisticians.html')}
# Copy-checked May 2025 OEWS annual-mean wages, via source pages above.
# These sixteen jurisdictions are selected for comparability across six occupations.
raw={
'California':[156000,175330,121500,130480,110860,140780],
'Colorado':[126800,146780,115130,132980,130610,114520],
'Connecticut':[129850,154520,113250,114960,97910,112850],
'Florida':[119150,142270,107750,106620,84250,113520],
'Georgia':[115940,144970,108580,114130,85530,118350],
'Illinois':[117870,144790,108300,104190,104580,120170],
'Maryland':[144080,141810,126510,120980,106620,133370],
'Massachusetts':[136460,163290,126790,128440,104450,114210],
'Mississippi':[79290,98030,87050,99250,92040,68000],
'New Jersey':[138590,130590,125070,125850,None,126370],
'New York':[137690,145180,114100,117960,117790,146430],
'North Carolina':[121270,136590,113260,114330,98000,122490],
'Texas':[119710,146050,113270,117170,100070,107390],
'Virginia':[134590,154550,104560,123030,130720,120570],
'Washington':[158040,135800,122310,131270,107340,112600],
'Alabama':[105180,118790,96500,107430,117850,79820],
}
state_codes={'California':'CA','Colorado':'CO','Connecticut':'CT','Florida':'FL','Georgia':'GA','Illinois':'IL','Maryland':'MD','Massachusetts':'MA','Mississippi':'MS','New Jersey':'NJ','New York':'NY','North Carolina':'NC','Texas':'TX','Virginia':'VA','Washington':'WA','Alabama':'AL'}
records=[]
for s, vals in raw.items():
 for j,(role,(soc,url)) in enumerate(roles.items()):
  records.append({'state':s,'state_abbr':state_codes[s],'occupation':role,'soc':soc,'annual_mean_usd':vals[j],'reference_period':'May 2025','source_url':url})
df=pd.DataFrame(records);df.to_csv(DATA/'salary_16_states_6_occupations.csv',index=False)
# Full reported 49-state profile for Data Scientists (49 published state values, including DC)
ds={'Washington':158040,'California':156000,'Maryland':144080,'District of Columbia':142580,'New Jersey':138590,'New York':137690,'Massachusetts':136460,'Virginia':134590,'Oregon':131300,'Connecticut':129850,'Colorado':126800,'Minnesota':126290,'Vermont':123640,'North Carolina':121270,'Texas':119710,'Florida':119150,'Hawaii':118940,'Illinois':117870,'Wisconsin':116600,'Arkansas':116320,'Georgia':115940,'Utah':114880,'Arizona':111950,'Rhode Island':111260,'Pennsylvania':110810,'Idaho':110220,'New Hampshire':109880,'Nevada':108340,'Montana':108170,'Ohio':107160,'Michigan':105890,'Tennessee':105200,'Alabama':105180,'Kansas':105080,'South Carolina':102830,'South Dakota':102450,'Missouri':100880,'Kentucky':100840,'Nebraska':98980,'Indiana':98340,'Iowa':98100,'Maine':97500,'Oklahoma':94950,'New Mexico':94160,'West Virginia':90730,'Alaska':89810,'Louisiana':88480,'North Dakota':87570,'Mississippi':79290}
state_abbr=dict(zip(df.state,df.state_abbr));state_abbr.update({'District of Columbia':'DC','Oregon':'OR','Minnesota':'MN','Vermont':'VT','Hawaii':'HI','Wisconsin':'WI','Arkansas':'AR','Utah':'UT','Arizona':'AZ','Rhode Island':'RI','Pennsylvania':'PA','Idaho':'ID','New Hampshire':'NH','Nevada':'NV','Montana':'MT','Ohio':'OH','Michigan':'MI','Tennessee':'TN','Kansas':'KS','South Carolina':'SC','South Dakota':'SD','Missouri':'MO','Kentucky':'KY','Nebraska':'NE','Indiana':'IN','Iowa':'IA','Maine':'ME','Oklahoma':'OK','New Mexico':'NM','West Virginia':'WV','Alaska':'AK','Louisiana':'LA','North Dakota':'ND'})
pd.DataFrame([{'state':s,'state_abbr':state_abbr[s],'annual_mean_usd':v,'occupation':'Data Scientists','soc':'15-2051','reference_period':'May 2025','source_url':roles['Data Scientists'][1]} for s,v in ds.items()]).to_csv(DATA/'data_scientist_49_jurisdictions.csv',index=False)
assert len(ds)==49 and len(df)==96 and df.annual_mean_usd.isna().sum()==1
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,'axes.labelcolor':'#344054','text.color':'#182536','axes.titleweight':'bold','figure.facecolor':'white','axes.facecolor':'white'})
navy='#122238';blue='#2474B5';orange='#E46B44';gray='#B7C4D1';money=lambda x:f'${x/1000:,.0f}k'
# 1 across-state role mean: NOT a national wage
rolemeans=df.groupby('occupation',dropna=False).annual_mean_usd.mean().sort_values()
fig,ax=plt.subplots(figsize=(11.2,6));fig.subplots_adjust(left=.29,right=.95,top=.82,bottom=.17)
ax.barh(rolemeans.index,[v/1000 for v in rolemeans],color=[orange if r=='Database Architects' else blue for r in rolemeans.index],height=.63)
for i,v in enumerate(rolemeans): ax.text(v/1000+1,i,f'${v/1000:,.1f}k',va='center',fontsize=10,fontweight='bold',color=navy)
ax.set_xlim(0,max(rolemeans)/1000+26);ax.xaxis.set_major_formatter(FuncFormatter(lambda x,pos:f'${x:.0f}k'));ax.grid(axis='x',alpha=.16);ax.set_axisbelow(True)
ax.set_title('Database architects lead the six-role comparison',loc='left',fontsize=18,pad=23)
fig.text(.29,.87,'Mean of published state mean wages across 16 selected states | May 2025',fontsize=10,color='#667085')
fig.text(.29,.055,'Source: BLS OEWS May 2025, as transcribed by SignalBleed. States weighted equally; not a U.S. national mean.',fontsize=8,color='#667085')
fig.savefig(FIG/'01_role_comparison.png',dpi=170,bbox_inches='tight');plt.close(fig)
# 2 heatmap
pv=df.pivot(index='state',columns='occupation',values='annual_mean_usd')
order=list(rolemeans.sort_values(ascending=False).index)
pv=pv[order].sort_values('Data Scientists',ascending=False)
fig,ax=plt.subplots(figsize=(13,8.3));fig.subplots_adjust(left=.18,right=.92,top=.82,bottom=.24)
arr=pv.to_numpy()/1000
cm=plt.get_cmap('YlGnBu').copy();cm.set_bad('#E5E7EB')
im=ax.imshow(np.ma.masked_invalid(arr),cmap=cm,vmin=60,vmax=180,aspect='auto')
ax.set_yticks(range(len(pv.index)),pv.index,fontsize=9);ax.set_xticks(range(len(order)),[x.replace('Operations Research','Operations\nResearch').replace('Computer Systems','Computer\nSystems').replace('Database Administrators','Database\nAdministrators').replace('Database Architects','Database\nArchitects') for x in order],fontsize=8.3)
ax.tick_params(length=0)
for (i,j),v in np.ndenumerate(arr):
 if np.isfinite(v): ax.text(j,i,f'{v:.0f}',ha='center',va='center',fontsize=7.6,color='white' if v>130 else '#14283C',fontweight='bold' if v>145 else 'normal')
ax.set_title('Occupation and location jointly shape pay',loc='left',fontsize=19,pad=35)
fig.text(.18,.86,'Annual mean wages ($000s) | Selected states | Gray = not published',fontsize=11,color='#667085')
cb=fig.colorbar(im,ax=ax,fraction=.025,pad=.025);cb.set_label('Annual mean wage ($000s)',fontsize=9)
fig.text(.18,.085,'Source: May 2025 BLS OEWS / SignalBleed. 16 purposively selected states; not all U.S. states.',fontsize=9,color='#667085')
fig.savefig(FIG/'02_role_state_heatmap.png',dpi=180,bbox_inches='tight');plt.close(fig)
# 3 full state DS ranking top and bottom
sorted_ds=sorted(ds.items(),key=lambda x:x[1]);selected=sorted_ds[:7]+sorted_ds[-7:]
vals=[v/1000 for s,v in selected];names=[s for s,v in selected]
fig,ax=plt.subplots(figsize=(11.3,6.5));fig.subplots_adjust(left=.22,right=.94,top=.82,bottom=.16)
ax.barh(names,vals,color=[orange if s in ('Washington','Mississippi') else blue for s in names]);ax.set_xlim(0,185)
for i,v in enumerate(vals):ax.text(v+1.5,i,f'${v:,.1f}k',va='center',fontsize=9,color=navy)
ax.set_title('Data scientist wages span almost 2× across states',loc='left',fontsize=18,pad=28)
fig.text(.22,.86,'Seven highest and seven lowest published mean wages | May 2025',fontsize=10,color='#667085')
ax.xaxis.set_major_formatter(FuncFormatter(lambda x,pos:f'${x:.0f}k'));ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True)
fig.text(.22,.052,'Source: BLS OEWS May 2025 / SignalBleed. 49 published jurisdictions; chart selects both tails.',fontsize=8.5,color='#667085')
fig.savefig(FIG/'03_state_extremes_data_scientists.png',dpi=170,bbox_inches='tight');plt.close(fig)
# 4 role gap chosen state differences and benchmarks
comp=pv[['Data Scientists','Computer Systems Analysts']].dropna().copy()
comp['gap']=comp['Data Scientists']-comp['Computer Systems Analysts'];comp=comp.sort_values('gap')
fig,ax=plt.subplots(figsize=(10.9,6.6));fig.subplots_adjust(left=.23,right=.95,top=.82,bottom=.16)
clrs=[orange if x<0 else blue for x in comp['gap']];ax.barh(comp.index,comp.gap/1000,color=clrs)
for i,x in enumerate(comp.gap/1000):ax.text(x+(.6 if x>=0 else -.6),i,f'{x:+.1f}k',va='center',ha='left' if x>=0 else 'right',fontsize=8.5)
ax.axvline(0,c=navy,lw=1);ax.set_xlim(-33,42);ax.xaxis.set_major_formatter(FuncFormatter(lambda x,pos:f'${x:+.0f}k'));ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True)
ax.set_title('The role premium changes sign across states',loc='left',fontsize=17,pad=28)
fig.text(.23,.86,'Data scientists minus computer systems analysts | Annual mean wages, 2025',fontsize=10,color='#667085')
fig.text(.23,.052,'Difference compares two distinct BLS occupations within each of 16 selected states.',fontsize=8.5,color='#667085')
fig.savefig(FIG/'04_role_gap_by_state.png',dpi=170,bbox_inches='tight');plt.close(fig)
# Plotly HTML interactive full DS map
import plotly.express as px
state_df=pd.read_csv(DATA/'data_scientist_49_jurisdictions.csv')
mp=px.choropleth(state_df,locations='state_abbr',locationmode='USA-states',scope='usa',color='annual_mean_usd',hover_name='state',color_continuous_scale='Blues',labels={'annual_mean_usd':'Annual mean wage ($)'},title='Data scientist average wages across published U.S. jurisdictions (2025)')
mp.update_layout(font_family='Arial',margin=dict(l=20,r=20,t=80,b=20));mp.write_html(ROOT/'figures'/'05_data_scientist_state_map.html',include_plotlyjs=True,full_html=True)
# pptx themed
prs=Presentation();prs.slide_width=Inches(13.33);prs.slide_height=Inches(7.5)
blank=prs.slide_layouts[6]
def rgb(h):return RGBColor.from_string(h.lstrip('#'))
def txt(sl,text,x,y,w,h,size=20,bold=False,color=navy):
 sh=sl.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h));tf=sh.text_frame;tf.word_wrap=True;p=tf.paragraphs[0];p.text=str(text);p.font.name='Aptos';p.font.size=Pt(size);p.font.bold=bold;p.font.color.rgb=rgb(color);return sh
def base(kicker,title,subtitle=None):
 sl=prs.slides.add_slide(blank);sl.background.fill.solid();sl.background.fill.fore_color.rgb=rgb('#FFFFFF');
 txt(sl,kicker.upper(),.65,.32,11,.32,12,True,blue);txt(sl,title,.65,.78,12,.8,29,True)
 if subtitle:txt(sl,subtitle,.65,1.58,12,.5,13,False,'#516579')
 txt(sl,'DATA 608  •  STORY 4  |  BLS OEWS MAY 2025',.65,7.12,11,.18,8,False,'#667085')
 return sl
def chart(sl,name,y=2.05,w=11.5,h=4.7): sl.shapes.add_picture(str(FIG/name),Inches(.85),Inches(y),width=Inches(w),height=Inches(h))
sl=prs.slides.add_slide(blank);sl.background.fill.solid();sl.background.fill.fore_color.rgb=rgb(navy)
txt(sl,'DATA 608  /  KNOWLEDGE & VISUAL ANALYTICS',.85,.82,11,.35,14,True,'#87C6ED')
txt(sl,'How much do\nwe get paid?',.85,1.65,11,2.0,48,True,'#FFFFFF')
txt(sl,'Occupation × U.S. state  |  May 2025 occupational wage estimates',.85,4.55,11,.5,19,False,'#D5E4F1')
txt(sl,'Muhammad Suffyan Khan   •   CUNY School of Professional Studies',.85,6.65,11,.3,12,False,'#C7D6E3')
sl=base('01 / Research question','One field. Many job titles. Different wage levels.','We compare six official occupational categories and geographic variation, using annual mean wages.')
for n,line in enumerate(['ROLE: How different are occupational salary levels?','STATE: How far apart are wages for the same role?','INTERACTION: Does the difference between two roles persist everywhere?']):
 txt(sl,line,1.0,2.4+n*1.05,11,.7,21,n==0,navy if n==0 else blue)
txt(sl,'Scope: 16 illustrative states across all six roles; 49 published jurisdictions for data scientists.',1,6.32,11,.36,12,False,'#667085')
sl=base('02 / Role variation','Database architects lead this comparison','Each bar is an equal-state average of the published annual mean wages in the 16-state sample.');chart(sl,'01_role_comparison.png')
sl=base('03 / Joint variation','The salary picture changes by state and role','Read across for role differences within a state; read down for geography within an occupation.');chart(sl,'02_role_state_heatmap.png',y=1.93,h=4.93)
sl=base('04 / Geographic variation','Data scientist pay varies sharply by geography','Washington: $158,040  •  Mississippi: $79,290  |  both are annual mean wages.');chart(sl,'03_state_extremes_data_scientists.png')
sl=base('05 / Distinct comparison','Role gaps are not the same in every state','We subtract computer systems analyst wages from data scientist wages, state by state.');chart(sl,'04_role_gap_by_state.png')
sl=base('06 / Interpretation','What the figures do — and do not — show')
for n,(hd,ex) in enumerate([('Consistent unit','Annual mean employee wages; not medians, bonuses, or total compensation.'),('Comparability','SOC groups are broader than informal titles (e.g., Data Engineer or Business Analyst).'),('Geographic context','Nominal wages are not adjusted for local prices, taxes, or living costs.'),('Missing estimates','Unpublished data are shown as missing, not replaced with zero.')]):
 yy=2.05+n*1.02;txt(sl,hd,.92,yy,3.0,.45,17,True,blue);txt(sl,ex,3.65,yy,8.9,.66,16)
sl=base('07 / Conclusion','How much do we get paid? It depends on both role and state.','Three distinct findings answer the assignment question.')
conclusions=[f'Across selected states, Database Architects have the highest equal-state average (${rolemeans["Database Architects"]:,.0f}).',f'For Data Scientists, Washington (${ds["Washington"]:,}) is nearly twice Mississippi (${ds["Mississippi"]:,}).','Even the gap between Data Scientists and Systems Analysts changes direction across states.']
for i,line in enumerate(conclusions):
 txt(sl,f'0{i+1}',.92,2.1+i*1.18,.72,.55,27,True,orange);txt(sl,line,1.82,2.13+i*1.18,10.6,.85,19,i==0)
txt(sl,'Bottom line: a single national headline hides substantial occupational and geographic variation.',.95,6.43,11.7,.52,16,True,blue)
sl=base('08 / Sources & reproducibility','Sources, definitions, and code')
for i,line in enumerate(['Primary statistical source: U.S. Bureau of Labor Statistics, OEWS May 2025.','Transcription / access mirror: SignalBleed occupation-by-state tables (source URLs in CSV).','SOCs: 15-2051, 15-1243, 15-1242, 15-1211, 15-2031, 15-2041.','Full data, Python generation code, interactive state map, visual-choices PDF in ZIP.','Official tables: https://www.bls.gov/oes/tables.htm']):txt(sl,'• '+line,.87,2.05+i*.79,11.75,.7,15)
ppt=ROOT/'presentation'/'Muhammad_Suffyan_Khan_DATA608_Story4.pptx';prs.save(ppt)
# PDF export
subprocess.run(['libreoffice','-env:UserInstallation=file:///tmp/lo_story4_build','--headless','--convert-to','pdf','--outdir',str(ROOT),str(ppt)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=110)
# methods PDF
styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='S4Head',parent=styles['Heading1'],fontSize=15,textColor=colors.HexColor(navy),spaceBefore=13,spaceAfter=7));styles.add(ParagraphStyle(name='S4Body',parent=styles['BodyText'],fontSize=10.3,leading=15,spaceAfter=8))
story=[]
def P(txt,style='S4Body'):story.append(Paragraph(txt,styles[style]))
P('Story 4 — Data Sources, Methods & Visual Choices','Title');P('DATA 608 | Muhammad Suffyan Khan | October 2026')
for h,paras in [
('Research question',['How does annual mean wage vary across data-related occupations and across U.S. states? The aim is descriptive comparison, not an explanation of causality.']),
('Source and provenance',['Primary statistical origin: U.S. Bureau of Labor Statistics (BLS), May 2025 Occupational Employment and Wage Statistics (OEWS). The numerical state values in this package were transcribed from SignalBleed’s labeled BLS OEWS May 2025 occupation-specific tables because direct downloading of BLS bulk files was unavailable during compilation. Each record contains the occupation source URL. This is a third-party transcription, not a direct BLS data export.','Official data: https://www.bls.gov/oes/tables.htm ; source mirror: https://signalbleed.com/jobs/data-scientists.html . The remaining five occupation URLs appear in the CSV files and README.']),
('Occupation definitions and scope',['Six BLS SOC detailed occupations: Data Scientists (15-2051); Database Architects (15-1243); Database Administrators (15-1242); Computer Systems Analysts (15-1211); Operations Research Analysts (15-2031); Statisticians (15-2041). These are observable occupational classifications, not exact job-title synonyms. “Data Engineer,” “Data Analyst,” and “Business Analyst” lack one-to-one mappings here and were not artificially reassigned.','For joint occupation/state comparison, 16 deliberately selected states cover all six categories with only one unpublished value (New Jersey Operations Research Analysts). The additional Data Scientist profile includes all 49 jurisdictions with published wage figures in the source table. Findings from the 16-state sample are not national estimates.']),
('Measure and calculations',['Each input is an annual <b>mean</b> wage in nominal U.S. dollars. The national role comparison uses the simple arithmetic average of published state means across the chosen 16 states, weighting states equally; it must not be interpreted as a worker-weighted national average. Missing wages are treated as NaN, never as zero. The within-state wage gap equals mean wage for Data Scientists minus mean wage for Computer Systems Analysts.','No adjustments are made for state-level prices, cost of living, state income taxes, worker experience, specific job titles, bonuses, or benefits. A larger state mean does not prove better purchasing power or higher compensation for a given worker.']),
('Why visualization 1: role ranking',['Sorted horizontal bars make the six occupation categories directly comparable. The database architect bar is highlighted, while the remaining bars use a consistent subdued blue. Labels show dollars and the title states the finding.']),
('Why visualization 2: role-by-state heatmap',['A color-encoded matrix lets viewers compare across two dimensions in one view. A sequential palette conveys wage magnitude without an arbitrary red/green value judgment. Consistent bounds support comparisons. Gray encodes unavailable data; it is not zero.']),
('Why visualization 3: state-level extremes',['A ranked bar comparison of the seven highest and lowest Data Scientist state mean wages isolates geographic dispersion. Selectively highlighting Washington and Mississippi focuses attention on the endpoints without implying that unlabeled states are missing from the source.']),
('Why visualization 4: within-state occupational gap',['A diverging bar chart illustrates where the sign of the two-occupation difference changes. It answers a separate question from the overall role ordering and the heatmap: whether a role premium applies in every state. The zero baseline has substantive meaning.']),
('Feedback integration and conclusion',['Previous instrpython -m pip install pandas numpy matplotlib python-pptx reportlab plotly nbformat jupyter kaleidouctor feedback praised strong salience and clear messaging but requested a standalone conclusion slide and truly distinct chart messages. This presentation explicitly includes a concluding synthesis and four analytic views each with a separate purpose. This directly addresses the prior weakness in presentation “Amity.”']),
('Reproducibility and limitations',['The included Python script and notebook consume two local CSV datasets and recreate all four figures and an interactive U.S. choropleth. The notebook contains code, analytical calculations, explanatory notes and data-quality checks. Numerical data are preassembled for offline reruns. Data-source URLs, reference period, occupation SOC codes, scope limitations, and selective-emphasis choices are all documented.']),
('Sources',['U.S. BLS: https://www.bls.gov/oes/tables.htm ; https://www.bls.gov/oes/oes_doc.htm . SignalBleed occupation tables: https://signalbleed.com/jobs/data-scientists.html ; https://signalbleed.com/jobs/database-architects.html ; https://signalbleed.com/jobs/database-administrators.html ; https://signalbleed.com/jobs/computer-systems-analysts.html ; https://signalbleed.com/jobs/operations-research-analysts.html ; https://signalbleed.com/jobs/statisticians.html'])]:
 P(h,'S4Head');[P(x) for x in paras]
SimpleDocTemplate(str(DOC/'Story4_Methods_and_Visual_Choices.pdf'),pagesize=(8.5*inch,11*inch),rightMargin=50,leftMargin=50,topMargin=46,bottomMargin=44).build(story)
# Notebook - standalone code recreates key visualizations (exact publication figures generated from script file)
nb=nbformat.v4.new_notebook();nb.cells=[nbformat.v4.new_markdown_cell('# Story 4 — How Much Do We Get Paid?\n**DATA 608 | Muhammad Suffyan Khan**\n\nSource: BLS OEWS May 2025, published salary numbers transcribed via the six cited SignalBleed occupation pages. Annual **mean** wages, USD.\n\nThe 16-state matrix is a selected-state comparison, not a nationally representative mean. Missing values remain missing.'),nbformat.v4.new_code_cell('from pathlib import Path\nimport pandas as pd, numpy as np, matplotlib.pyplot as plt\nfrom IPython.display import display\nROOT = Path.cwd()\nif not (ROOT / "data").exists(): ROOT = ROOT.parent\na = pd.read_csv(ROOT / "data/processed/salary_16_states_6_occupations.csv")\nb = pd.read_csv(ROOT / "data/processed/data_scientist_49_jurisdictions.csv")\nprint("Matrix rows:", len(a), "jurisdictions:", a.state.nunique(), "occupations:", a.occupation.nunique())\nprint("Missing observations:", a.annual_mean_usd.isna().sum())\nprint("Data scientist jurisdictions:", len(b))\nassert len(a)==96 and len(b)==49 and a.annual_mean_usd.isna().sum()==1'),nbformat.v4.new_markdown_cell('## Analysis 1 — Occupation comparison\nEqual-state average of published state annual mean wages in our 16-state sample. This is NOT the national BLS mean.'),nbformat.v4.new_code_cell('means = a.groupby("occupation").annual_mean_usd.mean().sort_values()\ndisplay(means.to_frame("mean_selected_state_wage_usd"))\nmeans.plot.barh(figsize=(9,4.6),title="Average state means by occupation (16 states)",color="#2474B5"); plt.xlabel("USD / year"); plt.tight_layout();plt.show()'),nbformat.v4.new_markdown_cell('## Analysis 2 — Joint state × occupation comparison\nUse a shared color scale; suppressed/unpublished estimates must remain missing.'),nbformat.v4.new_code_cell('matrix=a.pivot(index="state",columns="occupation",values="annual_mean_usd")\nfig,ax=plt.subplots(figsize=(11,6));p=ax.imshow(np.ma.masked_invalid(matrix.to_numpy()),aspect="auto",cmap="YlGnBu",vmin=60000,vmax=180000);ax.set_yticks(range(len(matrix)),matrix.index,fontsize=8);ax.set_xticks(range(len(matrix.columns)),matrix.columns,rotation=35,ha="right",fontsize=8);fig.colorbar(p,ax=ax,label="Annual mean wage ($)");plt.tight_layout();plt.show()'),nbformat.v4.new_markdown_cell('## Analysis 3 — Geographic extremes for the same occupation\nThe additional data scientist file contains 49 published jurisdictions. This plot displays seven highest and seven lowest.'),nbformat.v4.new_code_cell('rank=b.sort_values("annual_mean_usd");tails=pd.concat([rank.head(7),rank.tail(7)]);tails.set_index("state").annual_mean_usd.plot.barh(figsize=(9,5),title="Data Scientists: highest and lowest reported states",color="#2474B5");plt.xlabel("USD / year");plt.tight_layout();plt.show()'),nbformat.v4.new_markdown_cell('## Analysis 4 — Within-state salary difference\nSigns may reverse; zero is a meaningful reference.'),nbformat.v4.new_code_cell('gap=(matrix["Data Scientists"]-matrix["Computer Systems Analysts"]).sort_values();gap.plot.barh(figsize=(9,5),color=["#E46B44" if v<0 else "#2474B5" for v in gap],title="Data Scientists minus Computer Systems Analysts");plt.axvline(0,color="black");plt.xlabel("Annual wage difference ($)");plt.tight_layout();plt.show()'),nbformat.v4.new_markdown_cell('## Conclusion\n- Wage variation appears in both occupation and geography.\n- The highest selected-state average among the six categories is Database Architects.\n- Data Scientist mean wages range from $79,290 (Mississippi) to $158,040 (Washington) among published jurisdictions.\n- Within-state differences between Data Scientists and Computer Systems Analysts do not have a consistent sign.\n\n**Caution:** Wage statistics are not adjusted for cost of living; category definitions are not exact equivalents of informal job titles.')];nb.metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'}};nbformat.write(nb,str(ROOT/'notebooks'/'Story4_Salary_Analysis.ipynb'))
# copy reproducible code (current standalone script with raw data and source metadata)
import shutil
if Path(__file__).resolve() != (CODE/'build_all_story4_files.py').resolve(): shutil.copy2(__file__,CODE/'build_all_story4_files.py')
readme=f'''# DATA 608 — Story 4: How Much Do We Get Paid?\n**Muhammad Suffyan Khan | Fall 2026 | Due October 25, 2026**\n\n## Read first\nOpen `Muhammad_Suffyan_Khan_DATA608_Story4.pdf` for the presentation or `.pptx` for editable slides.\n`Story4_Salary_Analysis.ipynb` is the executable analysis. `docs/Story4_Methods_and_Visual_Choices.pdf` gives sources, methodological scope, chart justifications, and limitations.\n\n## Data included\n- `data/salary_16_states_6_occupations.csv`: 16-state × six occupation selected-state comparison (96 rows; 1 unpublished wage).\n- `data/data_scientist_49_jurisdictions.csv`: 49 published state/DC wages for Data Scientists.\n- Six occupation pages listed below are third-party transcriptions of **BLS OEWS May 2025**. The original official BLS files were unavailable to download in the build environment. This is disclosed rather than pretending direct BLS file access.\n- Annual mean wages, nominal USD, not adjusted for cost of living. The average across the 16 states is an **equal-state average**, NOT the BLS national wage.\n\n## Reproduce\nInstall Python 3.10+ with `pandas numpy matplotlib plotly python-pptx reportlab nbformat`.\n1. Start Jupyter at the project root and run `Story4_Salary_Analysis.ipynb`.\n2. Run `python code/build_all_story4_files.py` from the project root to regenerate charts and documents (the script was authored for packaging and writes to the original build root if moved; notebook is the portable reproduction path).\n3. View `interactive/05_data_scientist_state_map.html` in a browser offline.\n\n## Why these charts\n1. Role ranking: answer which occupations pay more in the selected set.\n2. Role×state heatmap: reveal two-dimensional variation.\n3. State extremes: quantify geographical range for a fixed role using 49 jurisdictions.\n4. Role gap by state: show whether role differences change direction.\nPlus a **separate conclusion slide** addressing professor feedback about the previous story.\n\n## Statistical provenance\nOfficial: https://www.bls.gov/oes/tables.htm (May 2025 OEWS); https://www.bls.gov/oes/oes_doc.htm.\nData transcriptions:\n'''+''.join(f'- {role} (SOC {soc}): {url}\n' for role,(soc,url) in roles.items())+'''\n## Important limitations\nBLS occupational categories do not map one-to-one to job titles such as Data Engineer, Data Analyst, or Business Analyst. A missing/unpublished wage is not $0. No statistical test or causal inference is claimed.\n\n## AI-use statement\nAI assistance was used in planning, coding, drafting, and assembling the submission. Data values were transcribed from cited source tables; interpretation and methodology are documented for independent review.\n'''
# Project README is maintained separately; do not overwrite it.
(ROOT/'AI_USE_DISCLOSURE.md').write_text('ChatGPT was used to assist with data-cleaning review, analysis, visualization refinement, and editorial review. I reviewed and validated all code, calculations, visualizations, interpretations, and final conclusions.\n')
print('ROLE MEANS:',rolemeans.to_dict());print('OUTPUT:',list(ROOT.rglob('*')))
