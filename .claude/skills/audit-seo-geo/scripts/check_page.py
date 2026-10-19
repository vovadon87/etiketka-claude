#!/usr/bin/env python3
"""Подробная проверка одной страницы: python check_page.py <url>. Только чтение."""
import sys, json
import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from crawl import page, get
import re, html
def main():
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
    if len(sys.argv)<2: print(__doc__); return
    u=sys.argv[1]; d=page(u); print(json.dumps(d,ensure_ascii=False,indent=1))
    s,h,b,_=get(u); t=b.decode('utf-8','ignore')
    print('\nЗАГОЛОВКИ:'); [print(' ',m.group(1).upper(),re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>','',m.group(2)))).strip()[:90]) for m in re.finditer(r'<(h[1-3])[^>]*>(.*?)</\1>',t,re.S)]
    print('\nВНУТРЕННИЕ ССЫЛКИ:',d['internal_links'])
if __name__=='__main__': main()
