from pathlib import Path
import json, io, contextlib, base64, html, shutil
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter
import nbformat

root=Path(__file__).resolve().parent.parent
# Execute the actual notebook code using the saved data, capturing real outputs.
nbpath=root/'notebooks/Story_3_Gun_Laws_Firearm_Mortality.ipynb'
nb=nbformat.read(nbpath,as_version=4)
import os
old=os.getcwd();os.chdir(root)
ctx={};n=0
for c in nb.cells:
 if c.cell_type!='code':continue
 n+=1;stream=io.StringIO()
 with contextlib.redirect_stdout(stream):exec(c.source,ctx)
 c.execution_count=n;c.outputs=[]
 if stream.getvalue():c.outputs=[nbformat.v4.new_output('stream',name='stdout',text=stream.getvalue())]
os.chdir(old);nbformat.validate(nb);nbformat.write(nb,nbpath)

# The PDF uses the exact rendered slide images from the editable PowerPoint build.
pdf=root/'submission/Muhammad_Suffyan_Khan_DATA608_Story3.pdf'
c=canvas.Canvas(str(pdf),pagesize=(960,540));c.setTitle('DATA608 Story 3 - Gun Laws and Firearm Mortality');c.setAuthor('Muhammad Suffyan Khan')
for f in sorted((root/'presentation/slide_pngs').glob('*.png')):
 c.drawImage(ImageReader(str(f)),0,0,width=960,height=540);c.showPage()
c.save()

# Portable, self-contained HTML preview of the full analysis and 50-state table.
def data_uri(p):return 'data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode()
s=pd.read_csv(root/'data/processed/five_level_summary.csv');d=pd.read_csv(root/'data/processed/state_analysis_2024.csv').sort_values('state')
body='''<h1>Do stricter gun laws reduce firearm deaths?</h1><p>Muhammad Suffyan Khan · DATA 608 · Fall 2026</p><p><strong>Finding:</strong> stronger 2024 law grades accompany lower age-adjusted firearm mortality in 2024. This observational state comparison cannot establish that laws caused the differences.</p><h2>Sources and five-level scale</h2><p>The CDC open API supplies 2024 Q4 annual age-adjusted firearm-related injury rates. GIFFORDS 2024 grades define the ordered classification: F = 1, D = 2, C = 3, B = 4, A = 5. Plus/minus grades remain in the source table. The outcome includes suicides, homicides and other intents. The source files, API request and successful response are archived in this package.</p>'''
body+='<h2>Why these visual choices</h2><p>State tile maps keep every state visible. Direct annotations identify extremes and exceptions. The category matrix uses within-group shares to make unequal groups comparable, with state counts retained in every cell. Outlines connect the key comparisons to their labels: 68% of the most lax group at rates of 16 or more and 54% of the strictest group below 8. The geographic and category views provide different ways to understand the same evidence.</p>'
for f in sorted((root/'figures').glob('*.png')):body+=f'<figure><img alt="{html.escape(f.stem)}" src="{data_uri(f)}"></figure>'
body+='<h2>Group summary</h2><p>These are unweighted summaries of state-level age-adjusted rates, not national rates.</p>'+s.to_html(index=False,float_format=lambda x:f'{x:.1f}')
body+='<p>Spearman correlation of law level and mortality is -0.717. New Mexico (B-, 26.6) is an important exception. The strictest group mean is 8.4 versus 18.6 in the most lax group. The B-group mean exceeds the C-group mean, so the gradient is not uniform.</p><h2>Interpretation and limits</h2><p>Policy timing, gun ownership, economic conditions, demographics, geography, enforcement and neighboring laws remain uncontrolled. The law grades reflect one advocacy organization’s index. Age adjustment improves comparability but does not account for every state difference. The CDC API dataset is designated provisional. Causal testing needs implementation dates, repeated years and suitable comparison groups.</p>'
body+='<h2>Complete state assignments and rates</h2>'+d[['state','abbr','gun_law_grade','law_level','firearm_death_rate_2024']].to_html(index=False)
body+='<h2>Sources</h2><p><a href="https://data.cdc.gov/resource/489q-934x.json">CDC NCHS API</a> · <a href="https://giffords.org/resources/scorecard2024/">GIFFORDS 2024 scorecard</a> · <a href="https://www.cdc.gov/nchs/state-stats/deaths/firearms.html">CDC firearm mortality definitions</a></p><h2>AI assistance</h2><p>ChatGPT was used to assist with data-cleaning review, analysis,visualization refinement, and editorial review. I reviewed and validated all code, calculations, visualizations, interpretations, and final conclusions.</p>'
(root/'submission/Story3_Analysis.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DATA608 Story 3</title><style>body{font:17px/1.55 Arial,sans-serif;color:#102238;max-width:1120px;margin:40px auto;padding:0 24px}h1{font-size:36px}img{max-width:100%;height:auto}table{border-collapse:collapse;width:100%;font-size:15px}td,th{border-bottom:1px solid #cbd5df;padding:9px;text-align:left}figure{margin:35px 0}a{color:#075c9c}</style>'+body+'</html>',encoding='utf-8')
for f in (root/'figures').glob('*.png'):
 (f.with_suffix('.html')).write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>'+html.escape(f.stem)+'</title><body><img alt="'+html.escape(f.stem)+'" style="max-width:100%;height:auto" src="'+data_uri(f)+'"></body></html>')
(root/'requirements.txt').write_text('pandas>=2.0\nscipy>=1.10\nlxml>=4.9\nnbformat>=5.0\n')
(root/'Story3.Rproj').write_text('Version: 1.0\nRestoreWorkspace: No\nSaveWorkspace: No\nAlwaysSaveHistory: No\nEnableCodeIndexing: Yes\nUseSpacesForTab: Yes\nNumSpacesForTab: 2\nEncoding: UTF-8\n')
print('Executed notebook, created 8-page PDF, self-contained HTML and R project.')
