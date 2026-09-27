// Runs every 10 minutes, 08:00-21:50 Israel time (workflow "WhatsApp tick", ~0.2 credits a run). Two jobs:
//  1. send the scheduled messages that are due: at most ONE per run, so even a backlog goes out spaced;
//     a message more than 6 hours late is not sent (flagged instead), so nothing leaves in the middle of the night
//  2. read the last incoming messages and mark the leads that replied (unread + status "replied")
// The workflow passes {"key": TICK_KEY} in `with.args`; anything else is refused.
import { createClientFromRequest } from "npm:@base44/sdk";

const env = (k: string) => Deno.env.get(k) || "";
const api = (method: string, q = "") =>
  `${env("GREEN_API_URL")}/waInstance${env("GREEN_API_INSTANCE")}/${method}/${env("GREEN_API_TOKEN")}${q}`;
const digits = (n: string) => (n || "").replace(/\D/g, "");
const LATE_MS = 6 * 3600 * 1000;

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

    // 1. due messages
    const due: { lead: any; which: 1 | 2; at: number }[] = [];
    for (const l of leads) {
      if (l.msg1_at && !l.msg1_sent_at) due.push({ lead: l, which: 1, at: Date.parse(l.msg1_at) });
      if (l.msg2_at && !l.msg2_sent_at) due.push({ lead: l, which: 2, at: Date.parse(l.msg2_at) });
    }
    const ready = due.filter((d) => d.at <= now).sort((a, b) => a.at - b.at);
    for (const d of ready) {
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
