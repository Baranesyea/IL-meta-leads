import React, { useEffect, useRef } from "react";

// Home page — Eran's "about" page: who he is, how he works, what a business gets, the fixed monthly price.
// Content grown from the "למה לעבוד איתי" section of the client pages (ClientPitch.jsx → OFFER).
// Photos: Higgsfield Soul "Eran" generations, exported to /public/home. Fonts: Optimum (see index.css).
const WA = "https://wa.me/972545471522";

const CSS = `
.hp{--ivory:#f4eee4;--paper:#faf7f1;--ink:#17120d;--muted:#6d6257;--gold:#b08a4a;--night:#131517;
  font-family:Optimum,Georgia,serif;color:var(--ink);background:var(--ivory);direction:rtl;overflow-x:hidden}
.hp *{box-sizing:border-box}
.hp .wrap{max-width:1240px;margin:0 auto;padding:0 32px}
.hp .eyebrow{font-weight:400;font-size:15px;letter-spacing:.08em;color:var(--gold)}
.hp .btn{display:inline-flex;align-items:center;gap:12px;padding:17px 30px;border-radius:999px;font-weight:400;font-size:18px;
  text-decoration:none;transition:transform .25s ease,background .25s ease,color .25s ease}
.hp .btn:hover{transform:translateY(-2px)}
.hp .btn.gold{background:var(--gold);color:#fff}
.hp .btn.gold:hover{background:#9a7638}
.hp .btn.line{border:1px solid rgba(255,255,255,.45);color:#fff}
.hp .btn.line:hover{background:#fff;color:var(--ink)}
.hp .btn.dark{background:var(--ink);color:var(--paper)}
.hp .btn svg{width:20px;height:20px}
.hp .reveal{opacity:0;transform:translateY(26px);transition:opacity .9s ease,transform .9s ease}
.hp .reveal.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.hp .reveal{opacity:1;transform:none;transition:none}}

/* top bar */
.hp .bar{position:absolute;top:0;inset-inline:0;z-index:5;display:flex;justify-content:space-between;align-items:center;
  padding:26px 32px;color:#fff}
.hp .bar .name{font-weight:900;font-size:22px;letter-spacing:.02em}
.hp .bar nav{display:flex;gap:28px;font-size:16px}
.hp .bar nav a{color:rgba(255,255,255,.8);text-decoration:none}
.hp .bar nav a:hover{color:#fff}

/* hero: one full-bleed photo, words on its dark side */
.hp .hero{position:relative;min-height:100svh;background:var(--night);color:#fff;overflow:hidden}
.hp .hero .bg{position:absolute;inset:0;background:url(/home/eran_desk.webp) left center/auto 100% no-repeat}
/* the photo's right edge melts into the page (photo width = 0.806 x its height) */
.hp .hero .bg{-webkit-mask-image:linear-gradient(90deg,#000 calc(80.6svh - 240px),transparent calc(80.6svh - 10px));mask-image:linear-gradient(90deg,#000 calc(80.6svh - 240px),transparent calc(80.6svh - 10px))}
.hp .hero .shade{position:absolute;inset:0;background:linear-gradient(270deg,rgba(19,21,23,.96) 0%,rgba(19,21,23,.75) 38%,rgba(19,21,23,0) 62%)}
.hp .hero .copy{position:relative;z-index:2;min-height:100svh;display:flex;flex-direction:column;justify-content:center;
  max-width:1240px;margin:0 auto;padding:120px 32px 80px}
.hp .hero .copy > *{max-width:560px}
.hp .hero h1{margin:18px 0 26px;line-height:1}
.hp .hero h1 .b{display:block;font-weight:900;font-size:clamp(48px,6.4vw,96px)}
.hp .hero h1 .l{display:block;font-weight:300;font-size:clamp(40px,5.4vw,80px);color:rgba(255,255,255,.88)}
.hp .hero .lead{font-weight:300;font-size:21px;line-height:1.7;color:rgba(255,255,255,.78);margin:0 0 36px}
.hp .hero .ctas{display:flex;gap:14px;flex-wrap:wrap}

/* numbers */
.hp .nums{background:var(--paper);border-bottom:1px solid #e1d7c8}
.hp .nums ul{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,1fr)}
.hp .nums li{padding:46px 24px;text-align:center;border-inline-start:1px solid #e6dccd}
.hp .nums li:first-child{border-inline-start:0}
.hp .nums .v{display:block;font-weight:900;font-size:clamp(40px,4.4vw,62px);line-height:1;color:var(--ink)}
.hp .nums .k{display:block;margin-top:12px;font-weight:300;font-size:17px;color:var(--muted)}

/* story */
.hp .story{padding:140px 0 130px}
.hp .story .g{display:grid;grid-template-columns:1.05fr .95fr;gap:90px;align-items:center}
.hp .story h2,.hp .gets-sec h2,.hp .how h2,.hp .end h2{margin:14px 0 28px;line-height:1.02}
.hp h2 .b{display:block;font-weight:900;font-size:clamp(38px,4.6vw,66px)}
.hp h2 .l{display:block;font-weight:300;font-size:clamp(32px,3.9vw,56px)}
.hp .story p{font-weight:300;font-size:21px;line-height:1.8;color:var(--muted);margin:0 0 18px;max-width:46ch}
.hp .story p strong{font-weight:400;color:var(--ink)}
.hp .story .ph{position:relative;border-radius:4px;overflow:hidden;aspect-ratio:3/4;background:#ddd}
.hp .story .ph img{width:100%;height:100%;object-fit:cover;display:block}

/* what you get */
.hp .gets-sec{background:var(--paper);padding:130px 0 120px;border-top:1px solid #e1d7c8}
.hp .gets-sec .head{display:grid;grid-template-columns:1fr 1fr;gap:80px;align-items:end;margin-bottom:40px}
.hp .gets-sec .head p{font-weight:300;font-size:20px;line-height:1.75;color:var(--muted);margin:0}
.hp .gets{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:0 48px}
.hp .gets li{padding:34px 0;border-top:1px solid #dccfbd}
.hp .gets .n{display:block;font-weight:300;font-size:36px;line-height:1;color:var(--gold);margin-bottom:18px}
.hp .gets h3{font-weight:900;font-size:22px;margin:0 0 10px;line-height:1.3}
.hp .gets p{font-weight:300;font-size:17px;line-height:1.7;color:var(--muted);margin:0}

/* how it starts */
.hp .how{padding:130px 0 120px}
.hp .how .steps{list-style:none;margin:50px 0 0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:28px;counter-reset:s}
.hp .how .steps li{background:var(--paper);border:1px solid #e1d7c8;border-radius:4px;padding:40px 34px 38px}
.hp .how .steps .n{font-weight:300;font-size:44px;color:var(--gold);line-height:1}
.hp .how .steps h3{font-weight:900;font-size:24px;margin:16px 0 12px;line-height:1.25}
.hp .how .steps p{font-weight:300;font-size:18px;line-height:1.7;color:var(--muted);margin:0}

/* price */
.hp .price{background:var(--ink);color:var(--paper);padding:120px 0}
.hp .price .g{display:grid;grid-template-columns:1fr 1fr;gap:80px;align-items:center}
.hp .price h2{margin:14px 0 0;line-height:1.05}
.hp .price h2 .l{color:rgba(250,247,241,.75)}
.hp .price p{font-weight:300;font-size:21px;line-height:1.8;color:rgba(250,247,241,.8);margin:0 0 30px}
.hp .price ul{list-style:none;margin:0 0 36px;padding:0;display:flex;flex-wrap:wrap;gap:10px}
.hp .price li{border:1px solid rgba(250,247,241,.28);border-radius:999px;padding:9px 18px;font-size:16px;color:rgba(250,247,241,.9)}

/* closing */
.hp .end{background:#e9dfd0;overflow:hidden}
.hp .end .g{display:grid;grid-template-columns:1fr 1fr;align-items:end;gap:40px}
.hp .end .txt{padding:130px 0 120px}
.hp .end p{font-weight:300;font-size:21px;line-height:1.75;color:var(--muted);margin:0 0 34px;max-width:40ch}
.hp .end .ph{align-self:end;height:100%;min-height:560px;background:url(/home/eran_point.webp) center bottom/cover no-repeat}
.hp footer{background:var(--ivory);padding:34px 0;text-align:center;font-size:15px;color:var(--muted);border-top:1px solid #e1d7c8}
.hp footer a{color:var(--muted)}

@media (max-width:980px){
  .hp .story .g,.hp .gets-sec .head,.hp .price .g,.hp .end .g{grid-template-columns:1fr;gap:40px}
  .hp .gets{grid-template-columns:1fr 1fr}
  .hp .how .steps{grid-template-columns:1fr}
  .hp .end .txt{padding:100px 0 10px}
  .hp .end .ph{min-height:520px;background-position:center 20%}
}
/* phones and portrait screens: the photo fills the screen, words on its dark top */
@media (max-width:760px),(max-aspect-ratio:1/1){
  .hp .bar nav{display:none}
  /* the photo sits at the bottom, full width; its dark wall continues the page colour, so the words above
     it never reach the face */
  .hp .hero .bg{background:url(/home/eran_desk.webp) center bottom/100% auto no-repeat}
  /* soft top edge instead of a hard line where the photo starts (photo height = 1.24 x screen width) */
  .hp .hero .bg{-webkit-mask-image:linear-gradient(180deg,transparent calc(100% - 124vw),#000 calc(100% - 124vw + 40px));mask-image:linear-gradient(180deg,transparent calc(100% - 124vw),#000 calc(100% - 124vw + 40px))}
  .hp .hero .shade{background:linear-gradient(180deg,rgba(19,21,23,1) 0%,rgba(19,21,23,1) 30%,rgba(19,21,23,0) 52%)}
  .hp .hero .copy{justify-content:flex-start;padding:96px 24px 40px}
  .hp .hero .lead{display:none}
  .hp .hero .ctas{gap:10px}
}
/* portrait tablets: a smaller photo, centred at the bottom, sides fading into the page */
@media (min-width:761px) and (max-aspect-ratio:1/1){
  .hp .hero .bg{background-size:auto 74%;
    -webkit-mask-image:linear-gradient(90deg,transparent 12%,#000 26%,#000 74%,transparent 88%),linear-gradient(180deg,transparent 26%,#000 28%);
    -webkit-mask-composite:source-in;
    mask-image:linear-gradient(90deg,transparent 12%,#000 26%,#000 74%,transparent 88%),linear-gradient(180deg,transparent 26%,#000 28%);
    mask-composite:intersect}
}
@media (max-width:760px){
  .hp .wrap{padding:0 22px}
  .hp .bar{padding:22px}
  .hp .hero h1{margin:12px 0 22px}
  .hp .btn{padding:15px 24px;font-size:17px}
  .hp .nums ul{grid-template-columns:1fr 1fr}
  .hp .nums li{padding:32px 14px;border-top:1px solid #e6dccd}
  .hp .nums li:nth-child(odd){border-inline-start:0}
  .hp .story,.hp .gets-sec,.hp .how{padding:90px 0 80px}
  .hp .story p,.hp .end p,.hp .price p{font-size:19px}
  .hp .gets{grid-template-columns:1fr}
  .hp .gets li{padding:26px 0}
  .hp .price{padding:90px 0}
  .hp .end .ph{min-height:440px}
}
@media (max-width:760px) and (max-height:700px){
  .hp .hero h1 .b{font-size:40px}.hp .hero h1 .l{font-size:34px}.hp .hero .copy{padding-top:76px}
  .hp .hero .eyebrow{font-size:13px}.hp .hero .btn.line{display:none}
}
`;

