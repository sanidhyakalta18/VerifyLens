"""Real OCR and labelled evaluation. No identity authenticity claims."""
import io,json,math,re,sqlite3,subprocess,time
from pathlib import Path
from PIL import Image,ImageOps
ROOT=Path(__file__).resolve().parent
DB=ROOT/'results.sqlite'
def connect():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row
 c.execute('CREATE TABLE IF NOT EXISTS runs(id INTEGER PRIMARY KEY, document TEXT, kind TEXT, condition TEXT, mode TEXT, latency_ms REAL, api_ok INTEGER, complete INTEGER, reason TEXT, matched INTEGER, total INTEGER, fields TEXT)'); return c

def extract(data,mode='raw'):
 if mode not in ('raw','threshold'): raise ValueError('Unknown preprocessing mode')
 image=Image.open(io.BytesIO(data)); image.load()
 if image.width*image.height>12000000: raise ValueError('Image too large')
 image=ImageOps.grayscale(image)
 if mode=='threshold': image=ImageOps.autocontrast(image).point(lambda p:255 if p>160 else 0)
 buf=io.BytesIO(); image.save(buf,format='PNG')
 result=subprocess.run(['tesseract','stdin','stdout','--psm','6'],input=buf.getvalue(),capture_output=True,timeout=20,check=True)
 text=result.stdout.decode(); fields={}
 for key in ('Name','Document ID','Date of Birth'):
  m=re.search(re.escape(key)+r'\s*:\s*([^\n]+)',text,re.I)
  fields[key]=m.group(1).strip() if m else ''
 return fields,text

def process(data,document,kind='uploaded',condition='unknown',mode='raw',expected=None):
 start=time.perf_counter(); fields={}; api_ok=1; reason='none'; text=''
 try: fields,text=extract(data,mode)
 except (OSError,ValueError,subprocess.SubprocessError): api_ok=0; reason='ocr_error'
 complete=int(api_ok and all(fields.get(k) for k in ('Name','Document ID','Date of Birth')))
 if api_ok and not complete: reason='missing_fields'
 if complete and not re.fullmatch(r'\d{4}-\d{2}-\d{2}',fields['Date of Birth']): complete=0; reason='invalid_date_format'
 matched=sum(fields.get(k,'').casefold()==v.casefold() for k,v in (expected or {}).items())
 total=len(expected or {})
 if expected and complete and matched<total: reason='ground_truth_mismatch'
 latency=(time.perf_counter()-start)*1000
 with connect() as c:
  c.execute('INSERT INTO runs VALUES(NULL,?,?,?,?,?,?,?,?,?,?,?)',(document,kind,condition,mode,latency,api_ok,complete,reason,matched,total,json.dumps(fields)))
 return dict(fields=fields,text=text,api_ok=bool(api_ok),complete=bool(complete),reason=reason,latency_ms=round(latency,2),matched=matched,total=total)

def analytics():
 with connect() as c:
  groups=[dict(r) for r in c.execute('SELECT mode,kind,condition,COUNT(*) AS requests,ROUND(100.0*SUM(api_ok)/COUNT(*),1) AS api_success_pct,ROUND(100.0*SUM(complete)/COUNT(*),1) AS field_completion_pct,ROUND(100.0*SUM(matched)/NULLIF(SUM(total),0),1) AS field_accuracy_pct,ROUND(AVG(latency_ms),1) AS avg_ms FROM runs GROUP BY mode,kind,condition')]
  failures=[dict(r) for r in c.execute("SELECT reason,COUNT(*) AS count FROM runs WHERE reason!='none' GROUP BY reason ORDER BY count DESC")]
  rows=[dict(r) for r in c.execute('SELECT * FROM runs ORDER BY id DESC LIMIT 100')]
  latency=[r[0] for r in c.execute('SELECT latency_ms FROM runs ORDER BY latency_ms')]
 return dict(groups=groups,failures=failures,recent=rows,requests=len(latency),p95_ms=round(latency[max(0,math.ceil(.95*len(latency))-1)],1) if latency else None)
