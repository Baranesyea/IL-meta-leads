import React, { useEffect, useMemo, useRef, useState } from "react";
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
/* typing: the untyped rest keeps its space (no layout jump), a thin caret leads */
.bp .ty-rest{color:transparent;text-shadow:none}
.bp .ty-caret{display:inline-block;width:.06em;min-width:2px;height:.82em;margin:0 .04em;background:currentColor;vertical-align:-.06em;animation:blink .9s steps(1) infinite}
@keyframes blink{50%{opacity:0}}

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
.bp .hero .copy{position:absolute;right:0;bottom:0;z-index:3;padding:0 6vw 11vh;max-width:760px;text-shadow:0 2px 24px rgba(0,0,0,.45)}
.bp .hero .eyebrow{color:#efe2c4;font-size:17px;letter-spacing:.06em}
.bp .hero h1{margin:18px 0 0;line-height:.9}
.bp .hero h1 .b{display:block;font-weight:900;font-size:clamp(58px,9.4vw,150px);letter-spacing:-.015em}
.bp .hero h1 .l{display:block;font-weight:300;font-size:clamp(50px,8vw,128px)}

.bp .hero .sig{font-size:clamp(70px,8vw,120px);line-height:1;margin-top:6px;opacity:.95}
.bp .fadein{animation:fu 1.6s cubic-bezier(.2,.7,.2,1) both}
.bp .d1{animation-delay:.25s}.bp .d2{animation-delay:.55s}.bp .d3{animation-delay:.9s}.bp .d4{animation-delay:1.3s}
@keyframes fu{from{opacity:0;transform:translateY(40px)}to{opacity:1;transform:none}}
/* phones: the words sit in the photo's own dark space on top, the photo below them untouched —
   the necklace and pendant (the product) are never under a shade or under type */
@media (max-width:760px){.bp .hero{background:#010c0b}
  .bp .hero .bg{inset:30% 0 -3% 0;background-position:center bottom;
    -webkit-mask-image:linear-gradient(to bottom,transparent 0,#000 14%);mask-image:linear-gradient(to bottom,transparent 0,#000 14%)}
  .bp .hero .shade{display:none}
  .bp .hero .copy{top:96px;bottom:auto;padding:0 22px}
  .bp .hero .eyebrow{font-size:15px}
  .bp .hero h1 .b{font-size:52px}.bp .hero h1 .l{font-size:44px}
  .bp .hero .sig{font-size:64px;margin-top:2px}}

/* campaign marquee */
.bp .marquee{padding:90px 0 70px;background:var(--paper);overflow:hidden}
.bp .marquee .head{display:flex;justify-content:space-between;align-items:end;margin-bottom:38px}
.bp .marquee h2{font-weight:900;font-size:clamp(34px,4.4vw,64px);margin:10px 0 0;line-height:1}
.bp .marquee h2 .l{font-weight:300}
.bp .strip{--h:clamp(360px,34vw,440px);direction:ltr;overflow-x:auto;overflow-y:hidden;-webkit-overflow-scrolling:touch;scrollbar-width:none;touch-action:pan-x pan-y}
.bp .strip::-webkit-scrollbar{display:none}
.bp .track{display:flex;gap:22px;width:max-content;align-items:flex-start;padding:0 11px 40px}
.bp .track .it{height:var(--h);width:calc(var(--h) * var(--ar));flex:none;box-shadow:0 26px 50px -30px rgba(30,20,10,.55)}

/* editorial split */
.bp .split{display:grid;grid-template-columns:1.05fr .95fr;min-height:92vh;background:var(--ivory)}
.bp .split .img{background-size:cover;background-position:center;min-height:60vh}
.bp .split .txt{display:flex;flex-direction:column;justify-content:center;padding:8vw 7vw}
.bp .split h2{margin:16px 0 0;line-height:.95}
.bp .split h2 .b{display:block;font-weight:900;font-size:clamp(46px,6vw,96px)}
.bp .split h2 .l{display:block;font-weight:300;font-size:clamp(40px,5.2vw,84px)}
.bp .split p{font-weight:300;font-size:20px;line-height:1.75;color:var(--muted);max-width:40ch;margin:30px 0 0}
.bp .split .price{margin-top:34px;font-weight:900;font-size:20px;letter-spacing:.04em}
@media (max-width:900px){.bp .split{display:block;position:relative;overflow:hidden;color:#f4eee4;background:#0e0b08}
  /* the photo owns the top of the screen and melts into the dark ground; the text comes after it, never on it */
  .bp .split .img{position:relative;height:72svh;min-height:420px;background-position:center 55%}
  .bp .split .img::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,#0e0b08 0%,rgba(14,11,8,0) 22%)}
  .bp .split .txt{position:relative;z-index:2;padding:8px 22px 90px}
  .bp .split p{color:rgba(244,238,228,.86)}.bp .split .eyebrow{color:#efe2c4}}

/* full-bleed quote band */
.bp .band{position:relative;height:88vh;min-height:560px;overflow:hidden;color:#f4eee4;display:flex;align-items:flex-start}
.bp .band .bg{position:absolute;inset:-12% 0;background-size:cover;background-position:center 62%;will-change:transform}
.bp .band .shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(6,5,4,.78) 0%,rgba(6,5,4,.45) 38%,rgba(6,5,4,0) 60%)}
.bp .band .q{position:relative;z-index:2;width:100%;text-align:center;padding:14vh 24px 0}
@media (max-width:760px){.bp .band .bg{background-position:center 85%}.bp .band .q{padding-top:11vh}}
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
.bp .ads{display:flex;flex-direction:column;gap:22px}
.bp .ads .row{display:flex;gap:22px;align-items:flex-start}
.bp .ads .card{min-width:0}  /* flex-grow set inline: aspect ratio × 100 (grow factors < 1 would leave the row half empty) */
.bp .card{cursor:zoom-in;box-shadow:0 22px 44px -26px rgba(40,25,10,.45);transition:transform .6s cubic-bezier(.2,.7,.2,1),box-shadow .6s}
@media (hover:hover){.bp .card:hover{transform:translateY(-8px);box-shadow:0 36px 70px -28px rgba(40,25,10,.55)}}
@media (max-width:540px){.bp .angle{padding:90px 0}.bp .angle .head{grid-template-columns:1fr;gap:6px}
  .bp .ads{gap:4px;margin:0 -24px}.bp .ads .row{gap:4px}.bp .card{box-shadow:none}}  /* phones: ads edge to edge */

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
.bp .lb{position:fixed;inset:0;z-index:60;background:#0b0907;overflow-y:auto;overscroll-behavior:contain;
  display:flex;align-items:center;justify-content:center;padding:84px 28px 40px}
.bp .lb .box{display:flex;gap:44px;max-width:1000px;width:100%;align-items:flex-start;justify-content:center;margin:auto}
.bp .lb .ad{flex:none;width:min(460px, calc(80svh * var(--ar)))}
.bp .lb .txt{color:#efe6d7;flex:1 1 360px;max-width:420px}
.bp .lb .txt b{font-weight:900;font-size:28px;display:block;margin:8px 0}
.bp .lb .txt pre{white-space:pre-wrap;font-family:Optimum,Georgia,serif;font-weight:300;font-size:18px;line-height:1.8;margin:18px 0}
.bp .lb .x{position:fixed;top:14px;left:14px;z-index:70;width:52px;height:52px;border-radius:50%;display:grid;place-items:center;
  color:#efe6d7;font-size:30px;line-height:1;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.35);cursor:pointer;font-family:inherit}
.bp .lb .x:hover{background:rgba(255,255,255,.22)}
@media (max-width:880px){.bp .lb{align-items:flex-start;padding:80px 16px 40px}.bp .lb .box{flex-direction:column;align-items:center;gap:26px}
  .bp .lb .ad{width:min(100%, calc(70svh * var(--ar)))}.bp .lb .txt{flex:none;width:100%;max-width:520px}}
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

// Types `text` in once it scrolls into view. The untyped rest is rendered transparent so the
// layout never jumps; reduced-motion users get the full text at once.
function Type({ text, speed = 42, delay = 0, as: Tag = "span", className, style }) {
  const ref = useRef(null);
  const chars = useMemo(() => Array.from(text || ""), [text]);
  const reduce = typeof window !== "undefined" && window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;
  const [n, setN] = useState(reduce ? chars.length : 0);
  const [go, setGo] = useState(false);
  useEffect(() => {
    const el = ref.current;
    if (!el || reduce) return;
    const io = new IntersectionObserver(([e]) => { if (e.isIntersecting) { setGo(true); io.disconnect(); } }, { threshold: 0.5 });
    io.observe(el);
    return () => io.disconnect();
  }, [reduce]);
  useEffect(() => {
    if (!go) return;
    let i = 0, t;
    const tick = () => { i += 1; setN(i); if (i < chars.length) t = setTimeout(tick, speed); };
    t = setTimeout(tick, delay);
    return () => clearTimeout(t);
  }, [go, chars, speed, delay]);
  return (
    <Tag ref={ref} className={className} style={style} aria-label={text}>
      <span aria-hidden="true">{chars.slice(0, n).join("")}</span>
      {go && n < chars.length && <span className="ty-caret" aria-hidden="true" />}
      <span className="ty-rest" aria-hidden="true">{chars.slice(n).join("")}</span>
    </Tag>
  );
}
const typeMs = (t, speed = 42) => Array.from(t || "").length * speed;

// Campaign strip: drifts on its own, stops the moment a finger or mouse touches it, can be swiped
// either way, and picks the drift back up a moment after release. Content is doubled for a seamless loop.
function Strip({ children }) {
  const ref = useRef(null);
  const held = useRef(false);
  const pos = useRef(0);
  const resume = useRef(0);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    let raf, last = performance.now();
    const half = () => el.scrollWidth / 2;
    const step = (t) => {
      const dt = Math.min(64, t - last); last = t;
      if (!held.current && half() > 0) {
        pos.current += dt * 0.045;
        if (pos.current >= half()) pos.current -= half();
        el.scrollLeft = pos.current;
      }
      raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
    const hold = () => { held.current = true; clearTimeout(resume.current); };
    const release = () => { clearTimeout(resume.current); resume.current = setTimeout(() => { pos.current = el.scrollLeft; held.current = false; }, 2200); };
    const onScroll = () => {
      if (!held.current) return;
      if (el.scrollLeft <= 1) el.scrollLeft += half();          // swiping back past the start wraps
      else if (el.scrollLeft >= half() * 1.5) el.scrollLeft -= half();
      pos.current = el.scrollLeft;
    };
    const onWheel = () => { hold(); release(); };
    const on = [["pointerdown", hold], ["touchstart", hold], ["pointerup", release], ["pointercancel", release],
      ["touchend", release], ["wheel", onWheel], ["mouseenter", hold], ["mouseleave", release], ["scroll", onScroll]];
    on.forEach(([ev, fn]) => el.addEventListener(ev, fn, { passive: true }));
    return () => { cancelAnimationFrame(raf); clearTimeout(resume.current); on.forEach(([ev, fn]) => el.removeEventListener(ev, fn)); };
  }, []);
  return <div className="strip" ref={ref}><div className="track">{children}</div></div>;
}

function useCols() {
  const get = () => (typeof window === "undefined" ? 4 : window.innerWidth > 980 ? 4 : window.innerWidth > 540 ? 2 : 1);
  const [cols, setCols] = useState(get);
  useEffect(() => {
    const on = () => setCols(get());
    window.addEventListener("resize", on);
    return () => window.removeEventListener("resize", on);
  }, []);
  return cols;
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

const chunk = (xs, n) => Array.from({ length: Math.ceil(xs.length / n) }, (_, i) => xs.slice(i * n, i * n + n));

export default function ClientPitch({ slug: fixedSlug }) {
  const params = useParams();
  const slug = fixedSlug || params.slug;
  const r = REPORTS[slug];
  const y = useScrollY();
  const [open, setOpen] = useState(null);
  const cols = useCols();
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

  useEffect(() => {
    if (!open) return;
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => { document.body.style.overflow = prev; };
  }, [open]);

  if (!r) {
    return <div style={{ minHeight: "100vh", display: "grid", placeItems: "center", fontFamily: "Optimum", direction: "rtl" }}>העמוד לא נמצא.</div>;
  }
  const b = r.business;
  const strip = r.ads.filter((a) => [1, 5, 11, 14, 17, 20, 7, 10].includes(a.no));
  const h1a = r.hero_title?.[0] || "פרחים נובלים.";
  const h1b = r.hero_title?.[1] || "זהב נשאר.";
  const two = (a, b2, speed = 42) => (<><Type className="b" text={a} speed={speed} /><Type className="l" text={b2} speed={speed} delay={typeMs(a, speed) + 200} /></>);

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
            <Type className="b" text={h1a} delay={700} speed={70} />
            <Type className="l" text={h1b} delay={700 + typeMs(h1a, 70) + 250} speed={70} />
          </h1>
          <div className="script sig fadein d4">{b.owner_first}</div>
        </div>
      </section>

      {/* campaign strip */}
      <section className="marquee" id="campaign">
        <div className="wrap head reveal">
          <div>
            <div className="eyebrow">הקמפיין</div>
            <h2><Type text={`${r.ads.length} מודעות. `} /><Type className="l" text="חמש זוויות. מותג אחד." delay={typeMs(`${r.ads.length} מודעות. `) + 150} /></h2>
          </div>
        </div>
        <Strip>
          {[...strip, ...strip].map((a, i) => (
            <div key={i} className="it" onClick={() => setOpen(a)} style={{ cursor: "zoom-in", "--ar": a.spec.w / a.spec.h }}>
              <AdCanvas spec={a.spec} img={a.img} brand={b.name} />
            </div>
          ))}
        </Strip>
      </section>

      {/* editorial split */}
      <section className="split" id="collection">
        <div className="img" style={{ backgroundImage: `url(${ad(5)?.img})` }} />
        <div className="txt reveal">
          <div className="eyebrow">יהלום מעבדה</div>
          <h2><Type className="b" text="אותו יהלום." /><Type className="l" text="אותו ברק." delay={typeMs("אותו יהלום.") + 200} /><Type className="l" text="בלי המכרה." delay={typeMs("אותו יהלום.אותו ברק.") + 400} /></h2>
          <p>סוליטר 1.50 קראט בחיתוך רדיאנט מוארך, בשיבוץ כוס חלק מזהב 14K. אותו פחמן, אותה קשיות, אותו ברק.</p>
          <div className="price">5,300 ש״ח</div>
        </div>
      </section>

      {/* quote band */}
      <section className="band">
        <div className="bg" style={{ backgroundImage: `url(${ad(3)?.img})`, transform: `translateY(${(y - 2200) * 0.12}px)` }} />
        <div className="shade" />
        <div className="q reveal">
          <Type as="div" className="script" text="כל תכשיט מתחיל אצלי בסקיצה." speed={60} />
          <div className="by">{b.name} · שינקין 48, תל אביב</div>
        </div>
      </section>

      {/* the pitch */}
      <section className="intro">
        <div className="wrap g">
          <div className="reveal">
            <div className="eyebrow">מה ראינו</div>
            <h2>{two("התכשיטים שלך ברמה של מגזין.", "המודעות עוד לא.")}</h2>
          </div>
          <p className="reveal">עברנו על המודעות הפעילות שלך בספריית המודעות של מטא, על האתר ועל הקולקציות. זה מה שבלט לנו, ומזה בנינו את הקמפיין שראית למעלה.</p>
        </div>
      </section>
      <section className="wrap ins">
        {r.insights.map((it, i) => (
          <div key={i} className="reveal" style={{ transitionDelay: `${i * 100}ms` }}>
            <div className="n">0{i + 1}</div>
            <Type as="h3" text={it.t} delay={i * 250} />
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
                <Type as="h3" text={ang.name} />
                <Type as="div" className="hook" text={`״${ang.hook}״`} delay={typeMs(ang.name) + 250} speed={30} />
                <p className="idea">{ang.idea}</p>
              </div>
            </div>
            {/* rows of `cols` ads, each row justified so every image in it has the same height */}
            <div className="ads">
              {chunk(byAngle[ang.id] || [], cols).map((row, ri) => (
                <div key={ri} className="row">
                  {row.map((a, k) => (
                    <div key={a.no} className="card reveal" style={{ transitionDelay: `${k * 90}ms`, flex: `${(a.spec.w / a.spec.h) * 100} 1 0` }} onClick={() => setOpen(a)}>
                      <AdCanvas spec={a.spec} img={a.img} brand={b.name} />
                    </div>
                  ))}
                </div>
              ))}
            </div>
          </div>
        </section>
      ))}

      <section className="cta">
        <div className="wrap reveal">
          <div className="eyebrow" style={{ color: "#d9c49a" }}>השלב הבא</div>
          <h2>{two(`${b.owner_first}, רוצה לראות`, "את זה באוויר?")}</h2>
          <p>נעלה את המודעות, נבדוק מה עובד הכי טוב, ונגדיל את מה שמוכר.</p>
          {r.contact_url
            ? <a className="btn" href={r.contact_url} target="_blank" rel="noreferrer">לשיחה קצרה בוואטסאפ</a>
            : <span className="btn" style={{ opacity: 0.5 }}>לשיחה קצרה בוואטסאפ</span>}
        </div>
      </section>
      <footer>הוכן במיוחד עבור {b.name}</footer>

      {open && (
        <div className="lb" onClick={() => setOpen(null)}>
          <button className="x" aria-label="סגירה" onClick={(e) => { e.stopPropagation(); setOpen(null); }}>✕</button>
          <div className="box" onClick={(e) => e.stopPropagation()}>
            <div className="ad" style={{ "--ar": open.spec.w / open.spec.h }}><AdCanvas key={open.no} spec={open.spec} img={open.img} brand={b.name} eager /></div>
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