const GETS = [
  ["אופטימיזציה פעילה, כל שבוע", "בחשבון המודעות ובעמודי המוצר שאליהם המודעות מביאות. לא מנחשים: מוצאים מה מזיז את המחט, ועושים ממנו יותר."],
  ["לפחות 10 קריאייטיבים חדשים בשבוע", "כל אחד עם סיבה ברורה למה הוא נבנה. הם נבדקים בחשבון, והמנצחים מקבלים יותר תקציב."],
  ["דוח שבועי קצר וברור", "מה עבד, מה פחות, מה התוצאות ומה ההמלצות לשבוע הבא. עם סיכום של כמה שורות, בלי לבזבז זמן."],
  ["מבצעים לחגים ולהזדמנויות", "קמפיין מוכן בזמן לכל חג ולכל מבצע מיוחד."],
  ["עמודי נחיתה כשצריך", "בעיצוב איכותי ומזמין. זה חלק מהאסטרטגיה, לא תוספת בתשלום."],
  ["מדידה מדויקת", "הטמעה ובדיקה של כלי המדידה בנכסים שלכם, כדי שכל החלטה תישען על מספרים אמיתיים."],
];

const STEPS = [
  ["אני עובר על מה שרץ אצלכם", "המודעות הפעילות, האתר והמוצרים. מה כבר עובד, ומה משאיר כסף על השולחן."],
  ["אתם מקבלים עמוד עם קמפיין שלם", "מה הייתי משנה, חמש זוויות חדשות ו-20 מודעות מוכנות על המוצרים שלכם. בחינם, בלי התחייבות."],
  ["מתחילים לעבוד", "מחיר חודשי קבוע, קריאייטיבים חדשים כל שבוע, ודוח קצר שמראה בדיוק לאן הכסף הולך."],
];

