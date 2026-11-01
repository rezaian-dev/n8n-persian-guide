"""Build a fully static RTL website from guide.md. No browser-side dependencies."""
from pathlib import Path
import re, json
import markdown
from html import escape
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'guide.md').read_text()
html=markdown.markdown(source,extensions=['tables','fenced_code','sane_lists'])
entries=[]
def heading(match):
 title=match.group(1);key=f'section-{len(entries)+1}'
 entries.append(f'<a href="#{key}">{title}</a>')
 return f'<h2 id="{key}">{title}</h2>'
html=re.sub(r'<h2>(.*?)</h2>',heading,html)
html=html.replace('<table>','<div class="table-wrap"><table>').replace('</table>','</table></div>')
words=len(source.split());minutes=max(1,round(words/170))
fa=lambda n:str(n).translate(str.maketrans('0123456789','۰۱۲۳۴۵۶۷۸۹'))
template=(ROOT/'scripts/template.html').read_text()
output=template.replace('{{TOC}}','\n'.join(entries)).replace('{{ARTICLE}}',html).replace('{{WORDS}}',fa(words)).replace('{{MINUTES}}',fa(minutes))
(ROOT/'docs/reader.html').write_text(output)
print(f'Built docs/reader.html: {words} words, {len(entries)} headings.')
meta=json.loads((ROOT/'docs/assets/book-meta.json').read_text())
titles=re.findall(r'<h2>(.*?)</h2>', markdown.markdown(source,extensions=['tables','fenced_code','sane_lists']))[:26]
groups=[('01','مبانی و مدل ذهنی','بخش‌های ۱ تا ۵',1,5),('02','اولین گردش‌کار واقعی','بخش‌های ۶ تا ۹',6,9),('03','اعتمادپذیری و اثر جانبی','بخش‌های ۱۰ تا ۱۲',10,12),('04','استقرار و عملیات','بخش‌های ۱۳ تا ۱۸',13,18),('05','هوش مصنوعی کنترل‌شده','بخش‌های ۱۹ تا ۲۲',19,22),('06','تست، عیب‌یابی و انتشار','بخش‌های ۲۳ تا ۲۶',23,26)]
modules=[]
for n,title,subtitle,start,end in groups:
    links=''.join(f'<li><a href="reader.html#section-{i}">{titles[i-1]}</a></li>' for i in range(start,end+1))
    modules.append(f'<details class="module"><summary><span class="module-number">{n}</span><span><b>{title}</b><small>{subtitle}</small></span><i aria-hidden="true">+</i></summary><ol>{links}</ol></details>')
landing=(ROOT/'scripts/landing.html').read_text().replace('{{MODULES}}',''.join(modules)).replace('{{PAGES_EN}}',str(meta['pages'])).replace('{{PAGES_FA}}',fa(meta['pages'])).replace('{{SIZE}}',fa(f"{meta['bytes']/1048576:.2f}"))
(ROOT/'docs/index.html').write_text(landing)
print(f"Built landing page for {meta['pages']}-page PDF.")
