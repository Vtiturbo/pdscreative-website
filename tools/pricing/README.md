# Pricing tools

`prices.py` is the single source of truth for every PDS Creative price (about 30% below typical London rates).

To change prices:
1. Edit `prices.py` (run `python3 prices.py` to check every price is still ~30% below London).
2. `python3 build_page.py` updates the data and tables on `pricing.html`.
3. `npm i @fontsource/instrument-sans @fontsource/hanken-grotesk @fontsource/jetbrains-mono` (first time only), then `python3 build_pdf.py && node render.js` rebuilds `PDS-Pricing-and-Packages.pdf`.
