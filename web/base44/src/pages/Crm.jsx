import React, { useEffect, useMemo, useRef, useState } from 'react';
import { base44 } from '@/api/base44Client';
import { useAuth } from '@/lib/AuthContext';

// Eran's private outreach CRM. Behind Base44 login + admin role; the LeadCRM entity has
// admin-only RLS, so nobody else can read the rows even through the API.
// WhatsApp goes through Green API in the backend function `waApi` (send, chat history); the
// workflow "WhatsApp tick" runs `waTick` every 10 minutes, 08:00-21:50 Israel time: it sends what is
// scheduled (one message per run) and marks the leads that replied.
const STATUSES = [
  { id: 'research', label: 'מחקר מוכן', color: '#6f8a8a', track: 'wa' },
  { id: 'new', label: 'חדש', color: '#8a8177', track: 'page' },
  { id: 'ready', label: 'מוכן לשליחה', color: '#1f7a4a' },
  { id: 'sent', label: 'נשלח', color: '#b08a4a' },
  { id: 'replied', label: 'נענה', color: '#3f6fb0' },
  { id: 'build', label: 'להכין עמוד', color: '#c26a2e', track: 'wa' },
  { id: 'page_ready', label: 'עמוד מוכן', color: '#2f7f8a', track: 'wa' },
  { id: 'meeting', label: 'נקבעה פגישה', color: '#7a4fb0' },
  { id: 'won', label: 'נסגר', color: '#2f8a4f' },
  { id: 'lost', label: 'לא מעוניין', color: '#b04a3f' },
  { id: 'not_relevant', label: 'לא רלוונטי', color: '#5d5750' },
];
const ST = Object.fromEntries(STATUSES.map((s) => [s.id, s]));
const today = () => new Date().toISOString().slice(0, 10);
const waLink = (num, text) => `https://wa.me/${(num || '').replace(/\D/g, '')}${text ? `?text=${encodeURIComponent(text)}` : ''}`;
const fmtDate = (d) => (d ? d.split('-').reverse().join('.') : '');
const fmtTime = (iso) => (iso ? new Date(iso).toLocaleString('he-IL', { timeZone: 'Asia/Jerusalem', day: 'numeric', month: 'numeric', hour: '2-digit', minute: '2-digit' }) : '');
// <input type="datetime-local"> works in the browser's local time
const toLocalInput = (d) => { const x = new Date(d); x.setMinutes(x.getMinutes() - x.getTimezoneOffset()); return x.toISOString().slice(0, 16); };
const fromLocalInput = (v) => (v ? new Date(v).toISOString() : null);
const unwrap = (r) => (r && r.data !== undefined ? r.data : r);
const wa = async (payload) => {
  const r = unwrap(await base44.functions.invoke('waApi', payload));
  if (r?.error) throw new Error(r.error);
  return r;
};

