"""RSS metadata only; country mentions are retrieval hints, never conflict labels."""
import concurrent.futures,datetime,email.utils,hashlib,json,pathlib,re,urllib.parse,urllib.request,xml.etree.ElementTree as ET
ROOT=pathlib.Path(__file__).resolve().parents[1]
FEEDS=[('BBC News','https://feeds.bbci.co.uk/news/world/rss.xml'),('Noticias ONU','https://news.un.org/feed/subscribe/es/news/all/rss.xml')]
ALIASES={'USA':['united states','u.s.','us','estados unidos'],'CHN':['china','chinese'],'RUS':['russia','russian','rusia'],'IND':['india','indian'],'GBR':['united kingdom','britain','british','reino unido'],'FRA':['france','french','francia'],'DEU':['germany','german','alemania'],'JPN':['japan','japanese','japón'],'KOR':['south korea','corea del sur'],'PRK':['north korea','corea del norte'],'TWN':['taiwan','taiwán'],'PAK':['pakistan','pakistán'],'IRN':['iran','iranian','irán'],'ISR':['israel','israeli'],'SAU':['saudi arabia','saudi','arabia saudí','arabia saudita'],'TUR':['turkey','türkiye','turkish','turquía'],'UKR':['ukraine','ukrainian','ucrania'],'ESP':['spain','spanish','españa'],'MAR':['morocco','moroccan','marruecos'],'DZA':['algeria','algerian','argelia']}
def mentions(text):
 out=[]
 for code,terms in ALIASES.items():
  for term in terms:
   # 'us' is ambiguous in prose: only match capitalized US.
   if re.search(r'(?<!\w)'+re.escape('US' if term=='us' else term)+r'(?!\w)',text,0 if term=='us' else re.I):out.append(code);break
 return out

def parse_feed(raw,source,now):
 records=[]
 for item in ET.fromstring(raw).findall('.//item'):
  title=' '.join((item.findtext('title') or '').split());url=(item.findtext('link') or '').strip();date=item.findtext('pubDate')
  if urllib.parse.urlparse(url).scheme!='https' or not title or not date:continue
  try:dt=email.utils.parsedate_to_datetime(date).astimezone(datetime.timezone.utc)
  except (ValueError,TypeError,OverflowError):continue
  if dt>now+datetime.timedelta(minutes=10) or dt<now-datetime.timedelta(days=14):continue
  countries=mentions(title)
  if not countries:continue
  records.append({'id':hashlib.sha256(url.encode()).hexdigest()[:16],'title':title[:350],'url':url,'source':source,'publishedAt':dt.isoformat(),'eventDate':None,'countries':countries,'classification':'Mención automática en titular; no verificación del acontecimiento'})
 return records

def update():
 now=datetime.datetime.now(datetime.timezone.utc);target=ROOT/'dist/news.json';old={}
 if target.exists():old=json.loads(target.read_text())
 def fetch(feed):
  name,url=feed
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'CivitasResearchReader/0.4 (+https://github.com/devrafag/civitas-world-lab)'})
   with urllib.request.urlopen(req,timeout=25) as r:raw=r.read(2000000)
   rows=parse_feed(raw,name,now);return rows,{'name':name,'url':url,'ok':True,'checkedAt':now.isoformat(),'items':len(rows)}
  except Exception as e:return [],{'name':name,'url':url,'ok':False,'checkedAt':now.isoformat(),'error':type(e).__name__}
 rows=[];status=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
  for items,s in ex.map(fetch,FEEDS):rows.extend(items);status.append(s)
 # Keep previously obtained records when a feed fails; preserve original publication dates.
 for r in old.get('items',[]):
  try:
   date=datetime.datetime.fromisoformat(r['publishedAt'])
   if now-datetime.timedelta(days=14)<=date<=now:rows.append(r)
  except (ValueError,KeyError):pass
 unique={r['url']:r for r in rows};items=sorted(unique.values(),key=lambda r:r['publishedAt'],reverse=True)[:80]
 obj={'schemaVersion':1,'checkedAt':now.isoformat(),'lastSuccessfulFetch':now.isoformat() if any(s['ok'] for s in status) else old.get('lastSuccessfulFetch'),'sources':status,'items':items,'notice':'Titulares externos. La mención conjunta de países no implica confrontación. Sin corroboración automática.'}
 temp=target.with_suffix('.tmp');temp.write_text(json.dumps(obj,ensure_ascii=False,indent=2));temp.replace(target)
 print(json.dumps({'items':len(items),'sources':status},ensure_ascii=False))
 return any(s['ok'] for s in status)
if __name__=='__main__':
 import sys
 sys.exit(0 if update() else 1)
