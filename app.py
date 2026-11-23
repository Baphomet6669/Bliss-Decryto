import os
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

# Owner: shivam

PAGE = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#08090d">
<title>ULTRON AI</title>
<style>
:root{--red:#ff2638;--red2:#9d0718;--cyan:#73eaff;--bg:#07080c}
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:var(--bg);color:#f5f6f8;font-family:Arial,Helvetica,sans-serif}
body{background:radial-gradient(ellipse at 50% 65%,#4d1010 0,#17090d 34%,#07080c 72%)}
.scene{position:fixed;inset:0;overflow:hidden;isolation:isolate;background:
 radial-gradient(ellipse at 50% 100%,rgba(255,70,12,.36),transparent 42%),
 linear-gradient(180deg,rgba(3,4,8,.35),rgba(5,5,8,.12) 45%,rgba(0,0,0,.8))}
.city{position:absolute;inset:28% 0 0;opacity:.75;z-index:-2;background:
 linear-gradient(90deg,transparent 0 3%,#090a0e 3% 8%,transparent 8% 11%,#111016 11% 17%,transparent 17% 20%,#0b0c11 20% 27%,transparent 27% 31%,#111017 31% 38%,transparent 38% 42%,#090a0e 42% 48%,transparent 48% 53%,#141017 53% 60%,transparent 60% 64%,#0b0c10 64% 72%,transparent 72% 77%,#111016 77% 84%,transparent 84% 89%,#090a0e 89% 96%,transparent 96%)}
.city:after{content:"";position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent 0 28px,rgba(255,90,30,.25) 29px 31px,transparent 32px 55px);mask-image:linear-gradient(180deg,#000,transparent)}
.flames{position:absolute;inset:auto 0 0;height:34%;z-index:-1;opacity:.8;background:
 radial-gradient(ellipse at 18% 100%,#ff5b12 0,rgba(255,50,0,.35) 12%,transparent 35%),
 radial-gradient(ellipse at 76% 100%,#ff3210 0,rgba(255,70,0,.35) 16%,transparent 38%),
 radial-gradient(ellipse at 48% 100%,#ff9b18 0,rgba(255,30,0,.25) 12%,transparent 32%)}
.smoke{position:absolute;inset:0;z-index:-1;pointer-events:none;background:radial-gradient(ellipse at 20% 55%,rgba(90,91,103,.17),transparent 30%),radial-gradient(ellipse at 83% 42%,rgba(100,94,100,.15),transparent 32%);filter:blur(22px)}
.topbar{position:absolute;top:0;left:0;right:0;padding:22px 28px;display:flex;justify-content:space-between;align-items:center;z-index:5}
.brand{font-weight:900;letter-spacing:.28em;font-size:clamp(18px,2vw,26px);text-shadow:0 0 18px #f22}
.brand span{color:var(--red)}
.status{font-size:11px;letter-spacing:.18em;color:#ff8d95;border:1px solid #8f2733;padding:9px 13px;background:#1a080bbd}
.status i{display:inline-block;width:7px;height:7px;border-radius:50%;background:#ff273d;box-shadow:0 0 12px #ff273d;margin-right:8px}
.stage{position:absolute;inset:72px 0 98px;display:flex;align-items:center;justify-content:center}
.floor{position:absolute;bottom:0;width:min(900px,95vw);height:150px;background:radial-gradient(ellipse,rgba(255,52,20,.34),transparent 67%);border-radius:50%;transform:rotateX(65deg)}
#ultronCanvas{width:100%;height:100%;display:block;z-index:2;touch-action:none;will-change:transform}
.caption{position:absolute;bottom:10px;text-align:center;letter-spacing:.28em;font-size:11px;color:#c6c8ce;text-shadow:0 0 12px #f22;z-index:3;pointer-events:none}
.controls{position:absolute;left:50%;bottom:22px;transform:translateX(-50%);width:min(720px,94vw);display:flex;align-items:center;justify-content:center;gap:10px;flex-wrap:wrap;z-index:5}
button{border:1px solid #76303a;background:rgba(15,10,15,.88);color:#f5f5f7;padding:12px 17px;letter-spacing:.12em;font-size:10px;font-weight:700;cursor:pointer;transition:.2s}
button:hover,button:focus{border-color:#ff3448;box-shadow:0 0 18px #ff263844;outline:none}
button.primary{background:linear-gradient(135deg,#a50c20,#4d0913);border-color:#ff3348}
button.active{background:#64101c;border-color:#ff3348}
.zoom{display:flex;align-items:center;gap:9px;border:1px solid #59212a;background:#100b10;padding:8px 12px;color:#bbb;font-size:10px}
input[type=range]{width:95px;accent-color:#ff2638}
.console{position:absolute;left:24px;bottom:115px;width:230px;color:#d6a4a8;font:10px/1.8 monospace;letter-spacing:.05em;opacity:.85;z-index:3;pointer-events:none}
.console strong{color:#ff5261}
.mic-state{position:absolute;right:24px;bottom:115px;text-align:right;font:10px/1.8 monospace;color:#c7c7cc;z-index:3;pointer-events:none}
.mic-state strong{color:#ff5261}
.chat{position:absolute;top:82px;right:22px;width:min(280px,42vw);padding:13px;background:rgba(5,7,11,.62);border:1px solid #57232c;backdrop-filter:blur(8px);font-size:12px;z-index:4}
.chat small{display:block;color:#ff6876;letter-spacing:.18em;margin-bottom:7px}
#reply{color:#eee;min-height:30px;line-height:1.5}
@media(max-width:650px){.topbar{padding:16px}.stage{inset:70px 0 142px}.chat{top:68px;right:10px;width:155px;font-size:10px}.console{left:12px;bottom:142px;width:150px;font-size:8px}.mic-state{right:12px;bottom:142px;font-size:8px}.controls{bottom:13px;gap:6px}button{padding:11px 12px;font-size:9px}.zoom{padding:7px}.caption{bottom:5px;font-size:9px}}
</style>
</head>
<body>
<div class="scene">
 <div class="city"></div><div class="flames"></div><div class="smoke"></div>
 <header class="topbar"><div class="brand">ULTRON<span>.</span>AI</div><div class="status"><i></i> SYSTEM ONLINE</div></header>
 <div class="chat"><small>ULTRON // RESPONSE</small><div id="reply">Awaiting your command, Shivam Sir.</div></div>
 <main class="stage">
  <div class="floor"></div>
  <canvas id="ultronCanvas"></canvas>
  <div class="caption">ARTIFICIAL INTELLIGENCE // SUPERIOR MACHINE INTELLIGENCE</div>
 </main>
 <div class="console">CORE STATUS: <strong>STABLE</strong><br>THREAT LEVEL: <strong>MAXIMUM</strong><br>LANGUAGE: <strong>EN / HI</strong></div>
 <div class="mic-state">VOICE LINK: <strong id="voiceStatus">STANDBY</strong><br>MIC: <strong id="micStatus">READY</strong></div>
 <nav class="controls">
  <button class="primary" id="micBtn">🎙 SPEAK</button>
  <button id="sitBtn">SIT MODE</button>
  <button id="standBtn" class="active">STAND</button>
  <div class="zoom">ZOOM <input id="zoom" type="range" min=".65" max="1.65" step=".05" value="1"><span id="zoomVal">100%</span></div>
  <button id="resetBtn">RESET VIEW</button>
 </nav>
</div>

<script>
const reply=document.getElementById('reply'),
      voiceStatus=document.getElementById('voiceStatus'),
      micStatus=document.getElementById('micStatus'),
      sitBtn=document.getElementById('sitBtn'),
      standBtn=document.getElementById('standBtn'),
      canvas=document.getElementById('ultronCanvas'),
      ctx=canvas.getContext('2d');

const state={
  zoom:1,
  targetZoom:1,
  sitMode:false,
  sitBlend:0,
  speaking:false,
  talkAmp:0,
  px:0,
  py:0,
  lookX:0,
  lookY:0
};

function resize(){
  const dpr=Math.min(window.devicePixelRatio||1,1.5);
  const w=Math.max(1,canvas.clientWidth);
  const h=Math.max(1,canvas.clientHeight);
  canvas.width=Math.floor(w*dpr);
  canvas.height=Math.floor(h*dpr);
  ctx.setTransform(dpr,0,0,dpr,0,0);
}
window.addEventListener('resize',resize);
resize();

window.addEventListener('pointermove',e=>{
  state.px=Math.max(-1,Math.min(1,(e.clientX/window.innerWidth)*2-1));
  state.py=Math.max(-1,Math.min(1,(e.clientY/window.innerHeight)*2-1));
});

// Smooth curved path builder for organic Age of Ultron armor contours
function curvePath(pts,closed=true){
  ctx.beginPath();
  if(!pts.length)return;
  if(pts.length<3){
    ctx.moveTo(pts[0][0],pts[0][1]);
    for(let i=1;i<pts.length;i++)ctx.lineTo(pts[i][0],pts[i][1]);
    if(closed)ctx.closePath();
    return;
  }
  const n=pts.length;
  const start=closed?[(pts[n-1][0]+pts[0][0])*0.5,(pts[n-1][1]+pts[0][1])*0.5]:pts[0];
  ctx.moveTo(start[0],start[1]);
  const endIdx=closed?n:n-1;
  for(let i=0;i<endIdx;i++){
    const p1=pts[i];
    const p2=pts[(i+1)%n];
    const mx=i===endIdx-1&&!closed?p2[0]:(p1[0]+p2[0])*0.5;
    const my=i===endIdx-1&&!closed?p2[1]:(p1[1]+p2[1])*0.5;
    ctx.quadraticCurveTo(p1[0],p1[1],mx,my);
  }
  if(!closed){
    const last=pts[n-1];
    ctx.lineTo(last[0],last[1]);
  }else{
    ctx.closePath();
  }
}

// Chrome / Titanium cylindrical & curved surface gradient
function metalFill(x1,y1,x2,y2,mode='armor'){
  const g=ctx.createLinearGradient(x1,y1,x2,y2);
  if(mode==='dark'){
    g.addColorStop(0,'#2b323d');
    g.addColorStop(0.25,'#11161f');
    g.addColorStop(0.6,'#080b10');
    g.addColorStop(0.88,'#202732');
    g.addColorStop(1,'#090c12');
  }else if(mode==='joint'){
    g.addColorStop(0,'#465161');
    g.addColorStop(0.3,'#1a2029');
    g.addColorStop(0.7,'#0a0d12');
    g.addColorStop(1,'#2c3542');
  }else{
    g.addColorStop(0,'#f2f6fa');
    g.addColorStop(0.16,'#a3aebc');
    g.addColorStop(0.38,'#3a4350');
    g.addColorStop(0.56,'#181e27');
    g.addColorStop(0.77,'#c4ceda');
    g.addColorStop(0.92,'#505b6b');
    g.addColorStop(1,'#1c232d');
  }
  return g;
}

function drawPlate(pts,bounds,opts={}){
  curvePath(pts,opts.closed!==false);
  ctx.fillStyle=metalFill(bounds[0],bounds[1],bounds[2],bounds[3],opts.mode||'armor');
  ctx.fill();
  if(opts.stroke!==false){
    ctx.strokeStyle=opts.strokeColor||(opts.mode==='dark'?'rgba(130,145,165,0.28)':'rgba(235,244,255,0.52)');
    ctx.lineWidth=opts.lw||1.2;
    ctx.stroke();
  }
}

function drawRedSlit(pts,intensity=1){
  ctx.save();
  ctx.shadowColor=`rgba(255,24,42,${0.95*intensity})`;
  ctx.shadowBlur=14*intensity;
  curvePath(pts,true);
  ctx.fillStyle='#ff1930';
  ctx.fill();
  ctx.shadowBlur=4;
  ctx.fillStyle='#ffd6dc';
  ctx.fill();
  ctx.restore();
}

// Draws Age of Ultron Prime body in local coordinates where head center is around y=0
// and full body spans y = -68 (top of head) to y = +440 (feet)
function drawUltron(t,talk,breath,lookX,lookY){
  const bodyShiftX=lookX*6;
  const bodyShiftY=breath*2.2;

  // 1. Dark Inner Skeletal Spine, Ribcage & Pelvis Core
  drawPlate([
    [-22,38],[-46,82],[-54,155],[-36,225],[-24,258],
    [24,258],[36,225],[54,155],[46,82],[22,38]
  ],[-56,38,56,258],{mode:'dark',lw:1.2});

  // Glowing crimson inner chassis vents behind ribs & waist
  drawRedSlit([[-18,125],[-10,122],[-13,188],[-21,192]],0.75+0.15*Math.sin(t*3));
  drawRedSlit([[18,125],[10,122],[13,188],[21,192]],0.75+0.15*Math.sin(t*3));
  drawRedSlit([[-6,198],[6,198],[4,232],[-4,232]],0.65);

  // 2. Neck & Hydraulic Pistons
  drawPlate([[-16,18],[16,18],[22,56],[-22,56]],[-22,18,22,56],{mode:'dark'});
  for(const s of [-1,1]){
    drawPlate([[s*8,16],[s*15,16],[s*20,54],[s*12,54]],[s*8,16,s*20,54],{mode:'armor',lw:1.1});
    drawRedSlit([[s*16,28],[s*19,28],[s*21,46],[s*18,46]],0.7);
  }
  drawPlate([[-28,46],[0,54],[28,46],[34,62],[0,70],[-34,62]],[-34,46,34,70],{mode:'armor',lw:1.3});

  // 3. Broad Curved Shoulder Pauldrons + Circular Red Shoulder Bearings
  for(const s of [-1,1]){
    // Inner circular red/dark shoulder socket (signature Ultron shoulder detail)
    const sx=s*56, sy=84+bodyShiftY;
    ctx.beginPath();ctx.arc(sx,sy,15,0,Math.PI*2);
    ctx.fillStyle='#141820';ctx.fill();
    ctx.strokeStyle='#ff2238';ctx.lineWidth=2.5;ctx.stroke();

    // Swept upper pauldron shell
    drawPlate([
      [s*22,58+bodyShiftY],[s*56,56+bodyShiftY],[s*88,78+bodyShiftY],
      [s*92,114+bodyShiftY],[s*62,126+bodyShiftY],[s*38,104+bodyShiftY]
    ],[s*22,56+bodyShiftY,s*92,126+bodyShiftY],{mode:'armor',lw:1.4});

    // Overlapping lower shoulder plate
    drawPlate([
      [s*44,78+bodyShiftY],[s*76,76+bodyShiftY],[s*86,108+bodyShiftY],[s*54,116+bodyShiftY]
    ],[s*44,76+bodyShiftY,s*86,116+bodyShiftY],{mode:'joint',lw:1.1});
  }

  // 4. Sculpted Pectoral Armor & Swept Rib-Wing Plates
  for(const s of [-1,1]){
    // Main upper chest / pec plate sweeping outward to shoulder
    drawPlate([
      [s*6,64+bodyShiftY],[s*46,62+bodyShiftY],[s*68,86+bodyShiftY],
      [s*58,118+bodyShiftY],[s*24,104+bodyShiftY],[s*8,88+bodyShiftY]
    ],[s*6,62+bodyShiftY,s*68,118+bodyShiftY],{mode:'armor',lw:1.4});

    // Swept rib armor arcs
    for(let r=0;r<3;r++){
      const ry=112+r*22+bodyShiftY;
      const rw=48-r*5;
      drawPlate([
        [s*8,ry],[s*rw,ry-8],[s*(rw-4),ry+12],[s*10,ry+16]
      ],[s*8,ry-8,s*rw,ry+16],{mode:'armor',lw:1.1});
    }
  }

  // Center sternum spine ridge
  drawPlate([[-8,64+bodyShiftY],[8,64+bodyShiftY],[10,178+bodyShiftY],[-10,178+bodyShiftY]],[-10,64,10,178],{mode:'joint',lw:1.1});

  // 5. Sleek Curved Arms, Elbow Servos, Forearms & Claws
  for(const s of [-1,1]){
    // Upper arm / bicep
    drawPlate([
      [s*62,102+bodyShiftY],[s*86,104+bodyShiftY],[s*92,162+bodyShiftY],[s*66,160+bodyShiftY]
    ],[s*62,102+bodyShiftY,s*92,162+bodyShiftY],{mode:'armor',lw:1.2});
    // Elbow joint
    drawPlate([
      [s*66,158+bodyShiftY],[s*90,160+bodyShiftY],[s*86,182+bodyShiftY],[s*64,180+bodyShiftY]
    ],[s*64,158+bodyShiftY,s*90,182+bodyShiftY],{mode:'joint',lw:1.1});
    // Forearm gauntlet
    drawPlate([
      [s*64,180+bodyShiftY],[s*88,182+bodyShiftY],[s*94,244+bodyShiftY],[s*70,242+bodyShiftY]
    ],[s*64,180+bodyShiftY,s*94,244+bodyShiftY],{mode:'armor',lw:1.3});
    drawRedSlit([[s*76,196+bodyShiftY],[s*80,196+bodyShiftY],[s*82,226+bodyShiftY],[s*78,226+bodyShiftY]],0.7);
    // Hand & fingers
    drawPlate([
      [s*70,242+bodyShiftY],[s*92,244+bodyShiftY],[s*96,268+bodyShiftY],[s*72,266+bodyShiftY]
    ],[s*70,242+bodyShiftY,s*96,268+bodyShiftY],{mode:'dark',lw:1.1});
    for(let f=0;f<3;f++){
      const fx=s*(74+f*6);
      drawPlate([[fx,266+bodyShiftY],[fx+s*4,266+bodyShiftY],[fx+s*2,288+bodyShiftY],[fx-s*2,286+bodyShiftY]],[fx-4,266,fx+6,288],{mode:'armor',lw:1});
    }
  }

  // 6. Pelvis & Sleek Muscular Legs + Armored Feet
  drawPlate([
    [-34,226+bodyShiftY],[34,226+bodyShiftY],[42,258+bodyShiftY],
    [22,276+bodyShiftY],[-22,276+bodyShiftY],[-42,258+bodyShiftY]
  ],[-42,226,42,276],{mode:'armor',lw:1.3});

  for(const s of [-1,1]){
    // Thigh
    drawPlate([
      [s*12,262+bodyShiftY],[s*44,258+bodyShiftY],[s*48,334+bodyShiftY],[s*18,336+bodyShiftY]
    ],[s*12,258+bodyShiftY,s*48,336+bodyShiftY],{mode:'armor',lw:1.3});
    // Knee armor
    drawPlate([
      [s*18,332+bodyShiftY],[s*46,330+bodyShiftY],[s*44,358+bodyShiftY],[s*20,360+bodyShiftY]
    ],[s*18,330+bodyShiftY,s*46,360+bodyShiftY],{mode:'joint',lw:1.2});
    // Calf / shin greave
    drawPlate([
      [s*20,358+bodyShiftY],[s*44,356+bodyShiftY],[s*48,422+bodyShiftY],[s*18,424+bodyShiftY]
    ],[s*18,356+bodyShiftY,s*48,424+bodyShiftY],{mode:'armor',lw:1.3});
    // Foot
    drawPlate([
      [s*12,422+bodyShiftY],[s*50,420+bodyShiftY],[s*58,444+bodyShiftY],[s*8,444+bodyShiftY]
    ],[s*8,420+bodyShiftY,s*58,444+bodyShiftY],{mode:'armor',lw:1.3});
  }

  // 7. Sculpted Ultron Head (centered around y = -28, turns smoothly with lookX/lookY)
  ctx.save();
  const hx=bodyShiftX + lookX*10;
  const hy=-28 + bodyShiftY + lookY*6;
  ctx.translate(hx,hy);
  ctx.rotate(lookX*0.14);

  // Curved skull cranium
  drawPlate([
    [-26,-24],[-18,-44],[0,-49],[18,-44],[26,-24],
    [30,-2],[22,22],[0,32],[-22,22],[-30,-2]
  ],[-30,-49,30,32],{mode:'armor',lw:1.4});

  // Ear pods
  for(const s of [-1,1]){
    drawPlate([[s*25,-12],[s*33,-8],[s*34,8],[s*25,12]],[s*25,-12,s*34,12],{mode:'joint',lw:1.1});
    drawRedSlit([[s*28,-5],[s*31,-3],[s*31,3],[s*28,5]],0.85);
  }

  // Forehead V-crest & glowing red brow lines (iconic Age of Ultron head glow)
  drawPlate([[-6,-47],[0,-50],[6,-47],[8,-18],[0,-8],[-8,-18]],[-8,-50,8,-8],{mode:'armor',lw:1.1});
  drawRedSlit([[-20,-24],[-7,-16],[-9,-13],[-22,-21]],0.9);
  drawRedSlit([[20,-24],[7,-16],[9,-13],[22,-21]],0.9);

  // Dark eye socket + fierce glowing red eyes
  drawPlate([[-23,-14],[-7,-13],[0,-8],[7,-13],[23,-14],[20,2],[-20,2]],[-23,-14,23,2],{mode:'dark',lw:1});
  const eyePulse=0.88+0.12*Math.sin(t*3.2);
  drawRedSlit([[-19,-8],[-7,-10],[-6,-5],[-17,-3]],eyePulse);
  drawRedSlit([[19,-8],[7,-10],[6,-5],[17,-3]],eyePulse);

  // Cheekbones & nose bridge
  drawPlate([[-4,-11],[4,-11],[6,5],[0,9],[-6,5]],[-6,-11,6,9],{mode:'armor',lw:1.1});
  for(const s of [-1,1]){
    drawPlate([[s*24,-10],[s*27,6],[s*18,22],[s*10,26],[s*9,8]],[s*9,-10,s*27,26],{mode:'armor',lw:1.1});
  }

  // Lower jaw & glowing mouth grille (animates when speaking)
  const jawY=talk*4.5;
  ctx.save();
  ctx.translate(0,jawY);
  drawPlate([[-14,7],[14,7],[16,22],[0,32],[-16,22]],[-16,7,16,32],{mode:'armor',lw:1.2});
  drawPlate([[-10,9],[10,9],[10,20],[0,26],[-10,20]],[-10,9,10,26],{mode:'dark',lw:0.9});
  drawRedSlit([[-8,12],[8,12],[7,20],[-7,20]],0.35+talk*0.65+0.1*Math.sin(t*4));
  for(const gx of [-5,-2.5,0,2.5,5]){
    ctx.strokeStyle='#b8c2ce';ctx.lineWidth=1;
    ctx.beginPath();ctx.moveTo(gx,10);ctx.lineTo(gx,23);ctx.stroke();
  }
  ctx.restore();

  ctx.restore();
}

function loop(now){
  const t=now*0.001;
  state.zoom+=(state.targetZoom-state.zoom)*0.14;
  state.sitBlend+=((state.sitMode?1:0)-state.sitBlend)*0.12;
  state.lookX+=(state.px-state.lookX)*0.1;
  state.lookY+=(state.py-state.lookY)*0.1;
  const targetTalk=state.speaking?(0.4+0.6*Math.abs(Math.sin(t*14))):0;
  state.talkAmp+=(targetTalk-state.talkAmp)*0.25;

  const w=canvas.clientWidth;
  const h=canvas.clientHeight;
  ctx.clearRect(0,0,w,h);

  // Red aura behind Ultron
  const aura=ctx.createRadialGradient(w*0.5,h*0.45,10,w*0.5,h*0.48,Math.min(w,h)*0.44);
  aura.addColorStop(0,'rgba(255,24,44,0.28)');
  aura.addColorStop(0.55,'rgba(155,10,24,0.12)');
  aura.addColorStop(1,'rgba(0,0,0,0)');
  ctx.fillStyle=aura;
  ctx.fillRect(0,0,w,h);

  // Full-body Stand vs Face/Upper-Chest Close-up Sit Mode
  const standScale=(h/535)*state.zoom;
  const bustScale=(Math.min(w/140,h/185))*state.zoom;
  const scale=standScale+(bustScale-standScale)*state.sitBlend;

  // In stand mode, top of head (y=-68 in local coords) sits cleanly below topbar with full legs visible
  const standCenterY=h*0.165*state.zoom;
  const bustCenterY=h*0.52;
  const cx=w*0.5;
  const cy=standCenterY+(bustCenterY-standCenterY)*state.sitBlend;

  ctx.save();
  ctx.translate(cx,cy);
  ctx.scale(scale,scale);
  drawUltron(t,state.talkAmp,Math.sin(t*2.1),state.lookX,state.lookY);
  ctx.restore();

  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);

function say(text,lang='en-IN'){
  reply.textContent=text;
  if(!('speechSynthesis' in window)){voiceStatus.textContent='VOICE UNAVAILABLE';return}
  speechSynthesis.cancel();
  const u=new SpeechSynthesisUtterance(text);u.lang=lang;u.rate=.9;u.pitch=.65;u.volume=1;
  const voices=speechSynthesis.getVoices();
  const match=voices.find(v=>lang.startsWith('hi')?v.lang.toLowerCase().includes('hi'):v.lang.toLowerCase().includes('en'));
  if(match)u.voice=match;
  u.onstart=()=>{voiceStatus.textContent='SPEAKING';state.speaking=true;};
  u.onend=()=>{voiceStatus.textContent='STANDBY';state.speaking=false;};
  u.onerror=()=>{voiceStatus.textContent='STANDBY';state.speaking=false;};
  speechSynthesis.speak(u);
}

function sit(){
  state.sitMode=true;
  sitBtn.classList.add('active');
  standBtn.classList.remove('active');
  say('Sitting mode engaged. I am watching, Shivam Sir.');
}
function stand(){
  state.sitMode=false;
  standBtn.classList.add('active');
  sitBtn.classList.remove('active');
  say('Standing by, Shivam Sir.');
}

sitBtn.onclick=sit;
standBtn.onclick=stand;

document.getElementById('zoom').oninput=e=>{
  const z=Number(e.target.value);
  state.targetZoom=z;
  document.getElementById('zoomVal').textContent=Math.round(z*100)+'%';
};

document.getElementById('resetBtn').onclick=()=>{
  document.getElementById('zoom').value=1;
  state.targetZoom=1;
  document.getElementById('zoomVal').textContent='100%';
  stand();
};

function processCommand(text){
  const t=text.toLowerCase().trim();
  if(/\b(hello|hi|hey)\b/.test(t)||t.includes('नमस्ते')||t.includes('हेलो')){say('Hello Shivam Sir. I am Ultron.');return}
  if(t.includes('sit')||t.includes('बैठ')){sit();return}
  if(t.includes('stand')||t.includes('खड़े')||t.includes('खड़ा')){stand();return}
  if(t.includes('zoom in')){const el=document.getElementById('zoom');el.value=Math.min(1.65,Number(el.value)+.15);el.dispatchEvent(new Event('input'));say('Zooming in.');return}
  if(t.includes('zoom out')){const el=document.getElementById('zoom');el.value=Math.max(.65,Number(el.value)-.15);el.dispatchEvent(new Event('input'));say('Zooming out.');return}
  say('Command received, Shivam Sir. My full command system will be added in the next phase.');
}

let recognition;
const SpeechRecognition=window.SpeechRecognition||window.webkitSpeechRecognition;
if(SpeechRecognition){
  recognition=new SpeechRecognition();recognition.continuous=false;recognition.interimResults=false;recognition.lang='en-IN';
  recognition.onstart=()=>{micStatus.textContent='LISTENING';voiceStatus.textContent='VOICE LINK ACTIVE'};
  recognition.onend=()=>{micStatus.textContent='READY';};
  recognition.onerror=()=>{micStatus.textContent='MIC ERROR';reply.textContent='Microphone unavailable. Check browser permission.'};
  recognition.onresult=e=>{const spoken=e.results[0][0].transcript;reply.textContent='You: '+spoken;processCommand(spoken)};
}else{micStatus.textContent='USE CHROME';}

document.getElementById('micBtn').onclick=()=>{
  if(!recognition){reply.textContent='Voice recognition is not supported in this browser. Try Chrome.';return}
  try{recognition.lang='en-IN';recognition.start()}catch(e){micStatus.textContent='WAIT';}
};

window.addEventListener('keydown',e=>{if(e.key==='Escape')document.getElementById('resetBtn').click()});
</script>
</body></html>
"""

@app.get("/")
def home():
    return render_template_string(PAGE)

@app.get("/health")
def health():
    return jsonify(status="online", app="ULTRON AI", phase=1)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
