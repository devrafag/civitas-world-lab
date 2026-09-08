import assert from 'node:assert/strict';import fs from 'node:fs';import {scenario} from '../dist/scenarios.mjs';
const p=JSON.parse(fs.readFileSync(new URL('../dist/profiles.json',import.meta.url))).profiles;const find=id=>p.find(p=>p.id===id);
assert.throws(()=>scenario(find('ESP'),find('ESP'),'trade'));assert.throws(()=>scenario(find('ESP'),find('MAR'),'war'));
const s=scenario(find('ESP'),find('FRA'),'diplomacy');assert(s.constraints.some(x=>x.includes('OTAN')));assert.equal(s.paths.length,3);assert(!('probability' in s));assert(!scenario(find('ESP'),find('MAR'),'trade').constraints.some(x=>x.includes('OTAN')));
const n={countries:['ESP','MAR'],title:'A trade story'};assert.equal(scenario(find('ESP'),find('MAR'),'trade',[n]).items.length,1);assert.equal(scenario(find('USA'),find('MAR'),'trade',[n]).items.length,0);
console.log('PASS: valid pairs, institutional constraints, conditional paths and news co-mentions.');
