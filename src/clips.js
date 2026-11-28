// node clips.js <codes…> -> JSON [[voice, text], …] every clip the app can play in those bundles (app.js clipsOf)
// node clips.js --by <codes…> -> JSON {code: [[voice, text], …]}
const {chromium} = require('playwright'), path = require('path');
(async () => {
  const b = await chromium.launch(), p = await b.newPage();
  await p.goto('file://' + path.join(__dirname, '..', 'site', 'index.html'));
  await p.waitForFunction(() => window.clipsOf);
  const args = process.argv.slice(2);
  if (args[0] === '--by'){   // {code: clips} for the audio packs (build.py audio_packs)
    const by = {}; for (const c of args.slice(1)) by[c] = await p.evaluate(c => clipsOf(c), c);
    process.stdout.write(JSON.stringify(by)); await b.close(); return;
  }
  const out = [];
  for (const c of args) out.push(...await p.evaluate(c => clipsOf(c), c));
  process.stdout.write(JSON.stringify(out)); await b.close();
})();
