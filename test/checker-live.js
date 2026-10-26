'use strict';
// Opt-in live, read-only GETs. Never run as part of deterministic fixture tests.
const assert=require('node:assert/strict');
const {checkBox}=require('../docs/vaultcheck');
(async()=>{
 for(const [label,id,expected] of [
  ['Box A','f3590347ca2a6bd8ea4fcfaca5eafb6f209e25de537f177df07ebf6e7d82dd39',/^SEALED-(VERIFIED|PENDING)$/],
  ['Box B','2aaa4efa643ea03ffaa2af4542c17d841ad9eaa558f382edab5a61f02107e67f',/^OPENED-(VERIFIED|PENDING)$/],
 ]){const r=await checkBox(id);console.log(JSON.stringify({label,checkedAt:new Date().toISOString(),...r}));assert.match(r.verdict,expected);}
})().catch(e=>{console.error(e);process.exitCode=1;});