const CSS = `
.crm{min-height:100svh;background:#f4eee4;color:#17120d;direction:rtl;font-family:Optimum,Georgia,serif}
.crm .wrap{max-width:1180px;margin:0 auto;padding:56px 20px 80px}
.crm .eyebrow{font-size:14px;letter-spacing:.08em;color:#b08a4a}
.crm h1{font-weight:900;font-size:clamp(38px,6vw,64px);margin:10px 0 6px;line-height:1}
.crm .sub{font-weight:300;font-size:18px;color:#6d6257;margin:0 0 22px}
.crm .conn{font-size:14px;margin-bottom:18px}.crm .conn b{font-weight:700}
.crm .tabs{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:26px}
.crm .tab{padding:9px 16px;border:1px solid #cdbfa9;background:transparent;font:inherit;font-size:15px;cursor:pointer;color:#17120d}
.crm .tab.on{background:#17120d;color:#f4eee4;border-color:#17120d}
.crm .tab b{font-weight:700;margin-inline-start:6px}
.crm .tracks{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:22px}
.crm .track{text-align:right;padding:16px 18px;border:1px solid #cdbfa9;background:transparent;font:inherit;cursor:pointer;color:#17120d}
.crm .track{font-size:21px;font-weight:900}.crm .track b{font-weight:700;font-size:17px;margin-inline-start:8px;color:#b08a4a}
.crm .track i{font-style:normal;font-size:13px;background:#3f6fb0;color:#fff;padding:2px 8px;margin-inline-start:8px;vertical-align:middle}
.crm .track small{display:block;font-weight:300;font-size:14px;color:#6d6257;margin-top:4px}
.crm .track.on{background:#17120d;color:#f4eee4;border-color:#17120d}.crm .track.on small{color:#cdbfa9}
.crm .finding{margin-top:10px;padding:10px 12px;background:#efe7da;font-size:14px;line-height:1.5}
.crm .finding b{display:block;font-size:12px;color:#8a6d3b;letter-spacing:.04em;margin-bottom:2px}
@media (max-width:760px){.crm .tracks{grid-template-columns:1fr}}
.crm .panel{background:#faf7f1;box-shadow:0 18px 40px -30px rgba(40,25,10,.5);padding:20px 22px;margin-bottom:22px}
.crm .panel h2{font-weight:900;font-size:22px;margin:0 0 4px}
.crm .panel p{margin:0 0 12px;color:#6d6257;font-size:15px}
.crm .queue{display:grid;gap:6px;margin-top:14px;font-size:15px}
.crm .queue div{display:flex;justify-content:space-between;border-bottom:1px solid #e6dccd;padding:6px 0}
.crm .card{background:#faf7f1;box-shadow:0 18px 40px -30px rgba(40,25,10,.5);padding:22px;margin-bottom:16px;
  display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.35fr);gap:24px}
.crm .card.hot{box-shadow:0 0 0 2px #3f6fb0,0 18px 40px -30px rgba(40,25,10,.5)}
.crm .name{font-weight:900;font-size:27px;line-height:1.1}
.crm .meta{font-weight:300;font-size:15px;color:#6d6257;margin-top:6px}
.crm .pill{display:inline-block;padding:4px 12px;color:#fff;font-size:14px;margin-top:12px}
.crm .badge{display:inline-block;padding:4px 10px;background:#3f6fb0;color:#fff;font-size:14px;margin-inline-start:8px}
.crm .err{color:#b04a3f;font-size:14px;margin-top:8px}
.crm .links{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.crm .links a{padding:8px 12px;border:1px solid #cdbfa9;color:#17120d;text-decoration:none;font-size:14px;background:#fff}
.crm .links a:hover{border-color:#17120d}
.crm .row{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-top:12px}
.crm select,.crm textarea,.crm input{font:inherit;font-size:15px;border:1px solid #cdbfa9;background:#fff;color:#17120d;padding:9px 10px}
.crm label{font-size:13px;color:#6d6257;display:block;margin:14px 0 6px}
.crm textarea{width:100%;box-sizing:border-box;resize:vertical;line-height:1.55}
.crm .msg{min-height:170px}
.crm .mtabs{display:flex;gap:0;margin-bottom:-1px}
.crm .mtab{padding:8px 14px;border:1px solid #cdbfa9;background:#efe7da;font:inherit;font-size:14px;cursor:pointer;color:#17120d}
.crm .mtab.on{background:#fff;border-bottom-color:#fff}
.crm .btn{padding:10px 16px;font:inherit;font-size:15px;cursor:pointer;border:1px solid #17120d;background:transparent;color:#17120d;text-decoration:none;display:inline-block}
.crm .btn:disabled{opacity:.45;cursor:default}
.crm .btn.dark{background:#17120d;color:#f4eee4}
.crm .btn.wa{background:#1f7a4a;border-color:#1f7a4a;color:#fff}
.crm .btn.small{padding:7px 12px;font-size:14px}
.crm .saved{font-size:13px;color:#2f8a4f}
.crm .date{font-size:13px;color:#6d6257}
.crm .empty{padding:40px;text-align:center;color:#6d6257}
.crm .chat{margin-top:14px;border:1px solid #cdbfa9;background:#efe9df}
.crm .chat .log{height:300px;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:8px}
.crm .chat .b{max-width:82%;padding:8px 11px;font-size:15px;line-height:1.45;white-space:pre-wrap;box-shadow:0 1px 1px rgba(0,0,0,.08)}
.crm .chat .b.out{align-self:flex-start;background:#d9f2d0}
.crm .chat .b.in{align-self:flex-end;background:#fff}
.crm .chat .t{display:block;font-size:11px;color:#6d6257;margin-top:4px}
.crm .imgmsg{margin-top:10px;border:1px solid #cdbfa9;background:#efe9df;padding:10px}
.crm .imgmsg .lbl{font-size:13px;color:#6d6257;margin-bottom:8px}
.crm .imgmsg img{display:block;width:100%;height:auto;margin-bottom:8px;box-shadow:0 1px 2px rgba(0,0,0,.15)}
.crm .chat .bimg{display:block;max-width:100%;margin-bottom:6px}
.crm .chat form{display:flex;gap:6px;padding:8px;border-top:1px solid #cdbfa9;background:#faf7f1}
.crm .chat form input{flex:1}
@media (max-width:760px){.crm .card{grid-template-columns:1fr;gap:6px}.crm .wrap{padding:36px 14px 60px}}
`;

