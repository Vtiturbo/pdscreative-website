// Renders pricelist.html to ../../PDS-Pricing-and-Packages.pdf and reports any page whose content runs into the footer.
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+__dirname+'/pricelist.html');await p.evaluate(()=>document.fonts.ready);
const o=await p.evaluate(()=>[...document.querySelectorAll('.page')].map((pg,i)=>{const f=pg.querySelector('.foot').getBoundingClientRect();let max=0;pg.querySelectorAll('*').forEach(el=>{if(el.closest('.foot')||el.closest('.tiles'))return;const r=el.getBoundingClientRect();if(r.bottom>max)max=r.bottom});return i+1+':'+Math.round(f.top-max)}));
console.log('space above footer (px):',o.join(' '));
await p.pdf({path:__dirname+'/../../PDS-Pricing-and-Packages.pdf',format:'A4',printBackground:true,preferCSSPageSize:true});await b.close()})()
