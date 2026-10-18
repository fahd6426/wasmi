# يبني صفحات: أماكن البر (places.html + places/*.html) وأنظمة البر (rules.html)
# تشغيل: python3 tools/build_pages.py  (من جذر الريبو)
import os, urllib.parse, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPDATED = "أكتوبر ٢٠٢٦"

MENU = [("/", "الرئيسية"), ("/seasons.html", "تقويم المواسم"), ("/places.html", "أماكن البر"), ("/rules.html", "أنظمة البر")]

def nav(active):
    items = "".join(f'<li><a href="{h}"{" class=\"on\"" if h == active else ""}>{t}</a></li>' for h, t in MENU)
    return f'''<nav class="nav"><div class="wrap">
<a class="logo" href="/">وسمي</a>
<button class="burger" aria-label="القائمة" onclick="document.querySelector('.menu').classList.toggle('open')">☰</button>
<ul class="menu">
{items}
<li><a class="wx" href="https://ncm.gov.sa" target="_blank" rel="noopener">الطقس الرسمي ↗</a></li>
</ul></div></nav>'''

FOOT = '''<footer class="wrap foot">
<div class="links"><a href="/about.html">من نحن</a><a href="/about.html#contact">تواصل معنا</a><a href="/privacy.html">سياسة الخصوصية</a></div>
<p>وسمي ليس جهة أرصاد، ولا يقدّم توقعات أو تنبيهات جوية. للطقس والتنبيهات: <a href="https://ncm.gov.sa" target="_blank" rel="noopener">المركز الوطني للأرصاد</a>.</p>
<p>© <span id="yr"></span> وسمي</p>
</footer>
<script>document.getElementById('yr').textContent=new Date().getFullYear()</script>'''

def page(title, desc, canon, active, body, extra_css=""):
    return f'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="https://wasmii.com{canon}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Reem+Kufi:wght@500;700&family=Tajawal:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css">