function Chat({ lead }) {
  const [msgs, setMsgs] = useState(null);
  const [text, setText] = useState('');
  const [err, setErr] = useState('');
  const [busy, setBusy] = useState(false);
  const logRef = useRef(null);

  const load = async () => {
    try { const r = await wa({ action: 'history', id: lead.id }); setMsgs(r.messages || []); setErr(''); }
    catch (e) { setErr(String(e.message || e)); }
  };
  useEffect(() => { load(); const t = setInterval(load, 15000); return () => clearInterval(t); }, [lead.id]);
  useEffect(() => { if (logRef.current) logRef.current.scrollTop = logRef.current.scrollHeight; }, [msgs]);

  const send = async (e) => {
    e.preventDefault();
    if (!text.trim() || busy) return;
    setBusy(true);
    try { await wa({ action: 'send', id: lead.id, which: 'text', text }); setText(''); await load(); }
    catch (e2) { setErr(String(e2.message || e2)); }
    setBusy(false);
  };

  return (
    <div className="chat">
      <div className="log" ref={logRef}>
        {!msgs && !err && <div className="date">טוען את השיחה...</div>}
        {msgs && msgs.length === 0 && <div className="date">עוד אין הודעות בשיחה הזאת.</div>}
        {(msgs || []).map((m) => (
          <div key={m.id} className={`b ${m.out ? 'out' : 'in'}`}>
            {m.image && <img className="bimg" src={m.image} alt="" />}
            {m.text}
            <span className="t">{fmtTime(new Date(m.at).toISOString())}{m.out && m.status ? ` · ${m.status === 'read' ? 'נקרא' : m.status === 'delivered' ? 'נמסר' : 'נשלח'}` : ''}</span>
          </div>
        ))}
        {err && <div className="err">{err}</div>}
      </div>
      <form onSubmit={send}>
        <input value={text} onChange={(e) => setText(e.target.value)} placeholder="כתיבת תשובה..." />
        <button className="btn dark small" disabled={busy || !text.trim()}>שליחה</button>
      </form>
    </div>
  );
}

