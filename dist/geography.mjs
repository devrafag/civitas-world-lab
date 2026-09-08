export function polygons(f){return f.geometry.type==='Polygon'?[f.geometry.coordinates]:f.geometry.coordinates}
export function unwrap(ring){let prev=ring[0][0];return ring.map(([lon,lat])=>{while(lon-prev>180)lon-=360;while(lon-prev< -180)lon+=360;prev=lon;return [lon,lat]})}
function inRing(lon,lat,ring){let inside=false;for(let i=0,j=ring.length-1;i<ring.length;j=i++){const a=ring[i],b=ring[j];if((a[1]>lat)!==(b[1]>lat)&&lon<(b[0]-a[0])*(lat-a[1])/(b[1]-a[1])+a[0])inside=!inside}return inside}
export function contains(f,lon,lat){return polygons(f).some(poly=>{const rings=poly.map(unwrap);return [-360,0,360].some(shift=>inRing(lon+shift,lat,rings[0])&&!rings.slice(1).some(r=>inRing(lon+shift,lat,r)))})}
