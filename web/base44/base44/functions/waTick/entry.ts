// Runs every 10 minutes, 08:00-21:50 Israel time (workflow "WhatsApp tick", ~0.2 credits a run). Two jobs:
//  1. send the scheduled messages that are due, only inside the sending hours set in /crm (entity SendSettings;
//     default Sunday to Thursday 09:00-17:00) and never on Shabbat: at most ONE per run, so even a backlog goes out spaced;
//     a message that comes due outside the hours is moved to the start of the next allowed window (keeping its order);
//     a message more than 6 hours late is not sent (flagged instead), so nothing leaves in the middle of the night
//  2. read the last incoming messages and mark the leads that replied (unread + status "replied")
// The workflow passes {"key": TICK_KEY} in `with.args`; anything else is refused.
import { createClientFromRequest } from "npm:@base44/sdk";

const env = (k: string) => Deno.env.get(k) || "";
const api = (method: string, q = "") =>
  `${env("GREEN_API_URL")}/waInstance${env("GREEN_API_INSTANCE")}/${method}/${env("GREEN_API_TOKEN")}${q}`;
const digits = (n: string) => (n || "").replace(/\D/g, "");
const LATE_MS = 6 * 3600 * 1000;
// Sending hours (entity SendSettings, one row; Israel time). Same logic as src/lib/sendWindow.js in the app (keep in
// sync): allowed weekdays (0 = Sunday) + start and end time; outside it, the next allowed day's start.
const DEFAULT_WINDOW = { days: [0, 1, 2, 3, 4], start: "09:00", end: "17:00" };
const WD = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
function ilParts(date: Date) {
  const p: any = Object.fromEntries(new Intl.DateTimeFormat("en-US", { timeZone: "Asia/Jerusalem", year: "numeric",
    month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", weekday: "short", hourCycle: "h23" })
    .formatToParts(date).map((x) => [x.type, x.value]));
  return { y: +p.year, m: +p.month, d: +p.day, h: +p.hour, min: +p.minute, wd: WD.indexOf(p.weekday) };
}
function ilToDate(y: number, m: number, d: number, h: number, min: number): Date {
  const want = Date.UTC(y, m - 1, d, h, min);
  let t = want;
  for (let i = 0; i < 3; i++) { const p = ilParts(new Date(t)); t -= Date.UTC(p.y, p.m - 1, p.d, p.h, p.min) - want; }
  return new Date(t);
}
function normWindow(w: any) {
  const ok = (s: string) => /^\d{1,2}:\d{2}$/.test(s || "");
  return { days: Array.isArray(w?.days) && w.days.length ? w.days.map(Number) : DEFAULT_WINDOW.days,
    start: ok(w?.start) ? w.start : DEFAULT_WINDOW.start, end: ok(w?.end) ? w.end : DEFAULT_WINDOW.end };
}
function nextAllowed(date: Date, win: any): Date | null {
  const w = normWindow(win);
  const [sh, sm] = w.start.split(":").map(Number);
  const [eh, em] = w.end.split(":").map(Number);
  let t = new Date(date);
  let p = ilParts(t);
  for (let i = 0; i < 15; i++) {
    if (w.days.includes(p.wd)) {
      const s = ilToDate(p.y, p.m, p.d, sh, sm), e = ilToDate(p.y, p.m, p.d, eh, em);
      if (t < s) return s;
      if (t < e) return t;
    }
    const n = new Date(Date.UTC(p.y, p.m - 1, p.d + 1));
    p = { y: n.getUTCFullYear(), m: n.getUTCMonth() + 1, d: n.getUTCDate(), h: 0, min: 0, wd: n.getUTCDay() };
    t = ilToDate(p.y, p.m, p.d, 0, 0);
  }
  return null;
}
async function loadWindow(base44: any) {
  try { const rows: any[] = await base44.asServiceRole.entities.SendSettings.list("-updated_date", 1); return normWindow(rows[0]); }
  catch { return normWindow(null); }
}


// no sending on Shabbat: from Friday 14:00 to Saturday night (Israel time). Replies are still read.
function isShabbat(d = new Date()): boolean {
  const p = Object.fromEntries(new Intl.DateTimeFormat("en-US", { timeZone: "Asia/Jerusalem", weekday: "short",
    hour: "numeric", hourCycle: "h23" }).formatToParts(d).map((x) => [x.type, x.value]));
  return p.weekday === "Sat" || (p.weekday === "Fri" && Number(p.hour) >= 14);
}

export default async function (req: Request): Promise<Response> {
  try {
    let body: any = {};
    try { body = await req.json(); } catch { /* no body */ }
    // the workflow wraps its payload (args / payload / input...), so look for "key" a few levels down
    const findKey = (o: any, d = 0): string | undefined => (!o || typeof o !== "object" || d > 3) ? undefined
      : typeof o.key === "string" ? o.key : Object.values(o).map((v) => findKey(v, d + 1)).find(Boolean);
    const key = findKey(body) || new URL(req.url).searchParams.get("key");
    if (!env("TICK_KEY") || key !== env("TICK_KEY")) return Response.json({ error: "forbidden" }, { status: 403 });

    if (body?.dry) {  // health check: secrets readable, Green API reachable; nothing is sent or written
      const st = await fetch(api("getStateInstance"));
      return Response.json({ ok: st.ok, state: st.ok ? await st.json() : st.status });
    }
    const base44 = createClientFromRequest(req);
    const db = base44.asServiceRole.entities.LeadCRM;
    const leads: any[] = await db.list("sort_order", 500);
    const now = Date.now();
    const log: string[] = [];

    // "do not send": numbers on the DoNotSend list, plus any lead set to "do_not_send" (added to the list here, so the
    // number stays blocked even if the status is changed later). Checked before every send.
    const dnsDb = base44.asServiceRole.entities.DoNotSend;
    const dnsList: any[] = await dnsDb.list("-created_date", 2000);
    const blocked = new Set(dnsList.map((x) => digits(x.phone)).filter(Boolean));
    for (const l of leads) {
      const d = digits(l.whatsapp);
      if (l.status !== "do_not_send" || !d || blocked.has(d)) continue;
      await dnsDb.create({ phone: d, business_name: l.business_name, lead_id: l.lead_id || l.id, reason: "",
        added_at: new Date().toISOString() });
      blocked.add(d);
      log.push(`listed ${l.business_name}`);
    }

    // 1. due messages
    const due: { lead: any; which: 1 | 2; at: number }[] = [];
    for (const l of leads) {
      if (l.msg1_at && !l.msg1_sent_at) due.push({ lead: l, which: 1, at: Date.parse(l.msg1_at) });
      if (l.msg2_at && !l.msg2_sent_at) due.push({ lead: l, which: 2, at: Date.parse(l.msg2_at) });
    }
    const win = await loadWindow(base44);
    const next = nextAllowed(new Date(now), win);
    const open = !isShabbat() && !!next && next.getTime() === now;
    const overdue = due.filter((d) => d.at <= now).sort((a, b) => a.at - b.at);
    if (!open) {
      // outside the sending hours: push what is already due to the next window, one minute apart, same order
      const base = next && !isShabbat() ? next.getTime() : (nextAllowed(new Date(now + 36 * 3600 * 1000), win)?.getTime() ?? 0);
      for (const [i, d] of overdue.entries()) {
        if (!base) break;
        const at = new Date(base + i * 60 * 1000).toISOString();
        await db.update(d.lead.id, { [`msg${d.which}_at`]: at });
        log.push(`moved ${d.lead.business_name} #${d.which} to ${at}`);
      }
      if (!overdue.length) log.push("outside sending hours");
    }
    const ready = open ? overdue : [];
    for (const d of ready) {
      if (!digits(d.lead.whatsapp) || blocked.has(digits(d.lead.whatsapp))) {
        await db.update(d.lead.id, { msg1_at: null, msg2_at: null, send_error: "לא נשלח: המספר ברשימת לא לשלוח" });
        log.push(`blocked ${d.lead.business_name} #${d.which}`);
        continue;
      }
      if (now - d.at > LATE_MS) {
        await db.update(d.lead.id, { [`msg${d.which}_at`]: null, send_error: `הודעה ${d.which} לא נשלחה: התזמון עבר לפני יותר משש שעות` });
        log.push(`late ${d.lead.business_name} #${d.which}`);
        continue;
      }
      const text = d.which === 1 ? d.lead.message : d.lead.message2;
      const r = await fetch(api("sendMessage"), {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ chatId: `${digits(d.lead.whatsapp)}@c.us`, message: text }),
      });
      if (r.ok && d.which === 1 && d.lead.msg1_image) {   // then the image with its caption, as the next bubble
        await fetch(api("sendFileByUrl"), {
          method: "POST", headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ chatId: `${digits(d.lead.whatsapp)}@c.us`, urlFile: d.lead.msg1_image,
            fileName: "report.jpg", caption: d.lead.msg1_caption || "" }),
        });
      }
      const iso = new Date().toISOString();
      if (r.ok) {
        const patch: Record<string, unknown> = { [`msg${d.which}_sent_at`]: iso, [`msg${d.which}_at`]: null,
          send_error: "", last_contact_date: iso.slice(0, 10) };
        if (d.which === 1 && ["new", "ready"].includes(d.lead.status || "new")) patch.status = "sent";
        await db.update(d.lead.id, patch);
        log.push(`sent ${d.lead.business_name} #${d.which}`);
      } else {
        await db.update(d.lead.id, { send_error: `שליחה נכשלה (${r.status})` });
        log.push(`fail ${d.lead.business_name} #${d.which} ${r.status}`);
      }
      break; // one message per run
    }

    // 2. replies
    // 12 hours back, so the first run of the morning also catches the replies that came in overnight;
    // last_reply_at makes it idempotent
    const r = await fetch(api("lastIncomingMessages", "?minutes=720"));
    const incoming: any[] = r.ok ? await r.json() : [];
    const byNum = new Map(leads.filter((l) => l.msg1_sent_at || l.msg2_sent_at).map((l) => [digits(l.whatsapp), l]));
    for (const m of incoming) {
      const l = byNum.get(digits((m.chatId || "").split("@")[0]));
      if (!l) continue;
      const at = new Date((m.timestamp || 0) * 1000).toISOString();
      if (l.last_reply_at && at <= l.last_reply_at) continue;
      const text = m.textMessage || m.extendedTextMessage?.text || m.caption || `[${m.typeMessage || "הודעה"}]`;
      const patch: Record<string, unknown> = { last_reply_at: at, last_reply_text: String(text).slice(0, 500), unread: true };
      if ((l.status || "new") === "sent") patch.status = "replied";
      await db.update(l.id, patch);
      l.last_reply_at = at;
      log.push(`reply ${l.business_name}`);
    }
    return Response.json({ ok: true, due: ready.length, log });
  } catch (e) {
    return Response.json({ error: String((e as Error).message || e) }, { status: 500 });
  }
}
