// Sending hours for WhatsApp outreach (Israel time). Same logic as in base44/functions/waTick and waApi (keep in sync).
// A window = allowed weekdays (0 = Sunday ... 6 = Saturday) + a start and an end time. Anything outside it moves to the
// start of the next allowed day, skipping the days that are off (by default Friday and Saturday).
export const TZ = 'Asia/Jerusalem';
export const DEFAULT_WINDOW = { days: [0, 1, 2, 3, 4], start: '09:00', end: '17:00' };
export const DAY_NAMES = ['ראשון', 'שני', 'שלישי', 'רביעי', 'חמישי', 'שישי', 'שבת'];
const WD = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

export function ilParts(date) {
  const p = Object.fromEntries(new Intl.DateTimeFormat('en-US', { timeZone: TZ, year: 'numeric', month: '2-digit',
    day: '2-digit', hour: '2-digit', minute: '2-digit', weekday: 'short', hourCycle: 'h23' })
    .formatToParts(date).map((x) => [x.type, x.value]));
  return { y: +p.year, m: +p.month, d: +p.day, h: +p.hour, min: +p.minute, wd: WD.indexOf(p.weekday) };
}

// the UTC instant of an Israel wall-clock time
export function ilToDate(y, m, d, h, min) {
  const want = Date.UTC(y, m - 1, d, h, min);
  let t = want;
  for (let i = 0; i < 3; i++) {
    const p = ilParts(new Date(t));
    t -= Date.UTC(p.y, p.m - 1, p.d, p.h, p.min) - want;
  }
  return new Date(t);
}

export function normWindow(w) {
  const days = Array.isArray(w?.days) && w.days.length ? w.days.map(Number) : DEFAULT_WINDOW.days;
  const ok = (s) => /^\d{1,2}:\d{2}$/.test(s || '');
  return { days, start: ok(w?.start) ? w.start : DEFAULT_WINDOW.start, end: ok(w?.end) ? w.end : DEFAULT_WINDOW.end };
}

// the first moment at or after `date` that is inside the window (null if the window has no days)
export function nextAllowed(date, win) {
  const w = normWindow(win);
  const [sh, sm] = w.start.split(':').map(Number);
  const [eh, em] = w.end.split(':').map(Number);
  let t = new Date(date);
  let p = ilParts(t);
  for (let i = 0; i < 15; i++) {
    if (w.days.includes(p.wd)) {
      const s = ilToDate(p.y, p.m, p.d, sh, sm);
      const e = ilToDate(p.y, p.m, p.d, eh, em);
      if (t < s) return s;
      if (t < e) return t;
    }
    const n = new Date(Date.UTC(p.y, p.m - 1, p.d + 1));   // next calendar day in Israel
    p = { y: n.getUTCFullYear(), m: n.getUTCMonth() + 1, d: n.getUTCDate(), wd: n.getUTCDay() };
    t = ilToDate(p.y, p.m, p.d, 0, 0);
  }
  return null;
}

export const isAllowed = (date, win) => { const n = nextAllowed(date, win); return !!n && n.getTime() === new Date(date).getTime(); };

export function describeWindow(win) {
  const w = normWindow(win);
  const days = [...w.days].sort((a, b) => a - b).map((d) => DAY_NAMES[d]).join(', ');
  return `${days}, ${w.start} עד ${w.end}`;
}
