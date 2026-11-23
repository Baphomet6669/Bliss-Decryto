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
#ultronCanvas{width:100%;height:100%;display:block;z-index:2;filter:drop-shadow(0 16px 35px rgba(0,0,0,.85))}
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

let state={
  zoom:1,
  targetZoom:1,
  sitMode:false,
  sitBlend:0,
  speaking:false,
  pointerX:0,
  pointerY:0,
  smoothX:0,
  smoothY:0
};

function resizeCanvas(){
  const dpr=Math.min(window.devicePixelRatio||1,2);
  const rect=canvas.getBoundingClientRect();
  canvas.width=Math.max(1,Math.floor(rect.width*dpr));
  canvas.height=Math.max(1,Math.floor(rect.height*dpr));
  ctx.setTransform(dpr,0,0,dpr,0,0);
}
window.addEventListener('resize',resizeCanvas);
resizeCanvas();

window.addEventListener('pointermove',e=>{
  const nx=(e.clientX/window.innerWidth)*2-1;
  const ny=(e.clientY/window.innerHeight)*2-1;
  state.pointerX=Math.max(-1,Math.min(1,nx));
  state.pointerY=Math.max(-1,Math.min(1,ny));
});

function poly(pts){
  ctx.beginPath();
  ctx.moveTo(pts[0][0],pts[0][1]);
  for(let i=1;i<pts.length;i++) ctx.lineTo(pts[i][0],pts[i][1]);
  ctx.closePath();
}

function chromeGrad(x1,y1,x2,y2,dark=false){
  const g=ctx.createLinearGradient(x1,y1,x2,y2);
  if(dark){
    g.addColorStop(0,'#2e3540');
    g.addColorStop(.25,'#141922');
    g.addColorStop(.55,'#090c12');
    g.addColorStop(.85,'#232a35');
    g.addColorStop(1,'#0b0e14');
  }else{
    g.addColorStop(0,'#f4f7fb');
    g.addColorStop(.16,'#9ba6b4');
    g.addColorStop(.38,'#3a4350');
    g.addColorStop(.56,'#171d26');
    g.addColorStop(.78,'#c8d1dc');
    g.addColorStop(.92,'#535e6d');
    g.addColorStop(1,'#1e2530');
  }
  return g;
}

function drawArmorPlate(pts,x1,y1,x2,y2,opts={}){
  poly(pts);
  ctx.fillStyle=chromeGrad(x1,y1,x2,y2,opts.dark);
  ctx.fill();
  if(opts.rim!==false){
    ctx.strokeStyle=opts.rimColor||(opts.dark?'rgba(110,124,142,0.45)':'rgba(235,244,255,0.65)');
    ctx.lineWidth=opts.lw||1.3;
    ctx.stroke();
  }
  if(opts.innerShadow){
    ctx.save();
    ctx.clip();
    const sg=ctx.createRadialGradient(0,0,10,0,0,260);
    sg.addColorStop(0,'rgba(255,40,55,0.08)');
    sg.addColorStop(1,'rgba(0,0,0,0.55)');
    ctx.fillStyle=sg;
    ctx.fill();
    ctx.restore();
  }
}

function drawGlowSlit(pts,intensity=1){
  ctx.save();
  ctx.shadowColor=`rgba(255,28,46,${0.95*intensity})`;
  ctx.shadowBlur=18*intensity;
  poly(pts);
  ctx.fillStyle='#ff1c32';
  ctx.fill();
  ctx.shadowBlur=6;
  ctx.fillStyle='#ffd2d8';
  ctx.fill();
  ctx.restore();
}

