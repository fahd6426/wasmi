# يبني app.html (جوال وسمي) من القالب ومحتوى صفحات الموقع
import re, json, html, os, io, base64
from PIL import Image
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = 'https://wasmii.com'
def rd(p): return open(os.path.join(R, p), encoding='utf-8').read()
def strip(x): return html.unescape(re.sub(r'<[^>]+>', '', x)).strip()

p = rd('places.html')
places = [dict(r=m[1], u=S+m[2], rg=strip(m[3]), n=strip(m[4]), b=strip(m[5]), d=strip(m[6])) for m in re.finditer(
    r'<a class="pk" data-r="([^"]+)" href="([^"]+)"><span class="rg">(.*?)</span><h2>(.*?)<span class="badge">(.*?)</span></h2><p>(.*?)</p></a>', p)]
b = rd('birds.html')
birds = [dict(u=S+m[1], i=S+m[2], n=strip(m[3])) for m in re.finditer(r'<a class="bk" href="([^"]+)"><img src="([^"]+)"[^>]*><span>(.*?)</span></a>', b)]
def thumb(url):
    im = Image.open(os.path.join(R, url.replace(S + '/', ''))).convert('RGB')
    im.thumbnail((420, 420))
    b = io.BytesIO(); im.save(b, 'JPEG', quality=72, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
for x in birds: x['i'] = thumb(x['i'])
seen = [dict(n=strip(m[1]), w=strip(m[2]), d=strip(m[3])) for m in re.finditer(r'<div class="bc"><h3>(.*?)</h3><span class="when">(.*?)</span><p>(.*?)</p></div>', b)]
r = rd('rules.html')
secs = [s for s in re.findall(r'(<section class="rs">.*?</section>)', r, re.S) if 'المصادر' not in s]
rules = ''.join(secs)
rules = re.sub(r'<a href="#[^"]*"[^>]*>.*?</a>', '', rules)
rules = re.sub(r'href="/', f'href="{S}/', rules)
rules = re.sub(r'\s*(target|rel|style)="[^"]*"', '', rules)
rules = rules.replace('<a ', '<a target="_blank" rel="noopener" ')
prods = json.loads(rd('data/products.json'))['items']
data = json.dumps(dict(places=places, birds=birds, seen=seen, rules=rules, prods=prods), ensure_ascii=False).replace('</', '<\\/')

t = rd('tools/app.template.html')
t = t.replace('/*BASECSS*/', rd('tools/app.base.css'))
t = t.replace('/*SEASONS*/', rd('seasons-data.js'))
t = t.replace('/*DATA*/', data)
open(os.path.join(R, 'app.html'), 'w', encoding='utf-8').write(t)
print('app.html', len(t), 'places', len(places), 'birds', len(birds), 'prods', len(prods))