function MessageBox({ lead, which, onSave, flash }) {
  const field = which === 1 ? 'message' : 'message2';
  const [text, setText] = useState(lead[field] || '');
  const [caption, setCaption] = useState(lead.msg1_caption || '');
  const [when, setWhen] = useState(() => toLocalInput(Date.now() + 60 * 60 * 1000));
  const [busy, setBusy] = useState(false);
  const sentAt = lead[`msg${which}_sent_at`];
  const at = lead[`msg${which}_at`];
  useEffect(() => { setText(lead[field] || ''); }, [lead[field]]);

  const flush = async () => {
    if (text !== (lead[field] || '')) await onSave(lead.id, { [field]: text });
    if (which === 1 && caption !== (lead.msg1_caption || '')) await onSave(lead.id, { msg1_caption: caption });
  };
  const sendNow = async () => {
    await flush();
    if (!window.confirm(`לשלוח עכשיו את הודעה ${which} ל${lead.business_name}?`)) return;
    setBusy(true);
    try {
      const r = await wa({ action: 'send', id: lead.id, which });
      onSave(lead.id, r.patch || {}, true);
      if (which === 1 && lead.status === 'research') onSave(lead.id, { status: 'sent' });  // the server only moves new/ready
      flash('ההודעה נשלחה');
    }
    catch (e) { flash(`השליחה נכשלה: ${e.message || e}`); }
    setBusy(false);
  };
  const schedule = async () => {
    await flush();
    const iso = fromLocalInput(when);
    const patch = { [`msg${which}_at`]: iso, send_error: '' };
    if (which === 1 && ['new', 'research'].includes(lead.status || 'new')) patch.status = 'ready';
    await onSave(lead.id, patch);
    flash(`תוזמן ל־${fmtTime(iso)}`);
  };

  return (
    <div>
      <textarea className="msg" value={text} onChange={(e) => setText(e.target.value)}
        onBlur={() => text !== (lead[field] || '') && onSave(lead.id, { [field]: text }).then(() => flash('נשמר'))} />
      {which === 1 && lead.msg1_image && (
        <div className="imgmsg">
          <div className="lbl">ומיד אחריה, הודעה נפרדת: התמונה עם הטקסט שמתחתיה</div>
          <a href={lead.msg1_image} target="_blank" rel="noreferrer"><img src={lead.msg1_image} alt="" /></a>
          <textarea rows={4} value={caption} onChange={(e) => setCaption(e.target.value)}
            onBlur={() => caption !== (lead.msg1_caption || '') && onSave(lead.id, { msg1_caption: caption }).then(() => flash('נשמר'))} />
        </div>
      )}
      {sentAt ? (
        <div className="row"><span className="saved">נשלחה ב־{fmtTime(sentAt)}</span>
          <button className="btn small" disabled={busy} onClick={sendNow}>לשלוח שוב</button></div>
      ) : (
        <div className="row">
          <button className="btn wa" disabled={busy || !text.trim()} onClick={sendNow}>שליחה עכשיו</button>
          {at ? (
            <>
              <span className="date">מתוזמנת ל־{fmtTime(at)}</span>
              <button className="btn small" onClick={() => onSave(lead.id, { [`msg${which}_at`]: null }).then(() => flash('התזמון בוטל'))}>ביטול תזמון</button>
            </>
          ) : (
            <>
              <input type="datetime-local" value={when} onChange={(e) => setWhen(e.target.value)} />
              <button className="btn small" disabled={!text.trim()} onClick={schedule}>תזמון</button>
            </>
          )}
        </div>
      )}
    </div>
  );
}

