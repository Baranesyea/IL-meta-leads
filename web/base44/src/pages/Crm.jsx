import React, { useEffect, useMemo, useState } from 'react';
import { base44 } from '@/api/base44Client';
import { useAuth } from '@/lib/AuthContext';

// Eran's private outreach CRM. Behind Base44 login + admin role; the LeadCRM entity has
// admin-only RLS, so nobody else can read the rows even through the API.
const STATUSES = [
  { id: 'new', label: 'חדש', color: '#8a8177' },
  { id: 'sent', label: 'נשלח', color: '#b08a4a' },
  { id: 'replied', label: 'נענה', color: '#3f6fb0' },
  { id: 'meeting', label: 'נקבעה פגישה', color: '#7a4fb0' },
  { id: 'won', label: 'נסגר', color: '#2f8a4f' },
  { id: 'lost', label: 'לא מעוניין', color: '#b04a3f' },
  { id: 'not_relevant', label: 'לא רלוונטי', color: '#5d5750' },
];
const ST = Object.fromEntries(STATUSES.map((s) => [s.id, s]));
const today = () => new Date().toISOString().slice(0, 10);
const waLink = (num, text) => `https://wa.me/${(num || '').replace(/\D/g, '')}${text ? `?text=${encodeURIComponent(text)}` : ''}`;
const fmtDate = (d) => (d ? d.split('-').reverse().join('.') : '');

const CSS = `
.crm{min-height:100svh;background:#f4eee4;color:#17120d;direction:rtl;font-family:Optimum,Georgia,serif}
.crm .wrap{max-width:1100px;margin:0 auto;padding:56px 20px 80px}
.crm .eyebrow{font-size:14px;letter-spacing:.08em;color:#b08a4a}
.crm h1{font-weight:900;font-size:clamp(38px,6vw,64px);margin:10px 0 6px;line-height:1}
.crm .sub{font-weight:300;font-size:18px;color:#6d6257;margin:0 0 28px}
.crm .tabs{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:26px}
.crm .tab{padding:9px 16px;border:1px solid #cdbfa9;background:transparent;font:inherit;font-size:15px;cursor:pointer;color:#17120d}
.crm .tab.on{background:#17120d;color:#f4eee4;border-color:#17120d}
.crm .tab b{font-weight:700;margin-inline-start:6px}
.crm .card{background:#faf7f1;box-shadow:0 18px 40px -30px rgba(40,25,10,.5);padding:22px;margin-bottom:16px;
  display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.25fr);gap:24px}
.crm .name{font-weight:900;font-size:27px;line-height:1.1}
.crm .meta{font-weight:300;font-size:15px;color:#6d6257;margin-top:6px}
.crm .pill{display:inline-block;padding:4px 12px;color:#fff;font-size:14px;margin-top:12px}
.crm .links{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.crm .links a{padding:8px 12px;border:1px solid #cdbfa9;color:#17120d;text-decoration:none;font-size:14px;background:#fff}
.crm .links a:hover{border-color:#17120d}
.crm .row{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-top:16px}
.crm select,.crm textarea{font:inherit;font-size:15px;border:1px solid #cdbfa9;background:#fff;color:#17120d;padding:9px 10px}
.crm label{font-size:13px;color:#6d6257;display:block;margin:14px 0 6px}
.crm textarea{width:100%;box-sizing:border-box;resize:vertical;line-height:1.55}
.crm .msg{min-height:230px}
.crm .btn{padding:11px 18px;font:inherit;font-size:15px;cursor:pointer;border:1px solid #17120d;background:transparent;color:#17120d;text-decoration:none;display:inline-block}
.crm .btn.dark{background:#17120d;color:#f4eee4}
.crm .btn.wa{background:#1f7a4a;border-color:#1f7a4a;color:#fff}
.crm .saved{font-size:13px;color:#2f8a4f}
.crm .date{font-size:13px;color:#6d6257}
.crm .empty{padding:40px;text-align:center;color:#6d6257}
@media (max-width:760px){.crm .card{grid-template-columns:1fr;gap:6px}.crm .wrap{padding:36px 14px 60px}}
`;

