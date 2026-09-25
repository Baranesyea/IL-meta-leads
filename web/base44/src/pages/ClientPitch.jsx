import React, { useEffect, useMemo, useState } from "react";
import { useParams } from "react-router-dom";
import { REPORTS } from "@/reports/data";
import AdCanvas from "@/components/AdCanvas";

// Client pitch page — a standalone "this is how your brand could look" site.
// Route /p/:slug, no app chrome, nothing about other clients. Fonts: Optimum + Idealist (see index.css).
const CSS = `
.bp{--ivory:#f4eee4;--paper:#faf7f1;--ink:#17120d;--muted:#6d6257;--gold:#b08a4a;--deep:#0d231c;
  font-family:Optimum,Georgia,serif;color:var(--ink);background:var(--ivory);direction:rtl;overflow-x:hidden}
.bp *{box-sizing:border-box}
.bp .wrap{max-width:1240px;margin:0 auto;padding:0 24px}
.bp .reveal{opacity:0;transform:translateY(34px);transition:opacity 1.1s ease,transform 1.1s cubic-bezier(.2,.7,.2,1)}
.bp .reveal.in{opacity:1;transform:none}
.bp .eyebrow{font-weight:400;font-size:15px;letter-spacing:.08em;color:var(--gold)}
.bp .script{font-family:Idealist,cursive;font-weight:400}

/* top bar — transparent over the hero, ivory after scroll */
.bp .bar{position:fixed;inset:0 0 auto 0;z-index:40;height:74px;display:grid;grid-template-columns:1fr auto 1fr;align-items:center;padding:0 28px;
  color:#f4eee4;transition:background .5s,color .5s,box-shadow .5s}
.bp .bar.solid{background:rgba(250,247,241,.92);backdrop-filter:blur(14px);color:var(--ink);box-shadow:0 1px 0 rgba(0,0,0,.06)}
.bp .bar .mark{font-weight:900;font-size:30px;letter-spacing:.12em}
.bp .bar nav{display:flex;gap:28px;font-size:15px;font-weight:400}
.bp .bar nav a{color:inherit;text-decoration:none;opacity:.85}
.bp .bar .tag{justify-self:end;font-size:13px;letter-spacing:.04em;border:1px solid currentColor;padding:7px 14px;opacity:.8}
@media (max-width:820px){.bp .bar nav,.bp .bar .tag{display:none}.bp .bar{grid-template-columns:1fr;justify-items:center}.bp .bar .mark{font-size:26px}}

/* HERO */
.bp .hero{position:relative;height:100svh;min-height:640px;overflow:hidden;background:#070605;color:#f4eee4}
.bp .hero .bg{position:absolute;inset:-6% 0 -6% 0;background-size:cover;background-position:center 28%;animation:kb 22s ease-out both;will-change:transform}
@keyframes kb{from{scale:1.14}to{scale:1.02}}
.bp .hero .shade{position:absolute;inset:0;background:
  linear-gradient(270deg,rgba(7,6,5,.78) 0%,rgba(7,6,5,.35) 42%,rgba(7,6,5,0) 70%),
  linear-gradient(0deg,rgba(7,6,5,.55) 0%,rgba(7,6,5,0) 35%)}
.bp .hero .copy{position:absolute;right:0;bottom:0;z-index:3;padding:0 6vw 11vh;max-width:760px}
.bp .hero h1{margin:18px 0 0;line-height:.9}
.bp .hero h1 .b{display:block;font-weight:900;font-size:clamp(58px,9.4vw,150px);letter-spacing:-.015em}
.bp .hero h1 .l{display:block;font-weight:300;font-size:clamp(50px,8vw,128px)}

.bp .hero .sig{font-size:clamp(70px,8vw,120px);line-height:1;margin-top:6px;opacity:.95}
.bp .fadein{animation:fu 1.6s cubic-bezier(.2,.7,.2,1) both}
.bp .d1{animation-delay:.25s}.bp .d2{animation-delay:.55s}.bp .d3{animation-delay:.9s}.bp .d4{animation-delay:1.3s}
@keyframes fu{from{opacity:0;transform:translateY(40px)}to{opacity:1;transform:none}}
@media (max-width:760px){.bp .hero .shade{background:linear-gradient(0deg,rgba(7,6,5,.9) 0%,rgba(7,6,5,.2) 60%,rgba(7,6,5,0) 100%)}.bp .hero .line{display:none}}

/* campaign marquee */
.bp .marquee{padding:90px 0 70px;background:var(--paper);overflow:hidden}
.bp .marquee .head{display:flex;justify-content:space-between;align-items:end;margin-bottom:38px}
.bp .marquee h2{font-weight:900;font-size:clamp(34px,4.4vw,64px);margin:10px 0 0;line-height:1}
.bp .marquee h2 span{font-weight:300}
.bp .track{display:flex;gap:22px;width:max-content;align-items:flex-start;animation:mq 70s linear infinite}
.bp .track:hover{animation-play-state:paused}
.bp .track .it{width:clamp(220px,22vw,320px);flex:none;box-shadow:0 26px 50px -30px rgba(30,20,10,.55)}
@keyframes mq{from{transform:translateX(0)}to{transform:translateX(50%)}}

/* editorial split */
.bp .split{display:grid;grid-template-columns:1.05fr .95fr;min-height:92vh;background:var(--ivory)}
.bp .split .img{background-size:cover;background-position:center;min-height:60vh}
.bp .split .txt{display:flex;flex-direction:column;justify-content:center;padding:8vw 7vw}
.bp .split h2{margin:16px 0 0;line-height:.95}
.bp .split h2 .b{display:block;font-weight:900;font-size:clamp(46px,6vw,96px)}
.bp .split h2 .l{display:block;font-weight:300;font-size:clamp(40px,5.2vw,84px)}
.bp .split p{font-weight:300;font-size:20px;line-height:1.75;color:var(--muted);max-width:40ch;margin:30px 0 0}
.bp .split .price{margin-top:34px;font-weight:900;font-size:20px;letter-spacing:.04em}
@media (max-width:900px){.bp .split{grid-template-columns:1fr}}

/* full-bleed quote band */
.bp .band{position:relative;height:88vh;min-height:560px;overflow:hidden;color:#f4eee4;display:flex;align-items:center}
.bp .band .bg{position:absolute;inset:-12% 0;background-size:cover;background-position:center 40%;will-change:transform}
.bp .band .shade{position:absolute;inset:0;background:rgba(6,5,4,.5)}
.bp .band .q{position:relative;z-index:2;width:100%;text-align:center;padding:0 24px}
.bp .band .q .script{font-size:clamp(70px,9vw,150px);line-height:1.05}
.bp .band .q .by{margin-top:26px;font-size:16px;letter-spacing:.06em;opacity:.85}

/* pitch: what we saw */
.bp .intro{padding:130px 0 70px;background:var(--paper)}
.bp .intro .g{display:grid;grid-template-columns:1.1fr .9fr;gap:70px;align-items:end}
.bp .intro h2{margin:14px 0 0;line-height:1}
.bp .intro h2 .b{display:block;font-weight:900;font-size:clamp(38px,5vw,72px)}
.bp .intro h2 .l{display:block;font-weight:300;font-size:clamp(34px,4.4vw,64px)}
.bp .intro p{font-weight:300;font-size:21px;line-height:1.75;color:var(--muted);margin:0}
@media (max-width:880px){.bp .intro .g{grid-template-columns:1fr;gap:26px}}
.bp .ins{display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid #dcd1c1;background:var(--paper)}
.bp .ins > div{padding:40px 30px 80px;border-left:1px solid #dcd1c1}
.bp .ins > div:last-child{border-left:0}
.bp .ins .n{font-weight:300;font-size:72px;line-height:1;color:var(--gold)}
.bp .ins h3{font-weight:900;font-size:26px;margin:20px 0 12px}
.bp .ins p{font-weight:300;font-size:18px;line-height:1.7;color:var(--muted);margin:0}
@media (max-width:980px){.bp .ins{grid-template-columns:1fr 1fr}.bp .ins > div:nth-child(2){border-left:0}}
@media (max-width:560px){.bp .ins{grid-template-columns:1fr}.bp .ins > div{border-left:0;border-bottom:1px solid #dcd1c1;padding:30px 0 40px}}

/* angles */
.bp .angle{padding:120px 0;border-top:1px solid #e1d7c8}
.bp .angle.alt{background:var(--paper)}
.bp .angle .head{display:grid;grid-template-columns:auto 1fr;gap:34px;align-items:end;margin-bottom:54px}
.bp .angle .num{font-weight:300;font-size:clamp(90px,12vw,180px);line-height:.78;color:var(--gold)}
.bp .angle h3{font-weight:900;font-size:clamp(32px,4.2vw,58px);margin:8px 0 0;line-height:1}
.bp .angle .hook{font-weight:300;font-size:clamp(24px,2.6vw,36px);margin:14px 0 0}
.bp .angle .idea{font-weight:300;font-size:19px;line-height:1.75;color:var(--muted);max-width:62ch;margin:18px 0 0}
.bp .ads{display:flex;gap:22px;align-items:flex-start}
.bp .ads .card{flex:var(--ar) 1 0;min-width:0}
.bp .card{cursor:zoom-in;background:#fff;box-shadow:0 22px 44px -26px rgba(40,25,10,.45);transition:transform .6s cubic-bezier(.2,.7,.2,1),box-shadow .6s}
.bp .card:hover{transform:translateY(-8px);box-shadow:0 36px 70px -28px rgba(40,25,10,.55)}
.bp .card .cap{padding:16px 18px 20px}
.bp .card .cap b{font-weight:900;font-size:18px;display:block}
.bp .card .cap span{font-weight:300;font-size:14px;color:var(--muted)}
@media (max-width:980px){.bp .ads{flex-wrap:wrap}.bp .ads .card{flex:1 1 calc(50% - 11px)}}
@media (max-width:540px){.bp .angle .head{grid-template-columns:1fr;gap:6px}.bp .ads{gap:14px}.bp .ads .card{flex:1 1 100%}}

/* CTA */
.bp .cta{background:var(--deep);color:#efe6d7;padding:150px 0;text-align:center}
.bp .cta h2{margin:14px 0 0;line-height:1}
.bp .cta h2 .b{display:block;font-weight:900;font-size:clamp(44px,6vw,96px)}
.bp .cta h2 .l{display:block;font-weight:300;font-size:clamp(40px,5.4vw,86px)}
.bp .cta p{font-weight:300;font-size:21px;opacity:.85;margin:30px auto 0;max-width:44ch;line-height:1.65}
.bp .btn{display:inline-block;margin-top:48px;padding:20px 52px;border:1px solid #d9c49a;color:#efe6d7;font-size:18px;letter-spacing:.08em;text-decoration:none;transition:background .35s,color .35s}
.bp .btn:hover{background:#d9c49a;color:var(--deep)}
.bp footer{padding:36px 20px;text-align:center;font-size:13px;color:var(--muted);letter-spacing:.14em;background:var(--ivory)}

/* lightbox */
.bp .lb{position:fixed;inset:0;z-index:60;background:rgba(9,7,5,.94);display:flex;align-items:center;justify-content:center;padding:28px}
.bp .lb .box{display:grid;grid-template-columns:minmax(0,440px) 400px;gap:44px;max-width:980px;width:100%;max-height:92vh;align-items:start}
.bp .lb .ad{max-height:88vh;overflow:hidden}
.bp .lb .txt{color:#efe6d7;overflow:auto;max-height:88vh}
.bp .lb .txt b{font-weight:900;font-size:28px;display:block;margin:8px 0}
.bp .lb .txt pre{white-space:pre-wrap;font-family:Optimum,Georgia,serif;font-weight:300;font-size:18px;line-height:1.8;margin:18px 0}
.bp .lb .x{position:absolute;top:18px;left:24px;color:#efe6d7;font-size:34px;background:none;border:0;cursor:pointer}
@media (max-width:880px){.bp .lb .box{grid-template-columns:1fr;overflow:auto}}
`;