<style>{extra_css}</style>
</head>
<body>
{nav(active)}
<main class="wrap">
{body}
</main>
{FOOT}
</body>
</html>
'''

def maps(q):
    return "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(q)

# ---------------- أماكن البر ----------------
SP = "https://saudipedia.com/"
PLACES = [
 dict(slug="khuraim", name="روضة خريم", region="منطقة الرياض", near="نحو ١٠٠ كم شمال شرق الرياض", kind="روضة",
  summary="من أشهر روضات نجد، منخفض أخضر تصب فيه السيول من الشرق.",
  about=["منخفض طوله نحو ١٨ كم وعرضه نحو ٢٫٥ كم، تصب فيه ثلاثة أودية من جهة الشرق، ويحدّه من الشمال الشرقي عرق رملي من رمال الدهناء يُعرف بعرق فيض خريم.",
         "ينمو فيها نحو ١٣٢ نوعاً من النباتات البرية، منها الأرطى والسدر والطلح والشبرم والشيح والقيصوم."],
  reserve="داخل محمية الإمام عبدالعزيز بن محمد الملكية، وهي تحت إشراف هيئة تطوير المحمية.",
  rules="تأكد من ضوابط الدخول والتنزه في موقع هيئة تطوير محمية الإمام عبدالعزيز بن محمد الملكية قبل الزيارة.",
  best="تزهى بعد أمطار الشتاء والربيع.",
  map="روضة خريم",
  src=[("سعوديبيديا: روضة خريم", SP+"روضة-خريم"), ("سعوديبيديا: محمية الإمام عبدالعزيز بن محمد", SP+"محمية-الإمام-عبدالعزيز-بن-محمد")]),
 dict(slug="tunhat", name="روضة التنهات", region="منطقة الرياض", near="نحو ١٩٠ كم شمال الرياض", kind="روضة",
  summary="روضة واسعة شمال الرياض، صارت مع روضة الخفس نواة محمية الملك عبدالعزيز الملكية.",
  about=["تُعد من الروضات الطبيعية المعروفة في منطقة الرياض، وضُمّت مع روضة الخفس وما حولهما في محمية الملك عبدالعزيز الملكية."],
  reserve="داخل محمية الملك عبدالعزيز الملكية.",
  rules="ممنوع دخول المركبات إلى الروضات داخل المحمية. راجع ضوابط التنزه في موقع هيئة تطوير محمية الملك عبدالعزيز الملكية قبل الزيارة.",
  best="تزهى بعد أمطار الشتاء والربيع.",
  map="روضة التنهات",
  src=[("سعوديبيديا: قائمة عشر روضات طبيعية", SP+"قائمة-عشر-روضات-طبيعية-في-السعودية"), ("سعوديبيديا: قائمة المحميات الملكية", SP+"قائمة-المحميات-الملكية-في-السعودية")]),
 dict(slug="summan", name="الصمان", region="بين الرياض والمنطقة الشرقية", near="هضبة شرق رمال الدهناء", kind="هضبة",
  summary="هضبة واسعة شرق الدهناء، فيها روضات وفياض كثيرة، والتنزه فيها صار بتصريح.",
  about=["هضبة شرق عروق الدهناء تكثر فيها الروضات والفياض، ويقصدها أهل البر من الرياض والشرقية."],
  reserve="الجزء الواقع ضمن محمية الملك عبدالعزيز الملكية.",
  rules="التنزه بتصريح مسبق من موقع هيئة تطوير محمية الملك عبدالعزيز الملكية، ومسموح من ٦ الصباح لين ٦ المساء. ممنوع التخييم بكل أنواعه (مظلات مثبتة، خيام مبيت، كرافانات)، وممنوع دخول المركبات للروضات، والدراجات النارية، والسير خارج المسارات القائمة. يُستثنى أهالي مركزي المناخ والحيراء.",
  best="بعد أمطار الوسم والشتاء.",
  map="الصمان",
  src=[("عكاظ: «الدخول الإلكتروني» شرط التنزه في الصمان (فبراير ٢٠٢٥)", "https://www.okaz.com.sa/news/local/2181965")]),
 dict(slug="dahna", name="الدهناء", region="من شمال المملكة إلى الربع الخالي", near="حزام رملي شرق الرياض", kind="عروق رملية",
  summary="عروق رملية حمراء طويلة تصل النفود الكبير بالربع الخالي.",
  about=["حزام من العروق الرملية الحمراء يمتد على شكل قوس، ويربط النفود الكبير شمالاً بالربع الخالي جنوباً، ومن عروقه عرق فيض خريم المطل على روضة خريم."],
  reserve="أجزاء منها ضمن محمية الملك عبدالعزيز الملكية.",
  rules="التنزه في الأجزاء الواقعة ضمن محمية الملك عبدالعزيز الملكية يحتاج تصريح مسبق من موقع الهيئة، بنفس ضوابط الصمان.",
  best="الشتاء والربيع.",
  map="رمال الدهناء",
  src=[("سعوديبيديا: صحراء النفود الكبير", SP+"en/al-nufud-al-kabir-desert"), ("سعوديبيديا: روضة خريم", SP+"روضة-خريم"), ("الموجز السعودي: آلية التنزه في الصمان والدهناء", "https://x.com/saudistuff/status/1936803436688978415")]),
 dict(slug="nafud", name="النفود الكبير", region="حائل والجوف وتبوك", near="شمال المملكة", kind="صحراء رملية",
  summary="ثاني أكبر صحراء رملية في المملكة بعد الربع الخالي، برمالها الحمراء وكثبانها الهلالية.",
  about=["مساحته نحو ٦٥ ألف كم²، ويمتد في ثلاث مناطق: حائل والجوف وتبوك، ويتصل بالدهناء من الشرق والشمال الشرقي.",
         "رماله حمراء، وكثبانه هلالية وطولية وعرضية وهرمية. ينمو في الأجزاء المحمية منه الأرطى والطلح والأثل، ويعيش فيه الذئب العربي وغزال الريم والثعلب الأحمر والأرانب.",
         "في جنوبه موقع جبة الأثري المسجل في قائمة التراث العالمي."],
  reserve="ضُمّت ثلاث محميات سابقة في نطاقه (حرة الحرة والطبيق والخنفة) في محمية الملك سلمان بن عبدالعزيز الملكية.",
  rules="إذا كان مكانك داخل نطاق محمية الملك سلمان بن عبدالعزيز الملكية فراجع ضوابطها قبل التخييم. وخارج المحميات يحتاج التخييم تصريح من منصة «نباتي».",
  best="الشتاء.",
  map="النفود الكبير",
  src=[("سعوديبيديا: صحراء النفود الكبير", SP+"en/al-nufud-al-kabir-desert")]),
 dict(slug="aja-salma", name="جبال أجا وسلمى", region="منطقة حائل", near="غرب مدينة حائل", kind="جبال",
  summary="جبلا طيء، فيهما شعاب وأودية بالطلح والسدر ومتنزهات معروفة لأهل حائل.",
  about=["أجا أعلى جبال هضبة نجد وأكبرها بارتفاع ١٥٤٤ م، وسلمى بارتفاع ١٤٣٠ م.",
         "في أجا متنزهات طبيعية منها عقدة ومشار وتوارن، وتخترق الجبلين شعاب كثيفة بأشجار الطلح والسدر، ومن عيون سلمى عين صدى.",
         "شمال أجا يقع شعيب جو، ويقصده المتنزهون."],
  reserve="", rules="", best="الشتاء والربيع.",
  map="جبل أجا حائل",
  src=[("سعوديبيديا: جبلا أجا وسلمى", SP+"جبلا-أجا-وسلمى")]),
 dict(slug="jubbah", name="جبة", region="منطقة حائل", near="جنوب النفود الكبير، شمال غرب حائل", kind="موقع أثري",
  summary="من أقدم مواقع الرسوم الصخرية في المملكة، ومسجل في قائمة التراث العالمي.",
  about=["فيها بقايا مستوطنات بشرية من العصر الحجري، ورسوم ونقوش صخرية على جبلي أم سنمان والغوطة.",
         "سجّلتها اليونسكو في قائمة التراث العالمي عام ٢٠١٥، وكانت محطة على طريق القوافل."],
  reserve="", rules="العبث بالنقوش والآثار ممنوع ومُجرَّم.", best="الشتاء.",
  map="جبة حائل",
  src=[("سعوديبيديا: أين تقع مدينة جبة الأثرية؟", SP+"أين-تقع-مدينة-جبة-الأثرية؟"), ("سعوديبيديا: صحراء النفود الكبير", SP+"en/al-nufud-al-kabir-desert")]),
 dict(slug="zubayyah", name="روضة زعبية", region="منطقة الحدود الشمالية", near="شرق قرية لينة التاريخية، محافظة رفحاء", kind="روضة",
  summary="روضة على ضفاف وادي أعيوج، يكسوها النفل والخبيز بعد المطر.",
  about=["تقع على ضفاف وادي أعيوج شرق قرية لينة التاريخية في محافظة رفحاء.",
         "تنبت فيها بعد المطر نباتات موسمية مثل النفل والرشاد والخبيز، وفيها أشجار السدر."],
  reserve="", rules="", best="بعد أمطار الشتاء والربيع.",
  map="روضة زعبية لينة",
  src=[("سعوديبيديا: قائمة عشر روضات طبيعية", SP+"قائمة-عشر-روضات-طبيعية-في-السعودية")]),
 dict(slug="jabal-al-lawz", name="جبل اللوز", region="منطقة تبوك", near="نحو ٢٠٠ كم شمال غرب تبوك، شمال شرق البدع", kind="جبال",
  summary="أعلى قمم مرتفعات مدين، وتنزل عليه الثلوج في الشتاء تقريباً كل سنة.",
  about=["ارتفاعه نحو ٢٥٤٩ م، وهو أعلى قمة في مرتفعات جبال مدين، ويقع ضمن الحدود الجغرافية لنيوم.",
         "تتساقط عليه الثلوج شتاءً تقريباً كل عام، ويقصده الناس للقيادة على طرقه الجبلية والتنزه في الثلج. وفيه رسوم صخرية ونقوش وكتابات إسلامية."],
  reserve="", rules="الطرق الجبلية وقت الثلوج خطرة، فتابع تنبيهات المركز الوطني للأرصاد قبل الطلعة.", best="الشتاء.",
  map="جبل اللوز تبوك",
  src=[("سعوديبيديا: جبل اللوز", SP+"جبل-اللوز")]),
]

PCSS = """
.pl{display:grid;gap:14px;margin:18px 0 26px}@media(min-width:680px){.pl{grid-template-columns:1fr 1fr}}
.pk{display:block;text-decoration:none;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px 18px}
.pk:hover{border-color:var(--honey)}.pk h2{font-size:22px}.pk .rg{font-size:13.5px;color:var(--terra);font-weight:700}
.pk p{font-size:15px;margin-top:4px}.badge{display:inline-block;font-size:12px;background:var(--sand);border:1px solid var(--line);border-radius:999px;padding:0 10px;margin-inline-start:6px;font-weight:500;color:var(--muted)}
.filters{display:flex;gap:6px;flex-wrap:wrap;margin-top:14px}.filters button{font:inherit;font-size:14px;background:var(--card);border:1px solid var(--line);border-radius:999px;padding:4px 14px;color:var(--brown);cursor:pointer}
.filters button.on{background:var(--brown);color:var(--sand);border-color:var(--brown)}
"""

DCSS = """
.crumb{font-size:14px;color:var(--muted);margin-top:22px}.crumb a{color:var(--terra)}
.facts{display:grid;gap:10px;margin:16px 0}@media(min-width:640px){.facts{grid-template-columns:1fr 1fr}}
.fact{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:10px 14px}.fact small{display:block;color:var(--muted);font-size:12.5px}.fact b{font-size:15.5px}
.warn{background:#FFF4E5;border:1px solid var(--honey);border-radius:14px;padding:12px 16px;margin:14px 0;font-size:15px}
.srcs{font-size:13.5px;color:var(--muted);margin-top:22px}.srcs a{color:var(--terra)}
"""

def region_key(p):
    r = p["region"]
    if "حائل" in r or "الحدود الشمالية" in r or "تبوك" in r or "الجوف" in r: return "الشمال"
    return "الوسطى والشرقية"

def build_places():
    os.makedirs(os.path.join(ROOT, "places"), exist_ok=True)
    cards = []
    for p in PLACES:
        cards.append(f'<a class="pk" data-r="{region_key(p)}" href="/places/{p["slug"]}.html"><span class="rg">{p["region"]}</span><h2>{p["name"]}<span class="badge">{p["kind"]}</span></h2><p>{p["summary"]}</p></a>')
        facts = [("المنطقة", p["region"]), ("الموقع", p["near"]), ("النوع", p["kind"]), ("أحسن وقت", p["best"])]
        if p["reserve"]: facts.append(("المحمية", p["reserve"]))
        fx = "".join(f'<div class="fact"><small>{k}</small><b>{v}</b></div>' for k, v in facts)
        ab = "".join(f"<p>{t}</p>" for t in p["about"])
        rl = f'<div class="warn"><b style="color:var(--terra)">قبل ما تروح:</b> {p["rules"]} <a href="/rules.html" style="color:var(--terra)">أنظمة البر كاملة</a></div>' if p["rules"] else ""
        sr = " · ".join(f'<a href="{u}" target="_blank" rel="noopener">{t}</a>' for t, u in p["src"])
        body = f'''<div class="crumb"><a href="/places.html">أماكن البر</a> ‹ {p["name"]}</div>
