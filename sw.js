/* Service worker — deixa o app disponível sem internet.
   Estratégia: responde do cache na hora (abre mesmo sem sinal) e, quando há internet,
   busca a versão nova em segundo plano. Se o app mudou, avisa a página para o botão
   "Sincronizar" aplicar a atualização. Dados (Firebase) não passam por aqui. */
const CACHE='controle-massa-app-v1';
const SDK='https://www.gstatic.com/firebasejs/10.14.1/';
const CORE=['./','index.html','geo.json','manifest.webmanifest','logo-neovia.png','logo-neovia-white.png','neovia-mark.png','apple-touch-icon.png','icon-512.png'];
const EXTRA=[SDK+'firebase-app.js',SDK+'firebase-auth.js',SDK+'firebase-firestore.js'];

self.addEventListener('install',e=>{
  e.waitUntil((async()=>{
    const c=await caches.open(CACHE);
    await Promise.all([...CORE,...EXTRA].map(u=>c.add(new Request(u,{cache:'reload'})).catch(()=>{})));
    await self.skipWaiting();
  })());
});
self.addEventListener('activate',e=>{
  e.waitUntil((async()=>{
    for(const k of await caches.keys())if(k!==CACHE)await caches.delete(k);
    await self.clients.claim();
  })());
});

const isShell=req=>req.mode==='navigate';
async function notify(msg){for(const c of await self.clients.matchAll({includeUncontrolled:true}))c.postMessage(msg)}
async function revalidate(req,key,cache){
  try{
    const res=await fetch(req,{cache:'no-cache'});
    if(!res||!res.ok)return null;
    const old=await cache.match(key);
    if(key.endsWith('index.html')&&old){
      const [a,b]=await Promise.all([old.clone().text(),res.clone().text()]);
      if(a!==b){await cache.put(key,res.clone());notify({type:'app-update'});return res}
      return res;
    }
    await cache.put(key,res.clone());
    return res;
  }catch{return null}
}
self.addEventListener('fetch',e=>{
  const req=e.request;
  if(req.method!=='GET')return;
  const url=new URL(req.url);
  const same=url.origin===self.location.origin, sdk=req.url.startsWith(SDK);
  if(!same&&!sdk)return;                       // Firestore, login etc.: direto para a rede
  if(same&&url.pathname.endsWith('/sw.js'))return;
  e.respondWith((async()=>{
    const cache=await caches.open(CACHE);
    const key=isShell(req)?new URL('index.html',self.registration.scope).href:(same?url.origin+url.pathname:req.url);
    const hit=await cache.match(key);
    if(hit){ if(!sdk)e.waitUntil(revalidate(isShell(req)?key:req,key,cache)); return hit }
    const fresh=await revalidate(isShell(req)?key:req,key,cache);
    if(fresh)return fresh;
    if(isShell(req)){const shell=await cache.match(new URL('index.html',self.registration.scope).href);if(shell)return shell}
    return new Response('Sem conexão e sem cópia guardada deste arquivo.',{status:503,headers:{'Content-Type':'text/plain; charset=utf-8'}});
  })());
});
self.addEventListener('message',e=>{
  if(e.data==='check-update'){
    e.waitUntil((async()=>{const cache=await caches.open(CACHE);const key=new URL('index.html',self.registration.scope).href;
      await Promise.all(CORE.map(u=>revalidate(new Request(new URL(u,self.registration.scope).href),new URL(u,self.registration.scope).href.replace(/\/$/,'/'),cache)));
      notify({type:'checked'});})());
  }
});
