import json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
CUTOFF='2026-09-08'
SIPRI='https://www.sipri.org/sites/default/files/2026-04/2604_milex_2025.pdf'
NUCLEAR='https://www.sipri.org/media/press-release/2026/increasing-focus-nuclear-weapons-amid-heightened-escalation-risks-new-sipri-yearbook-out-now'
NATO='https://www.nato.int/en/about-us/organization/nato-member-countries'
rows=[
('USA','Estados Unidos','Global','Competencia entre potencias; compromisos de seguridad y comercio.','Costes de escalada, alianzas y canales diplomáticos.',['CHN','RUS','IRN']),
('CHN','China','Indopacífico','Estrecho de Taiwán; comercio y competencia tecnológica.','Interdependencia comercial y costes regionales de una crisis.',['USA','TWN','IND','JPN']),
('RUS','Rusia','Europa / Eurasia','Relación con Ucrania y seguridad europea.','Negociación, costes sostenidos y riesgo de escalada nuclear.',['UKR','USA','DEU']),
('IND','India','Asia meridional','Relaciones con Pakistán y China; comercio regional.','Canales de diálogo y costes de un enfrentamiento regional.',['PAK','CHN']),
('GBR','Reino Unido','Europa / Atlántico','Seguridad europea y compromisos colectivos.','Coordinación aliada y diplomacia.',['USA','FRA','RUS']),
('FRA','Francia','Europa / Mediterráneo','Seguridad europea y estabilidad mediterránea.','Instituciones multilaterales y cooperación regional.',['DEU','GBR','ESP']),
('DEU','Alemania','Europa','Seguridad europea; resiliencia industrial y comercial.','Coordinación aliada e interdependencia económica.',['RUS','FRA','USA']),
('JPN','Japón','Asia oriental','Seguridad marítima y estabilidad de cadenas productivas.','Acuerdos de seguridad y canales diplomáticos.',['CHN','USA','PRK']),
('KOR','Corea del Sur','Asia oriental','Estabilidad de la península coreana.','Disuasión y comunicación para evitar errores de cálculo.',['PRK','USA','JPN']),
('PRK','Corea del Norte','Asia oriental','Programa nuclear y relación intercoreana.','Costes de una escalada y contactos diplomáticos.',['KOR','USA']),
('TWN','Taiwán','Asia oriental','Estabilidad del estrecho y cadenas de semiconductores.','Costes comerciales y mecanismos de comunicación.',['CHN','USA','JPN']),
('PAK','Pakistán','Asia meridional','Relación con India y estabilidad regional.','Disuasión y vías de negociación.',['IND','CHN']),
('IRN','Irán','Oriente Medio','Seguridad regional, programa nuclear y navegación comercial.','Mediación y costes económicos de una crisis.',['USA','ISR','SAU']),
('ISR','Israel','Oriente Medio','Relación con Irán y seguridad regional.','Mediación y acuerdos diplomáticos.',['IRN','USA']),
('SAU','Arabia Saudí','Oriente Medio','Seguridad energética y estabilidad del Golfo.','Negociación y continuidad del comercio energético.',['IRN','USA']),
('TUR','Turquía','Europa / Oriente Medio','Mar Negro y estabilidad regional.','Cooperación aliada y negociación regional.',['RUS','UKR','USA']),
('UKR','Ucrania','Europa','Seguridad, reconstrucción y relación con Rusia.','Diplomacia y acuerdos verificables.',['RUS','USA','DEU']),
('ESP','España','Europa / Mediterráneo','Estrecho y cooperación con el norte de África.','Cooperación bilateral, comercio e instituciones europeas.',['MAR','DZA','FRA']),
('MAR','Marruecos','Magreb','Sáhara Occidental y relaciones con Argelia y España.','Diplomacia, cooperación comercial y mediación.',['DZA','ESP']),
('DZA','Argelia','Magreb','Relación con Marruecos y estabilidad mediterránea.','Mediación y cooperación energética.',['MAR','ESP'])]
spending={'USA':954,'CHN':336,'RUS':190,'DEU':114,'IND':92.1,'GBR':89,'UKR':84.1,'SAU':83.2,'FRA':68,'JPN':62.2,'ISR':48.3,'KOR':47.8,'ESP':40.2,'TUR':30,'DZA':25.4,'TWN':18.2,'PAK':11.9,'IRN':7.4,'MAR':6.3}
shares={'USA':3.1,'CHN':1.7,'RUS':7.5,'DEU':2.3,'IND':2.3,'GBR':2.4,'UKR':40,'SAU':6.5,'FRA':2,'JPN':1.4,'ISR':7.8,'KOR':2.6,'ESP':2.1,'TUR':1.9,'DZA':8.8,'TWN':2.1,'PAK':2.9,'IRN':2.1}
nuclear=set('USA RUS GBR FRA CHN IND PAK PRK ISR'.split());allies=set('USA GBR FRA DEU TUR ESP'.split())
indicators={'population':('Población','SP.POP.TOTL','personas'),'gdp':('PIB nominal','NY.GDP.MKTP.CD','USD'),'income':('PIB por habitante','NY.GDP.PCAP.CD','USD/persona'),'growth':('Crecimiento real del PIB','NY.GDP.MKTP.KD.ZG','% anual'),'inflation':('Inflación IPC','FP.CPI.TOTL.ZG','% anual'),'unemployment':('Desempleo estimado OIT','SL.UEM.TOTL.ZS','%'),'personnel':('Personal de fuerzas armadas · histórico','MS.MIL.TOTL.P1','personas')}
def datum(value,period,source,url,note=''):
 return {'value':value,'period':str(period),'source':source,'url':url,'retrieved':CUTOFF,'note':note}