<div class="prose"><h1 style="margin-top:6px">{p["name"]}</h1><p style="color:var(--muted)">{p["summary"]}</p></div>
<div class="facts">{fx}</div>
<div class="prose">{ab}</div>
{rl}
<p style="margin-top:16px"><a class="btn" href="{maps(p["map"])}" target="_blank" rel="noopener">افتح الموقع بالخرائط ↗</a></p>
<p class="srcs">المصادر: {sr}<br>آخر مراجعة: {UPDATED}</p>'''
        with open(os.path.join(ROOT, "places", p["slug"] + ".html"), "w", encoding="utf-8") as f:
            f.write(page(f'{p["name"]} | أماكن البر | وسمي', f'{p["name"]} ({p["region"]}): {p["summary"]}', f'/places/{p["slug"]}.html', "/places.html", body, DCSS))
    body = f'''<h1 style="font-size:30px;margin:26px 0 2px">أماكن البر</h1>
<p style="color:var(--muted)">روضات ونفود وجبال يقصدها أهل البر، مع موقعها والأنظمة اللي تحتاج تعرفها قبل الطلعة.</p>
<div class="filters"><button class="on" data-f="الكل">الكل</button><button data-f="الشمال">الشمال</button><button data-f="الوسطى والشرقية">الوسطى والشرقية</button></div>
<div class="pl" id="pl">{"".join(cards)}</div>
<p style="font-size:13.5px;color:var(--muted)">المعلومات من مصادر منشورة ومذكورة في صفحة كل مكان. الأنظمة تتغير، فتأكد من الجهة المسؤولة قبل الزيارة.</p>
<script>document.querySelectorAll('.filters button').forEach(b=>b.onclick=()=>{{document.querySelectorAll('.filters button').forEach(x=>x.classList.toggle('on',x===b));document.querySelectorAll('#pl .pk').forEach(c=>c.style.display=(b.dataset.f==='الكل'||c.dataset.r===b.dataset.f)?'':'none')}})</script>'''
    with open(os.path.join(ROOT, "places.html"), "w", encoding="utf-8") as f:
        f.write(page("أماكن البر في السعودية | وسمي", "دليل أماكن البر في السعودية: روضة خريم، التنهات، الصمان، الدهناء، النفود الكبير، أجا وسلمى، جبة، روضة زعبية، جبل اللوز، مع الموقع والأنظمة.", "/places.html", "/places.html", body, PCSS))

# ---------------- أنظمة البر ----------------
NCVC_V = "https://ncvc.gov.sa/ar/digitalKnowledge/Violation/Pages/default.aspx"
RULES_SRC = [
 ("عاجل: نشر القواعد التنظيمية للمخيمات البرية (ديسمبر ٢٠٢٥)", "https://ajel.sa/local/bbb5qcdvkc"),
 ("المركز الوطني لتنمية الغطاء النباتي: المخالفات والعقوبات", NCVC_V),
 ("المركز الوطني لتنمية الغطاء النباتي: دليل التخييم", "https://ncvc.gov.sa/en/Pages/CampingCaravanGuide2025.aspx"),
 ("عكاظ: ضوابط التنزه في الصمان (فبراير ٢٠٢٥)", "https://www.okaz.com.sa/news/local/2181965"),
 ("هيئة تطوير محمية الإمام تركي بن عبدالله الملكية: تصريح التخييم", "https://itba.gov.sa/permits/camping-permit"),
 ("سعوديبيديا: قائمة المحميات الملكية", SP+"قائمة-المحميات-الملكية-في-السعودية"),
]

FINES = [
 ("قطع شجرة أو اقتلاعها في أراضي الغطاء النباتي", "١٠٬٠٠٠", "١٥٬٠٠٠", "٢٠٬٠٠٠", "لكل شجرة"),
 ("قطع شجرة أو اقتلاعها داخل المحميات", "٢٠٬٠٠٠", "٣٠٬٠٠٠", "٤٠٬٠٠٠", "لكل شجرة"),
 ("قطع شجيرة", "٣٬٠٠٠", "٥٬٠٠٠", "٧٬٠٠٠", "لكل شجيرة"),
 ("نقل أو بيع أو تخزين أو جمع الحطب المحلي", "٥٬٠٠٠", "١٠٬٠٠٠", "١٦٬٠٠٠", "لكل متر مكعب"),
 ("نقل أو بيع أو تخزين الفحم المحلي", "٥٬٠٠٠", "١٠٬٠٠٠", "١٦٬٠٠٠", "لكل متر مكعب"),
 ("إشعال النار خارج الأماكن المخصصة في الغابات والمتنزهات الوطنية", "١٬٠٠٠", "٢٬٠٠٠", "٣٬٠٠٠", ""),
 ("دخول المركبات للروضات والأراضي المحمية", "٥٠٠", "١٬٠٠٠", "٢٬٠٠٠", "لكل مركبة"),
 ("رمي النفايات خارج أماكنها في الغابات والمتنزهات الوطنية", "٥٠٠", "١٬٠٠٠", "٢٬٠٠٠", ""),
 ("التخييم بدون تصريح في الغابات والمتنزهات الوطنية", "٥٠٠", "١٬٠٠٠", "٣٬٠٠٠", "لكل مخيم"),
]

RCSS = """
.toc{display:flex;gap:6px;flex-wrap:wrap;margin:14px 0 6px}.toc a{font-size:14px;text-decoration:none;background:var(--card);border:1px solid var(--line);border-radius:999px;padding:3px 12px}
.rs{margin:30px 0}.rs>h2{font-size:23px;margin-bottom:10px;scroll-margin-top:76px}
.rs ul{padding-inline-start:20px}.rs li{font-size:15.5px;margin:3px 0}.rs p{font-size:15.5px}
.tw{overflow-x:auto;border:1px solid var(--line);border-radius:14px;background:var(--card)}
table{border-collapse:collapse;width:100%;font-size:14px}th,td{padding:8px 8px;text-align:right;border-bottom:1px solid var(--line)}
th{background:var(--line);font-weight:700;font-size:13.5px}td.n{white-space:nowrap;font-weight:700;color:var(--terra)}tr:last-child td{border-bottom:0}
td small{display:block;color:var(--muted);font-size:12px}
.fee{display:grid;gap:10px}@media(min-width:640px){.fee{grid-template-columns:1fr 1fr 1fr}}
.fee div{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px 14px}.fee b{display:block;font-size:20px;color:var(--terra)}.fee small{color:var(--muted)}
.srcs{font-size:13.5px;color:var(--muted)}.srcs a{color:var(--terra)}.srcs li{margin:3px 0}
"""

def build_rules():
    rows = "".join(f'<tr><td>{a}{f"<small>{u}</small>" if u else ""}</td><td class="n">{b}</td><td class="n">{c}</td><td class="n">{d}</td></tr>' for a, b, c, d, u in FINES)
    srcs = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a></li>' for t, u in RULES_SRC)
    body = f'''<h1 style="font-size:30px;margin:26px 0 2px">أنظمة البر</h1>