function drawUltronHead(t,talk,lookX,lookY){
  ctx.save();
  ctx.translate(lookX*7,lookY*5);

  // Rear cranium & temple hydraulics
  drawArmorPlate([[-66,-68],[-44,-118],[0,-130],[44,-118],[66,-68],[74,-12],[60,44],[36,80],[-36,80],[-60,44],[-74,-12]],-75,-130,75,85,{dark:true});

  // Ear audio-actuator pods
  for(const s of [-1,1]){
    drawArmorPlate([[s*64,-34],[s*80,-24],[s*82,16],[s*63,28]],s*62,-34,s*82,28,{});
    drawArmorPlate([[s*68,-20],[s*76,-14],[s*77,8],[s*68,14]],s*68,-20,s*77,14,{dark:true});
    drawGlowSlit([[s*71,-11],[s*75,-8],[s*75,3],[s*71,5]],0.85);
  }

  // Sculpted Titanium Brow & Crown Helmet
  drawArmorPlate([
    [-58,-64],[-40,-112],[0,-125],[40,-112],[58,-64],
    [66,-28],[46,-16],[22,-27],[0,-18],[-22,-27],[-46,-16],[-66,-28]
  ],-65,-125,65,-15,{lw:1.6});

  // Center forehead crest & specular ridge
  drawArmorPlate([[-14,-122],[0,-127],[14,-122],[18,-62],[0,-22],[-18,-62]],-18,-127,18,-22,{lw:1.4});
  ctx.strokeStyle='rgba(255,255,255,0.75)';
  ctx.lineWidth=1.5;
  ctx.beginPath();ctx.moveTo(0,-123);ctx.lineTo(0,-25);ctx.stroke();

  // Brow overhanging shadow plates
  for(const s of [-1,1]){
    drawArmorPlate([[s*16,-32],[s*54,-46],[s*66,-26],[s*48,-12],[s*18,-22]],s*15,-46,s*66,-12,{dark:true});
  }

  // Deep dark ocular cavity
  drawArmorPlate([
    [-54,-22],[-20,-24],[0,-15],[20,-24],[54,-22],
    [48,10],[22,16],[-22,16],[-48,10]
  ],-54,-24,54,16,{dark:true,rimColor:'rgba(255,45,60,0.35)'});

  // Menacing Angled Ultron Eyes
  const pulse=0.85+0.15*Math.sin(t*3.2);
  for(const s of [-1,1]){
    drawGlowSlit([
      [s*15,-14],[s*50,-20],[s*53,-12],[s*38,-2],[s*17,-4]
    ],pulse);
    // Inner hot pupil flare
    ctx.save();
    ctx.fillStyle='#ffffff';
    ctx.globalAlpha=0.8;
    poly([[s*22,-12],[s*35,-14],[s*31,-8],[s*21,-8]]);
    ctx.fill();
    ctx.restore();
  }

  // Sharp angular cheekbones
  for(const s of [-1,1]){
    drawArmorPlate([
      [s*66,-24],[s*73,12],[s*56,52],[s*34,74],[s*28,36],[s*46,6]
    ],s*28,-24,s*73,74,{lw:1.5});
    // Cheek vent cut
    drawArmorPlate([
      [s*48,14],[s*63,10],[s*58,34],[s*44,36]
    ],s*44,10,s*63,36,{dark:true});
  }

  // Nasal bridge plate
  drawArmorPlate([[-11,-18],[11,-18],[15,18],[0,26],[-15,18]],-15,-18,15,26,{lw:1.5});

  // Animated Lower Jaw & Iconic Ultron Mouth Grille
  ctx.save();
  ctx.translate(0,talk*7);
  drawArmorPlate([
    [-36,24],[36,24],[42,58],[24,88],[0,96],[-24,88],[-42,58]
  ],-42,24,42,96,{lw:1.6});
  // Dark mouth recess with red internal furnace glow
  drawArmorPlate([
    [-26,28],[26,28],[29,56],[16,74],[-16,74],[-29,56]
  ],-29,28,29,74,{dark:true});

  // Red internal mouth glow when speaking or breathing
  const mouthGlow=0.35+talk*0.65+0.12*Math.sin(t*4);
  drawGlowSlit([[-21,34],[21,34],[19,63],[-19,63]],mouthGlow);

  // Vertical titanium teeth/grille bars over the glow
  for(const x of [-15,-7.5,0,7.5,15]){
    drawArmorPlate([[x-2.3,29],[x+2.3,29],[x+2,69],[x-2,69]],x-2.5,29,x+2.5,69,{lw:0.8});
  }
  // Chin armor cap
  drawArmorPlate([[-22,68],[22,68],[16,90],[0,95],[-16,90]],-22,68,22,95,{lw:1.4});
  ctx.restore();

  ctx.restore();
}