const WaIcon = () => (
  <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3Z"/></svg>
);

function useReveal() {
  const ref = useRef(null);
  useEffect(() => {
    const els = ref.current?.querySelectorAll(".reveal") || [];
    if (!("IntersectionObserver" in window)) { els.forEach((e) => e.classList.add("in")); return; }
    const io = new IntersectionObserver((es) => es.forEach((e) => {
      if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
    }), { threshold: 0.12 });
    els.forEach((e) => io.observe(e));
    return () => io.disconnect();
  }, []);
  return ref;
}

export default function Home() {
  const ref = useReveal();
  useEffect(() => { document.title = "ערן · קמפיינים במטא למותגי מוצר"; }, []);
  return (
    <main className="hp" ref={ref}>
      <style>{CSS}</style>

      <header className="bar">
        <span className="name">ערן</span>
        <nav>
          <a href="#story">מי אני</a>
          <a href="#gets">מה מקבלים</a>
          <a href="#how">איך מתחילים</a>
          <a href="#price">מחיר</a>
        </nav>
      </header>

      <section className="hero">
        <div className="bg" role="img" aria-label="ערן ליד שולחן העבודה" />
        <div className="shade" />
        <div className="copy">
          <div className="eyebrow">קמפיינים במטא לעסקים שמוכרים מוצרים</div>
          <h1><span className="b">קוראים לי ערן.</span><span className="l">17 שנה במרקטינג.</span></h1>
          <p className="lead">אני בונה ומנהל קמפיינים לעסקים שמוכרים מוצרים. ישירות מולכם, בלי צוות באמצע, במחיר חודשי קבוע שהכל כלול בו.</p>
          <div className="ctas">
            <a className="btn gold" href={WA} target="_blank" rel="noopener noreferrer"><WaIcon />בואו נדבר בוואטסאפ</a>
            <a className="btn line" href="#gets">מה מקבלים</a>
          </div>
        </div>
      </section>

      <section className="nums">
        <ul className="wrap">
          <li className="reveal"><span className="v">17</span><span className="k">שנים במרקטינג</span></li>
          <li className="reveal"><span className="v">10+</span><span className="k">קריאייטיבים חדשים בשבוע</span></li>
          <li className="reveal"><span className="v">1</span><span className="k">דוח קצר וברור בשבוע</span></li>
          <li className="reveal"><span className="v">0</span><span className="k">תוספות בחשבונית</span></li>
        </ul>
      </section>

      <section className="story" id="story">
        <div className="wrap g">
          <div className="reveal">
            <div className="eyebrow">מי אני</div>
            <h2><span className="b">העולם השתנה.</span><span className="l">גם הדרך שלי לעבוד.</span></h2>
            <p>ניהלתי אנשים וצוותים, ייעצתי לסוכנויות והייתי <strong>בעלים של סוכנות דיגיטל</strong>.</p>
            <p>אבל העולם השתנה. עם הכלים של היום אפשר לעבוד הרבה יותר מהר, <strong>בלי צוות שלם באמצע</strong>.</p>
            <p>ככה אני עובד היום: ישירות מולכם, עם יותר קריאייטיב, יותר בדיקות ותשובות מהירות. בלי שכבות, ובלי שהכסף שלכם הולך על ישיבות.</p>
          </div>
          <div className="ph reveal"><img src="/home/eran_report.webp" alt="ערן מחזיק דוח קמפיין" loading="lazy" /></div>
        </div>
      </section>

      <section className="gets-sec" id="gets">
        <div className="wrap">
          <div className="head reveal">
            <div>
              <div className="eyebrow">מה מקבלים</div>
              <h2><span className="b">שישה דברים</span><span className="l">שקורים כל חודש.</span></h2>
            </div>
            <p>לא חבילה עם כוכביות. זה מה שאתם מקבלים כשעובדים איתי, בכל חודש, בלי תוספות ובלי הפתעות בחשבונית.</p>
          </div>
          <ul className="gets">
            {GETS.map(([t, d], i) => (
              <li key={t} className="reveal">
                <span className="n">{String(i + 1).padStart(2, "0")}</span>
                <h3>{t}</h3>
                <p>{d}</p>
              </li>
            ))}
          </ul>
        </div>
      </section>

      <section className="how" id="how">
        <div className="wrap">
          <div className="reveal">
            <div className="eyebrow">איך מתחילים</div>
            <h2><span className="b">קודם אני מראה.</span><span className="l">אחר כך מדברים על כסף.</span></h2>
          </div>
          <ol className="steps">
            {STEPS.map(([t, d], i) => (
              <li key={t} className="reveal">
                <span className="n">{i + 1}</span>
                <h3>{t}</h3>
                <p>{d}</p>
              </li>
            ))}
          </ol>
        </div>
      </section>

      <section className="price" id="price">
        <div className="wrap g">
          <div className="reveal">
            <div className="eyebrow">מחיר</div>
            <h2><span className="b">מחיר חודשי קבוע.</span><span className="l">הכל כלול.</span></h2>
          </div>
          <div className="reveal">
            <p>בלי תשלום על כלים, בלי חיובים על עבודה נוספת ובלי ספקים נוספים. מחיר שאתם יכולים להרשות לעצמכם, ושמחזיר את עצמו בבירור, כי המטרה היא שהקמפיין יכניס הרבה יותר ממה שהוא עולה.</p>
            <ul><li>בלי תשלום על כלים</li><li>בלי עבודה נוספת בחיוב</li><li>בלי ספקים נוספים</li></ul>
            <a className="btn gold" href={WA} target="_blank" rel="noopener noreferrer"><WaIcon />לשאול על המחיר בוואטסאפ</a>
          </div>
        </div>
      </section>

      <section className="end">
        <div className="wrap g">
          <div className="txt reveal">
            <div className="eyebrow">בואו נדבר</div>
            <h2><span className="b">רוצים לראות</span><span className="l">מה אפשר לעשות עם המודעות שלכם?</span></h2>
            <p>שלחו לי הודעה עם שם העסק. אני אעבור על מה שרץ אצלכם היום, ואחזור עם דברים שהייתי משנה כבר מחר.</p>
            <a className="btn dark" href={WA} target="_blank" rel="noopener noreferrer"><WaIcon />בואו נדבר בוואטסאפ</a>
          </div>
          <div className="ph" role="img" aria-label="ערן מצביע למעלה" />
        </div>
      </section>

      <footer>ערן · קמפיינים במטא למותגי מוצר · <a href={WA} target="_blank" rel="noopener noreferrer">וואטסאפ</a></footer>
    </main>
  );
}
