import json
s=open('/mnt/project-files/hotel-english-app/site/data.js').read()
i=s.index('{');d,_=json.JSONDecoder().raw_decode(s[i:])
out=[]
for c,b in d['b'].items():
  if not c.startswith('8-'): continue
  dd=b.get('d',[])
  for j in range(len(dd)-1):
    if dd[j][0]=='I' and dd[j+1][0]=='C' and '?' in dd[j][1] or (dd[j][0]=='I' and dd[j+1][0]=='C' and dd[j][1].startswith(('Tell','Please','Describe'))):
      a=[];k=j+1
      while k<len(dd) and dd[k][0]=='C': a.append((dd[k][1],dd[k][2]));k+=1
      out.append((dd[j][1],dd[j][2],a))
  for w in b.get('w',[]):
    for p in w[4]:
      if '?' in p[0] or p[0].startswith('Tell'): out.append((p[0],p[1],[(p[2],p[3])]))
exec(open('mkcur.py').read())
L=['# 모의 면접 (RYU 2026-11-24): 기존 영어면접 질문을 분야별로 모아, 분야(라디오 버튼)를 고르고 한 문제씩 무작위로 냅니다. 음성은 기존 파일을 씁니다.',
   '# mk: [[분야, [[question, 질문 뜻, [[answer line, 뜻], ...], 질문 의도, 답변 방향], ...]], ...]  (generated from the interview bundles; keep the English identical so the clips match)']
mk=[[t,[[out[k][0],out[k][1],[list(x) for x in out[k][2]],v[0],v[1]] for k,v in qs.items()]] for (t,en,qs) in G]
L.append('MOCK = {"n": "모의 면접", "b": [{"t": "모의 면접", "en": "Mock Interview", "i": "분야를 고르고 [문제 내기]를 누르면 질문이 한 문제씩 무작위로 나옵니다. 먼저 영어로 답해 본 뒤 체크박스를 눌러 질문, 모범 답변, 질문 의도를 확인하세요.", "mk": '+repr(mk)+'}]}')
open('/mnt/project-files/hotel-english-app/src/content/m8d.py','w').write('\n'.join(L)+'\n')
print(sum(len(g[2]) for g in G))
