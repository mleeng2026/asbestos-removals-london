"""Rebuild the approved 22-page batch from its protected baseline.

Run with the repository's Python environment (BeautifulSoup and Pillow).
Photographs are metadata-remuxed without modifying their decoded pixels.
"""
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
from PIL.TiffImagePlugin import IFDRational
import json,re,csv,struct,html,subprocess,hashlib
from content import PAGES

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
BASE='https://asbestosremovalsinlondon.co.uk/'
BASELINE='66cc01d1ea8fc59a9506a130754c2a07ce373d6f'
G=json.loads((HERE/'geo-primary.json').read_text())
SG=json.loads((HERE/'geo-secondary.json').read_text())
ALIASES={'hackney-central':'hackney','ealing-london':'ealing','kensington-and-chelsea-london':'kensington','west-london':'west-kensington','south-london':'elephant-and-castle'}
NAMES={n:n.replace('-',' ').title() for n in PAGES}
NAMES.update({'barnet-london':'Barnet','croydon-london':'Croydon borough','ealing-london':'Ealing borough','kensington-and-chelsea-london':'Kensington and Chelsea','south-london':'South London','west-london':'West London'})
BOROUGHS={'angel':'Islington','chessington':'Kingston upon Thames','crouch-end':'Haringey','croydon':'Croydon','hackney-central':'Hackney','leytonstone':'Waltham Forest','muswell-hill':'Haringey','north-kensington':'Kensington and Chelsea','pinner':'Harrow','rainham':'Havering','shoreditch':'Hackney','south-norwood':'Croydon','thornton-heath':'Croydon','tottenham':'Haringey','twickenham':'Richmond upon Thames','wood-green':'Haringey'}
SERVICES={'asbestos Artex removal':'asbestos-artex-removal-london.html','asbestos textured coating removal':'asbestos-artex-removal-london.html','asbestos floor tile removal':'asbestos-floor-removal-london.html','asbestos bitumen adhesive removal':'asbestos-floor-removal-london.html','asbestos AIB removal':'asbestos-aib-removal-london.html','asbestos pipe lagging removal':'asbestos-pipe-removal-london.html','asbestos garage roof removal':'asbestos-garage-roof-removal-in-london.html','asbestos roof removal':'asbestos-roof-removal-london.html','licensed asbestos removal':'licensed-asbestos-removal-london.html'}
# Previously inspected approved photographs: service, actual visible subject, quote prompt.
PHOTOS={
 'floor':('asbestos-floor-tile-removal-richmond.webp','asbestos-floor-tile-removal','Asbestos floor tile removal','exposed dark floor finish beside a skirting board','Identify the confirmed floor layers and the surface your installer needs next.'),
 'ceiling':('asbestos-artex-textured-ceiling-london.webp','asbestos-artex-removal','Asbestos Artex removal','patterned textured ceiling with cornice detailing','Keep the sample location with the result and explain the proposed ceiling changes.'),
 'detail':('asbestos-artex-textured-coating-close-up-london.webp','asbestos-textured-coating-removal','Asbestos textured coating removal','decorative textured ceiling around a light fitting','Include the affected ceiling or wall areas in the refurbishment scope.'),
 'stairs':('asbestos-worker-textured-coating-stairwell-london.webp','asbestos-textured-coating-removal','Asbestos textured coating removal','stairwell ceiling with opened sections','Describe the stairwell height and how occupants reach the other rooms.'),
 'aib':('asbestos-aib-fireplace-removal-london.webp','asbestos-aib-removal','Asbestos AIB removal','opened fireplace and surrounding exposed surfaces','Send the report entry and planned fireplace or surrounding building alteration.'),
 'garage':('asbestos-garage-roof-london.webp','asbestos-garage-roof-removal','Asbestos garage roof removal','garage with corrugated roof sheets and wall cladding','Specify whether the roof alone or the complete garage is being removed.'),
 'roof':('commercial-asbestos-roof-removal-london.webp','asbestos-roof-removal','Asbestos roof removal','large pitched corrugated roof above a brick building','Include roof access, building use and the replacement contractor’s programme.'),
 'flue':('asbestos-cement-flue-pipe-london.webp','asbestos-cement-flue-removal','Asbestos cement flue removal','vertical flue pipe inside a cupboard','Describe connected services and who coordinates any necessary isolation.'),
 'garden':('asbestos-garden-building-roof-london.webp','asbestos-roof-removal','Asbestos roof removal','roof of a garden building','Explain the access route and which parts of the building will remain.'),
 'enclosure':('asbestos-removal-london-enclosure-hero.webp','asbestos-removal','Asbestos removal','screened enclosure with taped doors and an asbestos warning sign','Discuss the work boundary, building access and completion requirements.'),
 'refurb':('asbestos-removal-refurbishment-work-london.webp','asbestos-removal','Asbestos removal','room undergoing refurbishment with exposed ceiling structure','Match the survey findings to the areas your contractor intends to alter.'),
 'wall':('asbestos-textured-wall-removal-london.webp','asbestos-textured-coating-removal','Asbestos textured coating removal','wall with partly removed surface finishes','Identify the tested finish and the condition required by the next trade.'),
}
CHOICES={
 'angel':['ceiling','aib','stairs'],'chessington':['garage','floor','roof'],'crouch-end':['stairs','detail','aib'],
 'croydon':['floor','ceiling','enclosure'],'hackney-central':['aib','floor','refurb'],'leytonstone':['floor','garage','wall'],
 'muswell-hill':['detail','stairs','flue'],'north-kensington':['enclosure','aib','floor'],'pinner':['garage','aib','ceiling'],
 'rainham':['roof','garage','flue'],'shoreditch':['refurb','floor','aib'],'south-norwood':['ceiling','wall','garden'],
 'thornton-heath':['floor','detail','garage'],'tottenham':['aib','roof','floor'],'wood-green':['floor','wall','enclosure'],
 'ealing-london':['roof','garage','refurb'],'kensington-and-chelsea-london':['enclosure','aib','detail'],
 'west-london':['roof','enclosure','flue'],'south-london':['enclosure','roof','floor'],
 'barnet-london':['floor','garage','ceiling'],'croydon-london':['garage','roof','aib'],'twickenham':['garage','floor','aib']}

