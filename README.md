# PDS Creative website

The website for **pdscreative.com** (Pedro de Sousa: web design, photography and video).

- Hosted on Cloudflare Pages, connected to this repository.
- Every push to `main` goes live automatically.
- Plain HTML, CSS and JavaScript. There is no build step.

## Pages
- `index.html` is the homepage.
- `pricing.html` holds the pricing page and quote builder.
- `client-login.html` is the client portal. It's hidden from search engines.
  - Clients are listed in `PROJECTS` near the bottom of the file (access code, name, live demo URL, `sharedAt`).
  - Every free demo locks 48 hours after `sharedAt`. The demo site itself must also be locked (see verve-display `src/lib/demo.ts`).
  - Codes: NORTH-2026 (example project), VERVE-48K7 (Verve Display, expired 5 Nov 2026), VERVE-RV11 (Verve Display reopened, locks 8 Nov 2026 1:15pm).
  - Real client codes show the Demo Viewing & Copyright Agreement first; acceptance is emailed to pds.creativedesign@gmail.com.
- `PDS-Pricing-and-Packages.pdf` is the downloadable price list.

## Forms
The project brief form (homepage) and the quote form (pricing) send through Formspree.
`FORM_ENDPOINT` is set in `index.html` (Project brief form) and `pricing.html` (Quote request form). Submissions are emailed to pds.creativedesign@gmail.com.
