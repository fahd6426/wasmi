# يبني green.html («وسمت أرضك؟» المستقلة) من نفس كود الخانة اللي بالقالب
import re,pathlib
R=pathlib.Path(__file__).resolve().parent.parent
t=(R/'tools/app.template.html').read_text()
sec=t[t.index('<section class="scr" id="green">'):]
sec=sec[:sec.index('</section>')]
body=sec[sec.index('<div class="body">')+len('<div class="body">'):]
body=body[:body.rindex('</div>')]
body=body.replace('<div class="ttl">وسمت أرضك؟</div>','',1)
lines=t.split('\n')
helpers='\n'.join(l for l in lines if l.startswith(('var A=function','var dF=new','var PAGE_ICON=','function OPEN_SAFARI(','var DN=')))
def block(a,b):
    i=next(k for k,l in enumerate(lines) if l.startswith(a));j=next(k for k,l in enumerate(lines) if k>i and l.startswith(b))
    return '\n'.join(lines[i:j])
dev=block('function device(','var PAGE_ICON=')
loc=block('function locSteps(','function motionSteps(')
gd=block('function guide(','/* ================= وسمت أرضك؟')
js=block('/* ================= وسمت أرضك؟','/* ================= الساعة').replace('var GREEN=DATA.green||null','var GREEN=null')
page=f'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>وسمت أرضك؟ 🌱 نسبة الربيع حولك | وسمي</title>
<meta name="description" content="وسمت أرضك؟ شيك على نسبة الربيع حولك من صور الأقمار الصناعية، وقارنها بالأسبوع اللي فات، وشف أقرب الأماكن اللي ربّعت.">
<link rel="canonical" href="https://wasmii.com/green.html">
<meta name="theme-color" content="#1a0d06">
<meta property="og:type" content="website"><meta property="og:locale" content="ar_SA">
<meta property="og:title" content="وسمت أرضك؟ 🌱 نسبة الربيع حولك">
<meta property="og:description" content="نسبة الربيع حولك من صور الأقمار الصناعية، وكيف تغيّرت عن الأسبوع اللي فات.">
<link rel="icon" href="/assets/logo/wasmi-app-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Reem+Kufi:wght@700&family=Tajawal:wght@400;500;700;800&display=swap" rel="stylesheet">
<style>
:root{{--sand:#FAF3E6;--honey:#C98F3E;--dark:#1a0d06;--card:rgba(255,255,255,.08);--line:rgba(250,243,230,.12);--mut:rgba(250,243,230,.6)}}
*{{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}}
body{{background:var(--dark);color:var(--sand);font-family:'Tajawal',system-ui,sans-serif;line-height:1.6;min-height:100vh}}
a{{color:inherit;text-decoration:none}}
.gtop{{display:flex;align-items:center;justify-content:space-between;gap:10px;height:54px;padding:0 16px;padding-top:env(safe-area-inset-top);border-bottom:1px solid var(--line)}}
.gtop .logo{{font-family:'Reem Kufi';font-size:24px}}.gtop h1{{font-size:17px;font-weight:800;color:var(--honey)}}.gtop .sm{{font-size:13.5px;font-weight:700;color:var(--mut)}}
.body{{max-width:560px;margin:0 auto;padding:18px 16px 40px}}
.ttl{{font-size:26px;font-weight:800;margin:6px 0 14px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:22px;padding:16px 18px;margin-bottom:12px}}
.card h3{{font-size:18px;font-weight:800;margin:6px 0 2px}}.card p{{font-size:15px;color:rgba(250,243,230,.85)}}
.card.hero{{background:linear-gradient(135deg,#2a3a12,#4d6a1f 60%,#6f8f35);border:0;padding:20px}}
.card.hero small{{font-size:14px;color:#e6f5c8;font-weight:700}}.card.hero p{{margin-top:6px}}
.when{{display:inline-block;font-size:13px;font-weight:800;padding:3px 12px;border-radius:30px}}
.b{{display:flex;align-items:center;justify-content:center;gap:8px;width:100%;border:0;border-radius:16px;font-family:inherit;font-weight:800;cursor:pointer;padding:14px;font-size:17px;margin-top:10px}}
.b1{{background:var(--honey);color:#fff}}.b2{{background:var(--card);color:var(--sand);border:1px solid var(--line);font-size:15px;padding:11px}}
.note{{font-size:13px;color:var(--mut);margin-top:14px;text-align:center}}
.guide{{list-style:none;margin:12px 0 0;padding:0;display:grid;gap:8px;text-align:right}}
.guide li{{display:flex;gap:10px;align-items:flex-start;background:rgba(250,243,230,.08);border-radius:12px;padding:10px 12px;font-size:15px;line-height:1.6}}
.guide b{{flex:none;width:24px;height:24px;border-radius:50%;background:var(--honey);color:#fff;display:grid;place-items:center;font-size:13px}}
.guide .ic{{display:inline-flex;vertical-align:middle}}
.gbox{{display:none;background:rgba(201,143,62,.1);border:1px solid rgba(201,143,62,.35);border-radius:20px;padding:14px 16px;margin-top:12px}}
.gbox.on{{display:block}}.gbox h3{{font-size:17px;color:var(--honey)}}.gbox p{{font-size:14.5px;color:rgba(250,243,230,.85)}}
</style>
</head>
<body>
<header class="gtop"><a class="logo" href="/">وسمي</a><h1>وسمت أرضك؟ 🌱</h1><a class="sm" href="/">الرئيسية ‹</a></header>
<main class="body">
{body}
</main>
<script>
{helpers}
{dev}
{loc}
{gd}
{js}
loadGreen();
// لو الموقع مسموح من قبل: نشيك على أرضه على طول
try{{navigator.permissions&&navigator.permissions.query({{name:'geolocation'}}).then(function(r){{if(r.state==='granted')greenLoc()}})}}catch(e){{}}
</script>
</body>
</html>
'''
(R/'green.html').write_text(page)
print('green.html',len(page))
