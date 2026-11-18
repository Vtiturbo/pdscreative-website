"""Rebuilds the <main> content and quote builder of ../../pricing.html from prices.py. Run: python3 build_page.py"""
import html, json, pathlib, re
import prices as P

ROOT = pathlib.Path(__file__).resolve().parents[2]
PAGE = ROOT / "pricing.html"
e = html.escape
gbp = lambda v: f"£{v:,}"
pct = lambda p, l: round((1 - p / l) * 100)

lo_pkg = min(p["price"] for p in P.PACKAGES.values())
lo_site = min(s["price"] for s in P.SITES.values())
lo_care = min(c["price"] for c in P.CARE.values())
DESC = f"Complete brand packages from {gbp(lo_pkg)}: logo, custom-coded website, photography, video, social media and adverts, ready in 5 days. Around 30% below typical London rates."

CSS = """/* GEN-PRICING-CSS:start (tools/pricing/build_page.py) */
.lon{display:block;color:#7FD3A6;font-size:.8rem;margin-top:2px}
.q-card .lon{margin-top:0}
.pk-inc{font-size:.8rem;color:var(--ice)}
.q-x.locked{opacity:.55}
.q-x .inc{font:500 .72rem var(--f-mono);color:var(--ice);letter-spacing:.06em;text-transform:uppercase}
.q-opts.c3{grid-template-columns:repeat(3,minmax(0,1fr))}
@media (max-width:860px){.q-opts.c3{grid-template-columns:1fr}}
.cmp-tbl td.ok{color:#7FD3A6}
.pk-ref{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
@media (max-width:860px){.pk-ref{grid-template-columns:1fr}}
.pk-ref>div{border:1px solid var(--line);border-radius:18px;background:var(--deck);padding:22px;display:flex;flex-direction:column;gap:10px}
.pk-ref>div.pop{border-color:var(--ice)}
.pk-ref b.n{font:600 1.2rem var(--f-display)}
.pk-ref .pr{font:600 1.9rem var(--f-display);letter-spacing:-.02em}
.pk-ref ul{margin:0;padding-left:18px;color:var(--muted);font-size:.92rem;display:grid;gap:4px}
.pk-ref .row{display:flex;justify-content:space-between;font-size:.86rem;color:var(--muted);border-top:1px solid var(--line);padding-top:8px}
.pk-ref .row b{color:var(--fg)}
.pk-ref .row.ok b{color:#7FD3A6}
/* GEN-PRICING-CSS:end */"""


def li(items):
    return "".join(f"<li>{e(i)}</li>" for i in items)


def rows3(items):
    return "".join(f"<tr><th>{e(v['name'])}</th><td>{e(v.get('desc',''))}</td><td>{gbp(v['london'])}{v.get('unit','')}</td><td class=\"hl\">{gbp(v['price'])}{v.get('unit','')}</td></tr>" for v in items)


compare = [("Brand Launch package", P.PACKAGES["launch"]["price"], P.london_of_package(P.PACKAGES["launch"]), ""),
           (P.BRAND["kit"]["name"], P.BRAND["kit"]["price"], P.BRAND["kit"]["london"], ""),
           ("Signature website", P.SITES["signature"]["price"], P.SITES["signature"]["london"], ""),
           (P.SOCIAL["makeover"]["name"], P.SOCIAL["makeover"]["price"], P.SOCIAL["makeover"]["london"], ""),
           (P.PHOTO["half"]["name"], P.PHOTO["half"]["price"], P.PHOTO["half"]["london"], ""),
           (P.VIDEO["film"]["name"], P.VIDEO["film"]["price"], P.VIDEO["film"]["london"], ""),
           ("Growth care plan", P.CARE["growth"]["price"], P.CARE["growth"]["london"], "/mo")]
cmp_rows = "".join(f"<tr><th>{e(n)}</th><td>{gbp(l)}{u}</td><td class=\"hl\">{gbp(p)}{u}</td><td class=\"ok\">{pct(p, l)}% less</td></tr>" for n, p, l, u in compare)

pk_ref = ""
for k, p in P.PACKAGES.items():
    sep, lon = P.separate_of_package(p), P.london_of_package(p)
    pk_ref += f"""<div class="{'pop' if p.get('popular') else ''}"><b class="n">{e(p['name'])}{' <span class="q-tag">Most popular</span>' if p.get('popular') else ''}</b>
      <span style="color:var(--muted);font-size:.9rem">{e(p['best'])}</span>
      <span class="pr">{'From ' if p.get('from') else ''}{gbp(p['price'])}</span><span class="pk-inc">{e(p['days'])}</span>
      <ul>{li(p['lines'])}</ul>
      <div class="row"><span>Booked separately</span><b>{gbp(sep)}</b></div>
      <div class="row"><span>Typical London cost</span><b>{gbp(lon)}</b></div>
      <div class="row ok"><span>You save</span><b>{gbp(sep - p['price'])}</b></div></div>"""

site_head = "".join(f"<th{' class=\"hl\"' if s.get('popular') else ''}>{e(s['name'])}<small>{'From ' if s.get('from') else ''}{gbp(s['price'])}{' · Most popular' if s.get('popular') else ''}</small></th>" for s in P.SITES.values())
site_rows = [("Ideal for", [s["best"] for s in P.SITES.values()]), ("Live in", [s["days"] for s in P.SITES.values()])]
for i in range(5):
    site_rows.append(("" if i else "What's included", [s["feats"][i] for s in P.SITES.values()]))
