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
.stage{position:absolute;inset:75px 0 100px;display:flex;align-items:center;justify-content:center;perspective:1000px}
.floor{position:absolute;bottom:0;width:min(900px,95vw);height:150px;background:radial-gradient(ellipse,rgba(255,52,20,.34),transparent 67%);border-radius:50%;transform:rotateX(65deg)}
#ultronCanvas{width:100%;height:100%;display:block;z-index:2}
.caption{position:absolute;bottom:12px;text-align:center;letter-spacing:.28em;font-size:11px;color:#c6c8ce;text-shadow:0 0 12px #f22;z-index:3}
.controls{position:absolute;left:50%;bottom:22px;transform:translateX(-50%);width:min(720px,94vw);display:flex;align-items:center;justify-content:center;gap:10px;flex-wrap:wrap;z-index:5}
button{border:1px solid #76303a;background:rgba(15,10,15,.88);color:#f5f5f7;padding:12px 17px;letter-spacing:.12em;font-size:10px;font-weight:700;cursor:pointer;transition:.2s}
button:hover,button:focus{border-color:#ff3448;box-shadow:0 0 18px #ff263844;outline:none}
button.primary{background:linear-gradient(135deg,#a50c20,#4d0913);border-color:#ff3348}
button.active{background:#64101c;border-color:#ff3348}
.zoom{display:flex;align-items:center;gap:9px;border:1px solid #59212a;background:#100b10;padding:8px 12px;color:#bbb;font-size:10px}
input[type=range]{width:95px;accent-color:#ff2638}
.console{position:absolute;left:24px;bottom:115px;width:230px;color:#d6a4a8;font:10px/1.8 monospace;letter-spacing:.05em;opacity:.85;z-index:3}
.console strong{color:#ff5261}
.mic-state{position:absolute;right:24px;bottom:115px;text-align:right;font:10px/1.8 monospace;color:#c7c7cc;z-index:3}
.mic-state strong{color:#ff5261}
.chat{position:absolute;top:82px;right:22px;width:min(280px,42vw);padding:13px;background:rgba(5,7,11,.62);border:1px solid #57232c;backdrop-filter:blur(8px);font-size:12px;z-index:4}
.chat small{display:block;color:#ff6876;letter-spacing:.18em;margin-bottom:7px}
#reply{color:#eee;min-height:30px;line-height:1.5}
@media(max-width:650px){.topbar{padding:16px}.stage{inset:70px 0 145px}.chat{top:68px;right:10px;width:155px;font-size:10px}.console{left:12px;bottom:142px;width:150px;font-size:8px}.mic-state{right:12px;bottom:142px;font-size:8px}.controls{bottom:13px;gap:6px}button{padding:11px 12px;font-size:9px}.zoom{padding:7px}.caption{bottom:5px}}
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
  px:0,
  py:0,
  yaw:0,
  pitch:0
};

function resize(){
  const dpr=Math.min(window.devicePixelRatio||1,2);
  const r=canvas.getBoundingClientRect();
  canvas.width=Math.max(1,Math.floor(r.width*dpr));
  canvas.height=Math.max(1,Math.floor(r.height*dpr));
  ctx.setTransform(dpr,0,0,dpr,0,0);
}
window.addEventListener('resize',resize);
resize();

window.addEventListener('pointermove',e=>{
  state.px=Math.max(-1,Math.min(1,(e.clientX/window.innerWidth)*2-1));
  state.py=Math.max(-1,Math.min(1,(e.clientY/window.innerHeight)*2-1));
});

// 3D projection helper with true foreshortening
function proj(x,y,z,yaw,pitch,fov=620){
  const cy=Math.cos(yaw), sy=Math.sin(yaw);
  const x1=x*cy - z*sy;
  const z1=x*sy + z*cy;
  const cp=Math.cos(pitch), sp=Math.sin(pitch);
  const y2=y*cp - z1*sp;
  const z2=y*sp + z1*cp;
  const s=fov/(fov+z2);
  return {x:x1*s, y:y2*s, z:z2, s};
}

// Curved 3D metallic limb / cylinder renderer
function drawLimb(p1,p2,r1,r2,yaw,pitch,dark=false){
  const a=proj(p1[0],p1[1],p1[2],yaw,pitch);
  const b=proj(p2[0],p2[1],p2[2],yaw,pitch);
  const ra=r1*a.s, rb=r2*b.s;
  const dx=b.x-a.x, dy=b.y-a.y;
  const len=Math.hypot(dx,dy)||1;
  const nx=-dy/len, ny=dx/len;

  const g=ctx.createLinearGradient(a.x-nx*ra,a.y-ny*ra,a.x+nx*ra,a.y+ny*ra);
  if(dark){
    g.addColorStop(0,'#090c12');
    g.addColorStop(0.28,'#2b3340');
    g.addColorStop(0.55,'#11161f');
    g.addColorStop(0.85,'#3c4656');
    g.addColorStop(1,'#07090d');
  }else{
    g.addColorStop(0,'#1c222c');
    g.addColorStop(0.18,'#9ea9b8');
    g.addColorStop(0.34,'#f4f8fc');
    g.addColorStop(0.52,'#495363');
    g.addColorStop(0.76,'#19202a');
    g.addColorStop(0.92,'#a8b4c4');
    g.addColorStop(1,'#141922');
  }

  ctx.beginPath();
  ctx.moveTo(a.x+nx*ra,a.y+ny*ra);
  ctx.quadraticCurveTo((a.x+b.x)*0.5+nx*(ra+rb)*0.54,(a.y+b.y)*0.5+ny*(ra+rb)*0.54,b.x+nx*rb,b.y+ny*rb);
  ctx.lineTo(b.x-nx*rb,b.y-ny*rb);
  ctx.quadraticCurveTo((a.x+b.x)*0.5-nx*(ra+rb)*0.54,(a.y+b.y)*0.5-ny*(ra+rb)*0.54,a.x-nx*ra,a.y-ny*ra);
  ctx.closePath();
  ctx.fillStyle=g;
  ctx.fill();
  ctx.strokeStyle=dark?'rgba(120,135,155,0.28)':'rgba(230,242,255,0.45)';
  ctx.lineWidth=1.1;
  ctx.stroke();

  // Joint end-cap sphere shading
  const cap=ctx.createRadialGradient(a.x-ra*0.25,a.y-ra*0.25,1,a.x,a.y,ra);
  cap.addColorStop(0,dark?'#4b5668':'#eef5fc');
  cap.addColorStop(0.55,dark?'#181e28':'#566273');
  cap.addColorStop(1,'#090c12');
  ctx.beginPath();ctx.arc(a.x,a.y,ra*0.95,0,Math.PI*2);ctx.fillStyle=cap;ctx.fill();
}

// Sculpted 3D curved surface patch
function drawCurvedPatch(pts3d,yaw,pitch,opts={}){
  const pts=pts3d.map(p=>proj(p[0],p[1],p[2],yaw,pitch));
  let minX=1e9,maxX=-1e9,minY=1e9,maxY=-1e9,avgZ=0;
  for(const p of pts){
    if(p.x<minX)minX=p.x; if(p.x>maxX)maxX=p.x;
    if(p.y<minY)minY=p.y; if(p.y>maxY)maxY=p.y;
    avgZ+=p.z;
  }
  avgZ/=pts.length;

  ctx.beginPath();
  ctx.moveTo(pts[0].x,pts[0].y);
  for(let i=0;i<pts.length;i++){
    const p1=pts[i], p2=pts[(i+1)%pts.length];
    const mx=(p1.x+p2.x)*0.5, my=(p1.y+p2.y)*0.5;
    if(opts.sharp){
      ctx.lineTo(p2.x,p2.y);
    }else{
      ctx.quadraticCurveTo(p1.x,p1.y,mx,my);
    }
  }
  ctx.closePath();

  const g=ctx.createLinearGradient(minX,minY,maxX,maxY);
  if(opts.dark){
    g.addColorStop(0,'#272f3b');
    g.addColorStop(0.35,'#10151d');
    g.addColorStop(0.75,'#070a0f');
    g.addColorStop(1,'#1e2530');
  }else{
    g.addColorStop(0,'#f6faff');
    g.addColorStop(0.18,'#9ea9b8');
    g.addColorStop(0.42,'#3c4654');
    g.addColorStop(0.65,'#19202a');
    g.addColorStop(0.86,'#bcc7d6');
    g.addColorStop(1,'#29313d');
  }
  ctx.fillStyle=g;
  ctx.fill();

  if(opts.rim!==false){
    ctx.strokeStyle=opts.rimColor||(opts.dark?'rgba(110,125,145,0.35)':'rgba(240,248,255,0.6)');
    ctx.lineWidth=opts.lw||1.2;
    ctx.stroke();
  }
  return avgZ;
}

function drawGlow3D(pts3d,yaw,pitch,intensity=1){
  const pts=pts3d.map(p=>proj(p[0],p[1],p[2],yaw,pitch));
  ctx.save();
  ctx.shadowColor=`rgba(255,22,42,${0.95*intensity})`;
  ctx.shadowBlur=22*intensity;
  ctx.beginPath();
  ctx.moveTo(pts[0].x,pts[0].y);
  for(let i=1;i<pts.length;i++) ctx.lineTo(pts[i].x,pts[i].y);
  ctx.closePath();
  ctx.fillStyle='#ff1930';
  ctx.fill();
  ctx.shadowBlur=7;
  ctx.fillStyle='#ffe6ea';
  ctx.fill();
  ctx.restore();
}

function renderHead(t,talk,yaw,pitch){
  ctx.save();
  const hy=yaw*1.45;
  const hp=pitch*1.15;

  // 1. Rear spherical titanium cranium dome (eliminates flat hexagon look)
  const c0=proj(0,-42,-8,hy,hp);
  const rx=66*c0.s, ry=84*c0.s;
  const dome=ctx.createRadialGradient(c0.x-rx*0.32,c0.y-ry*0.35,rx*0.08,c0.x,c0.y,ry*1.15);
  dome.addColorStop(0,'#f7fbff');
  dome.addColorStop(0.22,'#9aa6b5');
  dome.addColorStop(0.52,'#343e4c');
  dome.addColorStop(0.8,'#131820');
  dome.addColorStop(1,'#4c5768');
  ctx.beginPath();
  ctx.ellipse(c0.x,c0.y,rx,ry,0,0,Math.PI*2);
  ctx.fillStyle=dome;
  ctx.fill();
  ctx.strokeStyle='rgba(220,235,250,0.45)';
  ctx.lineWidth=1.4;
  ctx.stroke();

  // 2. Ear / Temple Rotary Actuators
  for(const s of [-1,1]){
    const ear=proj(s*64,-24,2,hy,hp);
    const er=17*ear.s;
    const eg=ctx.createRadialGradient(ear.x-s*4,ear.y-4,2,ear.x,ear.y,er);
    eg.addColorStop(0,'#cfd9e6');eg.addColorStop(0.5,'#2f3846');eg.addColorStop(1,'#0b0e14');
    ctx.beginPath();ctx.ellipse(ear.x,ear.y,er*0.65,er,0,0,Math.PI*2);ctx.fillStyle=eg;ctx.fill();
    drawGlow3D([[s*66,-30,8],[s*69,-28,12],[s*69,-16,12],[s*66,-14,8]],hy,hp,0.85);
  }

  // 3. Sculpted Forehead Helmet & Menacing V-Brow Ridge
  drawCurvedPatch([
    [-56,-56,16],[-34,-108,8],[0,-118,18],[34,-108,8],[56,-56,16],
    [60,-28,34],[36,-22,48],[0,-14,54],[-36,-22,48],[-60,-28,34]
  ],hy,hp,{lw:1.5});

  // Central Cranial Ridge (iconic Ultron crest)
  drawCurvedPatch([
    [-11,-116,14],[0,-120,24],[11,-116,14],
    [14,-56,42],[0,-15,56],[-14,-56,42]
  ],hy,hp,{lw:1.3});

  // Deep Ocular Recess (shadowed socket under brow)
  drawCurvedPatch([
    [-54,-24,30],[-18,-22,46],[0,-13,52],[18,-22,46],[54,-24,30],
    [48,6,34],[18,12,44],[-18,12,44],[-48,6,34]
  ],hy,hp,{dark:true,sharp:true,rimColor:'rgba(255,35,55,0.4)'});

  // 4. Fierce Glowing Red Eyes (angled predator slits)
  const eyePulse=0.88+0.12*Math.sin(t*3.5);
  for(const s of [-1,1]){
    drawGlow3D([
      [s*15,-12,48],[s*48,-20,35],[s*51,-12,33],[s*36,-3,41],[s*17,-4,48]
    ],hy,hp,eyePulse);
  }

  // 5. High Angular Cheekbones & Swept Side-Plates
  for(const s of [-1,1]){
    drawCurvedPatch([
      [s*61,-24,26],[s*66,14,14],[s*48,54,22],[s*26,68,36],[s*24,24,44],[s*46,2,38]
    ],hy,hp,{lw:1.4});
    // Dark recessed cheek vent
    drawCurvedPatch([
      [s*44,14,32],[s*58,10,22],[s*52,36,24],[s*38,38,34]
    ],hy,hp,{dark:true,sharp:true});
  }

  // 6. Sharp Titanium Nasal Bridge
  drawCurvedPatch([
    [-9,-15,53],[9,-15,53],[13,18,52],[0,25,56],[-13,18,52]
  ],hy,hp,{sharp:true,lw:1.4});

  // 7. Articulated Lower Jaw & Glowing Furnace Mouth Grille
  const jawDrop=talk*9;
  drawCurvedPatch([
    [-32,22+jawDrop,38],[32,22+jawDrop,38],
    [36,56+jawDrop,32],[20,84+jawDrop,36],[0,90+jawDrop,40],[-20,84+jawDrop,36],[-36,56+jawDrop,32]
  ],hy,hp,{lw:1.5});

  // Dark mouth cavity + internal red furnace glow
  drawCurvedPatch([
    [-24,26+jawDrop,42],[24,26+jawDrop,42],
    [25,54+jawDrop,38],[14,68+jawDrop,40],[-14,68+jawDrop,40],[-25,54+jawDrop,38]
  ],hy,hp,{dark:true,sharp:true});

  const mouthHeat=0.32+talk*0.68+0.1*Math.sin(t*4.5);
  drawGlow3D([
    [-20,31+jawDrop,43],[20,31+jawDrop,43],[18,58+jawDrop,41],[-18,58+jawDrop,41]
  ],hy,hp,mouthHeat);

  // Titanium mouth grille bars
  for(const gx of [-14,-7,0,7,14]){
    drawCurvedPatch([
      [gx-2,27+jawDrop,45],[gx+2,27+jawDrop,45],
      [gx+1.8,63+jawDrop,43],[gx-1.8,63+jawDrop,43]
    ],hy,hp,{sharp:true,lw:0.8});
  }

  // Chin armor guard
  drawCurvedPatch([
    [-20,64+jawDrop,41],[20,64+jawDrop,41],[14,84+jawDrop,39],[0,89+jawDrop,42],[-14,84+jawDrop,39]
  ],hy,hp,{lw:1.3});

  ctx.restore();
}

function renderBody(t,talk,breath,yaw,pitch){
  const ty=yaw*0.45;
  const tp=pitch*0.35;

  // Hydraulic Neck Spine & Pistons
  drawLimb([0,56,-6],[0,136,-4],32,42,ty,tp,true);
  for(const s of [-1,1]){
    drawLimb([s*20,64,6],[s*30,134,12],9,12,ty,tp,false);
    drawLimb([s*28,74,-12],[s*38,136,-8],7,9,ty,tp,true);
  }

  // Upper Torso & Tapered V-Shape Chassis
  drawLimb([0,138,0],[0,256,6],94,76,ty,tp,true);
  drawLimb([0,254,6],[0,368,2],74,52,ty,tp,true);

  // Armored Collar Ring
  drawCurvedPatch([
    [-58,118,12],[-24,132,34],[0,138,40],[24,132,34],[58,118,12],
    [66,142,18],[0,158,46],[-66,142,18]
  ],ty,tp,{lw:1.5});

  // Massive Layered Shoulder Pauldrons (3D curved domes)
  for(const s of [-1,1]){
    drawLimb([s*96,154+breath*2,-4],[s*132,208+breath*2,4],48,38,ty,tp,false);
    drawCurvedPatch([
      [s*74,128+breath*2,14],[s*126,134+breath*2,6],[s*162,178+breath*2,12],
      [s*154,224+breath*2,24],[s*102,216+breath*2,34],[s*76,174+breath*2,32]
    ],ty,tp,{lw:1.6});
    drawGlow3D([
      [s*118,168+breath*2,28],[s*142,164+breath*2,20],[s*145,176+breath*2,20],[s*121,180+breath*2,28]
    ],ty,tp,0.8);
  }

  // Broad Sculpted Pectoral Armor Plates
  for(const s of [-1,1]){
    drawCurvedPatch([
      [s*12,142,42],[s*88,138,24],[s*104,204,32],[s*74,234,44],[s*15,222,50]
    ],ty,tp,{lw:1.6});
  }

  // Central Sternum & Glowing Arc-Core Slit
  drawCurvedPatch([
    [-20,144,48],[20,144,48],[26,246,48],[0,268,52],[-26,246,48]
  ],ty,tp,{dark:true,sharp:true});

  const corePulse=0.82+0.18*Math.sin(t*2.8)+talk*0.25;
  drawGlow3D([
    [-8,172,51],[8,172,51],[12,234,51],[0,248,54],[-12,234,51]
  ],ty,tp,corePulse);

  // Segmented Rib / Abdominal Muscle Armor
  for(let r=0;r<4;r++){
    const y=244+r*28;
    const w=72-r*6;
    const z=46-r*2;
    for(const s of [-1,1]){
      drawCurvedPatch([
        [s*10,y+3,z+4],[s*w,y-4,z-12],[s*(w-5),y+18,z-12],[s*12,y+23,z+4]
      ],ty,tp,{lw:1.3});
    }
  }

  // 3D Cylindrical Arms, Elbow Joints, Forearm Gauntlets & Claws
  for(const s of [-1,1]){
    const sh=[s*132,206+breath*2,4];
    const el=[s*152,306+breath*2,14];
    const wr=[s*162,418+breath*2,32];
    drawLimb(sh,el,26,21,ty,tp,true);
    drawLimb([s*134,218+breath*2,12],[s*148,292+breath*2,20],22,18,ty,tp,false);
    drawLimb(el,wr,23,17,ty,tp,false);
    drawGlow3D([
      [s*156,332+breath*2,34],[s*161,332+breath*2,32],[s*165,382+breath*2,39],[s*160,382+breath*2,41]
    ],ty,tp,0.75);
    // Mechanical Hand & Claws
    drawLimb(wr,[s*164,446+breath*2,38],16,13,ty,tp,true);
    for(let f=-1;f<=1;f++){
      drawLimb([s*(162+f*6),446+breath*2,38+f*4],[s*(160+f*7),476+breath*2,42+f*4],4.5,2.5,ty,tp,false);
    }
  }

  // Pelvis & Heavy Armored Legs
  drawLimb([0,366,2],[0,428,6],54,48,ty,tp,false);
  drawCurvedPatch([[-20,372,42],[20,372,42],[24,438,44],[0,452,48],[-24,438,44]],ty,tp,{dark:true,sharp:true});

  for(const s of [-1,1]){
    const hip=[s*46,418,4];
    const knee=[s*54,536,16];
    const ankle=[s*58,664,6];
    drawLimb(hip,knee,30,23,ty,tp,false);
    drawLimb(knee,ankle,25,18,ty,tp,false);
    drawGlow3D([[s*52,562,38],[s*57,562,38],[s*59,624,32],[s*54,624,32]],ty,tp,0.7);
    // Armored Foot
    drawCurvedPatch([
      [s*34,658,10],[s*82,658,10],[s*94,692,42],[s*26,692,42]
    ],ty,tp,{lw:1.5});
  }
}

function render(now){
  const t=now*0.001;
  state.zoom+=(state.targetZoom-state.zoom)*0.12;
  state.sitBlend+=((state.sitMode?1:0)-state.sitBlend)*0.1;
  state.yaw+=(state.px*0.36-state.yaw)*0.08;
  state.pitch+=(state.py*0.24-state.pitch)*0.08;

  const w=canvas.clientWidth;
  const h=canvas.clientHeight;
  ctx.clearRect(0,0,w,h);

  const talk=state.speaking?(0.35+0.65*Math.abs(Math.sin(t*14))):0;
  const breath=Math.sin(t*2.1);

  // Backlit crimson rim aura
  const aura=ctx.createRadialGradient(w*0.5,h*0.44,12,w*0.5,h*0.46,Math.min(w,h)*0.45);
  aura.addColorStop(0,'rgba(255,24,44,0.32)');
  aura.addColorStop(0.55,'rgba(160,10,24,0.14)');
  aura.addColorStop(1,'rgba(0,0,0,0)');
  ctx.fillStyle=aura;
  ctx.fillRect(0,0,w,h);

  ctx.save();
  const standScale=Math.min(w/420,h/840)*state.zoom;
  const bustScale=Math.min(w/260,h/400)*state.zoom;
  const scale=standScale+(bustScale-standScale)*state.sitBlend;

  const standY=h*0.20+breath*4;
  const bustY=h*0.45+breath*3;
  const cy=standY+(bustY-standY)*state.sitBlend;

  ctx.translate(w*0.5,cy);
  ctx.scale(scale,scale);

  renderBody(t,talk,breath,state.yaw,state.pitch);
  renderHead(t,talk,state.yaw,state.pitch);

  ctx.restore();
  requestAnimationFrame(render);
}
requestAnimationFrame(render);

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
