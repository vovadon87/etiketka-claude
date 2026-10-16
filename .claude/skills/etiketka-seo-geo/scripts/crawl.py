#!/usr/bin/env python3
"""Проверка сайта etiketka.express (или другого): варианты домена, robots, sitemap, страницы.
Использование: python crawl.py https://etiketka.express/ [--out crawl.json] [--pages /a,/b]
Только чтение. Стандартная библиотека."""
import sys, re, json, html, urllib.request, urllib.error
UA={'User-Agent':'Mozilla/5.0 (compatible; etiketka-seo-geo/1.0)','Accept-Language':'ru-RU,ru;q=0.9'}
class NoRedir(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*a,**k): return None
def get(u,follow=True):
    op=urllib.request.build_opener() if follow else urllib.request.build_opener(NoRedir)
    try:
        r=op.open(urllib.request.Request(u,headers=UA),timeout=60); return r.status,dict(r.headers),r.read(),r.geturl()
    except urllib.error.HTTPError as e: return e.code,dict(e.headers),(e.read() if e.fp else b''),u
    except Exception as e: return None,{},str(e).encode(),u
def meta(t,n,attr='name'):
    m=re.search(r'<meta[^>]*%s="%s"[^>]*content="([^"]*)"'%(attr,re.escape(n)),t,re.I) or re.search(r'<meta[^>]*content="([^"]*)"[^>]*%s="%s"'%(attr,re.escape(n)),t,re.I)
    return html.unescape(m.group(1)) if m else None
def page(u):
    s,h,b,final=get(u); t=b.decode('utf-8','ignore'); txt=html.unescape(re.sub(r'<[^>]+>',' ',re.sub(r'<(script|style)[\s\S]*?</\1>','',t)))
    ld=[]
    for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>',t,re.S):
        try: j=json.loads(x); ld+=[j.get('@type')] if isinstance(j,dict) else [y.get('@type') for y in j]
        except Exception: ld.append('INVALID_JSON')
    imgs=re.findall(r'<img[^>]*>',t)
    return dict(url=u,status=s,final_url=final,bytes=len(b),x_robots=h.get('X-Robots-Tag'),title=(re.search(r'<title>(.*?)</title>',t,re.S) or [None,None])[1],description=meta(t,'description'),meta_robots=meta(t,'robots'),canonical=re.findall(r'<link[^>]*rel="canonical"[^>]*href="([^"]*)"',t),h1=[re.sub(r'<[^>]+>','',x).strip() for x in re.findall(r'<h1[^>]*>(.*?)</h1>',t,re.S)],h2_count=len(re.findall(r'<h2[\s>]',t)),lang=(re.search(r'<html[^>]*lang="([^"]*)"',t) or [None,None])[1],og_title=meta(t,'og:title','property'),og_image=meta(t,'og:image','property'),jsonld_types=ld,images=len(imgs),images_without_alt=sum(1 for i in imgs if not re.search(r'\balt=',i)),metrika=bool(re.search(r'mc\.yandex|metrika/tag',t)),gsc_or_ga=bool(re.search(r'gtag|googletagmanager',t)),internal_links=sorted(set(re.findall(r'href="(/[^"#?]*)"',t))),phones=sorted(set(re.findall(r'\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}',t))),emails=sorted(set(re.findall(r'[\w.]+@[\w.-]+\.\w+',t))),legal=sorted(set(re.findall(r'ООО\s*«[^»]+»',txt))),deadline_phrases=sorted(set(re.findall(r'(?:готовность|срок)[^.]{0,45}',txt,re.I)))[:8],min_order=sorted(set(re.findall(r'от\s*\d[\d\s]*₽',txt))),words=len(txt.split()))
def main():
    a=sys.argv[1:]
    if not a: print(__doc__); return
    base=a[0].rstrip('/'); out='crawl.json'; pages=None
    if '--out' in a: out=a[a.index('--out')+1]
    if '--pages' in a: pages=a[a.index('--pages')+1].split(',')
    host=re.sub(r'^https?://(www\.)?','',base)
    rep={'domains':{},'robots':None,'sitemap':[],'pages':{}}
    for u in [f'http://{host}/',f'https://{host}/',f'http://www.{host}/',f'https://www.{host}/']:
        s,h,b,_=get(u,False); rep['domains'][u]={'status':s,'location':h.get('Location'),'bytes':len(b)}
    s,h,b,_=get(f'{base}/robots.txt'); rep['robots']={'status':s,'text':b.decode('utf-8','ignore')[:3000]}
    s,h,b,_=get(f'{base}/sitemap.xml'); rep['sitemap']=re.findall(r'<loc>([^<]+)</loc>',b.decode('utf-8','ignore'))
    if pages is None: pages=['/']+[re.sub(r'^https?://[^/]+','',l) for l in rep['sitemap'] if re.sub(r'^https?://[^/]+','',l) not in ('','/')]
    for p in pages: rep['pages'][p]=page(base+p)
    rep['pages']['/__404_test__']=page(base+'/etiketka-seo-geo-404-test')
    json.dump(rep,open(out,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
    # краткий отчёт
    print('ДОМЕНЫ:'); [print(' ',u,v['status'],v['location'] or '') for u,v in rep['domains'].items()]
    print('SITEMAP:',rep['sitemap'])
    for p,d in rep['pages'].items():
        print(f"\n{p} → {d['status']} | title: {d['title']} | canonical: {d['canonical']} | H1: {d['h1']} | robots: {d['meta_robots']} | ld: {d['jsonld_types']} | метрика: {d['metrika']} | ссылок внутр.: {len(d['internal_links'])} | без alt: {d['images_without_alt']}/{d['images']}")
        if d['deadline_phrases']: print('  сроки:',d['deadline_phrases'])
    # сигналы
    print('\nСИГНАЛЫ:')
    dom=rep['domains']; ok=[u for u,v in dom.items() if v['status']==200]
    if len(ok)>1: print(' - P0: несколько вариантов домена отдают 200 без редиректа:',ok)
    for p,d in rep['pages'].items():
        if d['status']==200 and d['canonical'] and d['canonical'][0].startswith('http://'): print(f' - P1: canonical на http:// — {p}')
        if d['status']==200 and not d['title']: print(f' - P1: пустой title — {p}')
        if d['status']==200 and not d['description'] and p not in ('/__404_test__',): print(f' - P2: нет description — {p}')
        if 'INVALID_JSON' in d['jsonld_types']: print(f' - P2: невалидный JSON-LD — {p}')
        s=' '.join(d['deadline_phrases']).lower()
        if ('от 1' in s or 'от\xa01' in s) and ('1–3' in s or '1-3' in s): print(f' - P1: противоречие сроков («от 1 дня» и «1–3 дня») — {p}')
        if d['status']==200 and not d['metrika']: print(f' - P1: нет счётчика Метрики — {p}')
    print('\nСохранено:',out)
if __name__=='__main__': main()