site_rows.append(("Typical London price", [gbp(s["london"]) for s in P.SITES.values()]))
site_tbody = "".join("<tr><th>" + e(r) + "</th>" + "".join(f"<td{' class=\"hl\"' if list(P.SITES.values())[j].get('popular') else ''}>{e(v)}</td>" for j, v in enumerate(vals)) + "</tr>" for r, vals in site_rows)
extras = "".join(f"<tr><th>{e(v['name'])}</th><td>{gbp(v['price'])}</td></tr>" for v in P.EXTRAS.values())
care_head = "".join(f"<th{' class=\"hl\"' if c.get('popular') else ''}>{e(c['name'])}<small>{gbp(c['price'])}/mo · {e(c['best'])}</small></th>" for c in P.CARE.values())
care_body = "".join("<tr><th>" + e(r) + "</th>" + "".join(f"<td{' class=\"hl\"' if list(P.CARE.values())[j].get('popular') else ''}>{e(v)}</td>" for j, v in enumerate(vals)) + "</tr>" for r, vals in P.CARE_ROWS + [("Typical London price", [gbp(c["london"]) + "/mo" for c in P.CARE.values()])])
subs = "".join(f"<div{' class=\"pop\"' if s.get('popular') else ''}><b>{e(s['name'])}{' <span class=\"q-tag\" style=\"margin-left:6px\">Most popular</span>' if s.get('popular') else ''}</b><span class=\"pr\">{gbp(s['price'])}/mo</span><ul>{li(s['feats'])}</ul><span class=\"lon\">Typical London {gbp(s['london'])}/mo · {pct(s['price'], s['london'])}% less</span></div>" for s in P.SUBS.values())
bundles = ""
for b in P.BUNDLES:
    c, s = P.CARE[b["care"]], P.SUBS[b["sub"]]
    sep = c["price"] + s["price"]
    bundles += f"<tr><th>{e(b['name'])}</th><td>{e(c['name'])} care + {e(s['name'])} content</td><td>{gbp(sep)}/mo</td><td class=\"hl\">{gbp(b['price'])}/mo</td><td>{gbp(sep - b['price'])}/mo</td></tr>"