function useScrollY() {
  const [y, setY] = useState(0);
  useEffect(() => {
    let raf = 0;
    const on = () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(() => setY(window.scrollY)); };
    on();
    window.addEventListener("scroll", on, { passive: true });
    return () => { window.removeEventListener("scroll", on); cancelAnimationFrame(raf); };
  }, []);
  return y;
}

function useReveal(dep) {
  useEffect(() => {
    const io = new IntersectionObserver(
      (es) => es.forEach((e) => e.isIntersecting && e.target.classList.add("in")),
      { threshold: 0.12 }
    );
    document.querySelectorAll(".bp .reveal").forEach((el) => io.observe(el));
    return () => io.disconnect();
  }, [dep]);
}

export default function ClientPitch() {
  const { slug } = useParams();
  const r = REPORTS[slug];
  const y = useScrollY();
  const [open, setOpen] = useState(null);
  useReveal(slug);

  const byAngle = useMemo(() => {
    const m = {};
    (r?.ads || []).forEach((a) => (m[a.angle] = m[a.angle] || []).push(a));
    return m;
  }, [r]);
  const ad = (n) => r?.ads.find((a) => a.no === n);

  useEffect(() => {
    if (r) document.title = r.business.name;
    const esc = (e) => e.key === "Escape" && setOpen(null);
    window.addEventListener("keydown", esc);
    return () => window.removeEventListener("keydown", esc);
  }, [r]);

  if (!r) {
    return <div style={{ minHeight: "100vh", display: "grid", placeItems: "center", fontFamily: "Optimum", direction: "rtl" }}>העמוד לא נמצא.</div>;
  }
  const b = r.business;
  const strip = r.ads.filter((a) => [1, 5, 11, 14, 17, 20, 7, 10].includes(a.no));

  return (
    <div className="bp">
      <style>{CSS}</style>

      <header className={`bar ${y > 60 ? "solid" : ""}`}>
        <nav>
          <a href="#campaign">הקמפיין</a>
          <a href="#collection">יהלום מעבדה</a>
          <a href="#angles">20 המודעות</a>
        </nav>
        <div className="mark">{b.wordmark || b.owner_first}</div>
        <div className="tag">הוכן עבור {b.name}</div>
      </header>

      {/* HERO — the brand's own campaign, full screen */}
      <section className="hero">
        <div className="bg" style={{ backgroundImage: `url(${r.hero_bg})`, transform: `translateY(${y * 0.3}px)` }} />
        <div className="shade" />
        <div className="copy">
          <div className="eyebrow fadein d1">{r.hero_eyebrow || "קולקציית הטבע · זהב 14K · אמרלד טבעי"}</div>
          <h1>
            <span className="b fadein d2">{r.hero_title?.[0] || "פרחים נובלים."}</span>
            <span className="l fadein d3">{r.hero_title?.[1] || "זהב נשאר."}</span>
          </h1>
          <div className="script sig fadein d4">{b.owner_first}</div>
        </div>
      </section>

      {/* campaign strip */}
      <section className="marquee" id="campaign">
        <div className="wrap head reveal">
          <div>
            <div className="eyebrow">הקמפיין</div>
            <h2>{r.ads.length} מודעות. <span>חמש זוויות. מותג אחד.</span></h2>
          </div>
        </div>
        <div className="track">
          {[...strip, ...strip].map((a, i) => (
            <div key={i} className="it" onClick={() => setOpen(a)} style={{ cursor: "zoom-in" }}>
              <AdCanvas spec={a.spec} img={a.img} brand={b.name} />
            </div>
          ))}
        </div>
      </section>

      {/* editorial split */}
      <section className="split" id="collection">
        <div className="img" style={{ backgroundImage: `url(${ad(5)?.img})` }} />
        <div className="txt reveal">
          <div className="eyebrow">יהלום מעבדה</div>
          <h2><span className="b">אותו יהלום.</span><span className="l">אותו ברק.</span><span className="l">בלי המכרה.</span></h2>
          <p>סוליטר 1.50 קראט בחיתוך רדיאנט מוארך, בשיבוץ כוס חלק מזהב 14K. אותו פחמן, אותה קשיות, אותו ברק.</p>
          <div className="price">5,300 ש״ח</div>
        </div>
      </section>

      {/* quote band */}
      <section className="band">
        <div className="bg" style={{ backgroundImage: `url(${ad(3)?.img})`, transform: `translateY(${(y - 2200) * 0.12}px)` }} />
        <div className="shade" />
        <div className="q reveal">
          <div className="script">כל תכשיט מתחיל אצלי בסקיצה.</div>
          <div className="by">{b.name} · שינקין 48, תל אביב</div>
        </div>
      </section>

      {/* the pitch */}
      <section className="intro">
        <div className="wrap g">
          <div className="reveal">
            <div className="eyebrow">מה ראינו</div>
            <h2><span className="b">התכשיטים שלך ברמה של מגזין.</span><span className="l">המודעות עוד לא.</span></h2>
          </div>
          <p className="reveal">עברנו על המודעות הפעילות שלך בספריית המודעות של מטא, על האתר ועל הקולקציות. זה מה שבלט לנו, ומזה בנינו את הקמפיין שראית למעלה.</p>
        </div>
      </section>
      <section className="wrap ins">
        {r.insights.map((it, i) => (
          <div key={i} className="reveal" style={{ transitionDelay: `${i * 100}ms` }}>
            <div className="n">0{i + 1}</div>
            <h3>{it.t}</h3>
            <p>{it.d}</p>
          </div>
        ))}
      </section>

      <div id="angles" />
      {r.angles.map((ang, i) => (
        <section key={ang.id} className={`angle ${i % 2 ? "alt" : ""}`}>
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
                <div key={a.no} className="card reveal" style={{ transitionDelay: `${k * 90}ms`, "--ar": a.spec.w / a.spec.h }} onClick={() => setOpen(a)}>
                  <AdCanvas spec={a.spec} img={a.img} brand={b.name} />
                  <div className="cap"><b>{a.headline}</b><span>{a.format} · לטקסט המלא</span></div>
                </div>
              ))}
            </div>
          </div>
        </section>
      ))}

      <section className="cta">
        <div className="wrap reveal">
          <div className="eyebrow" style={{ color: "#d9c49a" }}>השלב הבא</div>
          <h2><span className="b">{b.owner_first}, רוצה לראות</span><span className="l">את זה באוויר?</span></h2>
          <p>נעלה את המודעות, נבדוק מה עובד הכי טוב, ונגדיל את מה שמוכר.</p>
          {r.contact_url
            ? <a className="btn" href={r.contact_url} target="_blank" rel="noreferrer">לשיחה קצרה בוואטסאפ</a>
            : <span className="btn" style={{ opacity: 0.5 }}>לשיחה קצרה בוואטסאפ</span>}
        </div>
      </section>
      <footer>הוכן במיוחד עבור {b.name}</footer>

      {open && (
        <div className="lb" onClick={() => setOpen(null)}>
          <button className="x" aria-label="סגירה">×</button>
          <div className="box" onClick={(e) => e.stopPropagation()}>
            <div className="ad"><AdCanvas spec={open.spec} img={open.img} brand={b.name} /></div>
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
