import urllib.request,json,concurrent.futures,pathlib,datetime
ROOT=pathlib.Path(__file__).resolve().parents[1];out=ROOT/'research';out.mkdir(exist_ok=True)
ids='USA;CHN;RUS;IND;GBR;FRA;DEU;JPN;KOR;PRK;PAK;IRN;ISR;SAU;TUR;UKR;ESP;MAR;DZA'
indicators={'population':'SP.POP.TOTL','gdp':'NY.GDP.MKTP.CD','income':'NY.GDP.PCAP.CD','growth':'NY.GDP.MKTP.KD.ZG','inflation':'FP.CPI.TOTL.ZG','unemployment':'SL.UEM.TOTL.ZS','military':'MS.MIL.XPND.CD','militaryShare':'MS.MIL.XPND.GD.ZS','personnel':'MS.MIL.TOTL.P1'}
def fetch(k,code):
 period='2020' if k=='personnel' else '2024:2025'
 url=f'https://api.worldbank.org/v2/country/all/indicator/{code}?format=json&date={period}&per_page=1000'
 try:
  obj=json.load(urllib.request.urlopen(url,timeout=30));assert isinstance(obj,list) and len(obj)>1 and isinstance(obj[1],list)
  (out/(k+'.json')).write_text(json.dumps({'url':url,'retrieved':datetime.date.today().isoformat(),'data':obj[1]},ensure_ascii=False));return k,len(obj[1])
 except Exception as e:return k,str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
 for r in ex.map(lambda p:fetch(*p),indicators.items()):print(*r,flush=True)