function drawUltronBody(t,talk,breath,lookX,lookY){
  // Mechanical Neck & Hydraulic Pistons
  drawArmorPlate([[-38,72],[38,72],[48,142],[-48,142]],-48,72,48,142,{dark:true});
  for(const s of [-1,1]){
    drawArmorPlate([[s*16,74],[s*30,74],[s*38,138],[s*20,138]],s*16,74,s*38,138,{});
    // Neck tendons
    ctx.strokeStyle='#8f9aa8';ctx.lineWidth=2.5;
    ctx.beginPath();ctx.moveTo(s*24,78);ctx.lineTo(s*30,136);ctx.stroke();
  }
  // Throat collar ring
  drawArmorPlate([[-56,124],[-24,136],[0,142],[24,136],[56,124],[66,148],[0,162],[-66,148]],-66,124,66,162,{lw:1.6});

  // Massive Layered Pauldrons (Shoulders)
  for(const s of [-1,1]){
    ctx.save();
    ctx.translate(s*112,158+breath*2);
    ctx.rotate(s*0.08);
    // Outer upper shoulder armor
    drawArmorPlate([
      [s*-42,-28],[s*34,-34],[s*76,-4],[s*84,48],[s*46,72],[s*-28,54]
    ],s*-42,-34,s*84,72,{lw:1.7});
    // Secondary overlapping shoulder plate
    drawArmorPlate([
      [s*-22,-10],[s*44,-14],[s*68,26],[s*42,64],[s*-14,48]
    ],s*-22,-14,s*68,64,{lw:1.4});
    // Shoulder red energy vent
    drawGlowSlit([[s*18,12],[s*44,8],[s*48,20],[s*22,24]],0.8);
    ctx.restore();
  }

  // Sculpted Torso Chassis
  drawArmorPlate([
    [-92,140],[92,140],[114,225],[86,348],[54,392],[-54,392],[-86,348],[-114,225]
  ],-114,140,114,392,{dark:true,innerShadow:true});

  // Broad Armored Pectoral Plates
  for(const s of [-1,1]){
    drawArmorPlate([
      [s*12,148],[s*88,144],[s*108,214],[s*78,244],[s*16,232]
    ],s*12,144,s*108,244,{lw:1.7});
    // Upper pec bevel highlight
    drawArmorPlate([
      [s*22,156],[s*82,152],[s*94,192],[s*24,198]
    ],s*22,152,s*94,198,{lw:1.2});
  }

  // Central Sternum & Glowing Arc-Core Slit
  drawArmorPlate([[-22,148],[22,148],[28,256],[0,278],[-28,256]],-28,148,28,278,{dark:true});
  const corePulse=0.8+0.2*Math.sin(t*2.6)+talk*0.25;
  drawGlowSlit([[-9,176],[9,176],[13,242],[0,256],[-13,242]],corePulse);
  // Core cage bars
  drawArmorPlate([[-16,196],[16,196],[15,203],[-15,203]],-16,196,16,203,{});
  drawArmorPlate([[-15,222],[15,222],[13,229],[-13,229]],-15,222,15,229,{});

  // Segmented Rib / Abdominal Armor Plates
  for(let r=0;r<4;r++){
    const y=254+r*30;
    const w=78-r*7;
    for(const s of [-1,1]){
      drawArmorPlate([
        [s*10,y+4],[s*w,y-4],[s*(w-5),y+20],[s*12,y+25]
      ],s*10,y-4,s*w,y+25,{lw:1.3});
    }
  }

  // Upper Arms, Elbow Servos, Forearms & Articulated Claws
  for(const s of [-1,1]){
    ctx.save();
    ctx.translate(s*132,216+breath*2);
    ctx.rotate(s*0.06);
    // Bicep dark inner frame + outer armor
    drawArmorPlate([[s*-22,0],[s*26,0],[s*32,96],[s*-20,96]],s*-22,0,s*32,96,{dark:true});
    drawArmorPlate([[s*-12,8],[s*28,4],[s*34,84],[s*-8,88]],s*-12,4,s*34,88,{lw:1.4});
    // Elbow joint ring
    drawArmorPlate([[s*-24,92],[s*30,92],[s*26,124],[s*-22,124]],s*-24,92,s*30,124,{dark:true});
    // Heavy Forearm Gauntlet
    drawArmorPlate([[s*-24,122],[s*32,120],[s*38,218],[s*16,244],[s*-20,236]],s*-24,120,s*38,244,{lw:1.6});
    drawGlowSlit([[s*16,144],[s*23,144],[s*25,194],[s*18,194]],0.75);
    // Mechanical Hand & Claws
    drawArmorPlate([[s*-16,238],[s*22,240],[s*24,268],[s*-14,266]],s*-16,238,s*24,268,{dark:true});
    for(let f=0;f<3;f++){
      const fx=-10+f*12;
      drawArmorPlate([[s*fx,266],[s*(fx+8),266],[s*(fx+5),296],[s*(fx-2),294]],s*fx,266,s*(fx+8),296,{});
    }
    ctx.restore();
  }

  // Pelvis & Hip Armor
  drawArmorPlate([[-62,382],[62,382],[76,436],[44,468],[-44,468],[-76,436]],-76,382,76,468,{lw:1.6});
  drawArmorPlate([[-22,386],[22,386],[26,456],[0,470],[-26,456]],-26,386,26,470,{dark:true});

  // Heavy Armored Thighs, Knees & Greaves
  for(const s of [-1,1]){
    // Thigh
    drawArmorPlate([[s*22,436],[s*76,428],[s*82,534],[s*26,542]],s*22,428,s*82,542,{lw:1.6});
    drawArmorPlate([[s*32,448],[s*68,444],[s*72,518],[s*36,524]],s*32,444,s*72,524,{dark:true});
    // Knee guard
    drawArmorPlate([[s*24,528],[s*80,524],[s*76,568],[s*28,572]],s*24,524,s*80,572,{lw:1.6});
    // Shin / Greave
    drawArmorPlate([[s*26,566],[s*78,562],[s*86,668],[s*22,672]],s*22,562,s*86,672,{lw:1.6});
    drawGlowSlit([[s*52,584],[s*58,584],[s*60,644],[s*54,644]],0.7);
    // Armored Foot
    drawArmorPlate([[s*18,668],[s*88,666],[s*104,698],[s*14,698]],s*14,666,s*104,698,{lw:1.6});
  }
}

