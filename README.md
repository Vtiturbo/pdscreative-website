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
  - Live demos can have several design variants (`variants` in `PROJECTS`); the client switches between them with tabs and the approval email says which one they chose.
  - Codes: KNIFE-7K3Q (Knifeline tattoo studio, 3 variants, locks 20 Nov 2026 6:15pm; old code VOID-7K3Q still works), NORTH-2026 (example project), VERVE-48K7 (Verve Display, expired 5 Nov 2026), VERVE-RV11 (Verve Display reopened, locks 8 Nov 2026 1:15pm).
  - On phones (820px wide or less) the demo fills the screen; a floating timer button opens a slide-out panel with variants, approval, comments, timeline and the how-to video. Desktop is unchanged.
  - Real client codes show the Demo Viewing & Copyright Agreement first; acceptance is emailed to pds.creativedesign@gmail.com.
- `PDS-Pricing-and-Packages.pdf` is the downloadable price list.

## Forms
The project brief form (homepage) and the quote form (pricing) send through Formspree.
`FORM_ENDPOINT` is set in `index.html` (Project brief form) and `pricing.html` (Quote request form). Submissions are emailed to pds.creativedesign@gmail.com.

## Free demos hosted here
- `demos/vt-q8m2x/` holds the Knifeline demo (variants `a` UV Ritual, `b` Chrome Void, `c` Bone & Ink; the logo is left out of demos as it is a paid extra). Each page has the demo guard (watermark, copy blocking, countdown, lock).
- `functions/demos/vt-q8m2x/_middleware.js` (Cloudflare Pages Function) locks the files server-side at the deadline, stops search indexing and only allows framing by pdscreative.com.