MAIN = f"""<main>
<section class="p-hero">
  <div class="wrap">
    <span class="eyebrow mono">Pricing &amp; packages · {P.EDITION}</span>
    <h1>We create the brand. <span class="grad">You're ready in 5 days.</span></h1>
    <p class="lede">Logo and branding, a custom-coded website, photography, video, a new social media look and adverts, all from one studio, and around 30% below typical London rates.</p>
    <div class="glance">
      <div><span>Complete brand packages</span><b>from {gbp(lo_pkg)}</b><span>Brand, website, photos and social</span></div>
      <div><span>Custom-coded websites</span><b>from {gbp(lo_site)}</b><span>One-off price, live in 5 days</span></div>
      <div><span>Monthly care plans</span><b>from {gbp(lo_care)}/mo</b><span>Hosting, security and updates</span></div>
    </div>
    <div class="hero-btns">
      <a class="btn btn-prime" href="#quote">Build your quote</a>
      <a class="btn" href="PDS-Pricing-and-Packages.pdf" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 4v11M7 10l5 5 5-5M5 20h14"/></svg>Pricing PDF</a>
      <span class="vat">Prices exclude VAT where applicable.</span>
    </div>
  </div>
</section>

<section class="band" style="padding-block:clamp(48px,7vw,80px) 0">
  <div class="wrap ref" style="gap:48px">
    <div>
      <div class="ref-head"><span class="eyebrow mono">Why PDS Creative</span><h2>Everything your brand needs, made by one studio</h2>
        <p class="lede">Most new businesses juggle a designer, a web developer, a photographer, a videographer and a social media agency. With PDS Creative it's all done in one place, so everything looks like it belongs together.</p></div>
      <div class="why">
        <div><b>See it before you pay</b><p>We design a free demo of your website first, so you know exactly what you're getting.</p></div>
        <div><b>Ready in 5 days</b><p>Brand, website, photos and social look delivered together, with your business ready to launch.</p></div>
        <div><b>Never a template</b><p>Every logo, website and video is made from scratch. Websites are hand-coded and built for SEO and AI search.</p></div>
      </div>
    </div>
    <div>
      <div class="ref-head"><span class="eyebrow mono">How we price</span><h2>Affordable, without cutting corners</h2>
        <p class="lede">We believe great design shouldn't be out of reach for a new business. We check what London studios typically charge for every service and price around 30% below the average, with the same standard of work.</p></div>
      <div class="tbl"><table class="cmp-tbl">
        <thead><tr><th>Service</th><th>Typical London</th><th class="hl">PDS Creative</th><th>Saving</th></tr></thead>
        <tbody>{cmp_rows}</tbody>
      </table></div>
      <p class="honest">Typical London prices are mid-range figures based on published 2026 UK price guides for agencies and freelancers, where London sits at the top of the UK range. Checked {P.EDITION}.</p>
    </div>
    <div>
      <div class="ref-head"><span class="eyebrow mono">How it works</span><h2>From your idea to launch in a week</h2></div>
      <ol class="how">
        <li><span class="n">1</span><span class="when">Free, no obligation</span><b>Free demo</b><p>Tell us your idea and we'll design a demo of your new website, free.</p></li>
        <li><span class="n">2</span><span class="when">If you love it</span><b>Kick-off</b><p>Pay 50% to book your slot and send us what you have.</p></li>
        <li><span class="n">3</span><span class="when">Days 1–2</span><b>Brand &amp; design</b><p>Logo, brand and page designs, shared for your feedback.</p></li>
        <li><span class="n">4</span><span class="when">Days 3–4</span><b>Shoot &amp; build</b><p>Photos, video, website, social look and adverts, plus your revisions.</p></li>
        <li><span class="n">5</span><span class="when">Day 5</span><b>Launch</b><p>You're ready to go. The remaining 50% is due on launch day.</p></li>
      </ol>
      <p class="honest">The 5-day clock starts once we have your content, logins and any existing branding. Flagship websites and the Complete Brand package take 10–15 working days.</p>
      <p class="promise"><b>The 5-day promise:</b> if your Launch or Signature site isn't live within 5 working days of receiving everything needed, your first month of care is free.</p>
    </div>
  </div>
</section>

<section class="band" id="quote" style="padding-top:clamp(48px,7vw,80px)">
  <div class="wrap">
    <div class="ref-head" style="margin-bottom:28px"><span class="eyebrow mono">Quote builder</span><h2>Build your quote</h2>
      <p class="lede">Pick a complete package or build your own. Your total updates as you go, and nothing is booked until you've seen your free demo.</p></div>
  </div>
  <div class="wrap calc">
    <div class="q-steps">
      <div class="q-step">
        <div class="q-head"><span class="q-num">1</span><div><h2>Choose a package</h2><p>Everything a new business needs, for less than booking each service on its own.</p></div></div>
        <div class="q-opts c3" id="pkgOpts"></div>
      </div>
      <div class="q-step">
        <div class="q-head"><span class="q-num">2</span><div><h2>Branding</h2><p>Your logo, colours and fonts, made from scratch.</p></div></div>
        <div class="q-opts" id="brandOpts"></div>
      </div>
      <div class="q-step">
        <div class="q-head"><span class="q-num">3</span><div><h2>Website</h2><p>Custom-coded, never a template. 50% to book and 50% on launch day.</p></div></div>
        <div class="q-opts" id="siteOpts"></div>
      </div>
      <div class="q-step">
        <div class="q-head"><span class="q-num">4</span><div><h2>Social media &amp; adverts</h2><p>A new look online, and adverts ready for Instagram, Facebook, TikTok and Google.</p></div></div>
        <div class="q-group" id="socialOpts"></div>
      </div>
      <div class="q-step">
        <div class="q-head"><span class="q-num">5</span><div><h2>Photography &amp; video</h2><p>Every image and video is licensed for your website, social media and adverts.</p></div></div>
        <div class="q-group" id="mediaOpts"></div>
      </div>
      <div class="q-step">
        <div class="q-head"><span class="q-num">6</span><div><h2>Website extras</h2><p>Anything else your website needs.</p></div></div>
        <div class="q-group" id="extraOpts"></div>
      </div>
      <div class="q-step">
        <div class="q-head"><span class="q-num">7</span><div><h2>Monthly care plan</h2><p>Hosting, security and backups on every plan. 3-month minimum, then month to month.</p></div></div>
        <p class="q-note" id="careNote"></p>
        <div class="q-opts" id="careOpts"></div>
      </div>
      <div class="q-step">
        <div class="q-head"><span class="q-num">8</span><div><h2>Content subscription</h2><p>Fresh photos and video every month. 6-month minimum.</p></div></div>
        <div class="q-opts" id="subOpts"></div>
      </div>
    </div>

    <aside class="q-sum" id="summary" aria-live="polite">
      <div style="display:flex;justify-content:space-between;align-items:center;gap:10px"><h2>Your quote</h2><span class="mono" style="color:var(--dim)">GBP · ex VAT</span></div>
      <div class="big">
        <div><span>To start</span><b id="upAmt">£0</b><small id="upSub"></small></div>
        <div><span>Each month</span><b id="moAmt">£0</b><small id="moSub"></small></div>
      </div>
      <div class="lines" id="lines"></div>
      <div class="yr"><span>First year total</span><b id="yrAmt">£0</b></div>
      <p class="saves" id="saves" hidden></p>
      <p class="q-fine" id="london"></p>
      <div class="q-actions">
        <button class="btn btn-prime" type="button" id="sendBtn">Get my free demo</button>
        <div class="row"><button class="btn" type="button" id="copyBtn">Copy quote</button><button class="btn" type="button" id="resetBtn">Start again</button></div>
      </div>
      <form class="q-form" id="qForm" name="quote" method="POST" novalidate hidden>
        <p hidden><label>Leave this empty <input name="_gotcha" tabindex="-1" autocomplete="off"></label></p>
        <textarea name="quote" id="qText" hidden></textarea>
        <input type="hidden" name="_subject" value="New quote request from pdscreative.com">
        <label for="qName" style="color:var(--muted);font-size:.85rem">Your name</label>
        <input id="qName" name="name" autocomplete="name" placeholder="Alex Morgan">
        <label for="qEmail" style="color:var(--muted);font-size:.85rem">Email</label>
        <input id="qEmail" name="email" type="email" autocomplete="email" placeholder="alex@company.com">
        <p class="q-fine" id="qErr" aria-live="polite"></p>
        <button class="btn btn-prime" type="submit" style="justify-content:center">Send to Pedro</button>
      </form>
      <div class="q-ok" id="qOk" hidden></div>
      <p class="q-fine">An estimate based on the {P.EDITION} price list. Your final price is confirmed in writing after your free demo.</p>
    </aside>
  </div>
</section>

<section class="band process">
  <div class="wrap ref">
    <div>
      <div class="ref-head"><span class="eyebrow mono">Complete packages</span><h2>Your whole brand, ready to launch</h2>
        <p class="lede">Every package includes a free website demo before you pay, your first month of website care free, and one point of contact from first idea to launch day.</p></div>
      <div class="pk-ref">{pk_ref}</div>
    </div>
    <div>
      <div class="ref-head"><span class="eyebrow mono">Branding</span><h2>A brand people remember</h2></div>
      <div class="tbl"><table><thead><tr><th>Service</th><th>What you get</th><th>Typical London</th><th class="hl">PDS Creative</th></tr></thead><tbody>{rows3(P.BRAND.values())}</tbody></table></div>
    </div>
    <div>
      <div class="ref-head"><span class="eyebrow mono">Social media &amp; adverts</span><h2>A new look online, and adverts that sell</h2>
        <p class="lede">You stay in control of your ad budget; we make the ads that make it work.</p></div>
      <div class="tbl"><table><thead><tr><th>Service</th><th>What you get</th><th>Typical London</th><th class="hl">PDS Creative</th></tr></thead><tbody>{rows3(P.SOCIAL.values())}</tbody></table></div>
    </div>
    <div>
      <div class="ref-head"><span class="eyebrow mono">Websites</span><h2>Custom-coded, never a template</h2>
        <p class="lede">One simple, one-off price. Pay 50% to book your slot and 50% on launch day, with no hidden extras.</p></div>
      <div class="tbl"><table><thead><tr><th></th>{site_head}</tr></thead><tbody>{site_tbody}</tbody></table></div>
      <div class="ref-head" style="margin:32px 0 16px"><h2 style="font-size:1.4rem">Website extras</h2></div>
      <div class="tbl"><table><thead><tr><th>Extra</th><th>Price</th></tr></thead><tbody>{extras}</tbody></table></div>
    </div>
    <div>
      <div class="ref-head"><span class="eyebrow mono">Photography &amp; video</span><h2>Real photos and video of your real business</h2>
        <p class="lede">Stock photos make every business look the same. We photograph and film your team, premises, products and work.</p></div>
      <div class="tbl"><table><thead><tr><th>Shoot</th><th>What you get</th><th>Typical London</th><th class="hl">PDS Creative</th></tr></thead><tbody>{rows3(list(P.PHOTO.values()) + list(P.VIDEO.values()))}</tbody></table></div>
    </div>
    <div>
      <div class="ref-head"><span class="eyebrow mono">Monthly care plans</span><h2>We look after your site, so you don't have to</h2>
        <p class="lede">Every plan includes hosting, security and backups. Your first month is free with any new website. 3-month minimum, then month to month.</p></div>
      <div class="tbl"><table><thead><tr><th></th>{care_head}</tr></thead><tbody>{care_body}</tbody></table></div>
      <p class="honest">Essential suits most Launch sites, Growth suits Signature and Partner suits Flagship. Move up or down a plan with a month's notice. Work beyond your included hours is £85/hour or £550/day.</p>
    </div>
    <div>
      <div class="ref-head" style="margin:0 0 16px"><span class="eyebrow mono">Content subscriptions</span><h2>Fresh photos and video, every month</h2>
        <p class="lede">Regular shoots so your website and social media always look current. 6-month minimum. Shoots in London and Hertfordshire, travel included.</p></div>
      <div class="subs">{subs}</div>
      <div class="ref-head" style="margin:32px 0 16px"><h2 style="font-size:1.4rem">All-in bundles</h2>
        <p class="lede">Combine your care plan and content subscription into one monthly payment. The quote builder applies these automatically.</p></div>
      <div class="tbl"><table><thead><tr><th>Bundle</th><th>Includes</th><th>Separately</th><th class="hl">Bundle price</th><th>You save</th></tr></thead><tbody>{bundles}</tbody></table></div>
      <p class="refer"><b>Refer a friend:</b> recommend PDS Creative to another business and get a free month of your care plan when they sign up.</p>
    </div>
    <div>
      <div class="ref-head"><span class="eyebrow mono">Good to know</span><h2>The small print, kept simple</h2></div>
      <ul class="small-print">
        <li><b>Payment:</b> one-off work is 50% to book and 50% on launch day. Monthly plans are paid by Direct Debit.</li>
        <li><b>Your files:</b> logos, brand files, photos and videos are yours to use once paid in full.</li>
        <li><b>Timeline:</b> the 5-day clock starts once we have your content, logins and any existing branding.</li>
        <li><b>Minimums:</b> care plans 3 months, content subscriptions 6 months, then month to month.</li>
        <li><b>Revisions:</b> 2 rounds included (3 on Flagship and Complete Brand). Further changes are billed hourly.</li>
        <li><b>VAT:</b> prices exclude VAT where applicable.</li>
      </ul>
    </div>
    <div class="cta-band">
      <div><h2>Got an idea? Let's build your brand.</h2><p class="lede" style="margin-top:8px">Ask for your free website demo and see it before you pay a penny.</p>
        <p style="margin-top:12px;color:var(--muted);font-size:.93rem">Email <button class="copy-btn mail" type="button" id="copyMail">pedro.de.sousa@hotmail.co.uk</button></p></div>
      <div class="hero-btns"><a class="btn btn-prime" href="book-a-call.html">Book a free call</a><a class="btn" href="#quote">Build your quote</a></div>
    </div>
  </div>
</section>
</main>"""