function LeadCard({ lead, onSave }) {
  const [notes, setNotes] = useState(lead.notes || '');
  const [note, setNote] = useState('');
  const [tab, setTab] = useState(lead.msg1_sent_at ? 2 : 1);
  const [chat, setChat] = useState(false);
  const pageUrl = `${window.location.origin}/p/${lead.slug}`;
  const st = ST[lead.status] || ST.new;
  const flash = (t) => { setNote(t); setTimeout(() => setNote(''), 2500); };

  const setStatus = (status) => {
    const patch = { status };
    if (!['new', 'ready'].includes(status)) patch.last_contact_date = today();
    onSave(lead.id, patch).then(() => flash('נשמר'));
  };
  const openChat = () => { setChat((c) => !c); if (lead.unread) onSave(lead.id, { unread: false }, true); };
  const copy = async (t) => { try { await navigator.clipboard.writeText(t); flash('הועתק'); } catch { /* ignore */ } };

  const links = [
    ['העמוד שלהם אצלנו', pageUrl], ['אתר', lead.website], ['פייסבוק', lead.facebook],
    ['אינסטגרם', lead.instagram], ['אינסטגרם של הבעלים', lead.owner_instagram],
  ].filter(([, u]) => u);

  return (
    <div className={`card ${lead.unread ? 'hot' : ''}`}>
      <div>
        <div className="name">{lead.business_name}</div>
        <div className="meta">{[lead.category, lead.city, lead.owner_name].filter(Boolean).join(' · ')}</div>
        <div className="meta" style={{ direction: 'ltr', textAlign: 'right' }}>{lead.whatsapp}</div>
        <span className="pill" style={{ background: st.color }}>{st.label}</span>
        {lead.unread && <span className="badge">תשובה חדשה</span>}
        {lead.last_contact_date && <span className="date" style={{ marginInlineStart: 10 }}>עדכון אחרון: {fmtDate(lead.last_contact_date)}</span>}
        {lead.last_reply_text && <div className="meta">התשובה האחרונה ({fmtTime(lead.last_reply_at)}): {lead.last_reply_text}</div>}
        {lead.send_error && <div className="err">{lead.send_error}</div>}
        {lead.finding && <div className="finding"><b>הממצא (פנימי)</b>{lead.finding}</div>}
        <div className="links">
          {links.map(([t, u]) => <a key={t} href={u} target="_blank" rel="noreferrer">{t}</a>)}
        </div>
        <label>סטטוס</label>
        <select value={lead.status || 'new'} onChange={(e) => setStatus(e.target.value)}>
          {STATUSES.map((s) => <option key={s.id} value={s.id}>{s.label}</option>)}
        </select>
        <label>הערות</label>
        <textarea rows={3} value={notes} onChange={(e) => setNotes(e.target.value)}
          onBlur={() => notes !== (lead.notes || '') && onSave(lead.id, { notes }).then(() => flash('נשמר'))} placeholder="מה נאמר, מתי לחזור אליהם..." />
      </div>
      <div>
        <div className="mtabs">
          <button className={`mtab ${tab === 1 ? 'on' : ''}`} onClick={() => setTab(1)}>הודעה 1 {lead.msg1_sent_at ? '✓' : ''}</button>
          <button className={`mtab ${tab === 2 ? 'on' : ''}`} onClick={() => setTab(2)}>הודעה 2 עם הקישור {lead.msg2_sent_at ? '✓' : ''}</button>
        </div>
        {tab === 2 && lead.track === 'wa' && !lead.message2
          ? <div className="empty" style={{ border: '1px solid #cdbfa9', background: '#fff' }}>ההודעה עם הקישור תופיע כאן כשהעמוד יהיה מוכן. כשהם עונים "כן", העבירו את הסטטוס ל"להכין עמוד".</div>
          : <MessageBox key={tab} lead={lead} which={tab} onSave={onSave} flash={flash} />}
        <div className="row">
          <button className="btn dark" onClick={openChat}>{chat ? 'סגירת השיחה' : 'השיחה בוואטסאפ'}</button>
          <a className="btn small" href={waLink(lead.whatsapp)} target="_blank" rel="noreferrer">פתיחה בוואטסאפ</a>
          <button className="btn small" onClick={() => copy(tab === 1 ? lead.message : lead.message2)}>העתקה</button>
          {note && <span className="saved">{note}</span>}
        </div>
        {chat && <Chat lead={lead} />}
      </div>
    </div>
  );
}

