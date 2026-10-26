'use strict';
const {drawPack,drawPackForOpen}=require('./draw');
function matches(result,claimed) {
  if(!result||!Array.isArray(claimed)||result.designs.length!==claimed.length) return false;
  return result.designs.every((id,i)=>Object.prototype.hasOwnProperty.call(claimed,i)&&id===claimed[i]);
}
function verifyPack(manifest,boxId,seed,claimedDesigns) {
  return matches(drawPack(manifest,boxId,seed),claimedDesigns);
}
function verifyMint(manifest,boxId,openHeight,blockHashAtHeight,claimedDesigns,delay=1) {
  return matches(drawPackForOpen(manifest,boxId,openHeight,blockHashAtHeight,delay),claimedDesigns);
}
module.exports={verifyPack,verifyMint};
