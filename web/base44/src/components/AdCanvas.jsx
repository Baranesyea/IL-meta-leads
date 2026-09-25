import React, { useLayoutEffect, useRef, useState } from "react";

// Renders one ad exactly like the IL-meta-leads overlay engine (templates/overlay.html.j2):
// a 1080px-wide canvas (photo + typography direction), scaled down to the container width.
// `spec` comes from the pipeline: direction, box, colours, headline, sub, note, signature…
// Legibility is measured in the pipeline (src/overlay.py legibility/brand_line): `scrim` and
// `plate_bg` carry the strength needed for the text to hold contrast on the real pixels,
// and `brand_color` is null when the brand line would sit on a busy area.

const CSS = `
.adc-wrap{position:relative;width:100%;overflow:hidden}
.adc{position:absolute;top:0;right:0;transform-origin:top right;overflow:hidden;direction:rtl}
.adc *{box-sizing:border-box}
.adc .photo{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.adc .zone{position:absolute;display:flex;flex-direction:column}
.adc .fit{white-space:nowrap}
.adc .brand{position:absolute;left:0;right:0;text-align:center;font-family:Optimum;font-weight:400;font-size:34px;letter-spacing:2px}
.adc .scrim{position:absolute;left:0;right:0}
.adc .sig,.adc .hand{-webkit-text-stroke:1.4px currentColor}
.adc.contrast .l1{font-family:Optimum;font-weight:900;font-size:112px;line-height:.95;letter-spacing:-1px}
.adc.contrast .l2{font-family:Optimum;font-weight:300;font-size:72px;line-height:1.1;margin-top:10px}
.adc.contrast .sub{font-family:Optimum;font-weight:400;font-size:38px;letter-spacing:1px;margin-top:26px}
.adc.contrast .zone{text-align:right}
.adc.quiet .zone{text-align:center;align-items:center}
.adc.quiet .hl{font-family:Optimum;font-weight:400;font-size:84px;line-height:1.2}
.adc.quiet .sig{font-family:Idealist;font-size:120px;margin-top:6px;line-height:1}
.adc.quiet .sub{font-family:Optimum;font-weight:400;font-size:38px;letter-spacing:1px;margin-top:14px}
.adc.stack .zone{text-align:right}
.adc.stack .l{font-family:Optimum;font-weight:900;font-size:170px;line-height:.9;letter-spacing:-2px}
.adc.stack .l.light{font-weight:300}
.adc.stack .sub{font-family:Optimum;font-weight:400;font-size:38px;letter-spacing:1px;margin-top:22px}
.adc.note .zone{text-align:right}
.adc.note .hand{font-family:Idealist;font-size:124px;line-height:1.05}
.adc.note .rule{width:90px;height:1.5px;opacity:.6;margin:22px 0 16px auto}
.adc.note .sub{font-family:Optimum;font-weight:400;font-size:38px;letter-spacing:1px}
.adc.note .hl{font-family:Optimum;font-weight:900;font-size:62px;margin-top:6px}
.adc.cover .frame{position:absolute;inset:34px;border:1.5px solid;opacity:.55}
.adc.cover .mast{position:absolute;left:0;right:0;text-align:center;font-family:Optimum;font-weight:900;font-size:30px;letter-spacing:6px}
.adc.cover .zone{text-align:center;align-items:center}
.adc.cover .hl{font-family:Optimum;font-weight:400;font-size:78px;line-height:1.08}
.adc.cover .sub{font-family:Optimum;font-weight:900;font-size:36px;letter-spacing:2px;margin-top:22px}
.adc.panel .pnl{position:absolute;display:flex;flex-direction:column;justify-content:center;padding:0 64px;text-align:right}
.adc.panel .hl{font-family:Optimum;font-weight:900;font-size:72px;line-height:1.05}
.adc.panel .l2{font-weight:300}
.adc.panel .sub{font-family:Optimum;font-weight:400;font-size:38px;letter-spacing:1px;margin-top:22px}
.adc.panel .sig{font-family:Idealist;font-size:104px;margin-top:10px;line-height:1}
.adc.label .zone{text-align:right}
.adc.label .card{display:inline-block;align-self:flex-start;max-width:600px}
.adc.label .hl{font-family:Optimum;font-weight:900;font-size:74px;line-height:1.12}
.adc.label .rule{width:100%;height:1px;opacity:.5;margin:20px 0}
.adc.label .sub{font-family:Optimum;font-weight:400;font-size:38px;line-height:1.5}
`;

let cssInjected = false;
function injectCss() {
  if (cssInjected || typeof document === "undefined") return;
  const el = document.createElement("style");
  el.textContent = CSS;
  document.head.appendChild(el);
  cssInjected = true;
}