<p style="color:var(--muted)">وش المسموح والممنوع بالكشتة والتخييم، والتصاريح والغرامات، من الأنظمة الرسمية.</p>
<div class="toc"><a href="#tanazzuh">التنزه والتخييم</a><a href="#permit">تصريح التخييم</a><a href="#mamnu">الممنوعات</a><a href="#mahmiyat">المحميات الملكية</a><a href="#fines">الغرامات</a></div>

<section class="rs"><h2 id="tanazzuh">الكشتة اليومية والتخييم</h2>
<ul><li><b>الكشتة اليومية</b> (أقل من ٢٤ ساعة) ما تحتاج تصريح تخييم، لكنها تخضع لضوابط التنزه.</li>
<li><b>التخييم والمبيت</b> يحتاج تصريح من المركز الوطني لتنمية الغطاء النباتي ومكافحة التصحر.</li>
<li><b>المحميات الملكية</b> لها أنظمتها الخاصة، وبعضها يطلب تصريح حتى للكشتة اليومية.</li></ul></section>

<section class="rs"><h2 id="permit">تصريح التخييم</h2>
<p>يطلع التصريح فوري من منصة <a href="https://nabati.ncvc.gov.sa" target="_blank" rel="noopener" style="color:var(--terra);font-weight:700">نباتي ↗</a>: تختار «طلب ترخيص تخييم»، وتعبي بياناتك وموقع المخيم، وتوافق على التعهد.</p>
<div class="fee" style="margin:12px 0"><div><small>مخيم فردي قصير</small><b>مجاناً</b><small>من يوم لين ١٠ أيام</small></div><div><small>مخيم فردي للموسم</small><b>٣٠٠ ريال</b><small>٣ أشهر</small></div><div><small>مساحة المخيم الفردي</small><b>٢٠٠٠ م²</b><small>كحد أعلى</small></div></div>
<ul><li>تصريح فردي واحد في موقع واحد خلال الموسم.</li>
<li>المخيم يكون بعيد عن بطون الأودية ومجاري السيول، وعن المناطق الحدودية.</li>
<li>يبعد ١٠٠ م على الأقل عن الطرق السريعة وخطوط الضغط العالي ومنشآت الخدمات.</li>
<li>ممنوع في المراعي المنظمة والغابات والمناطق عالية الحساسية البيئية.</li>
<li>تشيل مخيمك خلال ١٠ أيام من انتهاء التصريح.</li></ul></section>

