# يبني garmin.html (صفحة قارمن وسمي المستقلة) من نفس كود قارمن اللي بجوال وسمي
import re,pathlib
R=pathlib.Path(__file__).resolve().parent.parent
t=(R/'tools/app.template.html').read_text()
sec=t[t.index('<section class="scr" id="gps">'):]
sec=sec[:sec.index('</section>')]
css=re.search(r'<style>(.*?)</style>',sec,re.S).group(1)
html=sec[sec.index('<div class="nvw">'):].rstrip()
while html.count('<div')<html.count('</div>'):html=html[:html.rfind('</div>')].rstrip()
lines=t.split('\n')
def grab(start,end):
    i=next(k for k,l in enumerate(lines) if l.startswith(start))
    j=next(k for k,l in enumerate(lines) if k>=i and l.startswith(end))
    return '\n'.join(lines[i:j+1])
js=grab('var NV={','function nvSetCat(')
js=js.replace("function nvOpen(){go('gps');","function nvOpen(){")
js=js.replace("'https://wasmii.com/app#trk='","'https://wasmii.com/garmin.html#trk='")
helpers='\n'.join(l for l in lines if l.startswith(('var A=function','function esc(','function device(','var DN=','function OPEN_SAFARI(','function guide(','function unguide(')) or l.startswith(' inApp:') or l.startswith(' var ol=document.getElementById(px') or l.startswith("  if(typeof s==='string')"))
page=f'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>قارمن وسمي 🧭 خريطة البر بالأقمار الصناعية | وسمي</title>
<meta name="description" content="قارمن وسمي: خريطة البر بالأقمار الصناعية، تعرف وش حولك من جبال وشعبان وأودية وآبار، وسجّل جرتك وشاركها مع ربعك عشان يمشون على نفس الطريق.">
<link rel="canonical" href="https://wasmii.com/garmin.html">
<meta name="theme-color" content="#1a0d06">
<meta property="og:type" content="website">
<meta property="og:locale" content="ar_SA">
<meta property="og:title" content="قارمن وسمي 🧭 امشِ على نفس الجرة">
<meta property="og:description" content="خريطة بر بالأقمار الصناعية، وش حولك من جبال وشعبان، وسجّل جرتك وشاركها.">
<link rel="icon" href="/assets/logo/wasmi-app-icon.png">
<link rel="manifest" href="/garmin.webmanifest">
<link rel="apple-touch-icon" href="/assets/logo/wasmi-app-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="قارمن وسمي">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Reem+Kufi:wght@700&family=Tajawal:wght@400;500;700;800&display=swap" rel="stylesheet">
<style>
:root{{--sand:#FAF3E6;--honey:#C98F3E;--terra:#A5552E;--brown:#5A331C;--dark:#1a0d06;--card:rgba(255,255,255,.08);--line:rgba(250,243,230,.12);--mut:rgba(250,243,230,.6)}}
*{{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}}
html,body{{height:100%}}
body{{background:var(--dark);color:var(--sand);font-family:'Tajawal',system-ui,sans-serif;line-height:1.6;display:flex;flex-direction:column;height:100vh;height:100dvh;overflow:hidden}}
.gtop{{flex:none;display:flex;align-items:center;justify-content:space-between;gap:10px;height:54px;padding:0 14px;padding-top:env(safe-area-inset-top);border-bottom:1px solid var(--line)}}
.gtop a{{color:var(--sand);text-decoration:none}}
.gtop .logo{{font-family:'Reem Kufi';font-size:24px}}
.gtop h1{{font-size:17px;font-weight:800;color:var(--honey)}}
.gtop .sm{{font-size:13.5px;font-weight:700;color:var(--mut)}}
.b{{display:flex;align-items:center;justify-content:center;gap:8px;width:100%;border:0;border-radius:16px;font-family:inherit;font-weight:800;cursor:pointer}}
.b1{{background:var(--honey);color:#fff}}.b2{{background:var(--card);color:var(--sand);border:1px solid var(--line)}}
.guide{{list-style:none;margin:12px 0 0;padding:0;display:grid;gap:8px;text-align:right}}
.guide li{{display:flex;gap:10px;align-items:flex-start;background:rgba(250,243,230,.08);border-radius:12px;padding:10px 12px;font-size:15px;line-height:1.6}}
.guide b{{flex:none;width:24px;height:24px;border-radius:50%;background:var(--honey);color:#fff;display:grid;place-items:center;font-size:13px}}
.gbox{{display:none;background:rgba(201,143,62,.1);border:1px solid rgba(201,143,62,.35);border-radius:20px;padding:14px 16px;margin-top:12px}}
.gbox.on{{display:block}}.gbox h3{{font-size:17px;color:var(--honey)}}.gbox p{{font-size:14.5px;color:rgba(250,243,230,.85)}}
{css}
@media(min-width:900px){{.nvw{{flex-direction:row}}.nvsh{{max-height:none!important;height:auto!important;margin-top:0!important;border-radius:0!important;box-shadow:none!important;width:380px;border-top:0;border-right:1px solid var(--line)}}.nvgrab{{display:none!important}}#nvMap{{order:2}}.nvbar{{right:396px}}.nvlay{{right:396px}}}}
</style>
</head>
<body class="gpage">
<header class="gtop"><a class="logo" href="/">وسمي</a><h1>قارمن وسمي 🧭</h1><a class="sm" href="/">الرئيسية ‹</a></header>
{html}
<script>
{helpers}
{js}
nvOpen();
</script>
</body>
</html>
'''
(R/'garmin.html').write_text(page)
print('garmin.html',len(page))
