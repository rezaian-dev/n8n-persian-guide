"""Build a fully static RTL website from guide.md. No browser-side dependencies."""
from pathlib import Path
import re
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
(ROOT/'docs/index.html').write_text(output)
print(f'Built docs/index.html: {words} whitespace-separated words, {len(entries)} headings, ~{minutes} minutes.')
