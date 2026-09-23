"""Verify the actual risks of this multi-page static change."""
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
from urllib.parse import urlsplit
import json,re,subprocess,itertools,xml.etree.ElementTree as ET
from content import PAGES
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
BASE='https://asbestosremovalsinlondon.co.uk/';REV='66cc01d1ea8fc59a9506a130754c2a07ce373d6f'
manifest=json.loads((HERE/'manifest.json').read_text());assets=json.loads((HERE/'assets.json').read_text())
def parse(t):return BeautifulSoup(t,'html.parser')
def old(p):return parse(subprocess.check_output(['git','show',REV+':'+p],cwd=ROOT).decode())
def js(s):return [(x.get('src'),x.get_text()) for x in s.select('script:not([type="application/ld+json"])')]
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','i':'http://www.google.com/schemas/sitemap-image/1.1'}
xml=ET.parse(ROOT/'sitemap.xml');entries={x.find('s:loc',ns).text:x for x in xml.findall('s:url',ns)}
results=[];phrases={};warnings=[]
for m in manifest:
 s=parse((ROOT/m['path']).read_text());before=old(m['path']);url=m['url'];n=m['path'][17:-5]
 assert len(s.select('h1'))==1 and s.h1.get_text(' ',strip=True)==before.h1.get_text(' ',strip=True),m['path']
 assert s.select_one('link[rel=canonical]')['href']==before.select_one('link[rel=canonical]')['href']==url
 assert s.title.get_text()==before.title.get_text()
 assert [str(f) for f in s.select('form')]==[str(f) for f in before.select('form')]
 assert js(s)==js(before),('scripts',m['path'])
 assert str(s.header)==str(before.header) and str(s.footer)==str(before.footer)
 assert not any('noindex' in x.get('content','').lower() for x in s.select('meta[name=robots]'))
 ids=[x['id'] for x in s.select('[id]')];assert len(ids)==len(set(ids)),('ids',m['path'])
 assert len(s.select('.v3-panel'))==4 and len(s.select('main img'))==3
 assert len(s.select('.artex-faq details'))==6
 g=json.loads(s.select_one('#v3-connected-schema').string)['@graph'];byid={x['@id']:x for x in g}
 assert len(byid)==len(g)
 visible=[(x.summary.get_text(' ',strip=True),x.p.get_text(' ',strip=True)) for x in s.select('.artex-faq details')]
 schema=[(x['name'],x['acceptedAnswer']['text']) for x in byid[url+'#faq']['mainEntity']]
 assert visible==schema
 assert byid[url+'#webpage']['primaryImageOfPage']['@id']==url+'#primaryimage'
 assert byid[url+'#service']['image']['@id']==url+'#primaryimage'
 expected=BASE+m['primary'];assert byid[url+'#primaryimage']['contentUrl']==expected
 assert s.select_one('meta[property="og:image"]')['content']==s.select_one('meta[name="twitter:image"]')['content']==expected
 assert s.select_one('.legacy-hero img')['src']=='/'+m['primary']
 images=[x.text for x in entries[url].findall('i:image/i:loc',ns)];assert images==[BASE+a for a in m['assets']]
 for a in s.select('main a[href]'):
  href=a['href'];p=urlsplit(href)
  if href.startswith('/') and p.path!='/':assert (ROOT/p.path.lstrip('/')).is_file(),(m['path'],href)
  if href.startswith('#'):assert href[1:] in ids,(m['path'],href)
 for a in s.select('main img'):
  im=Image.open(ROOT/a['src'].lstrip('/'));assert (int(a['width']),int(a['height']))==im.size
 for x in s.select('main script,main #quote,main nav,main .v3-local-links'):x.decompose()
 text=s.main.get_text(' ',strip=True)
 assert not re.search(r'Search Console|local intent|buyer intent|ranking strongly|page to steal|signals|place-name stuffing|within an hour',text,re.I),m['path']
 words=re.findall(r'\b[\w’]+\b',text.lower());phrases[m['path']]=set(zip(*(words[i:] for i in range(5))))
 results.append({'page':m['path'],'editorial_words_including_captions':len(words),'faq_count':len(visible),'images':3,'protected_fields':'unchanged','forms_tracking':'unchanged','schema_sitemap_links':'pass'})
for a in assets:
 image=Image.open(ROOT/a['dest']);assert image.tobytes()==Image.open(ROOT/a['source']).tobytes()
 gps=image.getexif().get_ifd(34853)
 def degrees(k):return sum(float(x)/d for x,d in zip(gps[k],[1,60,3600]))
 assert abs(degrees(2)-a['lat'])<1e-6
 assert abs(degrees(4)-abs(a['lon']))<1e-6
 assert gps[3]==('E' if a['lon']>=0 else 'W')
 assert image.getexif()[270]==a['caption']
overlap=sorted([{'a':a,'b':b,'overlap_percent':round(100*len(phrases[a]&phrases[b])/min(len(phrases[a]),len(phrases[b])),2)} for a,b in itertools.combinations(phrases,2)],key=lambda x:x['overlap_percent'],reverse=True)
assert overlap[0]['overlap_percent']<15
hub=parse((ROOT/'locations.html').read_text())
for n in ['south-london','west-london']:assert hub.select_one('a[href="/asbestos-removal-'+n+'.html"]')
changed=subprocess.check_output(['git','diff','--name-only'],cwd=ROOT).decode().splitlines()
allowed={m['path'] for m in manifest}|{'locations.html','sitemap.xml','project/LOCATION-IMAGE-MAP.csv','project/SITE-INVENTORY.csv','project/PROJECT-CHECKPOINT.md'}
assert not set(changed)-allowed,('unexpected changes',set(changed)-allowed)
report={'status':'static checks passed','pages':results,'max_pairwise_five_word_overlap':overlap[:10],'live_verification':'pending','mobile_visual_verification':'pending'}
(HERE/'qa.json').write_text(json.dumps(report,indent=2));print(json.dumps({'pages':len(results),'word_range':[min(r['editorial_words_including_captions'] for r in results),max(r['editorial_words_including_captions'] for r in results)],'max_overlap':overlap[0],'assets_verified':len(assets),'status':'PASS'}))
