import React, { useEffect, useMemo, useRef, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { REPORTS } from "@/reports/data";
// Standalone client pitch page (no app chrome). Route: /p/:slug

// Brand fonts (web versions of Optimum + Idealist) live in /public/fonts
const FONT_CSS = `
@font-face{font-family:"Optimum";src:url("/fonts/FbOptimum-Light.woff2") format("woff2");font-weight:300;font-display:swap}
@font-face{font-family:"Optimum";src:url("/fonts/FbOptimum-Regular.woff2") format("woff2");font-weight:400;font-display:swap}
@font-face{font-family:"Optimum";src:url("/fonts/FbOptimum-Black.woff2") format("woff2");font-weight:900;font-display:swap}
@font-face{font-family:"Idealist";src:url("/fonts/FbIdealist-Regular.woff2") format("woff2");font-weight:400;font-display:swap}
.rp{--ivory:#f5efe6;--paper:#fbf8f3;--ink:#1c1611;--muted:#6f655a;--gold:#b08a4a;--deep:#0e241d;
  font-family:"Optimum",serif;color:var(--ink);background:var(--ivory);direction:rtl;overflow-x:hidden}
.rp *{box-sizing:border-box}
.rp .wrap{max-width:1180px;margin:0 auto;padding:0 20px}
.rp .reveal{opacity:0;transform:translateY(28px);transition:opacity .9s ease,transform .9s cubic-bezier(.2,.7,.2,1)}
.rp .reveal.in{opacity:1;transform:none}
.rp .eyebrow{font-weight:400;font-size:14px;letter-spacing:.18em;color:var(--gold)}
.rp .script{font-family:"Idealist",cursive}

/* HERO */
.rp .hero{position:relative;min-height:100svh;overflow:hidden;background:#0b0907;color:#f5efe6}
.rp .hero .bg{position:absolute;inset:-8% 0 0 0;background-size:cover;background-position:center 30%;will-change:transform}
.rp .hero .shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(8,6,4,.1) 0%,rgba(8,6,4,.35) 45%,rgba(8,6,4,.85) 100%)}
.rp .hero .copy{position:relative;z-index:3;min-height:100svh;display:flex;flex-direction:column;justify-content:flex-end;padding:0 20px 12vh;max-width:1180px;margin:0 auto}
.rp .hero h1{font-weight:900;font-size:clamp(46px,8.4vw,128px);line-height:.92;margin:14px 0 0;letter-spacing:-.01em;max-width:11ch}
.rp .hero h1 span{display:block;font-weight:300}
.rp .hero p{font-weight:300;font-size:clamp(18px,2vw,24px);max-width:36ch;margin:26px 0 0;opacity:.92;line-height:1.5}
.rp .hero .sig{font-size:clamp(44px,5vw,72px);margin-top:10px;opacity:.95}
.rp .floats{position:absolute;inset:0;z-index:2;pointer-events:none}
.rp .float{position:absolute;width:clamp(120px,17vw,250px);box-shadow:0 30px 60px rgba(0,0,0,.45);will-change:transform}
.rp .float img{display:block;width:100%}
.rp .cue{position:absolute;z-index:3;bottom:28px;left:50%;transform:translateX(-50%);font-size:13px;letter-spacing:.2em;opacity:.7}
@media (max-width:760px){.rp .float{display:none}.rp .hero .shade{background:linear-gradient(180deg,rgba(8,6,4,.05) 30%,rgba(8,6,4,.88) 100%)}}

/* INTRO */
.rp .intro{padding:120px 0 90px;background:var(--paper)}
.rp .intro .grid{display:grid;grid-template-columns:1.1fr .9fr;gap:60px;align-items:end}
.rp .intro h2{font-weight:900;font-size:clamp(34px,4.6vw,64px);line-height:1.02;margin:12px 0 0}
.rp .intro h2 span{font-weight:300;display:block}
.rp .intro p{font-weight:300;font-size:20px;line-height:1.7;color:var(--muted);margin:0}
@media (max-width:860px){.rp .intro .grid{grid-template-columns:1fr;gap:26px}}

/* INSIGHTS */
.rp .insights{padding:40px 0 120px;background:var(--paper)}
.rp .ins{display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid #ddd3c4}
.rp .ins > div{padding:34px 26px 10px 26px;border-left:1px solid #ddd3c4}
.rp .ins > div:last-child{border-left:0}
.rp .ins .n{font-weight:300;font-size:64px;line-height:1;color:var(--gold)}
.rp .ins h3{font-weight:900;font-size:24px;margin:18px 0 10px}
.rp .ins p{font-weight:300;font-size:17px;line-height:1.65;color:var(--muted);margin:0}
@media (max-width:980px){.rp .ins{grid-template-columns:1fr 1fr}.rp .ins > div:nth-child(2){border-left:0}}
@media (max-width:560px){.rp .ins{grid-template-columns:1fr}.rp .ins > div{border-left:0;border-bottom:1px solid #ddd3c4;padding:28px 0}}

/* ANGLES */
.rp .angle{padding:110px 0;border-top:1px solid #e3d9ca}
.rp .angle:nth-of-type(even){background:var(--paper)}
.rp .angle .head{display:grid;grid-template-columns:auto 1fr;gap:28px;align-items:end;margin-bottom:46px}
.rp .angle .num{font-weight:300;font-size:clamp(80px,11vw,160px);line-height:.8;color:var(--gold)}
.rp .angle h3{font-weight:900;font-size:clamp(30px,4vw,54px);margin:6px 0 0;line-height:1.02}
.rp .angle .hook{font-weight:300;font-size:clamp(22px,2.4vw,32px);margin:12px 0 0}
.rp .angle .idea{font-weight:300;font-size:18px;line-height:1.7;color:var(--muted);max-width:60ch;margin:16px 0 0}
.rp .ads{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;align-items:start}
.rp .card{cursor:zoom-in;background:#fff;box-shadow:0 1px 0 rgba(0,0,0,.04),0 18px 40px -22px rgba(40,25,10,.35);transition:transform .5s cubic-bezier(.2,.7,.2,1),box-shadow .5s}
.rp .card:hover{transform:translateY(-6px);box-shadow:0 30px 60px -24px rgba(40,25,10,.45)}
.rp .card img{display:block;width:100%;height:auto}
.rp .card .cap{padding:14px 16px 18px}
.rp .card .cap b{font-weight:900;font-size:17px;display:block}
.rp .card .cap span{font-weight:300;font-size:14px;color:var(--muted)}
@media (max-width:980px){.rp .ads{grid-template-columns:1fr 1fr}}
@media (max-width:520px){.rp .angle .head{grid-template-columns:1fr;gap:6px}}

/* CTA */
.rp .cta{background:var(--deep);color:#f1e9dc;padding:140px 0;text-align:center}
.rp .cta h2{font-weight:900;font-size:clamp(38px,5.6vw,84px);line-height:1;margin:0}
.rp .cta h2 span{display:block;font-weight:300}
.rp .cta p{font-weight:300;font-size:20px;opacity:.85;margin:26px auto 0;max-width:44ch;line-height:1.6}
.rp .btn{display:inline-block;margin-top:44px;padding:18px 44px;border:1px solid #d9c49a;color:#f1e9dc;font-size:18px;letter-spacing:.06em;text-decoration:none;transition:background .3s,color .3s}
.rp .btn:hover{background:#d9c49a;color:var(--deep)}
.rp footer{padding:34px 20px;text-align:center;font-size:13px;color:var(--muted);letter-spacing:.08em}

/* LIGHTBOX */
.rp .lb{position:fixed;inset:0;z-index:50;background:rgba(10,8,6,.92);display:flex;align-items:center;justify-content:center;padding:24px}
.rp .lb .box{display:grid;grid-template-columns:minmax(0,1fr) 380px;gap:36px;max-width:1080px;width:100%;max-height:92vh}
.rp .lb img{width:100%;max-height:88vh;object-fit:contain;background:#000}
.rp .lb .txt{color:#f1e9dc;overflow:auto}
.rp .lb .txt b{font-weight:900;font-size:26px;display:block;margin-bottom:6px}
.rp .lb .txt pre{white-space:pre-wrap;font-family:"Optimum",serif;font-weight:300;font-size:17px;line-height:1.75;margin:18px 0}
.rp .lb .x{position:absolute;top:18px;left:22px;color:#f1e9dc;font-size:30px;background:none;border:0;cursor:pointer}
@media (max-width:860px){.rp .lb .box{grid-template-columns:1fr;overflow:auto}}
`;

function useReveal() {
  useEffect(() => {
    const els = document.querySelectorAll(".rp .reveal");
    const io = new IntersectionObserver(
      (entries) => entries.forEach((e) => e.isIntersecting && e.target.classList.add("in")),
      { threshold: 0.12 }
    );
    els.forEach((el) => io.observe(el));
    return () => io.disconnect();
  }, []);
}

function useScrollY() {
  const [y, setY] = useState(0);
  useEffect(() => {
    let raf = 0;
    const on = () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(() => setY(window.scrollY)); };
    window.addEventListener("scroll", on, { passive: true });
    return () => { window.removeEventListener("scroll", on); cancelAnimationFrame(raf); };
  }, []);
  return y;
}