def original(path):return subprocess.check_output(['git','show',BASELINE+':'+path],cwd=ROOT).decode()
def soup(text):return BeautifulSoup(text,'html.parser')
def esc(text):return html.escape(str(text),quote=True)
def slug(text):return re.sub('[^a-z0-9]+','-',text.lower()).strip('-')
def coord(v):
 v=abs(v);d=int(v);m=int((v-d)*60);sec=((v-d)*60-m)*60
 return IFDRational(d),IFDRational(m),IFDRational(round(sec*1000000),1000000)
def chunk(k,d):return k+struct.pack('<I',len(d))+d+(b'\0' if len(d)%2 else b'')
def remux(src,dest,a):
 data=src.read_bytes();im=Image.open(src);w,h=im.size;ex=Image.Exif()
 ex[270]=a['caption'];ex[315]='Asbestos Removals London';ex[40091]=a['title'].encode('utf-16le')+b'\0\0'
 ex[40094]=(a['service']+';'+a['place']+';'+a['postcode']).encode('utf-16le')+b'\0\0'
 ex[34853]={1:'N',2:coord(a['lat']),3:'E' if a['lon']>=0 else 'W',4:coord(a['lon']),18:'WGS-84'}
 parts=[];pos=12;vp=None
 while pos<len(data):
  k=data[pos:pos+4];n=struct.unpack('<I',data[pos+4:pos+8])[0];b=data[pos+8:pos+8+n];pos+=8+n+n%2
  if k==b'VP8X':vp=bytearray(b)
  elif k not in [b'EXIF',b'XMP ']:parts.append(chunk(k,b))
 if vp is None:vp=bytearray(bytes([0,0,0,0])+(w-1).to_bytes(3,'little')+(h-1).to_bytes(3,'little'))
 vp[0]|=8;vp[0]&=~4
 body=b'WEBP'+chunk(b'VP8X',bytes(vp))+b''.join(parts)+chunk(b'EXIF',ex.tobytes())
 dest.parent.mkdir(exist_ok=True);dest.write_bytes(b'RIFF'+struct.pack('<I',len(body))+body)
 check=Image.open(dest);assert im.tobytes()==check.tobytes();assert check.getexif().get_ifd(34853)[1]=='N'
 return w,h

