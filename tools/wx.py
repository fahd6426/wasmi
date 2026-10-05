"""Builds outing forecasts (wind, gusts, temperature, rain, best time of day) for the Wasmi grid from MET Norway."""
import concurrent.futures as cf
import datetime as dt
import json
import math
import os
import time

import requests

UA = "wasmi-weather/1.0 https://fahd6426.github.io/wasmi/"
API = "https://api.met.no/weatherapi/locationforecast/2.0/complete"
STEP = 0.25
OUT = "data/wx"
RIYADH = dt.timezone(dt.timedelta(hours=3))
POLY = [[38.13,24.0],[51.0,24.0],[50.8,24.75],[50.2,25.7],[50.15,26.4],[49.7,27.0],[49.0,27.6],[48.6,28.1],[48.43,28.54],[47.67,28.53],[46.55,29.1],[44.7,29.2],[42.08,31.1],[40.4,31.95],[39.2,32.16],[37.0,31.5],[38.0,30.5],[37.67,30.34],[36.76,29.87],[36.5,29.5],[36.07,29.19],[34.96,29.36],[34.75,28.4],[34.6,28.05],[35.69,27.35],[36.45,26.24],[37.27,25.05],[37.45,24.8],[38.06,24.09]]
# time-of-day slots (Riyadh local hours)
SLOTS = [("sabah", range(6, 11)), ("dhuhr", range(11, 15)), ("asr", range(15, 18)), ("maghrib", range(18, 20)), ("layl", range(20, 24))]


def inside(x, y):
    c = False
    j = len(POLY) - 1
    for i in range(len(POLY)):
        xi, yi = POLY[i]
        xj, yj = POLY[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            c = not c
        j = i
    return c


def grid():
    pts = []
    lat = 24.0
    while lat <= 32.3:
        lon = 34.5
        while lon <= 51.0:
            if inside(lon, lat):
                pts.append((round(lat, 2), round(lon, 2)))
            lon += STEP
        lat += STEP
    return pts


def fetch(pt, session):
    for attempt in range(4):
        try:
            r = session.get(API, params={"lat": pt[0], "lon": pt[1]}, timeout=40)
            if r.status_code == 200:
                return pt, r.json()
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(3 * (attempt + 1))
                continue
            return pt, None
        except requests.RequestException:
            time.sleep(3 * (attempt + 1))
    return pt, None


def slot_score(w, g, t, r):
    s = 10
    if w >= 50: s -= 7
    elif w >= 38: s -= 5
    elif w >= 25: s -= 3
    elif w >= 15: s -= 1
    if g is not None and g >= 55: s -= 2
    if r >= 2: s -= 4
    elif r >= 0.3: s -= 2
    if t is not None:
        if t >= 40: s -= 5
        elif t >= 36: s -= 3
        elif t >= 33: s -= 1
        if t <= 5: s -= 3
        elif t <= 10: s -= 1
    return max(0, min(10, s))


def summarize(js):
    ts = js["properties"]["timeseries"]
    hours = {}
    for e in ts:
        t = dt.datetime.fromisoformat(e["time"].replace("Z", "+00:00")).astimezone(RIYADH)
        d = e["data"]
        inst = d["instant"]["details"]
        nxt = d.get("next_1_hours") or d.get("next_6_hours") or {}
        span = 1 if d.get("next_1_hours") else 6
        rain = (nxt.get("details") or {}).get("precipitation_amount", 0.0) or 0.0
        hours[t] = {
            "w": (inst.get("wind_speed") or 0) * 3.6,
            "g": (inst.get("wind_speed_of_gust") or 0) * 3.6 or None,
            "dir": inst.get("wind_from_direction"),
            "t": inst.get("air_temperature"),
            "r": rain / span,
            "c": inst.get("cloud_area_fraction"),
        }
    today = dt.datetime.now(RIYADH).date()
    days = []
    for k in range(7):
        day = today + dt.timedelta(days=k)
        slots = {}
        for name, hrs in SLOTS:
            vals = [v for t, v in hours.items() if t.date() == day and t.hour in hrs]
            if not vals:
                continue
            w = sum(v["w"] for v in vals) / len(vals)
            gs = [v["g"] for v in vals if v["g"]]
            g = max(gs) if gs else None
            temps = [v["t"] for v in vals if v["t"] is not None]
            t = sum(temps) / len(temps) if temps else None
            r = sum(v["r"] for v in vals) * (len(hrs) / len(vals))
            dirs = [v["dir"] for v in vals if v["dir"] is not None]
            if dirs:
                sx = sum(math.sin(math.radians(a)) for a in dirs); cy = sum(math.cos(math.radians(a)) for a in dirs)
                dr = round(math.degrees(math.atan2(sx, cy)) % 360)
            else:
                dr = None
            slots[name] = [round(w), round(g) if g else None, dr, round(t, 1) if t is not None else None, round(r, 1), slot_score(w, g, t, r)]
        night = [v["t"] for t, v in hours.items() if v["t"] is not None and ((t.date() == day and t.hour >= 20) or (t.date() == day + dt.timedelta(days=1) and t.hour <= 6))]
        if not slots:
            continue
        best = max(slots.items(), key=lambda kv: kv[1][5])
        days.append({"d": day.isoformat(), "s": slots, "best": best[0], "score": best[1][5], "night": round(min(night), 1) if night else None})
    return days


def main():
    pts = grid()
    print(f"Grid points: {len(pts)}", flush=True)
    session = requests.Session()
    session.headers["User-Agent"] = UA
    tiles, ok = {}, 0
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        for pt, js in ex.map(lambda p: fetch(p, session), pts):
            if not js:
                continue
            try:
                days = summarize(js)
            except Exception as e:
                print("parse error", pt, e, flush=True)
                continue
            ok += 1
            key = f"{math.floor(pt[0])}_{math.floor(pt[1])}"
            tiles.setdefault(key, []).append({"la": pt[0], "lo": pt[1], "days": days})
    updated = dt.datetime.now(RIYADH).isoformat(timespec="minutes")
    os.makedirs(OUT, exist_ok=True)
    for key, points in tiles.items():
        with open(f"{OUT}/{key}.json", "w") as f:
            json.dump({"updated": updated, "step": STEP, "points": points}, f, ensure_ascii=False, separators=(",", ":"))
    json.dump({"updated": updated, "tiles": sorted(tiles), "points": ok}, open(f"{OUT}/index.json", "w"))
    print(f"DONE points ok={ok}/{len(pts)} tiles={len(tiles)}", flush=True)
    if ok < len(pts) * 0.8:
        raise SystemExit("too many failures")


if __name__ == "__main__":
    main()
