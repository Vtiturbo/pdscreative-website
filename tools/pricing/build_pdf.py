"""Builds PDS-Pricing-and-Packages.pdf (via HTML) from prices.py. Run: python3 build_pdf.py && node render.js"""
import html, pathlib
import prices as P

e = html.escape
FONT = "node_modules/@fontsource"
gbp = lambda v: f"£{v:,}"
pct = lambda price, london: round((1 - price / london) * 100)

TICK = '<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#9DB1FF" stroke-width="3"><path d="M5 12l4 4 10-10"/></svg>'
LOGO = '<svg width="22" height="22" viewBox="0 0 32 32" fill="none" stroke-linecap="round"><path stroke="#9DB1FF" stroke-width="2.4" d="M2.5 9V5.5a3 3 0 0 1 3-3H9M23 2.5h3.5a3 3 0 0 1 3 3V9M29.5 23v3.5a3 3 0 0 1-3 3H23M9 29.5H5.5a3 3 0 0 1-3-3V23"/><path stroke="#EEF0F5" stroke-width="2.8" stroke-linejoin="round" d="M11.5 23.5v-15h5.2a4.6 4.6 0 0 1 0 9.2h-5.2"/><circle cx="21.6" cy="22" r="2" fill="#9DB1FF"/></svg>'

pages = []
def top():
    return f'<div class="top"><span class="brand">{LOGO}PDS <b>Creative</b></span><span class="tag">Pricing &amp; packages · {P.EDITION}</span></div>'
def foot():
    n = len(pages) + 1
    return f'<div class="foot"><span>PDS Creative · pdscreative.com · pedro.de.sousa@hotmail.co.uk · 07356 203744</span><span>Prices exclude VAT where applicable · {n}</span></div>'
def ul(items):
    return "<ul>" + "".join(f"<li>{TICK}<span>{e(i)}</span></li>" for i in items) + "</ul>"
def page(body, cls=""):
    pages.append(f'<section class="page {cls}">{top()}{body}{foot()}</section>')
def below(v):
    if pct(v["price"], v["london"]) < 10:
        return '<span class="vs" style="color:transparent">.</span>'
    return f'<span class="vs">London typical {gbp(v["london"])} · {pct(v["price"], v["london"])}% less</span>'

lo_pkg = min(p["price"] for p in P.PACKAGES.values())
lo_site = min(s["price"] for s in P.SITES.values())
lo_care = min(c["price"] for c in P.CARE.values())

# 1. Cover
page(f'''
<div class="cover-body">
  <div class="eyebrow">WEBSITES · VIDEO · PHOTOGRAPHY · BRANDING · SOCIAL MEDIA · ADVERTS</div>
  <h1>We create the brand.<br><span class="hl">You're ready in 5 days.</span></h1>
  <p class="lede">Got an idea? PDS Creative builds everything your business needs to look the part: your logo and brand, a custom-coded website, photography, video, a new social media look and adverts that sell. One studio, one point of contact, one consistent look.</p>
  <div class="pill"><span class="dot"></span>Most services priced well below typical London studio rates, with no compromise on quality</div>
</div>
<div class="tiles">
  <div class="tile"><span>Complete brand packages</span><b>from {gbp(lo_pkg)}</b><em>Brand, website, photos and social</em></div>
  <div class="tile"><span>Custom-coded websites</span><b>from {gbp(lo_site)}</b><em>One-off price, live in 5 days</em></div>
  <div class="tile"><span>Monthly care plans</span><b>from {gbp(lo_care)}/mo</b><em>Hosting, security and updates</em></div>
</div>''', "cover")

