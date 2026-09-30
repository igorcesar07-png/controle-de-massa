"""Gera geo.json (base compacta para o Controle de geometria) a partir de:
 - data-src/B2B3_KMZ_Estaca.kmz  (estaca, coordenadas, hodômetro contínuo)
 - data-src/R08_unifilar_solucoes_BR277.json (códigos de solução por sentido/faixa)
Nenhum campo é inventado: só copia o que existe nos arquivos. Uso: python3 tools/build_geo.py"""
import json, re, zipfile, sys, os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
kml=zipfile.ZipFile(os.path.join(ROOT,'data-src/B2B3_KMZ_Estaca.kmz')).read('doc.kml').decode('utf8')
pms=re.findall(r'<Placemark>(.*?)</Placemark>',kml,re.S)
K=[]
for p in pms:
    name=re.search(r'<name>(.*?)</name>',p).group(1).strip()
    lon,lat=re.search(r'<coordinates>\s*([-\d.]+),([-\d.]+)',p).groups()
    hod=float(re.search(r'Hodômetro Contínuo">\s*<value>([\d.]+)',p).group(1))
    bl=re.search(r'Bloco">\s*<value>([\d.]+)',p)
    K.append(dict(name=name,lat=float(lat),lon=float(lon),hod=hod,bloco=int(float(bl.group(1))) if bl else None))
U=json.load(open(os.path.join(ROOT,'data-src/R08_unifilar_solucoes_BR277.json'),encoding='utf8'))
E=U['estacas']
assert len(E)==len(K), 'KMZ e unifilar com quantidades diferentes'
for a,b in zip(K,E):
    assert a['name']==b['estaca'] and abs(a['lat']-b['latitude'])<1e-6 and abs(a['lon']-b['longitude'])<1e-6, ('divergência',a['name'],b['estaca'])
H=[k['hod'] for k in K]
steps={round(b-a,3) for a,b in zip(H,H[1:])}
assert steps=={20.0}, ('hodômetro não contínuo',steps)
COLS=[('c1','crescente','faixa_1_crescente'),('c2','crescente','faixa_2_adicional_crescente'),('ca','crescente','acostamento_crescente'),
      ('d1','decrescente','faixa_1_decrescente'),('d2','decrescente','faixa_2_adicional_decrescente'),('da','decrescente','acostamento_decrescente')]
codes=sorted({e['pavimento'][s][c] for e in E for _,s,c in COLS if e['pavimento'][s][c] is not None})
idx={c:i for i,c in enumerate(codes)}
sol={k:[idx[e['pavimento'][s][c]] if e['pavimento'][s][c] is not None else -1 for e in E] for k,s,c in COLS}
out={'v':1,'fonte':{'kmz':'B2B3_KMZ_Estaca.kmz','unifilar':U['fonte'].get('arquivo'),'obs_unifilar':U['fonte'].get('observacao')},
     'h0':H[0],'passo':20,'n':len(K),'nome':[k['name'] for k in K],'lat':[round(k['lat'],6) for k in K],'lon':[round(k['lon'],6) for k in K],
     'bloco':[k['bloco'] for k in K],'codigos':codes,'sol':sol}
json.dump(out,open(os.path.join(ROOT,'geo.json'),'w'),separators=(',',':'),ensure_ascii=False)
print('geo.json:',len(K),'estacas;',len(codes),'códigos:',codes,'; tamanho',os.path.getsize(os.path.join(ROOT,'geo.json'))//1024,'KB')