DATA = {
    "pkg": {k: {"name": p["name"], "p": p["price"], "from": bool(p.get("from")), "days": p["days"], "best": p["best"], "lines": p["lines"],
                "popular": bool(p.get("popular")), "inc": p["includes"], "london": P.london_of_package(p)} for k, p in P.PACKAGES.items()},
    "brand": {k: {"name": v["name"], "p": v["price"], "desc": v["desc"], "london": v["london"]} for k, v in P.BRAND.items()},
    "site": {k: {"name": v["name"], "p": v["price"], "best": v["best"], "feats": v["feats"][:4], "care": v["care"], "from": bool(v.get("from")),
                 "popular": bool(v.get("popular")), "london": v["london"]} for k, v in P.SITES.items()},
    "social": {k: {"name": v["name"], "p": v["price"], "desc": v["desc"], "london": v["london"]} for k, v in P.SOCIAL.items()},
    "photo": {k: {"name": v["name"], "p": v["price"], "desc": v["desc"], "london": v["london"]} for k, v in P.PHOTO.items()},
    "video": {k: {"name": v["name"], "p": v["price"], "desc": v["desc"], "london": v["london"]} for k, v in P.VIDEO.items()},
    "extra": {k: {"name": v["name"], "p": v["price"]} for k, v in P.EXTRAS.items()},
    "care": {k: {"name": v["name"], "p": v["price"], "disc": v["disc"], "best": v["best"], "london": v["london"], "popular": bool(v.get("popular"))} for k, v in P.CARE.items()},
    "sub": {k: {"name": v["name"], "p": v["price"], "feats": v["feats"], "london": v["london"], "popular": bool(v.get("popular"))} for k, v in P.SUBS.items()},
    "bundles": [{"name": b["name"], "care": b["care"], "sub": b["sub"], "p": b["price"]} for b in P.BUNDLES],
}