# 2. Why PDS, how we price, how it works
compare = [P.PACKAGES["launch"] | {"london": P.london_of_package(P.PACKAGES["launch"])}, P.BRAND["kit"], P.SITES["signature"], P.SOCIAL["makeover"], P.VIDEO["film"], P.SUBS["monthly"], P.CARE["growth"]]
rows = "".join(f"<tr><td><b>{e(v['name'])}</b></td><td class='r muted'>{gbp(v['london'])}{'/mo' if (v in P.CARE.values() or v in P.SUBS.values()) else ''}</td><td class='r now'>{gbp(v['price'])}{'/mo' if (v in P.CARE.values() or v in P.SUBS.values()) else ''}</td><td class='r ok'>{pct(v['price'], v['london'])}% less</td></tr>" for v in compare)
page(f'''
<div class="eyebrow">WHY PDS CREATIVE</div>
<h2>Everything your brand needs, made by one studio</h2>
<p class="lede sm">Most new businesses juggle a designer, a web developer, a photographer, a videographer and a social media agency. With PDS Creative it's all done in one place, by people who talk to each other, so everything looks like it belongs together.</p>
<div class="why">
  <div><b>See it before you pay</b><p>We design a free demo of your website first, so you know exactly what you're getting.</p></div>
  <div><b>Ready in 5 days</b><p>Brand, website, photos and social look delivered together, with your business ready to launch.</p></div>
  <div><b>Never a template</b><p>Every logo, website and video is made from scratch for your business. Websites are hand-coded and built for SEO and AI search.</p></div>
</div>
<div class="eyebrow" style="margin-top:9mm">HOW WE PRICE</div>
<h3 class="h3big">Affordable, without cutting corners</h3>
<p class="lede sm">We believe great design shouldn't be out of reach for a new business. We check what London studios typically charge and keep most of our prices well below the average, while delivering the same standard of work.</p>
<table><thead><tr><th>Service</th><th class="r">Typical London</th><th class="r">PDS Creative</th><th class="r">Saving</th></tr></thead><tbody>{rows}</tbody></table>
<p class="fine">Typical London prices are mid-range figures based on published 2026 UK price guides for agencies and freelancers, where London sits at the top of the UK range. Checked {P.EDITION}.</p>
<div class="eyebrow" style="margin-top:8mm">HOW IT WORKS</div>
<div class="how">
  <div><i>1</i><b>Free demo</b><span>Tell us your idea. We design a demo of your website, free.</span></div>
  <div><i>2</i><b>Kick-off</b><span>Love it? Pay 50% to book and send us what you have.</span></div>
  <div><i>3</i><b>Days 1–2</b><span>Brand, logo and page designs, shared for your feedback.</span></div>
  <div><i>4</i><b>Days 3–4</b><span>Shoot, build, social look and adverts, then your revisions.</span></div>
  <div><i>5</i><b>Day 5</b><span>You launch. The remaining 50% is due on launch day.</span></div>
</div>''')

# 3. Packages
cards = ""
for k, p in P.PACKAGES.items():
    lon, sep = P.london_of_package(p), P.separate_of_package(p)
    pre = "from " if p.get("from") else ""
    cards += f'''<div class="card{' pop' if p.get('popular') else ''}">{'<span class="badge">MOST POPULAR</span>' if p.get('popular') else ''}
      <h3>{e(p['name'])}</h3><p class="desc">{e(p['best'])}</p>
      <div class="now big">{pre}{gbp(p['price'])}</div>
      <div class="save">{e(p['days'])}</div>{ul(p['lines'])}
      <div class="cmp"><span>Booked separately</span><b>{gbp(sep)}</b></div>
      <div class="cmp"><span>Typical London cost</span><b>{gbp(lon)}</b></div>
      <div class="cmp ok"><span>You save</span><b>{gbp(sep - p['price'])} on our own prices</b></div></div>'''
page(f'''
<div class="eyebrow">COMPLETE PACKAGES</div>
<h2>Your whole brand, ready to launch</h2>
<p class="lede sm">Have an idea and need everything? Our packages bring your brand, website, photography, video, social media and adverts together for one price, for less than booking each service on its own.</p>
<div class="cards c3">{cards}</div>
<div class="note"><b>Every package includes:</b> a free website demo before you pay, your first month of website care free, and one point of contact from first idea to launch day. The 5-day clock starts once we have everything we need from you.</div>''')

# 4. Branding, social and adverts
def lon_cell(v):
    return f"{gbp(v['london'])}{v.get('unit','')}" if pct(v['price'], v['london']) >= 10 else "—"
