// ينسخ ملفات موقع وسمي داخل www (يشتغل بدون نت) ويضيف جسر الجوال لكل صفحة
const fs = require('fs'), path = require('path');
const SRC = path.resolve(__dirname, '..'), OUT = path.join(__dirname, 'www');
const SKIP = new Set(['native', '.git', '.github', 'tools', 'README.md', 'CNAME', 'node_modules']);
fs.rmSync(OUT, { recursive: true, force: true });
function copy(s, d) {
  const st = fs.statSync(s);
  if (st.isDirectory()) { fs.mkdirSync(d, { recursive: true }); for (const f of fs.readdirSync(s)) if (!SKIP.has(f)) copy(path.join(s, f), path.join(d, f)); }
  else fs.copyFileSync(s, d);
}
copy(SRC, OUT);
fs.copyFileSync(path.join(__dirname, 'native-bridge.js'), path.join(OUT, 'native-bridge.js'));
let n = 0;
(function inject(d) {
  for (const f of fs.readdirSync(d)) {
    const p = path.join(d, f);
    if (fs.statSync(p).isDirectory()) inject(p);
    else if (f.endsWith('.html')) {
      let h = fs.readFileSync(p, 'utf8');
      if (!h.includes('native-bridge.js')) { h = h.replace(/<head([^>]*)>/i, '<head$1><script src="/native-bridge.js"></script>'); fs.writeFileSync(p, h); n++; }
    }
  }
})(OUT);
// وضع الجولة (للتصوير الآلي بالمحاكي بس): ينقّل بين الصفحات لحاله
if (process.env.TOUR === '1') {
  const T = '<script>window.__TOUR=1;(function(){var s=sessionStorage,st=+(s.getItem("tour")||0),seq=["/garmin.html","/green.html","/garmin.html#to=26.6125,42.1975&n="+encodeURIComponent("بقعة الربيع")];if(st<seq.length)setTimeout(function(){s.setItem("tour",st+1);location.href=seq[st]},14000)})()</script>';
  for (const f of ['index.html', 'garmin.html', 'green.html']) { const p = path.join(OUT, f); fs.writeFileSync(p, fs.readFileSync(p, 'utf8').replace(/<head([^>]*)>/i, '<head$1>' + T)); }
  console.log('وضع الجولة شغال');
}
console.log('www جاهز، الصفحات:', n);