profiles=[]
for id,name,region,focus,brake,watch in rows:
 metrics={}
 for key,(label,code,unit) in indicators.items():
  path=ROOT/'research'/(key+'.json');valid=[]
  if path.exists():
   valid=[r for r in json.loads(path.read_text())['data'] if r.get('countryiso3code')==id and r.get('value') is not None and int(r['date'])<=2025]
  latest=max(valid,key=lambda r:int(r['date'])) if valid else None
  d=datum(latest['value'] if latest else None,latest['date'] if latest else '—','Banco Mundial',f'https://data.worldbank.org/indicator/{code}?locations={id}', 'No disponible en el corte consultado' if not latest else ('Referencia de 2020; no representa efectivos actuales.' if key=='personnel' else 'Último valor no nulo recuperado del intervalo 2024–2025.'))
  metrics[key]={'label':label,'unit':unit,**d}
 for k,v,label,unit in [('military',spending.get(id),'Gasto militar','miles de millones USD'),('militaryShare',shares.get(id),'Gasto militar / PIB','%')]:
  metrics[k]={'label':label,'unit':unit,**datum(v,'2025' if v is not None else '—','SIPRI',SIPRI,'Estimación SIPRI.' if id in ['CHN','RUS','UKR','SAU'] and v is not None else 'No disponible en la fuente consultada.' if v is None else 'Gasto anual; no equivale a capacidad operativa.')}
 if id=='TWN':
  metrics['growth']={'label':'Crecimiento real del PIB · interanual trimestral','unit':'%','value':12.93,'period':'2026 T2','source':'DGBAS','url':'https://eng.stat.gov.tw/News_Content.aspx?n=2317&s=236587','retrieved':CUTOFF,'note':'Estimación preliminar, publicada 14/08/2026. No comparable directamente con crecimiento anual.'}
  metrics['unemployment']={'label':'Desempleo sin ajuste estacional','unit':'%','value':3.39,'period':'2026-07','source':'DGBAS','url':'https://eng.stat.gov.tw/News_Content.aspx?n=2317&s=236627','retrieved':CUTOFF,'note':'Publicado 24/08/2026; dato mensual.'}
 links=[{'text':'Miembro de la OTAN' if id in allies else 'No figura entre los miembros de la OTAN','url':NATO}]
 if id=='JPN':links.append({'text':'Tratado de seguridad con Estados Unidos','url':'https://www.mofa.go.jp/region/n-america/us/q%26a/ref/1.html'})
 if id=='KOR':links.append({'text':'Tratado de defensa mutua con Estados Unidos','url':'https://www.mofa.go.kr/eng/wpge/m_4904/contents.do'})
 profiles.append({'id':id,'name':name,'region':region,'metrics':metrics,'nuclear':{'text':'Estado con armamento nuclear según SIPRI' if id in nuclear else 'No incluido por SIPRI entre los nueve estados con armamento nuclear','url':NUCLEAR,'period':'enero de 2026'},'alliances':links,'assessment':{'type':'Valoración cualitativa del proyecto; no predicción','focus':focus,'restraints':brake,'watch':watch},'limitations':['Las relaciones a observar incluyen cooperación y tensión: no son una lista de enemigos.','Sin evaluación de probabilidad de guerra ni inventario operativo validado.']+(['Cobertura económica parcial: Taiwán se trata como entidad de análisis diferenciada.'] if id=='TWN' else [])})
result={'version':'0.3','cutoff':CUTOFF,'automaticUpdates':False,'profiles':profiles,'methodology':'Datos publicados separados del simulador. No se recalibra el motor de aprendizaje con estas fichas. Relaciones a observar elegidas por criterio analítico, sin puntuaciones de riesgo. Las cifras ausentes permanecen nulas; no se imputan.'}
(ROOT/'dist'/'profiles.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print('20 profiles; populated values',sum(m['value'] is not None for p in profiles for m in p['metrics'].values()))
