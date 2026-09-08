export const POLICIES=[{name:'Servicios públicos',cost:8},{name:'Educación',cost:9},{name:'Industria',cost:10},{name:'Comercio',cost:6},{name:'Fiscalización',cost:7},{name:'Desvío ilegal',cost:3}];
export const clamp=(v,a=0,b=100)=>Math.max(a,Math.min(b,v));
export function random(seed,month,id,salt=0){let x=(seed^Math.imul(month+1,374761393)^Math.imul(id+1,668265263)^Math.imul(salt+1,1442695041))>>>0;x=Math.imul(x^(x>>>13),1274126177);return ((x^(x>>>16))>>>0)/4294967296}
export function createWorld(data,seed=42,learning=true){return {seed,learning,month:0,enforcement:.55,shock:0,events:[],history:[],countries:data.map((d,i)=>({...d,index:i,wealth:d.income?clamp(15+Math.log10(Math.max(1,d.income)/500)*30,10,90):50,health:60,knowledge:40,trust:55,treasury:30,privateGain:0,policy:0,switches:0,q:Array.from({length:3},()=>Array(6).fill(0)),visits:Array.from({length:3},()=>Array(6).fill(0)),agents:Array.from({length:24},(_,j)=>({id:j,wellbeing:55,income:.6+random(seed,0,i,j),trust:55})),last:null}))}}
export function tick(w){w.month++;const globalTrade=w.countries.reduce((s,c)=>s+(c.policy===3),0)/Math.max(1,w.countries.length);for(const c of w.countries){const state=c.trust<40?0:c.wealth<45?1:2;const before=.4*c.wealth+.35*c.health+.25*c.trust;let action=0;
 if(w.learning){const unseen=c.visits[state].findIndex(v=>v===0);action=unseen>=0?unseen:random(w.seed,w.month,c.index,8)<.12?Math.floor(random(w.seed,w.month,c.index,9)*6):c.q[state].indexOf(Math.max(...c.q[state]));}else action=c.health<50?0:c.treasury<12?3:c.knowledge<50?1:2;
 const requested=action;if(c.treasury<POLICIES[action].cost)action=3;
 const expected=c.q[state][action],cost=Math.min(c.treasury,POLICIES[action].cost);c.treasury-=cost;const strength=cost/POLICIES[action].cost;
 const noise=(random(w.seed,w.month,c.index,1)-.5)*1.2;
 const shock=w.shock; c.wealth=clamp(c.wealth+noise-.18-shock*.9);c.health=clamp(c.health-.23-shock*.5);c.knowledge=clamp(c.knowledge-.08);c.trust=clamp(c.trust-.12);let detected=false;
 if(action===0){c.health=clamp(c.health+1.5*strength);c.trust=clamp(c.trust+.6*strength)}
 if(action===1){c.knowledge=clamp(c.knowledge+1.4*strength);c.wealth=clamp(c.wealth+.12*strength)}
 if(action===2){c.wealth=clamp(c.wealth+(1.15+c.knowledge*.012)*strength);c.health=clamp(c.health-.2*strength)}
 if(action===3){c.wealth=clamp(c.wealth+(.7+globalTrade*.8-shock*.6)*strength)}
 if(action===4){c.trust=clamp(c.trust+.9*strength)}
 if(action===5){c.privateGain+=2*strength;c.health=clamp(c.health-.65*strength);c.trust=clamp(c.trust-.35*strength);detected=random(w.seed,w.month,c.index,2)<w.enforcement;if(detected){const fine=Math.min(c.privateGain,5);c.privateGain-=fine;c.treasury+=fine;c.trust=clamp(c.trust-2)}}
 c.wealth=clamp(c.wealth+(c.knowledge-40)*.008);c.treasury=clamp(c.treasury+4+c.wealth*.07,0,150);
 let wellbeing=0;for(const a of c.agents){const target=.4*c.wealth+.35*c.health+.25*c.trust+(a.income-1)*9;a.wellbeing=clamp(a.wellbeing*.8+target*.2);a.trust=clamp(a.trust*.9+c.trust*.1);wellbeing+=a.wellbeing}c.wellbeing=wellbeing/c.agents.length;
 const after=.4*c.wealth+.35*c.health+.25*c.trust;const reward=after-before+(action===5?(detected?-3:1.1)*strength:0);
 if(w.learning){c.visits[state][action]++;c.q[state][action]+=.28*(reward-c.q[state][action]);}
 const old=c.policy;if(action!==old)c.switches++;c.policy=action;c.last={month:w.month,from:old,action,state,expected,reward,detected,requested,reason:detected?'Infracción detectada y sancionada':requested!==action?'Presupuesto insuficiente; alternativa asequible':w.learning?'Selección y actualización por recompensa observada':'Regla fija de prioridades'};
 if(action!==old||detected)w.events.unshift({country:c.id,name:c.name,...c.last});
 }w.events=w.events.slice(0,400);w.history.push({month:w.month,wellbeing:w.countries.reduce((s,c)=>s+c.wellbeing,0)/w.countries.length});if(w.history.length>601)w.history.shift();return w}
