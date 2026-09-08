import assert from 'node:assert/strict';import fs from 'node:fs';import {contains,unwrap} from '../dist/geography.mjs';
const features=JSON.parse(fs.readFileSync(new URL('../dist/borders.json',import.meta.url))).features;
for(const [id,lon,lat] of [['ESP',-3.7,40.4],['FRA',2.35,48.85],['USA',-100,40],['BRA',-47.88,-15.79],['JPN',139.69,35.69],['AUS',149.1,-35.3]]){const f=features.find(f=>f.properties.id===id);assert(contains(f,lon,lat),id);assert(!contains(f,-30,0),id+' must not include the Atlantic');}
const dateline={geometry:{type:'Polygon',coordinates:[[[179,-10],[-179,-10],[-179,10],[179,10],[179,-10]]]}};assert(contains(dateline,179.5,0));assert(contains(dateline,-179.5,0));assert(!contains(dateline,0,0));assert.equal(unwrap([[179,0],[-179,0]])[1][0],181);
console.log('PASS: capital/territory selection, ocean exclusion and antimeridian wrapping.');