// Sequence scheduling: every "ready" lead without a scheduled or sent first message gets a slot,
// starting at `start`, every `gap` minutes, shifted by a few random minutes so it doesn't look automated.
function Scheduler({ leads, onSave, track }) {
  const [start, setStart] = useState(() => toLocalInput(Date.now() + 15 * 60 * 1000));
  const [gap, setGap] = useState(45);
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState('');
  const todo = leads.filter((l) => l.status === 'ready' && !l.msg1_sent_at && !l.msg1_at && l.message);
  const queue = leads.flatMap((l) => [
    l.msg1_at && !l.msg1_sent_at ? { l, which: 1, at: l.msg1_at } : null,
    l.msg2_at && !l.msg2_sent_at ? { l, which: 2, at: l.msg2_at } : null,
  ]).filter(Boolean).sort((a, b) => a.at.localeCompare(b.at));

  const run = async () => {
    if (!todo.length) return;
    setBusy(true);
    let t = new Date(start).getTime();
    for (const l of todo) {
      const jitter = Math.round((Math.random() * 10 - 5) * 60 * 1000);
      await onSave(l.id, { msg1_at: new Date(t + jitter).toISOString(), send_error: '' });
      t += gap * 60 * 1000;
    }
    setMsg(`תוזמנו ${todo.length} הודעות`); setBusy(false);
  };
  const clear = async () => {
    if (!window.confirm('לבטל את כל התזמונים שעוד לא נשלחו?')) return;
    setBusy(true);
    for (const q of queue) await onSave(q.l.id, { [`msg${q.which}_at`]: null });
    setMsg('כל התזמונים בוטלו'); setBusy(false);
  };
  const research = leads.filter((l) => l.status === 'research');
  const approveAll = async () => {
    if (!window.confirm(`להעביר ${research.length} לידים מ"מחקר מוכן" ל"מוכן לשליחה"? כדאי לעבור קודם על ההודעות.`)) return;
    setBusy(true);
    for (const l of research) await onSave(l.id, { status: 'ready' });
    setMsg(`${research.length} לידים מוכנים לשליחה`); setBusy(false);
  };

  return (
    <div className="panel">
      <h2>תזמון רצף</h2>
      <p>כל הלידים בסטטוס "מוכן לשליחה" מקבלים זמן שליחה להודעה הראשונה, אחד אחרי השני, עם כמה דקות הפרש אקראיות. המערכת שולחת הודעה אחת בכל פעם, ובודקת כל 10 דקות בין 8:00 ל־22:00. הודעה שמתוזמנת לשעות הלילה לא תצא.</p>
      <div className="row">
        <span>התחלה</span>
        <input type="datetime-local" value={start} onChange={(e) => setStart(e.target.value)} />
        <span>כל</span>
        <select value={gap} onChange={(e) => setGap(+e.target.value)}>
          {[30, 45, 60, 90].map((m) => <option key={m} value={m}>{m} דקות</option>)}
        </select>
        <button className="btn wa" disabled={busy || !todo.length} onClick={run}>תזמון {todo.length} לידים</button>
        {queue.length > 0 && <button className="btn small" disabled={busy} onClick={clear}>ביטול כל התזמונים</button>}
        {track === 'wa' && research.length > 0 && <button className="btn small" disabled={busy} onClick={approveAll}>אישור כל {research.length} המחקרים לשליחה</button>}
        {msg && <span className="saved">{msg}</span>}
      </div>
      {queue.length > 0 && (
        <div className="queue">
          {queue.map((q) => <div key={`${q.l.id}${q.which}`}><span>{q.l.business_name} · הודעה {q.which}</span><span>{fmtTime(q.at)}</span></div>)}
        </div>
      )}
    </div>
  );
}