function render(now){
  const t=now*0.001;
  state.zoom+=(state.targetZoom-state.zoom)*0.12;
  state.sitBlend+=((state.sitMode?1:0)-state.sitBlend)*0.1;
  state.smoothX+=(state.pointerX-state.smoothX)*0.08;
  state.smoothY+=(state.pointerY-state.smoothY)*0.08;

  const w=canvas.clientWidth;
  const h=canvas.clientHeight;
  ctx.clearRect(0,0,w,h);

  const talk=state.speaking?(0.35+0.65*Math.abs(Math.sin(t*14))):0;
  const breath=Math.sin(t*2.1);

  // Ambient red aura behind Ultron
  const aura=ctx.createRadialGradient(w*0.5,h*0.44,15,w*0.5,h*0.46,Math.min(w,h)*0.44);
  aura.addColorStop(0,'rgba(255,28,46,0.28)');
  aura.addColorStop(0.55,'rgba(170,12,26,0.12)');
  aura.addColorStop(1,'rgba(0,0,0,0)');
  ctx.fillStyle=aura;
  ctx.fillRect(0,0,w,h);

  ctx.save();
  // Stand view vs Sit Mode close-up bust framing
  const baseScale=Math.min(w/430,h/840)*state.zoom;
  const standScale=baseScale;
  const bustScale=Math.min(w/290,h/430)*state.zoom;
  const scale=standScale+(bustScale-standScale)*state.sitBlend;

  const standY=h*0.21+breath*4;
  const bustY=h*0.44+breath*3;
  const cy=standY+(bustY-standY)*state.sitBlend;

  ctx.translate(w*0.5,cy);
  ctx.scale(scale,scale);

  drawUltronBody(t,talk,breath,state.smoothX,state.smoothY);
  drawUltronHead(t,talk,state.smoothX,state.smoothY);

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