function LeadCard({ lead, onSave }) {
  const [msg, setMsg] = useState(lead.message || '');
  const [notes, setNotes] = useState(lead.notes || '');
  const [flash, setFlash] = useState('');
  const pageUrl = `${window.location.origin}/p/${lead.slug}`;
  const st = ST[lead.status] || ST.new;

  const save = async (patch, note = 'נשמר') => {
    await onSave(lead.id, patch);
    setFlash(note); setTimeout(() => setFlash(''), 1600);
  };
  const setStatus = (status) => {
    const patch = { status };
    if (status !== 'new') patch.last_contact_date = today();
    save(patch);
  };
  const copy = async () => {
    try { await navigator.clipboard.writeText(msg); setFlash('ההודעה הועתקה'); setTimeout(() => setFlash(''), 1600); } catch { /* ignore */ }
  };

  const links = [
    ['העמוד שלהם אצלנו', pageUrl], ['אתר', lead.website], ['פייסבוק', lead.facebook],
    ['אינסטגרם', lead.instagram], ['אינסטגרם של הבעלים', lead.owner_instagram],
  ].filter(([, u]) => u);

  return (
    <div className="card">
      <div>
        <div className="name">{lead.business_name}</div>
        <div className="meta">{[lead.category, lead.city, lead.owner_name].filter(Boolean).join(' · ')}</div>
        <div className="meta" style={{ direction: 'ltr', textAlign: 'right' }}>{lead.whatsapp}</div>
        <span className="pill" style={{ background: st.color }}>{st.label}</span>
        {lead.last_contact_date && <span className="date" style={{ marginInlineStart: 10 }}>עדכון אחרון: {fmtDate(lead.last_contact_date)}</span>}
        <div className="links">
          {links.map(([t, u]) => <a key={t} href={u} target="_blank" rel="noreferrer">{t}</a>)}
        </div>
        <label>סטטוס</label>
        <select value={lead.status || 'new'} onChange={(e) => setStatus(e.target.value)}>
          {STATUSES.map((s) => <option key={s.id} value={s.id}>{s.label}</option>)}
        </select>
        <label>הערות</label>
        <textarea rows={3} value={notes} onChange={(e) => setNotes(e.target.value)}
          onBlur={() => notes !== (lead.notes || '') && save({ notes })} placeholder="מה נאמר, מתי לחזור אליהם..." />
      </div>
      <div>
        <label style={{ marginTop: 0 }}>הודעה ראשונה (אפשר לערוך, נשמר אוטומטית)</label>
        <textarea className="msg" value={msg} onChange={(e) => setMsg(e.target.value)}
          onBlur={() => msg !== (lead.message || '') && save({ message: msg })} />
        <div className="row">
          <a className="btn wa" href={waLink(lead.whatsapp, msg)} target="_blank" rel="noreferrer">פתיחת שיחה בוואטסאפ</a>
          <button className="btn dark" onClick={copy}>העתקת ההודעה</button>
          {lead.status === 'new' && <button className="btn" onClick={() => setStatus('sent')}>סימון כנשלח</button>}
          {flash && <span className="saved">{flash}</span>}
        </div>
      </div>
    </div>
  );
}

export default function Crm() {
  const { user, isAuthenticated, authChecked, isLoadingAuth, checkUserAuth, navigateToLogin } = useAuth();
  const [leads, setLeads] = useState(null);
  const [filter, setFilter] = useState('all');
  const [err, setErr] = useState('');

  useEffect(() => {
    if (!authChecked && !isLoadingAuth) checkUserAuth();
    else if (authChecked && !isAuthenticated) navigateToLogin();
  }, [authChecked, isLoadingAuth, isAuthenticated]);

  const isAdmin = isAuthenticated && user?.role === 'admin';
  useEffect(() => {
    if (!isAdmin) return;
    base44.entities.LeadCRM.list('sort_order', 500).then(setLeads).catch((e) => setErr(String(e?.message || e)));
  }, [isAdmin]);

  const onSave = async (id, patch) => {
    setLeads((ls) => ls.map((l) => (l.id === id ? { ...l, ...patch } : l)));
    try { await base44.entities.LeadCRM.update(id, patch); } catch (e) { setErr('השמירה נכשלה, נסו לרענן'); }
  };

  const counts = useMemo(() => {
    const c = { all: leads?.length || 0 };
    (leads || []).forEach((l) => { c[l.status || 'new'] = (c[l.status || 'new'] || 0) + 1; });
    return c;
  }, [leads]);

  if (!authChecked || isLoadingAuth || !isAuthenticated) return null;
  if (!isAdmin) {
    return <main style={{ minHeight: '100svh', display: 'grid', placeItems: 'center', background: '#f4eee4', fontFamily: 'Optimum, Georgia, serif', direction: 'rtl' }}>אין הרשאה לעמוד הזה.</main>;
  }

  const shown = (leads || []).filter((l) => filter === 'all' || (l.status || 'new') === filter);
  return (
    <main className="crm">
      <style>{CSS}</style>
      <div className="wrap">
        <div className="eyebrow">IL META · CRM</div>
        <h1>לידים</h1>
        <p className="sub">כל ליד עם העמוד שלו, הקישורים, והודעה מוכנה לשליחה. העמוד הזה גלוי רק לך.</p>
        <div className="tabs">
          <button className={`tab ${filter === 'all' ? 'on' : ''}`} onClick={() => setFilter('all')}>הכול<b>{counts.all}</b></button>
          {STATUSES.map((s) => (
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