export default function Crm() {
  const { user, isAuthenticated, authChecked, isLoadingAuth, checkUserAuth, navigateToLogin } = useAuth();
  const [leads, setLeads] = useState(null);
  const [filter, setFilter] = useState('all');
  const [track, setTrack] = useState(() => { try { return localStorage.getItem('crm_track') || 'wa'; } catch { return 'wa'; } });
  const pickTrack = (t) => { setTrack(t); setFilter('all'); try { localStorage.setItem('crm_track', t); } catch { /* ignore */ } };
  const [err, setErr] = useState('');
  const [conn, setConn] = useState(null);

  useEffect(() => {
    if (!authChecked && !isLoadingAuth) checkUserAuth();
    else if (authChecked && !isAuthenticated) navigateToLogin();
  }, [authChecked, isLoadingAuth, isAuthenticated]);

  const isAdmin = isAuthenticated && user?.role === 'admin';
  const reload = () => base44.entities.LeadCRM.list('sort_order', 500).then(setLeads).catch((e) => setErr(String(e?.message || e)));
  useEffect(() => {
    if (!isAdmin) return;
    reload();
    wa({ action: 'state' }).then((r) => setConn(r.stateInstance || 'unknown')).catch(() => setConn('error'));
    const t = setInterval(reload, 60000);   // replies and scheduled sends show up without a refresh
    return () => clearInterval(t);
  }, [isAdmin]);

  // localOnly: the server already wrote it (the backend function), only mirror it on screen
  const onSave = async (id, patch, localOnly = false) => {
    setLeads((ls) => ls.map((l) => (l.id === id ? { ...l, ...patch } : l)));
    if (localOnly) return;
    try { await base44.entities.LeadCRM.update(id, patch); } catch (e) { setErr('השמירה נכשלה, נסו לרענן'); }
  };

  const inTrack = useMemo(() => (leads || []).filter((l) => (l.track || 'page') === track), [leads, track]);
  const trackCounts = useMemo(() => {
    const c = { page: 0, wa: 0, page_unread: 0, wa_unread: 0 };
    (leads || []).forEach((l) => { const t = l.track || 'page'; c[t] += 1; if (l.unread) c[`${t}_unread`] += 1; });
    return c;
  }, [leads]);
  const counts = useMemo(() => {
    const c = { all: inTrack.length, unread: 0 };
    inTrack.forEach((l) => { c[l.status || 'new'] = (c[l.status || 'new'] || 0) + 1; if (l.unread) c.unread += 1; });
    return c;
  }, [inTrack]);

  if (!authChecked || isLoadingAuth || !isAuthenticated) return null;
  if (!isAdmin) {
    return <main style={{ minHeight: '100svh', display: 'grid', placeItems: 'center', background: '#f4eee4', fontFamily: 'Optimum, Georgia, serif', direction: 'rtl' }}>אין הרשאה לעמוד הזה.</main>;
  }

  const shown = inTrack.filter((l) => filter === 'all' || (filter === 'unread' ? l.unread : (l.status || 'new') === filter))
    .sort((a, b) => (b.unread ? 1 : 0) - (a.unread ? 1 : 0));
  return (
    <main className="crm">
      <style>{CSS}</style>
      <div className="wrap">
        <div className="eyebrow">IL META · CRM</div>
        <h1>לידים</h1>
        <p className="sub">שני מסלולים: וואטסאפ קודם (מחקר והודעה אישית, עמוד רק אחרי "כן") ועמודים מוכנים. שליחה, תזמון והשיחה עצמה. העמוד הזה גלוי רק לך.</p>
        <div className="conn">וואטסאפ: {conn === null ? 'בודק...' : conn === 'authorized' ? <b style={{ color: '#1f7a4a' }}>מחובר</b> : <b style={{ color: '#b04a3f' }}>לא מחובר ({conn})</b>}</div>
        <div className="tracks">
          <button className={`track ${track === 'wa' ? 'on' : ''}`} onClick={() => pickTrack('wa')}>
            וואטסאפ קודם<b>{trackCounts.wa}</b>{trackCounts.wa_unread > 0 && <i>{trackCounts.wa_unread} תשובות</i>}
            <small>מחקר והודעה אישית. העמוד נבנה רק אחרי "כן".</small>
          </button>
          <button className={`track ${track === 'page' ? 'on' : ''}`} onClick={() => pickTrack('page')}>
            עמודים מוכנים<b>{trackCounts.page}</b>{trackCounts.page_unread > 0 && <i>{trackCounts.page_unread} תשובות</i>}
            <small>העמוד כבר בנוי. הודעה עם תמונה, ואחר כך הקישור.</small>
          </button>
        </div>
        {leads && <Scheduler leads={inTrack} onSave={onSave} track={track} />}
        <div className="tabs">
          <button className={`tab ${filter === 'all' ? 'on' : ''}`} onClick={() => setFilter('all')}>הכול<b>{counts.all}</b></button>
          {counts.unread > 0 && <button className={`tab ${filter === 'unread' ? 'on' : ''}`} onClick={() => setFilter('unread')}>תשובות חדשות<b>{counts.unread}</b></button>}
          {STATUSES.filter((s) => !s.track || s.track === track).map((s) => (
            <button key={s.id} className={`tab ${filter === s.id ? 'on' : ''}`} onClick={() => setFilter(s.id)}>
              {s.label}<b>{counts[s.id] || 0}</b>
            </button>
          ))}
        </div>
        {err && <div className="empty" style={{ color: '#b04a3f' }}>{err}</div>}
        {!leads && !err && <div className="empty">טוען...</div>}
        {leads && shown.length === 0 && <div className="empty">אין לידים בסטטוס הזה.</div>}
        {shown.map((l) => <LeadCard key={l.id} lead={l} onSave={onSave} />)}
      </div>
    </main>
  );
}
