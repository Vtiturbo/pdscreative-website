# Pricing tools

`prices.py` is the single source of truth for every PDS Creative price, with a typical London rate for each service for comparison.

To change prices:
1. Edit `prices.py` (run `python3 prices.py` to see each price against London).
2. `python3 build_page.py` updates the data and tables on `pricing.html`.
3. `npm i @fontsource/instrument-sans @fontsource/hanken-grotesk @fontsource/jetbrains-mono` (first time only), then `python3 build_pdf.py && node render.js` rebuilds `PDS-Pricing-and-Packages.pdf`.
