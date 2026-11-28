// help screenshots: phone width, light, cropped to the part each help page talks about
const {chromium}=require('playwright');const fs=require('fs');(async()=>{const b=await chromium.launch();const out=(process.argv[2]||__dirname)+'/hshots/';fs.mkdirSync(out,{recursive:true});
const U='file:///mnt/project-files/hotel-english-app/site/index.html#';
const open=async(code,w=390,ph=true)=>{const p=await b.newPage({viewport:{width:w,height:1600},deviceScaleFactor:2,colorScheme:'light',isMobile:ph,hasTouch:ph});p.on('pageerror',e=>console.log('ERR',e.message));await p.goto(U+code);if(ph)await p.addStyleTag({content:'.kc,.kbinfo{display:none!important}'});await p.waitForTimeout(1500);return p;};
const box=async(p,sels,pad=6)=>{const r=await p.evaluate(sels=>{let x0=1e9,y0=1e9,x1=0,y1=0;for(const s of sels){const e=typeof s==='string'?document.querySelector(s):null;if(!e)continue;const r=e.getBoundingClientRect();x0=Math.min(x0,r.left);y0=Math.min(y0,r.top+scrollY);x1=Math.max(x1,r.right);y1=Math.max(y1,r.bottom+scrollY);}return [x0,y0,x1,y1];},sels);return {x:Math.max(0,r[0]-pad),y:Math.max(0,r[1]-pad),width:r[2]-r[0]+pad*2,height:r[3]-r[1]+pad*2};};
const shot=async(p,name,clip)=>{clip.x=Math.max(0,clip.x);await p.screenshot({path:out+name+'.png',clip,fullPage:true});console.log(name,Math.round(clip.width),Math.round(clip.height));};
let p=await open('3-02-01');
await shot(p,'menu',await box(p,['.menubox','#bsel']));
await shot(p,'dialog',await box(p,['.dlg .line:nth-child(1)','.dlg .line:nth-child(2)','.sec>h3']));
await shot(p,'controls',await box(p,['#controls'],2));
await p.click('#tKo');await p.waitForTimeout(300);
await shot(p,'hide',await box(p,['#classRow','.sec>h3','.dlg .line:nth-child(1)','.dlg .line:nth-child(2)']));
await p.click('#tKo');
await p.click('#m-cards');await p.waitForTimeout(500);
{const c=await box(p,['.controls .seg','.wcards .wcard:nth-child(1)','.wcards .wcard:nth-child(2)','.wcards .wcard:nth-child(3)','.wcards .wcard:nth-child(4)']);c.x=0;c.width=390;await shot(p,'cards',c);}
await p.click('#m-quiz');await p.waitForTimeout(500);
{const c=await box(p,['#view']);c.x=0;c.width=390;c.height=Math.min(c.height,430);await shot(p,'quiz',c);}
await p.close();
p=await open('3-02-01');await p.fill('#q','deposit');await p.waitForTimeout(700);
{const c=await box(p,['.search']);c.x=0;c.width=390;c.height=470;await shot(p,'search',c);}
await p.close();
p=await open('3-02-01',760,false);
await shot(p,'keys',await box(p,['#controls'],0));
await p.close();
p=await open('3-02-01');{const c=await box(p,['.pnrow'],8);await shot(p,'pn',c);}
await p.close();
await b.close();})();