SCRIPT = """<script>
(function(){
  const $ = id => document.getElementById(id);
  const gbp = n => '£' + Math.round(n).toLocaleString('en-GB');
  const nav = $('nav'), mb = $('menuBtn');
  mb.addEventListener('click', ()=>{ const o = nav.classList.toggle('open'); mb.setAttribute('aria-expanded', o); });

  /* Price list: generated from tools/pricing/prices.py by build_page.py. Edit prices there, not here. */
  const PR = __DATA__;

  const DEFAULT = {pkg:'launch', brand:'none', site:'none', social:{}, photo:'none', film:false, reels:false, combo:false, heads:0, event:'none', pages:0, gbp:false, pay:false, audit:false, care:'growth', sub:'none'};
  let st = JSON.parse(JSON.stringify(DEFAULT));
  try{ const v = JSON.parse(localStorage.getItem('pds-quote-v2')||'null'); if(v) st = Object.assign(JSON.parse(JSON.stringify(DEFAULT)), v); }catch(e){}
  const save = ()=>{ try{ localStorage.setItem('pds-quote-v2', JSON.stringify(st)); }catch(e){} };
  const pk = ()=> PR.pkg[st.pkg];
  const inc = ()=> pk() ? pk().inc : {brand:null, site:null, social:[], photo:null, video:[]};
  const covered = {
    brand: k => { const b = inc().brand; return b && (b===k || (b==='kit' && k==='logo')); },
    site:  k => inc().site===k,
    social:k => inc().social.includes(k),
    photo: k => inc().photo===k || (inc().photo==='combo' && k==='half'),
    video: k => inc().video.includes(k) || (inc().photo==='combo' && (k==='combo' || k==='film'))
  };
  const curSite = ()=> inc().site || (st.site in PR.site ? st.site : null);
  const careDisc = ()=> (PR.care[st.care]||{disc:0}).disc;

  /* ---------- Calculation ---------- */
  function calc(){
    const once = [], monthly = [];
    let saving = 0, london = 0;
    const d = careDisc();
    const disc = (label, full)=>{ const v = full*(1-d); saving += full-v; once.push([label + (d ? ' ('+Math.round(d*100)+'% care plan discount)' : ''), v]); };
    if(pk()){ once.push([pk().name+' package'+(pk().from?' (from)':''), pk().p]); london += pk().london; }
    if(st.brand!=='none' && !covered.brand(st.brand)){ disc(PR.brand[st.brand].name, PR.brand[st.brand].p); london += PR.brand[st.brand].london; }
    if(!inc().site && st.site in PR.site){ once.push([PR.site[st.site].name+' website'+(PR.site[st.site].from?' (from)':''), PR.site[st.site].p]); london += PR.site[st.site].london; }
    Object.keys(PR.social).forEach(k=>{ if(st.social[k] && !covered.social(k)){ disc(PR.social[k].name, PR.social[k].p); london += PR.social[k].london; } });
    if(st.combo && !covered.video('combo')){ disc(PR.video.combo.name, PR.video.combo.p); london += PR.video.combo.london; }
    else if(!st.combo){
      if(st.photo!=='none' && !covered.photo(st.photo)){
        const full = st.photo==='full' && covered.photo('half') ? PR.photo.full.p - PR.photo.half.p : PR.photo[st.photo].p;
        disc(PR.photo[st.photo].name + (full!==PR.photo[st.photo].p ? ' (upgrade)' : ''), full); london += PR.photo[st.photo].london;
      }
      if(st.film && !covered.video('film')){ disc(PR.video.film.name, PR.video.film.p); london += PR.video.film.london; }
    }
    if(st.reels && !covered.video('reels')){ disc(PR.video.reels.name, PR.video.reels.p); london += PR.video.reels.london; }
    if(st.heads>0){ const n = Math.max(st.heads,6); disc('Team headshots, '+n+' people'+(st.heads<6?' (6 minimum)':''), PR.photo.headshot.p*n); london += PR.photo.headshot.london*n; }
    if(st.event!=='none'){ const ev = PR.photo['event_'+st.event]; disc(ev.name, ev.p); london += ev.london; }
    const site = curSite();
    if(st.pages>0) once.push([st.pages+' additional page'+(st.pages>1?'s':''), PR.extra.page.p*st.pages]);
    const gbpInc = site==='signature' || site==='flagship', payInc = site==='flagship';
    if(st.gbp) once.push([PR.extra.gbp.name, gbpInc?0:PR.extra.gbp.p, gbpInc?'Included':null]);
    if(st.pay) once.push([PR.extra.pay.name, payInc?0:PR.extra.pay.p, payInc?'Included':null]);
    if(st.audit){ if(site){ once.push(['Website audit', 0, 'Credited']); saving += PR.extra.audit.p; } else once.push(['Website audit', PR.extra.audit.p]); }

    const care = PR.care[st.care], sub = PR.sub[st.sub];
    const bundle = PR.bundles.find(b=>b.care===st.care && b.sub===st.sub);
    if(bundle){ monthly.push([bundle.name+' bundle ('+care.name+' care + '+sub.name+' content)', bundle.p]); saving += (care.p+sub.p-bundle.p)*12; }
    else { if(care) monthly.push([care.name+' care plan', care.p]); if(sub) monthly.push([sub.name+' content subscription', sub.p]); }
    let freeCredit = 0;
    if(site && care){ freeCredit = care.p; saving += care.p; }
    if(pk()){ const sep = separateOf(pk()); saving += sep - pk().p; }
    const upfront = once.reduce((n,l)=>n+l[1],0), mo = monthly.reduce((n,l)=>n+l[1],0);
    return {once, monthly, upfront, mo, freeCredit, year1: upfront + mo*12 - freeCredit, saving, care, sub, site, london};
  }
  function separateOf(p){
    const i = p.inc; let t = PR.brand[i.brand].p + PR.site[i.site].p;
    i.social.forEach(k=>t+=PR.social[k].p);
    t += i.photo==='combo' ? PR.video.combo.p : PR.photo[i.photo].p;
    i.video.forEach(k=>t+=PR.video[k].p);
    return t;
  }

  /* ---------- Render ---------- */
  const opt = (name, key, checked, inner, dis, wide)=> `<label class="q-opt${wide?' wide':''}"><input type="radio" name="${name}" value="${key}" ${checked?'checked':''} ${dis?'disabled':''}><span class="q-card">${inner}</span></label>`;
  const tag = t => `<span class="q-tag">${t}</span>`;
  const lon = (p, l, u='')=> `<span class="lon">Typical London ${gbp(l)}${u} · ${Math.round((1-p/l)*100)}% less</span>`;
  function sw(id, on, dis){ return `<label class="sw"><input type="checkbox" id="${id}" ${on?'checked':''} ${dis?'disabled':''}><span></span></label>`; }
  function row(label, desc, right, locked){ return `<div class="q-x${locked?' locked':''}"><div class="l"><b>${label}</b><span>${desc}</span></div><div class="r">${right}</div></div>`; }

  function render(){
    const p = pk(), d = careDisc();
    $('pkgOpts').innerHTML = Object.entries(PR.pkg).map(([k,v])=>opt('pkg',k,st.pkg===k,
      `<span class="t"><b>${v.name}</b>${v.popular?tag('Most popular'):''}</span><span class="best">${v.best}</span><ul>${v.lines.map(x=>`<li>${x}</li>`).join('')}</ul><span class="pk-inc">${v.days}</span><span class="pr">${v.from?'From ':''}${gbp(v.p)}</span>${lon(v.p, v.london)}`)).join('')
      + opt('pkg','none',st.pkg==='none',`<span class="t"><b>Build my own</b></span><span class="best">Pick individual services below</span>`, false, true);

    $('brandOpts').innerHTML = Object.entries(PR.brand).map(([k,v])=>{ const c = covered.brand(k);
      return opt('brand',k,st.brand===k||c,`<span class="t"><b>${v.name}</b>${c?tag('In your package'):''}</span><span class="best">${v.desc}</span><span class="pr">${c?'Included':gbp(v.p*(1-d))}</span>${c?'':lon(v.p,v.london)}`, !!inc().brand);
    }).join('') + opt('brand','none',st.brand==='none'&&!inc().brand,`<span class="t"><b>No branding</b></span><span class="best">I already have a logo and brand</span>`, !!inc().brand, true);

    $('siteOpts').innerHTML = Object.entries(PR.site).map(([k,v])=>{ const c = covered.site(k);
      return opt('site',k,(st.site===k&&!inc().site)||c,`<span class="t"><b>${v.name}</b>${c?tag('In your package'):(v.popular?tag('Most popular'):'')}</span><span class="best">${v.best}</span><ul>${v.feats.map(x=>`<li>${x}</li>`).join('')}</ul><span class="pr">${c?'Included':(v.from?'From ':'')+gbp(v.p)}</span>${c?'':lon(v.p,v.london)}`, !!inc().site);
    }).join('') + opt('site','none',st.site==='none'&&!inc().site,`<span class="t"><b>No new website</b></span><span class="best">Branding, content or care for a site you already have</span>`, !!inc().site, true);

    $('socialOpts').innerHTML = Object.entries(PR.social).map(([k,v])=>{ const c = covered.social(k);
      return row(v.name, v.desc, c?'<span class="inc">In your package</span>':`<span class="amt${st.social[k]?' on':''}">${gbp(v.p*(1-d))}</span>`+sw('so-'+k, !!st.social[k]), c);
    }).join('');

    const ph = (k)=> covered.photo(k) ? 'Included' : (k==='full' && covered.photo('half') ? '+'+gbp((PR.photo.full.p-PR.photo.half.p)*(1-d)) : gbp(PR.photo[k].p*(1-d)));
    const comboCov = covered.video('combo');
    let media = row('Brand photo shoot', 'Half day: 40+ images · Full day: 80+ images, multiple locations, headshots',
      `<div class="seg2" role="radiogroup" aria-label="Brand photo shoot">`+[['none','None'],['half','Half day '+ph('half')],['full','Full day '+ph('full')]].map(([v,l])=>`<label><input type="radio" name="photo" value="${v}" ${(st.photo===v || (v==='half'&&covered.photo('half')&&st.photo==='none'))?'checked':''} ${(st.combo||comboCov||(v==='none'&&covered.photo('half')))?'disabled':''}><span>${l}</span></label>`).join('')+`</div>`, comboCov);
    media += row(PR.video.film.name, PR.video.film.desc, comboCov?'<span class="inc">In your package</span>':`<span class="amt${st.film?' on':''}">${gbp(PR.video.film.p*(1-d))}</span>`+sw('film', st.film, st.combo), comboCov);
    media += row(PR.video.combo.name, PR.video.combo.desc, comboCov?'<span class="inc">In your package</span>':`<span class="amt${st.combo?' on':''}">${gbp(PR.video.combo.p*(1-d))}</span>`+sw('combo', st.combo), comboCov);
    media += row(PR.video.reels.name, PR.video.reels.desc, covered.video('reels')?'<span class="inc">In your package</span>':`<span class="amt${st.reels?' on':''}">${gbp(PR.video.reels.p*(1-d))}</span>`+sw('reels', st.reels), covered.video('reels'));
    media += row('Team headshots', `Consistent on-site headshots · ${gbp(PR.photo.headshot.p)} per person, minimum 6 people`,
      `<div class="stepper" data-key="heads"><button type="button" aria-label="Fewer people">−</button><output>${st.heads}</output><button type="button" aria-label="More people">+</button></div><span class="amt${st.heads?' on':''}">${gbp(st.heads?PR.photo.headshot.p*Math.max(st.heads,6)*(1-d):0)}</span>`);
    media += row('Event coverage', 'Launches, openings and corporate events', `<div class="seg2" role="radiogroup" aria-label="Event coverage">`+[['none','None'],['half','Half day '+gbp(PR.photo.event_half.p*(1-d))],['full','Full day '+gbp(PR.photo.event_full.p*(1-d))]].map(([v,l])=>`<label><input type="radio" name="event" value="${v}" ${st.event===v?'checked':''}><span>${l}</span></label>`).join('')+`</div>`);
    $('mediaOpts').innerHTML = media;

    const site = curSite();
    const gbpInc = site==='signature'||site==='flagship', payInc = site==='flagship';
    $('extraOpts').innerHTML =
      row('Additional pages', gbp(PR.extra.page.p)+' per page', `<div class="stepper" data-key="pages"><button type="button" aria-label="Fewer pages">−</button><output>${st.pages}</output><button type="button" aria-label="More pages">+</button></div><span class="amt${st.pages?' on':''}">${gbp(PR.extra.page.p*st.pages)}</span>`)
      + row(PR.extra.gbp.name, gbpInc?'Included with your website':gbp(PR.extra.gbp.p), sw('gbp', st.gbp))
      + row(PR.extra.pay.name, payInc?'Included with Flagship':gbp(PR.extra.pay.p), sw('pay', st.pay))
      + row('Website audit', site?'Credited against your new website, so it\\'s free':gbp(PR.extra.audit.p)+', credited if you go ahead with a new website', sw('audit', st.audit));

    const suit = site ? PR.site[site].care : null;
    $('careNote').textContent = site ? `Your first month of care is free with a new website. ${PR.care[suit].name} suits most ${PR.site[site].name} sites.` : 'Care plans also work for websites we didn\\'t build.';
    $('careOpts').innerHTML = Object.entries(PR.care).map(([k,c])=>opt('care',k,st.care===k,
      `<span class="t"><b>${c.name}</b>${k===suit?tag('Suits '+PR.site[site].name):(c.popular&&!suit?tag('Most popular'):'')}</span><span class="best">${c.best}${c.disc?' · '+Math.round(c.disc*100)+'% off photo, video and design':''}</span><span class="pr">${gbp(c.p)} <small>/ month</small></span>${lon(c.p,c.london,'/mo')}`)).join('')
      + opt('care','none',st.care==='none',`<span class="t"><b>No care plan</b></span><span class="best">You look after hosting and updates yourself</span>`, false, true);

    $('subOpts').innerHTML = Object.entries(PR.sub).map(([k,u])=>{ const b = PR.bundles.find(x=>x.sub===k);
      return opt('sub',k,st.sub===k,`<span class="t"><b>${u.name}</b>${u.popular?tag('Most popular'):''}</span><ul>${u.feats.map(x=>`<li>${x}</li>`).join('')}</ul>${b?`<span class="best">With ${PR.care[b.care].name} care: ${b.name} bundle, ${gbp(b.p)}/mo</span>`:''}<span class="pr">${gbp(u.p)} <small>/ month</small></span>${lon(u.p,u.london,'/mo')}`);
    }).join('') + opt('sub','none',st.sub==='none',`<span class="t"><b>No subscription</b></span><span class="best">Book shoots as you need them</span>`, false, true);

    bindSteppers(); summary(); save();
  }

  function summary(){
    const r = calc();
    $('upAmt').textContent = gbp(r.upfront);
    const dep = Math.round(r.upfront/2);
    $('upSub').textContent = r.upfront ? gbp(dep)+' to book, '+gbp(r.upfront-dep)+' at launch' : 'Nothing upfront';
    $('moAmt').textContent = gbp(r.mo);
    $('moSub').textContent = r.mo ? (r.freeCredit ? 'First month of care free' : 'By Direct Debit') : 'No monthly costs';
    let h = '';
    if(r.once.length) h += '<div class="cap">One-off</div>' + r.once.map(l=>`<div class="ln"><span>${l[0]}</span><span>${l[2]||gbp(l[1])}</span></div>`).join('');
    if(r.monthly.length) h += '<div class="cap">Monthly</div>' + r.monthly.map(l=>`<div class="ln"><span>${l[0]}</span><span>${gbp(l[1])}/mo</span></div>`).join('');
    if(r.freeCredit) h += `<div class="ln save"><span>First month of ${r.care.name} care free</span><span>−${gbp(r.freeCredit)}</span></div>`;
    const mins = []; if(r.care) mins.push('care plans have a 3-month minimum'); if(r.sub) mins.push('content subscriptions have a 6-month minimum');
    if(mins.length) h += `<p class="q-fine" style="padding-top:8px">${mins.join(' and ').replace(/^./,c=>c.toUpperCase())}.</p>`;
    if(!h) h = '<p class="q-fine" style="padding-block:8px">Choose a package or add a service to see your quote.</p>';
    $('lines').innerHTML = h;
    $('yrAmt').textContent = gbp(r.year1);
    $('saves').hidden = r.saving < 1; $('saves').textContent = 'You save '+gbp(r.saving)+' in your first year with packages, discounts and bundles';
    $('london').textContent = r.london > r.upfront && r.upfront ? 'Your one-off work would typically cost around '+gbp(r.london)+' from a London studio.' : '';
    $('mbUp').textContent = gbp(r.upfront)+' to start';
    $('mbMo').textContent = r.mo ? gbp(r.mo)+' / month' : 'No monthly costs';
  }

  function bindSteppers(){
    document.querySelectorAll('.stepper').forEach(el=>{
      const key = el.dataset.key, [minus,,plus] = el.children;
      minus.onclick = ()=>{ st[key] = Math.max(0, st[key]-1); render(); };
      plus.onclick = ()=>{ st[key] = Math.min(key==='heads'?80:30, (st[key]===0 && key==='heads') ? 6 : st[key]+1); render(); };
    });
  }

  document.addEventListener('change', e=>{
    const t = e.target;
    if(t.name==='pkg'){ st.pkg = t.value; if(pk()){ st.brand='none'; st.site='none'; st.photo='none'; st.combo=false; st.film=false; st.care = PR.site[pk().inc.site].care; } }
    else if(t.name==='brand') st.brand = t.value;
    else if(t.name==='site'){ st.site = t.value; if(PR.site[t.value]) st.care = PR.site[t.value].care; }
    else if(t.name==='photo') st.photo = t.value;
    else if(t.name==='event') st.event = t.value;
    else if(t.name==='care') st.care = t.value;
    else if(t.name==='sub') st.sub = t.value;
    else if(t.id && t.id.startsWith('so-')) st.social[t.id.slice(3)] = t.checked;
    else if(['film','combo','reels','gbp','pay','audit'].includes(t.id)){ st[t.id] = t.checked; if(t.id==='combo' && t.checked){ st.photo='none'; st.film=false; } }
    else return;
    render();
  });
  $('resetBtn').addEventListener('click', ()=>{ st = JSON.parse(JSON.stringify(DEFAULT)); $('qForm').hidden = true; $('qOk').hidden = true; render(); });

  function quoteText(){
    const r = calc(), out = ['PDS Creative quote (prices exclude VAT where applicable)', ''];
    r.once.forEach(l=>out.push(l[0]+': '+(l[2]||gbp(l[1]))));
    r.monthly.forEach(l=>out.push(l[0]+': '+gbp(l[1])+'/month'));
    if(r.freeCredit) out.push('First month of care free: -'+gbp(r.freeCredit));
    out.push('', 'To start: '+gbp(r.upfront), 'Each month: '+gbp(r.mo), 'First year total: '+gbp(r.year1));
    return out.join('\\n');
  }
  function copy(btn, txt, label){
    const done = ()=>{ btn.textContent='Copied'; setTimeout(()=>btn.textContent=label,1500); };
    if(navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(done).catch(()=>{});
  }
  $('copyBtn').addEventListener('click', ()=>copy($('copyBtn'), quoteText(), 'Copy quote'));
  const FORM_ENDPOINT = 'https://formspree.io/f/myeevwqa';
  $('copyMail').addEventListener('click', ()=>copy($('copyMail'), 'pedro.de.sousa@hotmail.co.uk', 'pedro.de.sousa@hotmail.co.uk'));
  $('sendBtn').addEventListener('click', ()=>{ $('qForm').hidden = false; $('qOk').hidden = true; $('qName').focus(); });
  $('qForm').addEventListener('submit', e=>{
    e.preventDefault();
    const n = $('qName').value.trim(), m = $('qEmail').value.trim();
    if(!n){ $('qErr').textContent = 'Add your name so we know who the demo is for.'; $('qName').focus(); return; }
    if(!/^\\S+@\\S+\\.\\S+$/.test(m)){ $('qErr').textContent = 'Check your email address. It needs an @ and a domain.'; $('qEmail').focus(); return; }
    $('qErr').textContent = 'Sending…'; $('qText').value = quoteText();
    fetch(FORM_ENDPOINT, {method:'POST', headers:{'Accept':'application/json'}, body:new FormData($('qForm'))}).then(r=>{ if(!r.ok) throw new Error(r.status); }).then(()=>{
      $('qErr').textContent = ''; $('qForm').hidden = true;
      const ok = $('qOk'); ok.hidden = false; ok.innerHTML = '<b>Request sent</b><span class="q-fine" style="color:var(--muted)"></span>';
      ok.querySelector('span').textContent = 'Thanks, '+n+'. Pedro will be in touch at '+m+' to start your free demo.';
    }).catch(()=>{ $('qErr').textContent = 'That didn\\'t send. Please try again, or email pedro.de.sousa@hotmail.co.uk.'; });
  });
  try{ new IntersectionObserver(es=>es.forEach(en=>$('mbar').classList.toggle('hide', en.isIntersecting)), {threshold:.15}).observe($('summary')); }catch(e){}
  render();
})();
</script>""".replace("__DATA__", json.dumps(DATA, ensure_ascii=False))

src = PAGE.read_text(encoding="utf-8")
src = re.sub(r"<main>.*?</main>", lambda m: MAIN, src, count=1, flags=re.S)
src = re.sub(r"<script>\s*\(function\(\)\{.*?</script>", lambda m: SCRIPT, src, count=1, flags=re.S)
src = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + e(DESC), src, count=1)
src = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + e(DESC), src, count=1)
if "GEN-PRICING-CSS:start" in src:
    src = re.sub(r"/\* GEN-PRICING-CSS:start.*?GEN-PRICING-CSS:end \*/", lambda m: CSS, src, count=1, flags=re.S)
else:
    i = src.index("</style>\n</head>")
    src = src[:i] + CSS + "\n" + src[i:]
PAGE.write_text(src, encoding="utf-8")
print("pricing.html updated")
