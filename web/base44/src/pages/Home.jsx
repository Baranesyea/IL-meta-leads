import React from 'react';

// Home page — placeholder until Eran's "about" content is ready. Intentionally links nowhere.
export default function Home() {
  return (
    <main style={{ minHeight: '100svh', display: 'grid', placeItems: 'center', background: '#f4eee4', color: '#17120d', direction: 'rtl' }}>
      <div style={{ textAlign: 'center', padding: 24 }}>
        <div style={{ fontFamily: 'Optimum', fontWeight: 400, fontSize: 13, letterSpacing: '.32em', color: '#b08a4a' }}>IL META</div>
        <h1 style={{ fontFamily: 'Optimum', fontWeight: 900, fontSize: 'clamp(44px,7vw,110px)', lineHeight: 1, margin: '18px 0 0' }}>כאן יהיה תוכן</h1>
      </div>
    </main>
  );
}