export default function AdCanvas({ spec, img, brand, eager = false }) {
  injectCss();
  const wrapRef = useRef(null);
  const adRef = useRef(null);
  const [scale, setScale] = useState(0.3);
  const { w, h, direction: d, box, top, ink, paper, obj_pos, plate, plate_bg, scrim, brand_color } = spec;
  const lines = (spec.headline || "").split("<br>");
  const onDark = ink === "#f4ecdf";

  // scale the 1080px canvas to the card width
  useLayoutEffect(() => {
    const el = wrapRef.current;
    if (!el) return;
    const ro = new ResizeObserver(() => setScale(el.clientWidth / w));
    ro.observe(el);
    return () => ro.disconnect();
  }, [w]);

  // same fitting pass as the image renderer: shrink lines to the box width, then make the block fit
  // its height — drop the signature, then the sub line, before shrinking the headline
  useLayoutEffect(() => {
    let cancelled = false;
    document.fonts.ready.then(() => {
      const root = adRef.current;
      if (cancelled || !root) return;
      for (const el of root.querySelectorAll(".fit, .fitw")) {
        const bx = el.closest(".zone, .pnl");
        if (!bx) continue;
        let size = parseFloat(getComputedStyle(el).fontSize);
        el.style.display = "inline-block";
        while (el.scrollWidth > bx.clientWidth && size > 18) { size -= 2; el.style.fontSize = size + "px"; }
        el.style.display = "";
      }
      for (const z of root.querySelectorAll(".zone, .pnl")) {
        for (const sel of [".sig", ".sub"]) {
          if (z.scrollHeight <= z.clientHeight + 2) break;
          z.querySelectorAll(sel).forEach((el) => (el.style.display = "none"));
        }
        let guard = 0;
        while (z.scrollHeight > z.clientHeight + 2 && guard++ < 30) {
          for (const el of z.querySelectorAll("*")) {
            const fs = parseFloat(getComputedStyle(el).fontSize);
            if (fs > 22) el.style.fontSize = fs * 0.94 + "px";
          }
        }
      }
    });
    return () => { cancelled = true; };
  }, [spec]);

  const zoneStyle = plate
    ? { maxWidth: box[2] - box[0], right: w - box[2], padding: "30px 38px", backdropFilter: "blur(12px)",
        background: plate_bg || (onDark ? "rgba(14,11,8,.66)" : "rgba(250,246,238,.84)"),
        ...(top ? { top: box[1] } : { bottom: h - box[3] }) }
    : { left: box[0], top: box[1], width: box[2] - box[0], height: box[3] - box[1],
        justifyContent: top ? "flex-start" : "flex-end" };
  if (onDark) zoneStyle.textShadow = "0 2px 18px rgba(0,0,0,.45)";

  // scrim holds its measured strength across the whole text box, then fades out
  const hold = top ? box[3] + 20 : h - box[1] + 20;
  const scrimStyle = {
    ...(top ? { top: 0, height: hold + 180 } : { bottom: 0, height: hold + 180 }),
    background: `linear-gradient(${top ? "to bottom" : "to top"}, ${scrim} 0, ${scrim} ${hold}px, transparent)`,
  };

  const photoStyle = { objectPosition: obj_pos };
  if (d === "panel") Object.assign(photoStyle, { height: Math.floor(h * 0.68) });
  const brandStyle = {
    ...(d === "panel" ? { top: 40 } : { [top ? "bottom" : "top"]: 54 }),
    color: brand_color,
    textShadow: brand_color === "#f4ecdf" ? "0 1px 12px rgba(0,0,0,.5)" : "none",
  };

  return (
    <div ref={wrapRef} className="adc-wrap" style={{ aspectRatio: `${w} / ${h}` }}>
      <div ref={adRef} className={`adc ${d}`}
           style={{ width: w, height: h, transform: `scale(${scale})`, background: paper, color: ink }}>
        <img className="photo" src={img} alt="" style={photoStyle} loading={eager ? "eager" : "lazy"} />
        {d === "panel" ? (
          <div className="pnl" style={{ left: 0, right: 0, bottom: 0, height: Math.floor(h * 0.32), background: paper }}>
            <div className="hl fitw">{lines[0]}{lines.length > 1 && (<><br /><span className="l2">{lines.slice(1).join(" ")}</span></>)}</div>
            {spec.sub && <div className="sub">{spec.sub}</div>}
            {spec.signature && <div className="sig">{spec.signature}</div>}
          </div>
        ) : (
          <>
            {!plate && <div className="scrim" style={scrimStyle} />}
            {d === "cover" && (<>
              <div className="frame" style={{ borderColor: ink }} />
              <div className="mast" style={{ [top ? "bottom" : "top"]: 64, color: ink }}>{brand}</div>
            </>)}
            <div className="zone" style={zoneStyle}>
              {d === "contrast" && (<>
                <div className="l1 fit">{lines[0]}</div>
                {lines.length > 1 && <div className="l2 fit">{lines.slice(1).join(" ")}</div>}
                {spec.sub && <div className="sub">{spec.sub}</div>}
              </>)}
              {d === "quiet" && (<>
                <div className="hl">{lines.map((l, i) => <div key={i}>{l}</div>)}</div>
                {spec.signature && <div className="sig">{spec.signature}</div>}
                {spec.sub && <div className="sub">{spec.sub}</div>}
              </>)}
              {d === "stack" && (<>
                {lines.map((l, i) => <div key={i} className={`l fit ${i === 1 ? "light" : ""}`}>{l}</div>)}
                {spec.sub && <div className="sub">{spec.sub}</div>}
              </>)}
              {d === "note" && (<>
                <div className="hand">{spec.note || lines.join(" ")}</div>
                <div className="rule" style={{ background: ink }} />
                {spec.note && <div className="hl">{lines.join(" ")}</div>}
                {spec.sub && <div className="sub">{spec.sub}</div>}
              </>)}
              {d === "cover" && (<>
                <div className="hl">{lines.map((l, i) => <div key={i}>{l}</div>)}</div>
                {spec.sub && <div className="sub">{spec.sub}</div>}
              </>)}
              {d === "label" && (
                <div className="card">
                  <div className="hl">{lines.map((l, i) => <div key={i}>{l}</div>)}</div>
                  <div className="rule" style={{ background: ink }} />
                  {spec.sub && <div className="sub">{spec.sub.split(" · ").map((s, i) => <div key={i}>{s}</div>)}</div>}
                </div>
              )}
            </div>
          </>
        )}
        {brand && brand_color && d !== "cover" && <div className="brand" style={brandStyle}>{brand}</div>}
      </div>
    </div>
  );
}