def places(n):
 key=ALIASES.get(n,n)
 if n=='barnet-london':p={'place':'High Barnet','postcode':'EN5','lat':51.65338,'lon':-.20731,'url':'https://www.ukcitymap.com/chipping-barnet-high-barnet-greater-london-england-satellite-view.html'}
 elif n=='croydon-london':p={'place':'East Croydon','postcode':'CR0','lat':51.375452,'lon':-.09278,'url':'https://www.ukcitymap.com/east-croydon-railway-station.html'}
 else:
  g=G[key];p={'place':key.replace('-',' ').title(),'postcode':g['pc'].split()[0],'lat':float(g['lat']),'lon':float(g['lon']),'url':g['url']}
  if n=='hackney-central':p['place']='Hackney Central'
  if n=='twickenham':p['place']='Twickenham town centre'
  if n=='kensington-and-chelsea-london':p['place']='Kensington borough centre'
  if n=='ealing-london':p['place']='Ealing borough centre'
  if n in ['angel','chessington','crouch-end','croydon','leytonstone','muswell-hill','north-kensington','pinner','rainham','shoreditch','south-norwood','thornton-heath','tottenham','wood-green']:p['place']+=' centre'
 return [p]+SG[key if n not in ['barnet-london','croydon-london'] else n]

CSS='''
.v3-local-gallery,.v3-local-content,.v3-local-links{padding:40px 0;background:#faf8f2;color:#102d33}
.v3-local-gallery .frame,.v3-local-content .frame,.v3-local-links .frame{max-width:1180px}
.v3-local-gallery h2,.v3-local-content h2,.v3-local-links h2{font-size:30px!important;line-height:1.2!important;letter-spacing:0!important;margin:0 0 18px!important}
.v3-photo-grid{display:grid;grid-template-columns:1fr 1fr;gap:24px}
.v3-photo-grid figure{margin:0;background:white;border:1px solid #d7dedb;border-top:5px solid #eabb18}
.v3-photo-grid img{display:block;width:100%;height:260px;object-fit:cover}
.v3-photo-grid figcaption{padding:18px;font-size:16px;line-height:1.55;color:#142e34}
.v3-photo-grid strong,.v3-photo-grid span{display:block}.v3-photo-grid span{margin-top:8px}
.v3-local-content{padding-top:12px}.v3-panel{border:1px solid #bcc9c6;background:#fff;margin:0 0 14px}
.v3-panel>summary{display:flex;align-items:center;gap:16px;padding:23px;cursor:pointer;list-style:none;color:#092f38;background:#fff;min-height:64px}
.v3-panel>summary::-webkit-details-marker{display:none}.v3-panel>summary:after{content:'+';font-size:32px;line-height:1;margin-left:auto;color:#092f38}
.v3-panel[open]>summary:after{content:'−'}.v3-panel>summary h2{font-size:25px!important;margin:0!important;text-transform:none!important}
.v3-panel>summary:focus-visible{outline:3px solid #a87500;outline-offset:-4px}.v3-panel-body{padding:0 24px 24px;max-width:90ch}
.v3-panel-body p{font-size:18px;line-height:1.75;margin:0 0 18px}.v3-panel-body a{color:#07536a;text-decoration:underline;text-underline-offset:3px}
.v3-local-links .borough-links{display:flex;flex-wrap:wrap;gap:12px}.v3-local-links .borough-links a{background:#fff;color:#092f38!important;border:1px solid #adbdba;padding:14px 18px;min-height:48px;text-decoration:underline;font-size:17px;font-weight:600}
.v3-quote-prompt{margin:24px 0 0;font-size:18px;line-height:1.6}.v3-quote-prompt a{color:#07536a;text-decoration:underline}
.v3-local-page .legacy-hero-inner{text-align:center}.v3-local-page .legacy-hero-inner>p,.v3-local-page .legacy-hero h1{margin-left:auto;margin-right:auto}
.v3-local-page .service-label,.v3-local-page .hero-actions{justify-content:center}.v3-local-page .legacy-hero-inner>p:not(.service-label){max-width:800px}
.v3-local-page .artex-faq-list summary{min-height:48px}
@media(max-width:700px){.v3-local-gallery,.v3-local-content,.v3-local-links{padding:26px 0}.v3-photo-grid{grid-template-columns:1fr;gap:20px}.v3-photo-grid img{height:230px}.v3-local-gallery h2,.v3-local-links h2{font-size:27px!important}.v3-panel>summary{padding:18px;gap:12px}.v3-panel>summary h2{font-size:22px!important}.v3-panel-body{padding:0 18px 20px}.v3-panel-body p{font-size:17px}.v3-local-links .borough-links a{flex:1 1 140px}.v3-local-page .legacy-hero-inner>p:not(.service-label){font-size:18px;line-height:1.6}}
'''
(ROOT/'assets/v3-local-pages-20260923.css').write_text(CSS)
allassets=[];manifest=[]
for n,data in PAGES.items():
 filename='asbestos-removal-'+n+'.html';url=BASE+filename;s=soup(original(filename));main=s.main;name=NAMES[n]
 main['class']=list(main.get('class',[]))+['v3-local-page']
 preserved_links={a['href']:a.get_text(' ',strip=True) for a in main.select('a[href]') if a['href'].startswith('/asbestos-removal-') and a['href']!='/asbestos-removal-services.html'}
 if n in BOROUGHS:
  borough=BOROUGHS[n];bn=slug(borough);preserved_links['/asbestos-removal-'+bn+'-london.html']=borough+' borough'
 if n=='west-london':
  for b in ['Ealing','Hammersmith and Fulham','Hounslow','Hillingdon','Kensington and Chelsea']:preserved_links['/asbestos-removal-'+slug(b)+'-london.html']=b
 if n=='twickenham':preserved_links['/asbestos-artex-removal-twickenham.html']='Asbestos Artex removal Twickenham'
 if n=='ealing-london':
  for b in ['Ealing','Acton','Southall','Greenford','Hanwell']:preserved_links['/asbestos-removal-'+slug(b)+'.html']=b
 if n=='kensington-and-chelsea-london':
  for b in ['Kensington','Chelsea','North Kensington']:preserved_links['/asbestos-removal-'+slug(b)+'.html']=b
 if n=='south-london':
  for b in ['Merton','Lewisham','Greenwich']:preserved_links['/asbestos-removal-'+slug(b)+'-london.html']=b
 if n=='ealing-london':preserved_links['/asbestos-removal-west-london.html']='West London'
 if n=='croydon-london':preserved_links['/asbestos-removal-south-london.html']='South London'
 preserved_links.pop('/'+filename,None)
 preserved_links={h:t for h,t in preserved_links.items() if (ROOT/h.lstrip('/')).is_file()}
 preserved_links['/locations.html']='All London areas';preserved_links['/']='Asbestos Removal London'
 hero=main.select_one('.legacy-hero');hero.select_one('.legacy-hero-inner>p:not(.service-label)').string=data['intro']
 cta=hero.select_one('a[href="#quote"]')
 if cta:cta.string='Free quote ↓'
 quote=main.select_one('#quote')
 qtext=quote.select_one('.phone-first p:last-child')
 if qtext:qtext.string='Call with the postcode and what needs removing. A real person answers the phone. We normally reply within 30 minutes or less.'
 for x in list(main.find_all('section',recursive=False)):
  if x not in [hero,quote]:x.decompose()
 assets=[]
 for i,(point,key) in enumerate(zip(places(n),CHOICES[n])):
  source,service_slug,service,subject,prompt=PHOTOS[key]
  dest='media/'+service_slug+'-'+n+'-'+slug(point['place'])+'-'+slug(point['postcode'])+'.webp'
  title=(('Asbestos Removal '+name+' - '+service.lower()) if i==0 else service+' '+name)+' - '+point['place']+' '+point['postcode']
  a=dict(page=filename,source=source,dest=dest,place=point['place'],postcode=point['postcode'],lat=point['lat'],lon=point['lon'],service=service+' '+name,subject=subject,primary=i==0,source_url=point['url'],title=title,alt=title+'; '+subject,caption=title+'. '+subject[0].upper()+subject[1:]+'.')
  a['width'],a['height']=remux(ROOT/source,ROOT/dest,a);assets.append(a)
 primary=assets[0];im=hero.select_one('img');im.attrs.update(src='/'+primary['dest'],alt=primary['alt'],title=primary['title'],width=str(primary['width']),height=str(primary['height']),fetchpriority='high',loading='eager',decoding='async');im.attrs.pop('srcset',None)
 gallery='<section class="v3-local-gallery"><div class="frame"><h2>Plan the next stage of your '+esc(name)+' project</h2><div class="v3-photo-grid">'
 for a,key in zip(assets[1:],CHOICES[n][1:]):
  gallery+=f'<figure><img src="/{a["dest"]}" alt="{esc(a["alt"])}" title="{esc(a["title"])}" width="{a["width"]}" height="{a["height"]}" loading="lazy" decoding="async"><figcaption><strong>{esc(a["caption"])}</strong><span>{esc(PHOTOS[key][4])}</span></figcaption></figure>'
 gallery+='</div></div></section>';hero.insert_after(soup(gallery).section)
 used=set()
 def paragraph(text):
  out=esc(text)
  # One contextual link per service phrase per page, without nesting links.
  for phrase,path in SERVICES.items():
   if path not in used and phrase in text:
    out=out.replace(esc(phrase),f'<a href="/{path}">{esc(phrase)}</a>',1);used.add(path)
  return '<p>'+out+'</p>'
 sections='<section class="v3-local-content"><div class="frame">'
 for i,(heading,body) in enumerate(data['sections']):
  sections+=f'<details class="v3-panel" id="project-detail-{i+1}"><summary><h2>{esc(heading)}</h2></summary><div class="v3-panel-body">'+''.join(paragraph(p) for p in body.split('\n\n'))+'</div></details>'
 sections+='<p class="v3-quote-prompt">Tell us what is holding up the work. <a href="#quote">Request your free quote</a> or call <a href="tel:+442080880271">020 8088 0271</a>.</p></div></section>'
 main.select_one('.v3-local-gallery').insert_after(soup(sections).section)
 # Native details retain all copy in HTML and work without JavaScript.
 faq='<section class="artex-faq"><div class="frame"><p class="section-label">YOUR QUESTIONS</p><h2>Asbestos removal in '+esc(name)+': practical questions</h2><div class="artex-faq-list">'
 for q,a in data['faqs']:faq+='<details><summary>'+esc(q)+'</summary><p>'+esc(a)+'</p></details>'
 faq+='</div></div></section>';quote.insert_after(soup(faq).section)
 links='<section class="v3-local-links"><div class="frame"><h2>Local coverage and related services</h2><div class="borough-links">'+''.join(f'<a href="{h}">{esc(t)}</a>' for h,t in preserved_links.items())+'</div></div></section>'
 main.append(soup(links).section)
 description=data['intro'].split('?')[0]+'?' if '?' in data['intro'] else data['intro'].split('. ')[0]+'.'
 if len(description)>170:description='Asbestos removal in '+name+'. Get a free quote for your home, garage or commercial refurbishment. Call with the finding and planned work.'
 for selector,attr,value in [('meta[name="description"]','content',description),('meta[property="og:description"]','content',description),('meta[name="twitter:description"]','content',description),('meta[property="og:image"]','content',BASE+primary['dest']),('meta[name="twitter:image"]','content',BASE+primary['dest']),('meta[property="og:image:alt"]','content',primary['alt']),('meta[name="twitter:image:alt"]','content',primary['alt'])]:
  el=s.select_one(selector)
  if not el:
   field='property' if '[property' in selector else 'name';valuekey=selector.split('="')[1].split('"')[0];el=s.new_tag('meta',attrs={field:valuekey});s.head.append(el)
  el[attr]=value
 for typ in ['width','height']:
  el=s.select_one('meta[property="og:image:'+typ+'"]')
  if el:el['content']=str(primary[typ])
 for x in s.select('link[rel=preload][as=image]'):x.decompose()
 s.head.append(soup('<link rel="preload" as="image" href="/'+primary['dest']+'">').link)
 s.head.append(soup('<link rel="stylesheet" href="/assets/v3-local-pages-20260923.css">').link)
 graph=[]
 for sc in s.select('script[type="application/ld+json"]'):
  obj=json.loads(sc.string);graph.extend(obj.get('@graph',[obj]));sc.decompose()
 breadcrumb=next((g for g in graph if g.get('@type')=='BreadcrumbList'),None)
 if breadcrumb:breadcrumb['@id']=url+'#breadcrumb'
 else:breadcrumb={'@type':'BreadcrumbList','@id':url+'#breadcrumb','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':BASE},{'@type':'ListItem','position':2,'name':'Areas we cover','item':BASE+'locations.html'},{'@type':'ListItem','position':3,'name':name,'item':url}]}
 graph=[{'@type':'WebPage','@id':url+'#webpage','url':url,'name':s.title.get_text(' ',strip=True),'description':description,'isPartOf':{'@id':BASE+'#website'},'about':{'@id':url+'#service'},'breadcrumb':{'@id':url+'#breadcrumb'},'primaryImageOfPage':{'@id':url+'#primaryimage'},'hasPart':[{'@id':url+'#faq'}],'inLanguage':'en-GB'},
 {'@type':'Service','@id':url+'#service','name':'Asbestos removal '+name,'serviceType':'Asbestos removal','url':url,'provider':{'@id':BASE+'#organization'},'isRelatedTo':{'@id':BASE+'#service'},'areaServed':{'@id':url+'#area'},'image':{'@id':url+'#primaryimage'},'mainEntityOfPage':{'@id':url+'#webpage'}},breadcrumb,
 {'@type':'AdministrativeArea' if n.endswith('-london') and n not in ['south-london','west-london'] else 'Place','@id':url+'#area','name':name,'containedInPlace':{'@type':'Place','name':'Greater London'}},
 {'@type':'FAQPage','@id':url+'#faq','isPartOf':{'@id':url+'#webpage'},'mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in data['faqs']]}]
 for i,a in enumerate(assets):
  ident=url+('#primaryimage' if i==0 else '#image-'+str(i));placeid=ident+'-place'
  graph.append({'@type':'Place','@id':placeid,'name':a['place']+', '+name,'address':{'@type':'PostalAddress','addressLocality':name,'addressRegion':'Greater London','postalCode':a['postcode'],'addressCountry':'GB'},'geo':{'@type':'GeoCoordinates','latitude':a['lat'],'longitude':a['lon']}})
  graph.append({'@type':'ImageObject','@id':ident,'url':BASE+a['dest'],'contentUrl':BASE+a['dest'],'name':a['title'],'caption':a['caption'],'description':a['alt'],'width':a['width'],'height':a['height'],'encodingFormat':'image/webp','contentLocation':{'@id':placeid},'isPartOf':{'@id':url+'#webpage'},'representativeOfPage':i==0})
 sc=s.new_tag('script',type='application/ld+json',id='v3-connected-schema');sc.string=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False,separators=(',',':'));s.head.append(sc)
 (ROOT/filename).write_text(str(s));allassets.extend(assets)
 manifest.append({'path':filename,'url':url,'h1':s.h1.get_text(' ',strip=True),'canonical':s.select_one('link[rel=canonical]')['href'],'primary':primary['dest'],'assets':[a['dest'] for a in assets]})

# Give the two previously orphaned regional pages a direct hub entry.
loc=soup(original('locations.html'));section=loc.select_one('main .legacy-simple')
region=soup('<section class="regional-coverage"><h2>Projects across more than one borough</h2><p>Use our regional coverage for a project spanning several local areas, or choose a borough below.</p><div class="borough-links"><a href="/asbestos-removal-south-london.html">Asbestos removal South London</a><a href="/asbestos-removal-west-london.html">Asbestos removal West London</a></div></section>').section
section.append(region);(ROOT/'locations.html').write_text(str(loc))
xml=original('sitemap.xml')
for item in manifest+[{'url':BASE+'locations.html','assets':[]}]:
 def update(m):
  t=m.group(0);t=re.sub(r'<lastmod>.*?</lastmod>','',t);t=re.sub(r'<image:image>.*?</image:image>','',t,flags=re.S)
  return t.replace('</loc>','</loc>\n<lastmod>2026-09-23</lastmod>'+''.join('<image:image><image:loc>'+BASE+a+'</image:loc></image:image>' for a in item['assets']),1)
 xml,count=re.subn(r'<url>\s*<loc>'+re.escape(item['url'])+r'</loc>.*?</url>',update,xml,flags=re.S);assert count==1,item['url']
(ROOT/'sitemap.xml').write_text(xml)
old=list(csv.DictReader(original('project/LOCATION-IMAGE-MAP.csv').splitlines()))
old=[x for x in old if x['page'] not in [m['path'] for m in manifest]]
with (ROOT/'project/LOCATION-IMAGE-MAP.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(allassets[0]));w.writeheader();w.writerows(old+allassets)
with (ROOT/'project/SITE-INVENTORY.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['path','canonical','title','h1','primary_image','status'])
 for path in sorted(ROOT.glob('*.html')):
  s=soup(path.read_text());c=s.select_one('link[rel=canonical]');im=s.select_one('main img');h=s.h1
  w.writerow([path.name,c.get('href') if c else '',s.title.get_text() if s.title else '',h.get_text(' ',strip=True) if h else '',im.get('src') if im else '', '22-page V3 repair; live QA pending' if path.name in [m['path'] for m in manifest] else 'Existing; preserved'])
(HERE/'manifest.json').write_text(json.dumps(manifest,indent=2));(HERE/'assets.json').write_text(json.dumps(allassets,indent=2))
print('Built',len(manifest),'pages and',len(allassets),'image assets')
