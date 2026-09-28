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
    const { action, id, which, text, limit } = await req.json();
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
