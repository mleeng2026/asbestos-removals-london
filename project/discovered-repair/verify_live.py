"""Read-only live validation of the deployed batch. Never submits an enquiry."""
from pathlib import Path
from bs4 import BeautifulSoup
import json,hashlib,urllib.request,concurrent.futures,datetime
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
BASE='https://asbestosremovalsinlondon.co.uk/'
manifest=json.loads((HERE/'manifest.json').read_text())
paths=[m['path'] for m in manifest]+[a for m in manifest for a in m['assets']]+['assets/v3-local-pages-20260923.css','sitemap.xml','locations.html']
def check(p):
 try:
  r=urllib.request.urlopen(BASE+p,timeout=45);data=r.read();expected=(ROOT/p).read_bytes()
  result={'path':p,'status':r.status,'final_url':r.url,'bytes':len(data),'matches_reviewed_file':data==expected,'x_robots_tag':r.headers.get('X-Robots-Tag')}
  if p.endswith('.html'):
   s=BeautifulSoup(data,'html.parser');c=s.select_one('link[rel=canonical]');result['canonical']=c['href'] if c else None
   result['h1']=s.h1.get_text(' ',strip=True) if s.h1 else None
   result['panels']=len(s.select('.v3-panel'));result['faqs']=len(s.select('.artex-faq details'))
  return result
 except Exception as e:return {'path':p,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:results=list(ex.map(check,paths))
failed=[r for r in results if r.get('status')!=200 or not r.get('matches_reviewed_file') or r.get('final_url')!=BASE+r['path'] or 'noindex' in (r.get('x_robots_tag') or '').lower()]
report={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':results,'failed':failed,'status':'PASS' if not failed else 'FAIL'}
(HERE/'live-qa.json').write_text(json.dumps(report,indent=2));print(json.dumps({'checked':len(results),'status':report['status'],'failed':failed}))
