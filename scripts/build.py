"""Build the PDF-first landing page from committed book metadata and article headings."""
from pathlib import Path
import re, json
import markdown
ROOT=Path(__file__).resolve().parents[1]
meta=json.loads((ROOT/'docs/assets/book-meta.json').read_text())
source=(ROOT/'guide.md').read_text()
titles=re.findall(r'<h2>(.*?)</h2>',markdown.markdown(source,extensions=['tables','fenced_code']))[:26]
fa=lambda value:str(value).translate(str.maketrans('0123456789','۰۱۲۳۴۵۶۷۸۹'))
groups=[('01','مبانی و مدل ذهنی','بخش‌های ۱ تا ۵',1,5),('02','اولین گردش‌کار واقعی','بخش‌های ۶ تا ۹',6,9),('03','اعتمادپذیری و اثر جانبی','بخش‌های ۱۰ تا ۱۲',10,12),('04','استقرار و عملیات','بخش‌های ۱۳ تا ۱۸',13,18),('05','هوش مصنوعی کنترل‌شده','بخش‌های ۱۹ تا ۲۲',19,22),('06','تست، عیب‌یابی و انتشار','بخش‌های ۲۳ تا ۲۶',23,26)]
modules=[]
for number,title,subtitle,start,end in groups:
    links=''.join(f'<li><a class="chapter-link" href="N8N-Persian-Guide.pdf#page={meta["chapter_pages"][i-1]}" target="_blank" rel="noopener"><span class="chapter-number">{fa(f"{i:02d}")}</span><span>{re.sub(r"^[۰-۹0-9]+[.\s]+", "", titles[i-1])}</span><small>ص. {fa(meta["chapter_pages"][i-1])}</small></a></li>' for i in range(start,end+1))
    modules.append(f'<details class="module"><summary><span class="module-number">{number}</span><span><b>{title}</b><small>{subtitle}</small></span><i aria-hidden="true">+</i></summary><ol>{links}</ol></details>')
landing=(ROOT/'scripts/landing.html').read_text()
values={'MODULES':''.join(modules),'PAGES_EN':str(meta['pages']),'PAGES_FA':fa(meta['pages']),'SIZE':fa(f"{meta['bytes']/1048576:.2f}"),'SAMPLE1':str(meta['sample_pages'][1]),'SAMPLE2':str(meta['sample_pages'][2])}
for key,value in values.items():landing=landing.replace('{{'+key+'}}',value)
(ROOT/'docs/index.html').write_text(landing)
assert '{{' not in landing, 'Unresolved template variable'
print(f"Built landing page: {meta['pages']}-page PDF, 26 chapter links, Motion {meta['motion_version']}.")
