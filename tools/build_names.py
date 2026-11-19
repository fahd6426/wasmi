# يبني data/names/*.json (أسماء الجبال والشعبان والقيعان...) من GeoNames (CC-BY 4.0)
# الاستخدام: python3 tools/build_names.py /path/SA.txt
import sys,re,json,os,unicodedata,collections
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAT={'peak':'HLL HLLS MT MTS RDGE SCRP CONE LAVA PK PKS SPUR CLF GAP PASS MESA',
 'wadi':'WAD WADS STM STMI STMS RVN WADJ',
 'water':'WLL WLLS WTRH SPNG PNDI PND RSV LK LKI WLLQ CSTN',
 'place':'PPL PPLL PPLX PPLA PPLA2 PPLA3 PPLC LCTY FRM FRMS OAS',
 'sand':'DUNE SAND ERG DUNS',
 'qa':'DPR SBKH PLN PLAT BSND FLTT GRAZ AREA TRGD'}
FC={c:k for k,v in CAT.items() for c in v.split()}
AR=re.compile('[؀-ۿ]')
WORDS={'wadi':'وادي','wādī':'وادي','jabal':'جبل','jibāl':'جبال','sha‘īb':'شعيب','shi‘āb':'شعاب','nafūd':'نفود','qā‘':'قاع','umm':'أم','abū':'أبو','ab':'أبا','abā':'أبا','bi’r':'بئر',"bi'r":'بئر','biʼr':'بئر','rawḑat':'روضة','rawḑah':'روضة','khashm':'خشم','qārat':'قارة','qārah':'قارة','fayḑat':'فيضة','fayḑah':'فيضة','‘irq':'عرق','nuqrat':'نقرة','dhurā':'ذرى','sabkhat':'سبخة','ḩarrat':'حرة','hijrat':'هجرة','ţawq':'طوق','khabrā’':'خبراء','khabrāʼ':'خبراء','banī':'بني','ibn':'ابن','bin':'بن','ra’s':'رأس','raʼs':'رأس'}
MAP=[('sh','ش'),('kh','خ'),('th','ث'),('dh','ذ'),('gh','غ'),('ḩ','ح'),('ş','ص'),('ḑ','ض'),('ţ','ط'),('z̧','ظ'),('‘','ع'),('’','ء'),('ʼ','ء'),("'",'ء'),('ā','ا'),('ī','ي'),('ū','و'),('aw','و'),('ay','ي'),
 ('b','ب'),('t','ت'),('j','ج'),('d','د'),('r','ر'),('z','ز'),('s','س'),('f','ف'),('q','ق'),('k','ك'),('l','ل'),('m','م'),('n','ن'),('h','ه'),('w','و'),('y','ي'),('g','ج'),('v','ف'),('p','ب'),('c','ك'),('x','كس'),('o','و'),('e','')]
def tw(w):
    lw=w.lower()
    if lw in WORDS:return WORDS[lw]
    pre=''
    m=re.match(r"^(al|an|ar|as|ash|at|ath|ad|adh|az|aş|aţ|aḑ|az̧|al‘)[- ]?(.+)$",lw)
    o='';i=0;s=re.sub(r'([bcdfgjklmnpqrstvwyzḩşḑţ])\1',r'\1',lw)
    if s.startswith('a') and not s.startswith(('ā','aw','ay')) : o='ا';i=1
    elif s.startswith(('i','u')):o='ا';i=1
    while i<len(s):
        for a,b in MAP:
            if s.startswith(a,i):o+=b;i+=len(a);break
        else:i+=1          # a/i/u القصيرة تنحذف
    if lw.endswith('ya') or lw.endswith('yah'):o=re.sub('يي?ه?$','ي',o)+'ة'
    elif lw.endswith('ah'):o=o[:-1]+'ة'
    elif lw.endswith('at') and len(lw)>4 and o.endswith('ت'):o=o[:-1]+'ة'
    return o
def tr(name):
    name=name.replace('-',' ').replace('‐',' ')
    toks=name.split();out=[];k=0
    while k<len(toks):
        t=toks[k];lt=t.lower()
        if lt in('al','an','ar','as','ash','at','ath','ad','adh','az','aş','aţ','aḑ','az̧','al‘') and k+1<len(toks):
            out.append('ال'+tw(toks[k+1]));k+=2;continue
        out.append(tw(t));k+=1
    return ' '.join(x for x in out if x)
def clean(a):
    a=re.sub('[ً-ْـ]','',a).strip()   # بدون تشكيل
    return a
src=sys.argv[1];cells=collections.defaultdict(list);n=na=0
for l in open(src,encoding='utf-8'):
    f=l.rstrip('\n').split('\t')
    c=FC.get(f[7])
    if not c:continue
    lat,lon=float(f[4]),float(f[5])
    ar=[clean(x) for x in f[3].split(',') if AR.search(x)]
    ar=[x for x in ar if 1<len(x)<40]
    if ar:nm=min(ar,key=lambda x:(x.count(' ')>3,len(x)));na+=1
    else:nm=tr(f[1])
    if not nm:continue
    n+=1
    cells[f'{int(lat//1)}_{int(lon//1)}'].append([round(lat,4),round(lon,4),nm,c])
d=os.path.join(R,'data','names');os.makedirs(d,exist_ok=True)
for fn in os.listdir(d):os.remove(os.path.join(d,fn))
for k,v in cells.items():json.dump(v,open(os.path.join(d,k+'.json'),'w'),ensure_ascii=False,separators=(',',':'))
# فهرس البحث: كل الأسماء بملف واحد (يتحمّل أول ما تبحث)
idx=[[x[2],x[0],x[1],x[3]] for v in cells.values() for x in v]
json.dump(idx,open(os.path.join(R,'data','names-index.json'),'w'),ensure_ascii=False,separators=(',',':'))
print('names',n,'arabic-native',na,'cells',len(cells))