def tbl(items, unit=""):
    return "".join(f"<tr><td><b>{e(v['name'])}</b><br><span class='muted'>{e(v['desc'])}</span></td><td class='r muted'>{lon_cell(v)}</td><td class='r now'>{gbp(v['price'])}{v.get('unit','')}</td></tr>" for v in items)
def tbl_media(items):
    return "".join(f"<tr><td><b>{e(v['name'])}</b><br><span class='muted'>{e(v['desc'])}</span></td><td class='r muted'>{lon_cell(v)}</td><td class='r now'>{gbp(v['price'])}{v.get('unit','')}</td><td class='r now ok'>{gbp(v['w']) if 'w' in v else '—'}</td></tr>" for v in items)
page(f'''
<div class="eyebrow">BRANDING</div>
<h2>A brand people remember</h2>
<p class="lede sm">Your logo, colours and fonts, designed from scratch and delivered as a ready-to-use kit, so your website, social media, signage and business cards all look like one brand.</p>
<table><thead><tr><th>Service</th><th class="r">Typical London</th><th class="r">PDS Creative</th></tr></thead><tbody>{tbl(P.BRAND.values())}</tbody></table>
<div class="eyebrow" style="margin-top:9mm">SOCIAL MEDIA &amp; ADVERTS</div>
<h2>A new look online, and adverts that sell</h2>
<p class="lede sm">We give your social media a fresh, consistent look and create adverts ready for Instagram, Facebook, TikTok and Google. You stay in control of your ad budget; we make the ads that make it work.</p>
<table><thead><tr><th>Service</th><th class="r">Typical London</th><th class="r">PDS Creative</th></tr></thead><tbody>{tbl(P.SOCIAL.values())}</tbody></table>''')

# 5. Websites
cards = ""
for k, s in P.SITES.items():
    pre = "from " if s.get("from") else ""
    cards += f'''<div class="card{' pop' if s.get('popular') else ''}">{'<span class="badge">MOST POPULAR</span>' if s.get('popular') else ''}
      <h3>{e(s['name'])}</h3><p class="desc">{e(s['best'])}</p>
      <div class="now big">{pre}{gbp(s['price'])}</div><div class="save">Live in {e(s['days'])}</div>{ul(s['feats'])}{below(s)}</div>'''
ext = "".join(f"<tr><td>{e(v['name'])}</td><td class='r now'>{gbp(v['price'])}</td></tr>" for v in P.EXTRAS.values())
page(f'''
<div class="eyebrow">WEBSITES</div>
<h2>Custom-coded, never a template</h2>
<p class="lede sm">Every website is designed and hand-coded from scratch around your business, fast on every phone and built for SEO and AI search. One-off price: 50% to book, 50% on launch day.</p>
<div class="cards c3">{cards}</div>
<h4>Website extras</h4>
<table><thead><tr><th>Extra</th><th class="r">Price</th></tr></thead><tbody>{ext}</tbody></table>
<div class="note"><b>Our 5-day promise:</b> if your Launch or Signature site isn't live within 5 working days of receiving everything we need, your first month of care is free.</div>''')

# 6. Photo and video
page(f'''
<div class="eyebrow">PHOTOGRAPHY</div>
<h2>Real photos of your real business</h2>
<p class="lede sm">Stock photos make every business look the same. We photograph your team, premises, products and work, and every image is licensed for your website, social media and adverts.</p>
<table><thead><tr><th>Shoot</th><th class="r">Typical London</th><th class="r">PDS Creative</th><th class="r">With a new website</th></tr></thead><tbody>{tbl_media(P.PHOTO.values())}</tbody></table>
<div class="eyebrow" style="margin-top:9mm">VIDEO</div>
<h2>Video that makes people stop scrolling</h2>
<p class="lede sm">From a homepage brand film to short vertical videos for Reels and TikTok, filmed and edited by the same team that designs your brand.</p>
<table><thead><tr><th>Video</th><th class="r">Typical London</th><th class="r">PDS Creative</th><th class="r">With a new website</th></tr></thead><tbody>{tbl_media(P.VIDEO.values())}</tbody></table>''')