const FLOAT_POS = [
  { top: "14%", left: "6%", speed: -0.18, rot: -4 },
  { top: "46%", left: "20%", speed: -0.32, rot: 3 },
  { top: "8%", left: "33%", speed: -0.1, rot: 2 },
];

export default function ClientReport() {
  const { slug } = useParams();
  const r = REPORTS[slug];
  const y = useScrollY();
  const [open, setOpen] = useState(null);
  useReveal();

  const byAngle = useMemo(() => {
    const m = {};
    (r?.ads || []).forEach((a) => (m[a.angle] = m[a.angle] || []).push(a));
    return m;
  }, [r]);

  useEffect(() => {
    if (r) document.title = `${r.business.name} · IL Meta`;
    const esc = (e) => e.key === "Escape" && setOpen(null);
    window.addEventListener("keydown", esc);
    return () => window.removeEventListener("keydown", esc);
  }, [r]);

  if (!r) {
    return (
      <div style={{ padding: 80, textAlign: "center", direction: "rtl" }}>
        הדוח לא נמצא. <Link to="/">לעמוד הראשי</Link>
      </div>
    );
  }
  const heroAd = r.ads.find((a) => a.no === r.hero[0]);
  const floats = r.hero.slice(1).map((n) => r.ads.find((a) => a.no === n));

  return (
    <div className="rp">
      <style>{FONT_CSS}</style>

      <section className="hero">
        <div className="bg" style={{ backgroundImage: `url(${r.hero_bg || heroAd.img})`, transform: `translateY(${y * 0.25}px) scale(1.06)` }} />
        <div className="shade" />
        <div className="floats">
          {floats.map((a, i) => (
            <div key={a.no} className="float" style={{ top: FLOAT_POS[i].top, left: FLOAT_POS[i].left,
              transform: `translateY(${y * FLOAT_POS[i].speed}px) rotate(${FLOAT_POS[i].rot}deg)` }}>
              <img src={a.img} alt="" />
            </div>
          ))}
        </div>
        <div className="copy">
          <div className="eyebrow">הוכן במיוחד עבור {r.business.name}</div>
          <h1>{r.business.owner_first}, ככה<span>המותג שלך יכול להיראות.</span></h1>
          <p>{r.ads.length} מודעות חדשות, בחמש זוויות שונות, על התכשיטים האמיתיים שלך.</p>
        </div>
        <div className="cue">גללי למטה</div>
      </section>

      <section className="intro">
        <div className="wrap grid">
          <div className="reveal">
            <div className="eyebrow">מה ראינו</div>
            <h2>התכשיטים שלך ברמה של מגזין.<span>המודעות עוד לא.</span></h2>
          </div>
          <p className="reveal">עברנו על המודעות הפעילות שלך בספריית המודעות של מטא, על האתר ועל הקולקציות. הנה מה שבלט לנו, ומה בנינו מזה.</p>
        </div>
      </section>

      <section className="insights">
        <div className="wrap ins">
          {r.insights.map((it, i) => (
            <div key={i} className="reveal" style={{ transitionDelay: `${i * 90}ms` }}>
              <div className="n">0{i + 1}</div>
              <h3>{it.t}</h3>
              <p>{it.d}</p>
            </div>
          ))}
        </div>
      </section>

      {r.angles.map((ang, i) => (
        <section key={ang.id} className="angle">
          <div className="wrap">
            <div className="head reveal">
              <div className="num">0{i + 1}</div>
              <div>
                <div className="eyebrow">זווית {i + 1}</div>
                <h3>{ang.name}</h3>
                <div className="hook">״{ang.hook}״</div>
                <p className="idea">{ang.idea}</p>
              </div>
            </div>
            <div className="ads">
              {(byAngle[ang.id] || []).map((a, k) => (
                <div key={a.no} className="card reveal" style={{ transitionDelay: `${k * 80}ms` }} onClick={() => setOpen(a)}>
                  <img src={a.img} alt={a.headline} loading="lazy" />
                  <div className="cap"><b>{a.headline}</b><span>{a.format} · לחצי לטקסט המלא</span></div>
                </div>
              ))}
            </div>
          </div>
        </section>
      ))}

      <section className="cta">
        <div className="wrap reveal">
          <div className="eyebrow" style={{ color: "#d9c49a" }}>השלב הבא</div>
          <h2>רוצה לראות אותן<span>באוויר?</span></h2>
          <p>נשמח להראות לך איך מעלים את המודעות האלה, בודקים מה עובד הכי טוב ומגדילים את מה שמוכר.</p>
          <a className="btn" href={r.contact_url || "#"} target="_blank" rel="noreferrer">לשיחה קצרה בוואטסאפ</a>
        </div>
      </section>
      <footer>הוכן עבור {r.business.name} · IL Meta</footer>

      {open && (
        <div className="lb" onClick={() => setOpen(null)}>
          <button className="x" aria-label="סגירה">×</button>
          <div className="box" onClick={(e) => e.stopPropagation()}>
            <img src={open.img} alt={open.headline} />
            <div className="txt">
              <div className="eyebrow">מודעה {open.no} · {open.format}</div>
              <b>{open.headline}</b>
              <pre>{open.primary}</pre>
              <div className="eyebrow">כפתור: {open.cta}</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
