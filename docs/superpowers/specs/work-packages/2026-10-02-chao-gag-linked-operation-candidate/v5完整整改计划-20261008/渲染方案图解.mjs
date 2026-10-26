import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import sharp from '/Users/rayz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp/dist/index.mjs';
const dir=path.dirname(fileURLToPath(import.meta.url));
const figures=JSON.parse(await fs.readFile(path.join(dir,'图解清单.json'),'utf8'));
await Promise.all(figures.map(f=>sharp(path.join(dir,f.svg),{density:144}).resize(1740).png().toFile(path.join(dir,f.file))));
// Compact sheets are only for diagram QA, never presented as game screenshots.
for(let batch=0;batch<Math.ceil(figures.length/4);batch++){
 const files=figures.slice(batch*4,batch*4+4);
 const composite=await Promise.all(files.map(async(f,i)=>({input:await sharp(path.join(dir,f.file)).resize({width:700,height:620,fit:'contain',background:'#e6ebe6'}).png().toBuffer(),left:(i%2)*700,top:Math.floor(i/2)*620})));
 await sharp({create:{width:1400,height:1240,channels:3,background:'#e6ebe6'}}).composite(composite).png().toFile(path.join(dir,'图解',`核视-${batch+1}.png`));
}
console.log(JSON.stringify({rendered:figures.length}));