# 7. Care plans
cards = ""
for k, c in P.CARE.items():
    cards += f'''<div class="card{' pop' if c.get('popular') else ''}">{'<span class="badge">MOST POPULAR</span>' if c.get('popular') else ''}
      <h3>{e(c['name'])}</h3><div class="now">{gbp(c['price'])}<small>/mo</small></div><p class="desc">{e(c['best'])}</p>{below(c)}</div>'''
heads = "".join(f"<th>{e(c['name'])}</th>" for c in P.CARE.values())
crow = "".join(f"<tr><td><b>{e(r)}</b></td>" + "".join(f"<td>{e(x)}</td>" for x in vals) + "</tr>" for r, vals in P.CARE_ROWS)
page(f'''
<div class="eyebrow">MONTHLY CARE PLANS</div>
<h2>We look after your site, so you don't have to</h2>
<p class="lede sm">Every plan includes hosting, security and backups. Your first month is free with any new website. 3-month minimum, then month to month.</p>
<div class="cards c4">{cards}</div>
<h4>Compare the plans</h4>
<table><thead><tr><th></th>{heads}</tr></thead><tbody>{crow}</tbody></table>
<p class="fine">Essential suits most Launch sites, Growth suits Signature and Partner suits Flagship. Move up or down a plan with a month's notice. Work beyond your included hours is £85/hour or £550/day.</p>''')

# 8. Subscriptions, bundles, small print
cards = ""
for k, s in P.SUBS.items():
    cards += f'''<div class="card{' pop' if s.get('popular') else ''}">{'<span class="badge">MOST POPULAR</span>' if s.get('popular') else ''}
      <h3>{e(s['name'])}</h3><div class="now">{gbp(s['price'])}<small>/mo</small></div>{ul(s['feats'])}{below(s)}</div>'''
brows = ""
for b in P.BUNDLES:
    c, s = P.CARE[b["care"]], P.SUBS[b["sub"]]
    sep = c["price"] + s["price"]
    brows += f"<tr><td><b>{e(b['name'])}</b></td><td class='muted'>{e(c['name'])} care + {e(s['name'])} content</td><td class='r muted'>{gbp(sep)}/mo</td><td class='r now'>{gbp(b['price'])}/mo</td><td class='r ok'>{gbp(sep - b['price'])}/mo</td></tr>"
page(f'''
<div class="eyebrow">CONTENT SUBSCRIPTIONS · 6-MONTH MINIMUM</div>
<h2>Fresh photos and video, every month</h2>
<p class="lede sm">Regular shoots so your website and social media always look current, for less than booking shoots one at a time. Shoots in London and Hertfordshire, travel included.</p>
<div class="cards c3">{cards}</div>
<h4>All-in bundles</h4>
<table><thead><tr><th>Bundle</th><th>Includes</th><th class="r">Separately</th><th class="r">Bundle</th><th class="r">You save</th></tr></thead><tbody>{brows}</tbody></table>
<div class="eyebrow" style="margin-top:8mm">GOOD TO KNOW</div>
<div class="print">
  <p><b>Payment:</b> one-off work is 50% to book and 50% on launch day. Monthly plans are paid by Direct Debit.</p>
  <p><b>Timeline:</b> the 5-day clock starts once we have your content, logins and any existing branding.</p>
  <p><b>Revisions:</b> 2 rounds included (3 on Flagship and Complete Brand). Further changes are billed hourly.</p>
  <p><b>Your files:</b> logos, brand files, photos and videos are yours to use once paid in full.</p>
  <p><b>Minimums:</b> care plans 3 months, content subscriptions 6 months, then month to month.</p>
  <p><b>Refer a friend:</b> get a free month of your care plan when a business you recommend signs up.</p>
</div>
<div class="cta"><b>Got an idea? Let's build your brand.</b><span>Ask for your free website demo or book a free 15-minute call at pdscreative.com/book-a-call.html · pedro.de.sousa@hotmail.co.uk · 07356 203744</span></div>''')

