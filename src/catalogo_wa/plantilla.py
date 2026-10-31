# Plantilla v2 del sitio generado. Marcadores reemplazados por generador.py con
# datos escapados: __NEGOCIO__, __NEGOCIO_JSON__, __TELEFONO__, __MONEDA__,
# __COLOR__, __BIENVENIDA__, __PRODUCTOS_JSON__, __I18N_JSON__, __JSONLD__,
# __CUPONES_JSON__, __ENVIO_JSON__, __LANG__
PLANTILLA = r"""<!DOCTYPE html>
<html lang="__LANG__"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__NEGOCIO__ — Catalogo</title>
<meta name="description" content="Catalogo en linea de __NEGOCIO__. Pide por WhatsApp, sin registro.">
<meta property="og:title" content="__NEGOCIO__"><meta property="og:type" content="website">
<link rel="manifest" href="manifest.webmanifest">
<script type="application/ld+json">__JSONLD__</script>
<style>
:root{--c:__COLOR__}*{box-sizing:border-box}body{margin:0;font-family:system-ui,Arial,sans-serif;background:#f6f6f8;color:#1a1a2e}
header{background:var(--c);color:#fff;padding:20px 16px;position:sticky;top:0;z-index:5}
header h1{margin:0;font-size:22px}header p{margin:4px 0 0;opacity:.9;font-size:14px}
.bar{display:flex;gap:8px;flex-wrap:wrap;margin:12px 16px}
input,select{padding:10px;border:1px solid #ccc;border-radius:10px;font-size:15px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(175px,1fr));gap:12px;padding:0 16px 90px}
.card{background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.08);display:flex;flex-direction:column;position:relative}
.badge{position:absolute;top:8px;left:8px;background:#e0245e;color:#fff;padding:2px 8px;border-radius:8px;font-size:12px;font-weight:700}
.card img{width:100%;height:150px;object-fit:cover;background:#e8e8f0}
.foto{height:150px;display:flex;align-items:center;justify-content:center;background:#e8e8f0;font-size:44px}
.card .c{padding:10px;flex:1;display:flex;flex-direction:column;gap:4px}
.precio{font-weight:700;font-size:17px}.antes{text-decoration:line-through;color:#888;font-size:13px}
.cat{font-size:12px;color:#666}button{cursor:pointer;border:0;border-radius:10px;padding:10px;font-size:15px}
.add{background:var(--c);color:#fff;margin-top:auto}.add:disabled{background:#999}
#cartbar{position:fixed;left:0;right:0;bottom:0;background:#fff;border-top:1px solid #ddd;padding:12px 16px;display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap}
#send{background:#25d366;font-weight:700;color:#063}
#panel{position:fixed;inset:auto 0 0 0;max-height:65vh;overflow:auto;background:#fff;border-top:2px solid #1a1a2e;padding:14px 16px;display:none;z-index:9}
#panel.open{display:block}.row{display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #eee;gap:8px}
.q button{padding:2px 10px;background:#eee}.desglose p{margin:4px 0;text-align:right}
</style></head><body>
<header><h1>__NEGOCIO__</h1><p>__BIENVENIDA__</p></header>
<div class="bar"><input id="q" type="search" aria-label="buscar">
<select id="cat"></select>
<select id="ord"></select></div>
<main class="grid" id="grid"></main>
<div id="cartbar"><span id="resumen"></span>
<span><button id="ver"></button> <button id="send"></button></span></div>
<div id="panel"><h3 id="t-pedido"></h3><div id="items"></div>
<div class="bar"><input id="cup" type="text"><button id="aplicar"></button></div>
<div class="desglose" id="desglose"></div></div>
<script>
const TEL="__TELEFONO__", MONEDA="__MONEDA__", NEGOCIO=__NEGOCIO_JSON__, T=__I18N_JSON__;
const PRODUCTOS=__PRODUCTOS_JSON__, CUPONES=__CUPONES_JSON__, ENVIO=__ENVIO_JSON__;
const SIMB={PEN:"S/",USD:"$",EUR:"€",MXN:"$",COP:"$",CLP:"$",ARS:"$"};
const fmt=n=>(SIMB[MONEDA]||"")+" "+Number(n).toLocaleString("es",{minimumFractionDigits:2,maximumFractionDigits:2});
let carrito=new Map(JSON.parse(localStorage.getItem("carrito")||"[]")); let cuponActivo="";
document.querySelector("header p").textContent=document.querySelector("header p").textContent||"";
const $=id=>document.getElementById(id);
$("q").placeholder=T.buscar; $("ver").textContent=T.ver; $("send").textContent=T.enviar;
$("t-pedido").textContent=T.pedido; $("cup").placeholder=T.cupon; $("aplicar").textContent=T.aplicar;
const catSel=$("cat"); catSel.innerHTML=""; const o0=document.createElement("option"); o0.value=""; o0.textContent=T.todas; catSel.appendChild(o0);
[...new Set(PRODUCTOS.map(p=>p.categoria))].forEach(c=>{const o=document.createElement("option");o.value=c;o.textContent=c;catSel.appendChild(o)});
const ord=$("ord"); [["",T.ordenar+": "+T.recientes],["precio_asc",T.precio_asc],["precio_desc",T.precio_desc],["nombre",T.nombre]].forEach(([v,t])=>{const o=document.createElement("option");o.value=v;o.textContent=t;ord.appendChild(o)});
function guardar(){localStorage.setItem("carrito",JSON.stringify([...carrito]))}
function clave(p,v){return v?p.id+"::"+v:p.id}
function pintar(){
  const q=$("q").value.toLowerCase(), cat=catSel.value;
  let lista=PRODUCTOS.filter(p=>(!cat||p.categoria===cat)&&p.nombre.toLowerCase().includes(q));
  if(ord.value==="precio_asc")lista.sort((a,b)=>a.precio_final-b.precio_final);
  if(ord.value==="precio_desc")lista.sort((a,b)=>b.precio_final-a.precio_final);
  if(ord.value==="nombre")lista.sort((a,b)=>a.nombre.localeCompare(b.nombre));
  const g=$("grid"); g.innerHTML="";
  lista.forEach(p=>{
    const d=document.createElement("div"); d.className="card";
    if(p.descuento_pct>0){const b=document.createElement("span");b.className="badge";b.textContent=T.oferta+" -"+p.descuento_pct+"%";d.appendChild(b)}
    const media=p.imagen_url?Object.assign(document.createElement("img"),{src:p.imagen_url,alt:p.nombre}):Object.assign(document.createElement("div"),{className:"foto",textContent:"🛍️"});
    const c=document.createElement("div"); c.className="c";
    const n=document.createElement("strong"); n.textContent=p.nombre;
    const ct=document.createElement("span"); ct.className="cat"; ct.textContent=p.categoria;
    const des=document.createElement("span"); des.textContent=p.descripcion||"";
    const pr=document.createElement("span");
    if(p.descuento_pct>0){const a=document.createElement("span");a.className="antes";a.textContent=fmt(p.precio);pr.append(a,document.createTextNode(" "));}
    const pf=document.createElement("span"); pf.className="precio"; pf.textContent=fmt(p.precio_final); pr.appendChild(pf);
    let sel=null;
    if(p.variantes&&p.variantes.length){sel=document.createElement("select");p.variantes.forEach(v=>{const o=document.createElement("option");o.value=v.nombre;o.textContent=v.nombre+(v.stock===0?" ("+T.agotado+")":"");o.disabled=v.stock===0;sel.appendChild(o)});}
    const b=document.createElement("button"); b.className="add"; b.textContent=p.agotado?T.agotado:T.agregar; b.disabled=!!p.agotado;
    b.onclick=()=>{const k=clave(p,sel?sel.value:"");carrito.set(k,(carrito.get(k)||0)+1);guardar();resumen()};
    c.append(n,ct,des,pr); if(sel)c.appendChild(sel); c.appendChild(b); d.append(media,c); g.appendChild(d);
  });
  resumen();
}
function desglose(){
  let sub=0; carrito.forEach((cant,k)=>{const [id,v]=k.split("::");const p=PRODUCTOS.find(x=>x.id===id); if(p)sub+=cant*p.precio_final});
  let desc=0; const cup=CUPONES.find(c=>c.codigo===cuponActivo);
  if(cup)desc=cup.tipo==="porcentaje"?sub*cup.valor/100:Math.min(cup.valor,sub);
  const base=sub-desc; const envio=ENVIO.gratis_desde!==null&&base>=ENVIO.gratis_desde?0:ENVIO.costo;
  return {sub,desc,envio,total:base+envio};
}
function resumen(){
  let cant=0; carrito.forEach(c=>cant+=c); const d=desglose();
  $("resumen").textContent=cant?cant+" — "+fmt(d.total):T.vacio;
  const it=$("items"); it.innerHTML="";
  carrito.forEach((c,k)=>{const [id,v]=k.split("::");const p=PRODUCTOS.find(x=>x.id===id); if(!p)return;
    const r=document.createElement("div"); r.className="row";
    const s=document.createElement("span"); s.textContent=c+" x "+p.nombre+(v?" ("+v+")":"")+" = "+fmt(c*p.precio_final);
    const q=document.createElement("span"); q.className="q";
    const menos=document.createElement("button"); menos.textContent="−"; menos.onclick=()=>{c<=1?carrito.delete(k):carrito.set(k,c-1);guardar();pintar()};
    const mas=document.createElement("button"); mas.textContent="+"; mas.onclick=()=>{carrito.set(k,c+1);guardar();pintar()};
    q.append(menos,mas); r.append(s,q); it.appendChild(r);});
  $("desglose").innerHTML="";
  [[T.subtotal,d.sub],[T.descuento,-d.desc],[T.envio,d.envio],[T.total,d.total]].forEach(([t,v])=>{
    if(t===T.descuento&&!d.desc)return; const p=document.createElement("p"); p.textContent=t+": "+(t===T.envio&&d.envio===0?T.gratis:fmt(Math.abs(v))); $("desglose").appendChild(p);});
}
$("aplicar").onclick=()=>{cuponActivo=$("cup").value.trim().toUpperCase();resumen()};
$("ver").onclick=()=>{$("panel").classList.toggle("open");resumen()};
$("q").oninput=pintar; catSel.onchange=pintar; ord.onchange=pintar;
$("send").onclick=()=>{
  if(!carrito.size){alert(T.vacio);return}
  const d=desglose(); const lineas=[T.saludo.replace("{negocio}",NEGOCIO),""];
  carrito.forEach((c,k)=>{const [id,v]=k.split("::");const p=PRODUCTOS.find(x=>x.id===id); if(p)lineas.push("- "+c+" x "+p.nombre+(v?" ("+v+")":"")+" = "+fmt(c*p.precio_final))});
  if(d.desc)lineas.push(T.descuento+" ("+cuponActivo+"): -"+fmt(d.desc));
  lineas.push(T.envio+": "+(d.envio===0?T.gratis:fmt(d.envio)),"",T.total+": "+fmt(d.total),T.gracias);
  window.open("https://wa.me/"+TEL+"?text="+encodeURIComponent(lineas.join("\n")),"_blank");
};
pintar();
</script></body></html>
"""
