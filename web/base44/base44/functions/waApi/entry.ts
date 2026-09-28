// WhatsApp for Eran's CRM, through Green API. Admin only (called from /crm with the logged-in user).
// Secrets: GREEN_API_URL, GREEN_API_INSTANCE, GREEN_API_TOKEN (set in the app, never in the code).
// The instance's webhook belongs to another system of Eran's, so we never touch settings or the
// notification queue: replies are read from the chat history instead.
import { createClientFromRequest } from "npm:@base44/sdk";

const env = (k: string) => Deno.env.get(k) || "";
const api = (method: string) =>
  `${env("GREEN_API_URL")}/waInstance${env("GREEN_API_INSTANCE")}/${method}/${env("GREEN_API_TOKEN")}`;
const digits = (n: string) => (n || "").replace(/\D/g, "");
const chatId = (num: string) => `${digits(num)}@c.us`;

// "Do not send" list (entity DoNotSend, one row per number). Every send checks it first: a number is blocked if it is
// on the list, or if any lead with that number has the status "do_not_send". Leaving the list only happens through
// action "unblock" (the list panel in /crm); changing a lead's status back does not unblock the number.
async function isBlocked(base44: any, num: string): Promise<boolean> {
  const d = digits(num);
  if (!d) return true;
  const list: any[] = await base44.asServiceRole.entities.DoNotSend.list("-created_date", 2000);
  if (list.some((x) => digits(x.phone) === d)) return true;
  const leads: any[] = await base44.asServiceRole.entities.LeadCRM.list("sort_order", 1000);
  return leads.some((l) => l.status === "do_not_send" && digits(l.whatsapp) === d);
}

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

async function green(method: string, body?: unknown) {
  const r = await fetch(api(method), body === undefined ? {} : {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body),
  });
  const text = await r.text();
  if (!r.ok) throw new Error(`Green API ${method} ${r.status}: ${text.slice(0, 200)}`);
  return text ? JSON.parse(text) : null;
}

export default async function (req: Request): Promise<Response> {
  try {
    const base44 = createClientFromRequest(req);
    const user = await base44.auth.me();
    if (!user || user.role !== "admin") return Response.json({ error: "Unauthorized" }, { status: 401 });
    const { action, id, which, text, limit, force } = await req.json();
    const db = base44.asServiceRole.entities.LeadCRM;

    if (action === "state") return Response.json(await green("getStateInstance"));
    if (action === "unblock") {   // id here is the DoNotSend row
      await base44.asServiceRole.entities.DoNotSend.delete(id);
      return Response.json({ ok: true });
    }

    const lead = id ? await db.get(id) : null;
    if (!lead) return Response.json({ error: "lead not found" }, { status: 404 });

    if (action === "history") {
      const h = await green("getChatHistory", { chatId: chatId(lead.whatsapp), count: limit || 40 });
      const msgs = (h || []).filter((m: any) => m.textMessage || m.extendedTextMessage || m.caption || m.typeMessage === "imageMessage")
        .map((m: any) => ({
          id: m.idMessage, out: m.type === "outgoing", at: m.timestamp * 1000,
          text: m.textMessage || m.extendedTextMessage?.text || m.caption || "",
          image: m.typeMessage === "imageMessage" ? (m.downloadUrl || m.jpegThumbnail && `data:image/jpeg;base64,${m.jpegThumbnail}` || null) : null,
          status: m.statusMessage || null,
        })).sort((a: any, b: any) => a.at - b.at);
      if (lead.unread) await db.update(id, { unread: false });
      return Response.json({ messages: msgs });
    }

    if (action === "block") {   // status "do_not_send" + the number on the list + no scheduled messages
      const dns = base44.asServiceRole.entities.DoNotSend;
      const d = digits(lead.whatsapp);
      const exists = (await dns.list("-created_date", 2000)).some((x: any) => digits(x.phone) === d);
      if (d && !exists) await dns.create({ phone: d, business_name: lead.business_name, lead_id: lead.lead_id || lead.id,
        reason: text || "", added_at: new Date().toISOString() });
      const patch = { status: "do_not_send", msg1_at: null, msg2_at: null, send_error: "" };
      await db.update(id, patch);
      return Response.json({ ok: true, patch });
    }

    if (action === "send") {
      if (await isBlocked(base44, lead.whatsapp)) {
        const patch = { msg1_at: null, msg2_at: null, send_error: "לא נשלח: המספר ברשימת לא לשלוח" };
        await db.update(id, patch);
        return Response.json({ error: "המספר ברשימת לא לשלוח. ההודעה לא נשלחה.", patch }, { status: 403 });
      }
      // which: 1 = first message, 2 = second message, "text" = a free reply typed in the chat window
      // outside the sending hours a manual send needs an explicit ok from the screen (force)
      if (!force) {
        const nxt = nextAllowed(new Date(), await loadWindow(base44));
        if (!nxt || nxt.getTime() > Date.now() + 1000) {
          return Response.json({ error: "outside_hours", next: nxt ? nxt.toISOString() : null }, { status: 409 });
        }
      }
      const body = which === 1 ? lead.message : which === 2 ? lead.message2 : text;
      if (!body || !body.trim()) return Response.json({ error: "empty message" }, { status: 400 });
      const res = await green("sendMessage", { chatId: chatId(lead.whatsapp), message: body });
      // message 1 continues with the image (4 screens of their page) and its caption: a second bubble right after
      if (which === 1 && lead.msg1_image) {
        await green("sendFileByUrl", { chatId: chatId(lead.whatsapp), urlFile: lead.msg1_image,
          fileName: "report.jpg", caption: lead.msg1_caption || "" });
      }
      const now = new Date().toISOString();
      const patch: Record<string, unknown> = { send_error: "", last_contact_date: now.slice(0, 10) };
      if (which === 1) Object.assign(patch, { msg1_sent_at: now, msg1_at: null });
      if (which === 2) Object.assign(patch, { msg2_sent_at: now, msg2_at: null });
      if (which === 1 && ["new", "ready"].includes(lead.status || "new")) patch.status = "sent";
      await db.update(id, patch);
      return Response.json({ ok: true, idMessage: res?.idMessage, patch });
    }
    return Response.json({ error: "unknown action" }, { status: 400 });
  } catch (e) {
    return Response.json({ error: String((e as Error).message || e) }, { status: 500 });
  }
}
