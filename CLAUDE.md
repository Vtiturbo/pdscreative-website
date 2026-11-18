# Working on this repo

This is Pedro's live website, pdscreative.com. Cloudflare Pages deploys every push to `main` within a couple of minutes.

- Static site with no build step. Edit the HTML files directly.
- Prices live in `tools/pricing/prices.py` (the source of truth, about 30% below typical London rates). Never edit prices by hand in `pricing.html` or the PDF: change `prices.py`, then run `build_page.py` and `build_pdf.py` + `render.js` (see `tools/pricing/README.md`). The homepage shows no prices.
- Before pushing, check that the JavaScript parses and that pages don't scroll sideways at phone width (390px).
- Forms post to Formspree via `FORM_ENDPOINT` in `index.html` and `pricing.html`.
- `client-login.html` must keep its `noindex` meta tag.
- Brand name: PDS Creative. Owner: Pedro de Sousa. Contact: pedro.de.sousa@hotmail.co.uk.
