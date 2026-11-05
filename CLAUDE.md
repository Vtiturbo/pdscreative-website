# Working on this repo

This is Pedro's live website, pdscreative.com. Cloudflare Pages deploys every push to `main` within a couple of minutes.

- Static site with no build step. Edit the HTML files directly.
- Keep prices consistent across `index.html` (pricing preview, services, FAQ) and `pricing.html` (quote builder data in the `SITES`, `CARE`, `SUBS` and `BUNDLES` objects, plus the reference tables). `PDS-Pricing-and-Packages.pdf` is the source of truth for prices.
- Before pushing, check that the JavaScript parses and that pages don't scroll sideways at phone width (390px).
- Forms post to Formspree via `FORM_ENDPOINT` in `index.html` and `pricing.html`.
- `client-login.html` must keep its `noindex` meta tag.
- Brand name: PDS Creative. Owner: Pedro de Sousa. Contact: pedro.de.sousa@hotmail.co.uk.