<section class="rs"><h2 id="mamnu">الممنوعات بالبر</h2>
<ul><li>قطع الأشجار والشجيرات، والاحتطاب، وجمع الحطب المحلي أو نقله أو بيعه.</li>
<li>إشعال النار بالحطب أو الفحم المحلي، أو في غير الأماكن المخصصة.</li>
<li>دخول السيارات للروضات والفياض المحمية، والسير فوق النبات.</li>
<li>سياج المخيم بالعقوم الترابية أو الحواجز الحديد أو الشبوك. المسموح شراع ارتفاعه ما يزيد عن ٣ م.</li>
<li>البناء بالإسمنت أو الإسفلت، أو أي شي يسد مجرى السيل.</li>
<li>حفر الآبار، ونثر البذور أو التشجير بدون ترخيص.</li>
<li>تصوير الدرون بدون ترخيص من الجهة المشرفة.</li>
<li>ترك النفايات أو دفنها أو حرقها.</li></ul></section>

<section class="rs"><h2 id="mahmiyat">المحميات الملكية</h2>
<p>في المملكة ٨ محميات ملكية، لكل وحدة هيئة تطوير وضوابط خاصة. أبرز اللي يهم أهل البر:</p>
<ul><li><b>محمية الملك عبدالعزيز الملكية</b> (التنهات والخفس والصمان والدهناء): التنزه في الصمان والدهناء بتصريح مسبق من موقع الهيئة، من ٦ الصباح لين ٦ المساء، والتخييم فيها ممنوع بكل أنواعه. يُستثنى أهالي مركزي المناخ والحيراء.</li>
<li><b>محمية الإمام تركي بن عبدالله الملكية</b>: التخييم في المواقع المخصصة بتصريح من <a href="https://itba.gov.sa/permits/camping-permit" target="_blank" rel="noopener" style="color:var(--terra)">موقع الهيئة ↗</a>، والحطب والفحم ممنوعين فيها حتى المستورد.</li>
<li><b>محمية الإمام عبدالعزيز بن محمد الملكية</b> (روضة خريم وما حولها).</li>
<li><b>محمية الملك سلمان بن عبدالعزيز الملكية</b> (الخنفة والطبيق وحرة الحرة، في الشمال).</li></ul>
<p style="font-size:14px;color:var(--muted)">قبل ما تطلع لأي محمية، شيك على موقع هيئتها لأن الضوابط تتحدث.</p></section>

