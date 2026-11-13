export function pose(progress){
 const p=Math.max(0,Math.min(1,progress));
 return {lid:p<=.25?0:-105*Math.PI/180*((p-.25)/.75),latch:p===0?0:-80*Math.PI/180*Math.min(1,p/.25)};
}
export function validateAsset({lid,triangles,bounds}){
 if(!lid||!(triangles>0)||!bounds.length||!bounds.every(Number.isFinite)) throw Error('Invalid Haiti geometry');
}
