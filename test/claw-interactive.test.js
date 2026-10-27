const { test } = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
function fixture(reduced=false) {
  let now=0; const context={window:{},performance:{now:()=>now},matchMedia:()=>({matches:reduced})};
  vm.runInNewContext(fs.readFileSync('docs/claw-motion.js','utf8'),context);
  const game=context.window.ClawMotion.create();
  return {game,spots:context.window.ClawMotion.spots,tick(ms){now+=ms;game.step(now)}};
}
test('inertia responds within one frame, clamps both axes, ignores duplicate drops and always delivers nearest wrapping',()=>{
  const {game:g,tick,spots}=fixture();let result;g.arm({onDrop:r=>result=r});
  g.move(1,-1);tick(16);assert(g.state.x>0&&g.state.z<0);
  for(let i=0;i<300;i++)tick(16);
  assert.equal(g.state.x,.9);assert.equal(g.state.z,-.5);
  assert.equal(g.drop('button'),true);assert.equal(g.drop('button'),false);assert.equal(g.arm({}),false);
  assert.equal(g.state.selected,5);const x=g.state.x;g.move(-1,1);tick(16);assert.equal(g.state.x,x);
  for(let i=0;i<400;i++)tick(16);
  assert.equal(g.state.phase,'reveal');assert.equal(result.selected,5);assert.equal(g.state.drops,1);
  assert.equal(g.arm({}),true);assert.equal(g.state.remaining,30);assert.equal(g.state.selected,-1);
  assert.equal(spots.length,6);g.disarm();assert.equal(g.state.phase,'idle');
});
test('timeout is clock based, exactly once; reduced motion preserves thirty seconds',()=>{
  for(const reduced of [false,true]) {const {game:g,tick}=fixture(reduced);let calls=0;g.arm({onDrop:()=>calls++});tick(29999);assert.equal(g.state.phase,'armed');tick(1);assert.equal(g.state.phase,'descend');assert.equal(g.state.reason,'timeout');for(let i=0;i<400;i++)tick(20);assert.equal(calls,1);assert.equal(g.state.drops,1);}
});