<section class="rs"><h2 id="fines">الغرامات</h2>
<p style="font-size:14px;color:var(--muted);margin-bottom:8px">بالريال، للمرة الأولى والثانية والثالثة. المصدر: المركز الوطني لتنمية الغطاء النباتي.</p>
<div class="tw"><table><thead><tr><th>المخالفة</th><th>أول مرة</th><th>ثاني مرة</th><th>ثالث مرة</th></tr></thead><tbody>{rows}</tbody></table></div>
<ul style="margin-top:10px"><li>تكرار نفس المخالفة خلال سنة تتضاعف فيه الغرامة.</li>
<li>قطع الأشجار بدون ترخيص يوصل في المحكمة لسجن ١٠ سنوات أو غرامة ٣٠ مليون ريال أو الاثنين.</li></ul></section>

<section class="rs"><h2>المصادر</h2><ul class="srcs">{srcs}</ul>
<p class="srcs">آخر مراجعة: {UPDATED}. هذي الصفحة للتوعية وليست استشارة نظامية.</p></section>'''
    with open(os.path.join(ROOT, "rules.html"), "w", encoding="utf-8") as f:
        f.write(page("أنظمة البر والتخييم وغراماتها | وسمي", "أنظمة البر في السعودية: تصريح التخييم من منصة نباتي ورسومه، ممنوعات الكشتة، ضوابط المحميات الملكية، وغرامات الاحتطاب ودخول الروضات.", "/rules.html", "/rules.html", body, RCSS))

if __name__ == "__main__":
    build_places()
    build_rules()
    print("done")