fonts = "".join(
    f"@font-face{{font-family:'{fam}';font-weight:{w};src:url('{FONT}/{pkg}/files/{pkg}-latin-{w}-normal.woff2') format('woff2')}}"
    for fam, pkg, ws in [("Instrument Sans", "instrument-sans", (500, 600, 700)), ("Hanken Grotesk", "hanken-grotesk", (400, 500, 600)), ("JetBrains Mono", "jetbrains-mono", (400, 500))]
    for w in ws)
CSS = fonts + """
@page{size:A4;margin:0}
*{box-sizing:border-box}
html,body{margin:0;background:#0E1015;color:#EEF0F5;font-family:'Hanken Grotesk',sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:210mm;height:297mm;padding:13mm 14mm 14mm;position:relative;overflow:hidden;page-break-after:always;background:#0E1015}
.page:last-child{page-break-after:auto}
.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:9mm}
.brand{display:flex;align-items:center;gap:8px;font:600 13px 'Instrument Sans'}
.brand b{font-weight:500;color:#9CA2B2}
.tag{font:500 8px 'JetBrains Mono';letter-spacing:.08em;color:#9CA2B2}
.eyebrow{font:500 8.5px 'JetBrains Mono';letter-spacing:.14em;color:#9DB1FF;margin-bottom:3mm;display:flex;align-items:center;gap:8px}
.eyebrow:before{content:"";width:14px;height:1px;background:#9DB1FF}
h1{font:600 50px/1.02 'Instrument Sans';letter-spacing:-.035em;margin:0 0 7mm}
h1 .hl{color:#9DB1FF}
h2{font:600 23px/1.12 'Instrument Sans';letter-spacing:-.025em;margin:0 0 2.5mm}
h3{font:600 15px 'Instrument Sans';margin:0 0 1.5mm}
.h3big{font-size:18px;margin-bottom:2mm}
h4{font:600 12px 'Instrument Sans';margin:6mm 0 2.5mm}
.lede{color:#9CA2B2;font-size:13px;line-height:1.55;max-width:160mm;margin:0 0 7mm}
.lede.sm{font-size:10.5px;margin-bottom:5mm}
.muted{color:#8A90A2;font-weight:400}
.cover{background:radial-gradient(70% 45% at 85% 0%,rgba(157,177,255,.20),transparent 70%),radial-gradient(55% 40% at 0% 100%,rgba(232,176,122,.10),transparent 70%),#0E1015}
.cover-body{margin-top:44mm}
.pill{display:inline-flex;align-items:center;gap:8px;font-size:10.5px;color:#EEF0F5;border:1px solid rgba(157,177,255,.45);background:rgba(157,177,255,.08);padding:7px 13px;border-radius:99px}
.dot{width:7px;height:7px;border-radius:50%;background:#7FD3A6}
.tiles{position:absolute;left:14mm;right:14mm;bottom:24mm;display:grid;grid-template-columns:repeat(3,1fr);gap:4mm}
.tile{border:1px solid rgba(200,206,224,.16);background:#14171E;border-radius:12px;padding:5mm;display:grid;gap:1.5mm}
.tile span{font-size:9px;color:#9CA2B2}
.tile b{font:600 19px 'Instrument Sans';letter-spacing:-.02em}
.tile em{font-style:normal;font-size:9px;color:#666C7C}
.why{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm}
.why div{border-top:1px solid rgba(200,206,224,.16);padding-top:3mm}
.why b{font:600 12px 'Instrument Sans'}
.why p{font-size:9.5px;color:#9CA2B2;line-height:1.5;margin:1.5mm 0 0}
.how{display:grid;grid-template-columns:repeat(5,1fr);gap:3mm}
.how div{border:1px solid rgba(200,206,224,.14);background:#14171E;border-radius:10px;padding:3.5mm;display:grid;gap:1.5mm;align-content:start}
.how i{font:500 9px 'JetBrains Mono';font-style:normal;width:20px;height:20px;border-radius:50%;border:1px solid #9DB1FF;color:#9DB1FF;display:grid;place-items:center}
.how b{font:600 11px 'Instrument Sans'}
.how span{font-size:8.8px;color:#9CA2B2;line-height:1.45}
.cards{display:grid;gap:3.5mm}
.c3{grid-template-columns:repeat(3,1fr)}.c4{grid-template-columns:repeat(4,1fr)}
.card{position:relative;border:1px solid rgba(200,206,224,.14);background:#14171E;border-radius:12px;padding:5mm 4.5mm;display:flex;flex-direction:column}
.card.pop{border-color:#9DB1FF;box-shadow:0 0 0 1px rgba(157,177,255,.25)}
.badge{position:absolute;top:-2.4mm;left:4.5mm;font:500 7px 'JetBrains Mono';letter-spacing:.1em;background:#9DB1FF;color:#0E1015;padding:2px 7px;border-radius:99px}
.now{font:600 22px 'Instrument Sans';letter-spacing:-.03em;color:#EEF0F5}
.now.big{font-size:25px}
.now small{font-size:11px;color:#9CA2B2;font-weight:500}
.save{font:500 7.8px 'JetBrains Mono';color:#9DB1FF;letter-spacing:.06em;margin:1.5mm 0 3mm;text-transform:uppercase}
.desc{font-size:9.3px;color:#9CA2B2;margin:0 0 3mm;line-height:1.45}
ul{list-style:none;margin:0 0 3mm;padding:0;display:grid;gap:1.8mm}
li{display:flex;gap:6px;font-size:9.3px;line-height:1.4;color:#C9CDD8}
li svg{flex:none;margin-top:1px}
.vs{margin-top:auto;font-size:8.3px;color:#7FD3A6;padding-top:2mm;border-top:1px solid rgba(200,206,224,.08)}
.cmp{display:flex;justify-content:space-between;font-size:8.8px;color:#9CA2B2;padding:1.4mm 0;border-top:1px solid rgba(200,206,224,.08)}
.cmp:first-of-type{margin-top:auto}
.cmp b{color:#EEF0F5;font-weight:600}
.cmp.ok b,.ok{color:#7FD3A6}
table{width:100%;border-collapse:collapse;font-size:9.3px;border:1px solid rgba(200,206,224,.12)}
th{text-align:left;font:500 7.6px 'JetBrains Mono';letter-spacing:.08em;text-transform:uppercase;color:#9CA2B2;background:#14171E;padding:2.4mm 3mm}
td{padding:2.3mm 3mm;border-top:1px solid rgba(200,206,224,.08);color:#C9CDD8;vertical-align:top;line-height:1.4}
td .muted{font-size:8.6px}
td.r,th.r{text-align:right;white-space:nowrap}
td.now{font:600 11px 'Instrument Sans'}
.note{margin-top:5mm;border:1px solid rgba(200,206,224,.14);background:#14171E;border-radius:10px;padding:4mm;font-size:9.5px;color:#C9CDD8;line-height:1.5}
.fine{font-size:8.3px;color:#8A90A2;margin:3mm 0 0;line-height:1.5}
.print{display:grid;grid-template-columns:1fr 1fr;gap:2mm 8mm}
.print p{margin:0;font-size:9.2px;line-height:1.5;color:#9CA2B2}
.print b{color:#EEF0F5}
.cta{margin-top:6mm;border:1px solid #9DB1FF;border-radius:14px;padding:5mm 6mm;background:linear-gradient(110deg,rgba(157,177,255,.12),rgba(232,176,122,.05))}
.cta b{display:block;font:600 16px 'Instrument Sans';margin-bottom:1.5mm}
.cta span{font-size:10px;color:#C9CDD8}
.foot{position:absolute;left:14mm;right:14mm;bottom:8mm;display:flex;justify-content:space-between;font-size:7.5px;color:#666C7C;border-top:1px solid rgba(200,206,224,.08);padding-top:2.5mm}
"""
doc = f'<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>PDS Creative — Pricing &amp; Packages {P.EDITION}</title><style>{CSS}</style></head><body>{"".join(pages)}</body></html>'
pathlib.Path("pricelist.html").write_text(doc, encoding="utf-8")
print(len(pages), "pages")
