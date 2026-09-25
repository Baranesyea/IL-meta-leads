import React, { useState } from 'react';
import { REPORTS } from '@/reports/data';
import { useAuth } from '@/lib/AuthContext';

// Eran's private index of client pages. Behind login (see App.jsx) — clients never see this.
export default function Admin() {
  const { user } = useAuth();
  const [copied, setCopied] = useState(null);
  const origin = typeof window !== 'undefined' ? window.location.origin : '';
  const pages = Object.values(REPORTS);

  const copy = async (url, slug) => {
    try { await navigator.clipboard.writeText(url); setCopied(slug); setTimeout(() => setCopied(null), 1800); } catch { /* ignore */ }
  };

  // Only the app admin (Eran). A registered visitor who isn't admin sees nothing.
  if (user?.role !== 'admin') {
    return <main style={{ minHeight: '100svh', display: 'grid', placeItems: 'center', background: '#f4eee4', fontFamily: 'Optimum, Georgia, serif', direction: 'rtl' }}>אין הרשאה לעמוד הזה.</main>;
  }

  return (
    <main style={{ minHeight: '100svh', background: '#f4eee4', color: '#17120d', direction: 'rtl', fontFamily: 'Optimum, Georgia, serif' }}>
      <div style={{ maxWidth: 980, margin: '0 auto', padding: '72px 24px' }}>
        <div style={{ fontSize: 15, letterSpacing: '.08em', color: '#b08a4a' }}>IL META · ניהול</div>
        <h1 style={{ fontWeight: 900, fontSize: 'clamp(40px,6vw,72px)', margin: '12px 0 8px', lineHeight: 1 }}>עמודי לקוחות</h1>
        <p style={{ fontWeight: 300, fontSize: 19, color: '#6d6257', margin: '0 0 44px' }}>כל לקוח רואה רק את הקישור שלו. העמוד הזה גלוי רק לך.</p>
        {pages.map((p) => {
          const url = `${origin}/p/${p.slug}`;
          const cover = p.ads.find((a) => a.no === p.hero?.[0]);
          return (
            <div key={p.slug} style={{ display: 'grid', gridTemplateColumns: '120px 1fr auto', gap: 24, alignItems: 'center',
              background: '#faf7f1', padding: 18, marginBottom: 14, boxShadow: '0 18px 40px -30px rgba(40,25,10,.5)' }}>
              <div style={{ width: 120, height: 150, backgroundImage: `url(${p.hero_bg || cover?.img})`, backgroundSize: 'cover', backgroundPosition: 'center' }} />
              <div>
                <div style={{ fontWeight: 900, fontSize: 28 }}>{p.business.name}</div>
                <div style={{ fontWeight: 300, fontSize: 16, color: '#6d6257', marginTop: 6 }}>{p.ads.length} מודעות · {p.angles.length} זוויות</div>
                <div style={{ fontSize: 14, color: '#6d6257', marginTop: 8, direction: 'ltr', textAlign: 'right' }}>{url}</div>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                <a href={`/p/${p.slug}`} target="_blank" rel="noreferrer"
                   style={{ padding: '12px 22px', background: '#17120d', color: '#f4eee4', textDecoration: 'none', textAlign: 'center' }}>לפתיחת העמוד</a>
                <button onClick={() => copy(url, p.slug)}
                   style={{ padding: '12px 22px', border: '1px solid #17120d', background: 'transparent', cursor: 'pointer', fontFamily: 'inherit', fontSize: 15 }}>
                  {copied === p.slug ? 'הקישור הועתק' : 'העתקת קישור ללקוח'}
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </main>
  );
}
