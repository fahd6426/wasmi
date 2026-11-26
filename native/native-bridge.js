/* جسر تطبيق وسمي: يشتغل داخل التطبيق بس (Capacitor)، وبالموقع العادي ما يسوي شي */
(function () {
  var C = window.Capacitor;
  if (!C || !C.isNativePlatform || !C.isNativePlatform()) return;
  document.documentElement.classList.add('in-app');
  var st = document.createElement('style');
  st.textContent = '.in-app .leaflet-container{background:#cdb68b}'; // بدون نت: خلفية رملية بدل الأبيض
  document.head.appendChild(st);
  var P = C.Plugins || {};

  /* ١) البيانات: لو فيه نت نجيب أحدث نسخة من الموقع، وإلا نستخدم النسخة اللي داخل التطبيق */
  var of = window.fetch.bind(window);
  window.fetch = function (u, o) {
    if (typeof u === 'string' && /^\/data\//.test(u) && navigator.onLine) {
      return of('https://wasmii.com' + u, o).then(function (r) { if (!r.ok) throw 0; return r; }).catch(function () { return of(u, o); });
    }
    return of(u, o);
  };

  /* ٢) الموقع: دقيق، ويكمّل يسجّل الجرة والشاشة مقفلة */
  var geo = navigator.geolocation, BG = P.BackgroundGeolocation, G = P.Geolocation;
  function errOf(e) { var m = (e && e.message) || ''; return { code: (e && e.code === 'NOT_AUTHORIZED') || /denied|permission|authori/i.test(m) ? 1 : 2, message: m }; }
  if (geo && BG) {
    var ws = {}, n = 0;
    geo.watchPosition = function (ok, err) {
      var id = ++n;
      BG.addWatcher({
        backgroundTitle: 'قارمن وسمي شغال',
        backgroundMessage: 'يسجّل جرتك ويوجّهك وأنت بالبر',
        requestPermissions: true, stale: false, distanceFilter: 3
      }, function (l, e) {
        if (e) { if (err) err(errOf(e)); return; }
        if (!l) return;
        ok({ coords: { latitude: l.latitude, longitude: l.longitude, accuracy: l.accuracy, altitude: l.altitude, altitudeAccuracy: l.altitudeAccuracy, heading: l.bearing, speed: l.speed }, timestamp: l.time || Date.now() });
      }).then(function (wid) { if (ws[id] === 'x') BG.removeWatcher({ id: wid }); else ws[id] = wid; });
      return id;
    };
    geo.clearWatch = function (id) { if (ws[id] && ws[id] !== 'x') BG.removeWatcher({ id: ws[id] }); ws[id] = 'x'; };
  }
  if (geo && G) {
    geo.getCurrentPosition = function (ok, err, opt) {
      G.getCurrentPosition({ enableHighAccuracy: true, timeout: (opt && opt.timeout) || 20000, maximumAge: (opt && opt.maximumAge) || 0 })
        .then(function (p) { ok({ coords: p.coords, timestamp: p.timestamp }); })
        .catch(function (e) { if (err) err(errOf(e)); });
    };
  }

  /* ٣) الإشعارات: دخول مواسم البر + تذكير «نسبة الربيع تحدّثت» (الإثنين والخميس) */
  var LN = P.LocalNotifications;
  function scheduleAll() {
    if (!LN) return;
    LN.requestPermissions().then(function (r) {
      if (r.display !== 'granted') return;
      return fetch('/seasons-data.js').then(function (x) { return x.text(); }).then(function (t) {
        var S = new Function(t + ';return S')(), now = new Date(), list = [];
        S.forEach(function (s, i) {
          var d = new Date(now.getFullYear(), s.m - 1, s.d, 9, 0, 0);
          if (d <= now) d = new Date(now.getFullYear() + 1, s.m - 1, s.d, 9, 0, 0);
          list.push({ id: 100 + i, title: 'دخل ' + s.n + ' 🌿', body: (s.b || s.h || '').slice(0, 140), schedule: { at: d, allowWhileIdle: true }, extra: { url: '/seasons.html' } });
        });
        [[2, 900], [5, 901]].forEach(function (w) {
          list.push({ id: w[1], title: 'نسبة الربيع تحدّثت 🌱', body: 'شيك على أرضك وقارنها بالأسبوع اللي فات', schedule: { on: { weekday: w[0], hour: 18, minute: 30 }, allowWhileIdle: true }, extra: { url: '/green.html' } });
        });
        return LN.getPending().then(function (p) {
          var old = (p.notifications || []).map(function (x) { return { id: x.id }; });
          return (old.length ? LN.cancel({ notifications: old }) : Promise.resolve()).then(function () { return LN.schedule({ notifications: list }); });
        });
      });
    }).catch(function () {});
  }
  if (LN) {
    LN.addListener('localNotificationActionPerformed', function (e) {
      var u = e && e.notification && e.notification.extra && e.notification.extra.url;
      if (u) location.href = u;
    });
    var last = 0; try { last = +localStorage.getItem('w_ln') || 0; } catch (e) {}
    if (Date.now() - last > 3 * 864e5) { setTimeout(scheduleAll, 4000); try { localStorage.setItem('w_ln', Date.now()); } catch (e) {} }
  }

  /* ٤) روابط wasmii:// تفتح الصفحة داخل التطبيق */
  if (P.App) P.App.addListener('appUrlOpen', function (e) {
    var m = /^wasmii:\/\/(.*)$/.exec((e && e.url) || '') || /^https:\/\/(?:www\.)?wasmii\.com(\/.*)$/.exec((e && e.url) || '');
    if (m) { var p = m[1]; if (p.charAt(0) !== '/') p = '/' + p; location.href = p; }
  });

  /* بدون نت: تنبيه صغير */
  function net() {
    var b = document.getElementById('w-off');
    if (!navigator.onLine) {
      if (!b) { b = document.createElement('div'); b.id = 'w-off'; b.textContent = 'بدون نت · الطريق والجرة والأسماء شغالة'; b.style.cssText = 'position:fixed;left:50%;transform:translateX(-50%);top:calc(env(safe-area-inset-top) + 58px);z-index:99999;background:rgba(26,13,6,.92);color:#FAF3E6;font:700 13px Tajawal,system-ui,sans-serif;padding:7px 14px;border-radius:20px;border:1px solid rgba(201,143,62,.5);pointer-events:none'; document.body && document.body.appendChild(b); }
    } else if (b) b.remove();
  }
  window.addEventListener('online', net); window.addEventListener('offline', net);
  document.addEventListener('DOMContentLoaded', net);
})();
