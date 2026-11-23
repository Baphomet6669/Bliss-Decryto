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
.stage{position:absolute;inset:65px 0 92px;display:flex;align-items:center;justify-content:center}
.floor{position:absolute;bottom:0;width:min(900px,95vw);height:150px;background:radial-gradient(ellipse,rgba(255,52,20,.34),transparent 67%);border-radius:50%;transform:rotateX(65deg)}
#glCanvas{width:100%;height:100%;display:block;z-index:2;touch-action:none}
.caption{position:absolute;bottom:8px;text-align:center;letter-spacing:.28em;font-size:11px;color:#c6c8ce;text-shadow:0 0 12px #f22;z-index:3;pointer-events:none}
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
@media(max-width:650px){.topbar{padding:16px}.stage{inset:65px 0 138px}.chat{top:68px;right:10px;width:155px;font-size:10px}.console{left:12px;bottom:142px;width:150px;font-size:8px}.mic-state{right:12px;bottom:142px;font-size:8px}.controls{bottom:13px;gap:6px}button{padding:11px 12px;font-size:9px}.zoom{padding:7px}.caption{bottom:4px;font-size:9px}}
</style>
</head>
<body>
<div class="scene">
 <div class="city"></div><div class="flames"></div><div class="smoke"></div>
 <header class="topbar"><div class="brand">ULTRON<span>.</span>AI</div><div class="status"><i></i> SYSTEM ONLINE</div></header>
 <div class="chat"><small>ULTRON // RESPONSE</small><div id="reply">Awaiting your command, Shivam Sir.</div></div>
 <main class="stage">
  <div class="floor"></div>
  <canvas id="glCanvas"></canvas>
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

<script id="vs" type="x-shader/x-vertex">
attribute vec2 aPos;
void main(){
  gl_Position = vec4(aPos, 0.0, 1.0);
}
</script>

<script id="fs" type="x-shader/x-fragment">
precision highp float;

uniform vec2 uRes;
uniform float uTime;
uniform float uZoom;
uniform float uSit;
uniform float uTalk;
uniform vec2 uLook;

mat2 rot(float a){
  float c = cos(a), s = sin(a);
  return mat2(c, -s, s, c);
}

float smin(float a, float b, float k){
  float h = clamp(0.5 + 0.5*(b - a)/k, 0.0, 1.0);
  return mix(b, a, h) - k*h*(1.0 - h);
}

float smax(float a, float b, float k){
  return -smin(-a, -b, k);
}

float sdSphere(vec3 p, float r){
  return length(p) - r;
}

float sdEllipsoid(vec3 p, vec3 r){
  float k0 = length(p/r);
  float k1 = length(p/(r*r));
  return k0*(k0 - 1.0)/k1;
}

float sdCapsule(vec3 p, vec3 a, vec3 b, float r1, float r2){
  vec3 pa = p - a, ba = b - a;
  float h = clamp(dot(pa, ba)/dot(ba, ba), 0.0, 1.0);
  return length(pa - ba*h) - mix(r1, r2, h);
}

float sdRoundBox(vec3 p, vec3 b, float r){
  vec3 q = abs(p) - b;
  return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0) - r;
}

// Returns vec2(distance, materialID)
// 1.0 = brushed titanium armor, 2.0 = dark carbon inner skeleton, 3.0 = glowing crimson plasma
vec2 mapScene(vec3 p){
  float breath = sin(uTime * 2.1) * 0.015;
  p.y -= breath;

  // Subtle torso turn following gaze
  vec3 bp = p;
  bp.xz *= rot(uLook.x * 0.22);
  bp.yz *= rot(uLook.y * 0.10);

  // ---------------- HEAD (Sculpted Age of Ultron Prime Skull) ----------------
  vec3 hp = bp - vec3(0.0, 0.86, 0.05);
  hp.xz *= rot(uLook.x * 0.58);
  hp.yz *= rot(uLook.y * 0.38);

  // Cranium dome
  float skull = sdEllipsoid(hp - vec3(0.0, 0.06, -0.03), vec3(0.24, 0.30, 0.28));
  // Temple & ear audio pods
  vec3 ehp = vec3(abs(hp.x), hp.y, hp.z);
  float earPod = sdCapsule(ehp, vec3(0.21, -0.02, -0.03), vec3(0.24, 0.05, -0.05), 0.055, 0.045);
  skull = smin(skull, earPod, 0.02);

  // Iconic central forehead crest & brow plates
  float crest = sdCapsule(hp, vec3(0.0, 0.34, 0.02), vec3(0.0, 0.06, 0.255), 0.022, 0.036);
  vec3 browP = ehp - vec3(0.11, 0.08, 0.20);
  browP.xy *= rot(-0.28);
  browP.xz *= rot(0.32);
  float brow = sdRoundBox(browP, vec3(0.11, 0.036, 0.07), 0.018);

  // Sculpted angular cheekbones
  vec3 cheekP = ehp - vec3(0.145, -0.05, 0.14);
  cheekP.xy *= rot(0.35);
  cheekP.xz *= rot(0.45);
  float cheek = sdRoundBox(cheekP, vec3(0.085, 0.075, 0.09), 0.025);

  // Sharp nasal bridge
  vec3 noseP = hp - vec3(0.0, -0.015, 0.245);
  noseP.yz *= rot(-0.18);
  float nose = sdRoundBox(noseP, vec3(0.024, 0.062, 0.032), 0.012);

  // Animated Lower Jaw & Chin
  float jawDrop = uTalk * 0.038;
  vec3 jawP = hp - vec3(0.0, -0.175 - jawDrop, 0.11);
  jawP.yz *= rot(0.12 + uTalk * 0.12);
  float jaw = sdRoundBox(jawP, vec3(0.125, 0.082, 0.12), 0.035);
  float chin = sdRoundBox(jawP - vec3(0.0, -0.055, 0.055), vec3(0.068, 0.032, 0.065), 0.016);
  jaw = smin(jaw, chin, 0.02);

  float headArmor = smin(skull, brow, 0.018);
  headArmor = smin(headArmor, crest, 0.015);
  headArmor = smin(headArmor, cheek, 0.022);
  headArmor = smin(headArmor, nose, 0.012);
  headArmor = smin(headArmor, jaw, 0.025);

  // Carve deep menacing eye sockets
  vec3 sockP = ehp - vec3(0.105, 0.032, 0.225);
  sockP.xy *= rot(-0.24);
  sockP.xz *= rot(0.28);
  float socket = sdRoundBox(sockP, vec3(0.078, 0.028, 0.065), 0.012);
  headArmor = smax(headArmor, -socket, 0.012);

  // Carve cheek vents & mouth cavity
  vec3 ventP = ehp - vec3(0.165, -0.065, 0.14);
  ventP.xz *= rot(0.5);
  float cheekVent = sdRoundBox(ventP, vec3(0.045, 0.032, 0.05), 0.008);
  headArmor = smax(headArmor, -cheekVent, 0.008);

  vec3 mouthCavP = jawP - vec3(0.0, 0.018, 0.095);
  float mouthCav = sdRoundBox(mouthCavP, vec3(0.078, 0.036 + jawDrop*0.5, 0.055), 0.01);
  headArmor = smax(headArmor, -mouthCav, 0.008);

  // Vertical titanium teeth / grille bars over mouth cavity
  float gx = abs(fract((hp.x + 0.016) / 0.032) - 0.5) * 0.032;
  float grilleBars = max(abs(hp.x) - 0.075, max(gx - 0.0045, length(jawP.yz - vec2(0.018, 0.118)) - 0.032));
  headArmor = min(headArmor, grilleBars);

  // Glowing Red Predator Eyes
  vec3 eyeP = ehp - vec3(0.105, 0.030, 0.205);
  eyeP.xy *= rot(-0.25);
  eyeP.xz *= rot(0.28);
  float eyes = sdRoundBox(eyeP, vec3(0.064, 0.014, 0.032), 0.006);

  // Internal Mouth Furnace Glow & Temple Glow
  float mouthGlow = sdRoundBox(jawP - vec3(0.0, 0.018, 0.078), vec3(0.068, 0.026 + jawDrop*0.45, 0.032), 0.008);
  float earGlow = sdRoundBox(ehp - vec3(0.238, 0.015, -0.035), vec3(0.012, 0.028, 0.012), 0.004);
  float glow = min(eyes, min(mouthGlow, earGlow));

  // Dark inner cranium backing
  float headInner = sdEllipsoid(hp - vec3(0.0, 0.02, 0.01), vec3(0.21, 0.25, 0.23));

  // ---------------- NECK & HYDRAULICS ----------------
  vec3 ebp = vec3(abs(bp.x), bp.y, bp.z);
  float neckCore = sdCapsule(bp, vec3(0.0, 0.48, -0.02), vec3(0.0, 0.72, 0.02), 0.115, 0.095);
  float piston1 = sdCapsule(ebp, vec3(0.075, 0.46, 0.03), vec3(0.055, 0.70, 0.05), 0.024, 0.020);
  float piston2 = sdCapsule(ebp, vec3(0.105, 0.46, -0.04), vec3(0.075, 0.69, -0.02), 0.022, 0.018);
  float collar = sdCapsule(ebp, vec3(0.0, 0.44, 0.08), vec3(0.22, 0.52, -0.02), 0.045, 0.038);

  // ---------------- TORSO, PECTORALS & ARC REACTOR ----------------
  float chestCore = sdEllipsoid(bp - vec3(0.0, 0.24, 0.0), vec3(0.32, 0.26, 0.21));
  float absCore = sdCapsule(bp, vec3(0.0, -0.18, 0.01), vec3(0.0, 0.16, 0.03), 0.175, 0.235);
  float torsoInner = smin(chestCore, absCore, 0.06);

  // Sculpted Pectoral Armor Plates
  vec3 pecP = ebp - vec3(0.165, 0.29, 0.145);
  pecP.xy *= rot(-0.14);
  pecP.xz *= rot(0.34);
  pecP.yz *= rot(-0.16);
  float pec = sdRoundBox(pecP, vec3(0.135, 0.105, 0.065), 0.028);

  // Ribbed Abdominal Armor Plates (4 stacked segments)
  float ribs = 1e5;
  for(int i = 0; i < 4; i++){
    float fi = float(i);
    float ry = 0.11 - fi * 0.078;
    float rw = 0.145 - fi * 0.012;
    vec3 ribP = ebp - vec3(rw * 0.65, ry, 0.155 - fi * 0.008);
    ribP.xy *= rot(-0.12);
    ribP.xz *= rot(0.35);
    float seg = sdRoundBox(ribP, vec3(rw * 0.62, 0.026, 0.048), 0.012);
    ribs = min(ribs, seg);
  }

  // Glowing Arc Reactor Chest Core
  float chestGlow = sdCapsule(bp, vec3(0.0, 0.17, 0.215), vec3(0.0, 0.33, 0.225), 0.018, 0.026);
  glow = min(glow, chestGlow);

  // ---------------- LAYERED SHOULDER PAULDRONS ----------------
  vec3 shP = ebp - vec3(0.37, 0.35, -0.01);
  shP.xy *= rot(-0.42);
  float pauldron1 = sdEllipsoid(shP, vec3(0.17, 0.13, 0.16));
  float pauldron2 = sdEllipsoid(shP - vec3(0.04, -0.07, 0.01), vec3(0.14, 0.10, 0.14));
  float pauldrons = smin(pauldron1, pauldron2, 0.025);
  float shGlow = sdRoundBox(shP - vec3(0.05, 0.01, 0.135), vec3(0.045, 0.012, 0.015), 0.004);
  glow = min(glow, shGlow);

  // ---------------- ARMS, GAUNTLETS & CLAWS ----------------
  vec3 shJoint = vec3(0.42, 0.27, 0.0);
  vec3 elJoint = vec3(0.49, -0.02, 0.04);
  vec3 wrJoint = vec3(0.52, -0.32, 0.12);

  float upperArmInner = sdCapsule(ebp, shJoint, elJoint, 0.082, 0.068);
  float upperArmArmor = sdCapsule(ebp, shJoint + vec3(0.02, -0.02, 0.01), elJoint + vec3(0.01, 0.03, 0.01), 0.095, 0.078);
  float forearm = sdCapsule(ebp, elJoint, wrJoint, 0.086, 0.064);
  float armGlow = sdCapsule(ebp, elJoint + vec3(0.04, -0.07, 0.065), wrJoint + vec3(0.03, 0.06, 0.055), 0.008, 0.006);
  glow = min(glow, armGlow);

  // Hand & Articulated Claws
  float hand = sdRoundBox(ebp - (wrJoint + vec3(0.0, -0.05, 0.02)), vec3(0.042, 0.055, 0.055), 0.018);
  float claws = 1e5;
  for(int f = -1; f <= 1; f++){
    float ff = float(f);
    vec3 cStart = wrJoint + vec3(-0.01, -0.10, 0.02 + ff * 0.028);
    vec3 cEnd = cStart + vec3(-0.025, -0.085, 0.01);
    claws = min(claws, sdCapsule(ebp, cStart, cEnd, 0.013, 0.005));
  }

  // ---------------- PELVIS & HEAVY ARMORED LEGS ----------------
  float pelvis = sdRoundBox(bp - vec3(0.0, -0.25, 0.02), vec3(0.185, 0.075, 0.135), 0.035);
  vec3 hipJ = vec3(0.145, -0.29, 0.01);
  vec3 kneeJ = vec3(0.175, -0.66, 0.04);
  vec3 ankleJ = vec3(0.19, -1.04, 0.0);

  float thigh = sdCapsule(ebp, hipJ, kneeJ, 0.112, 0.086);
  float kneeGuard = sdRoundBox(ebp - (kneeJ + vec3(0.0, 0.0, 0.075)), vec3(0.062, 0.058, 0.042), 0.018);
  float shin = sdCapsule(ebp, kneeJ, ankleJ, 0.092, 0.068);
  float legGlow = sdCapsule(ebp, kneeJ + vec3(0.02, -0.08, 0.082), ankleJ + vec3(0.02, 0.10, 0.065), 0.008, 0.006);
  glow = min(glow, legGlow);

  float foot = sdRoundBox(ebp - vec3(0.19, -1.09, 0.07), vec3(0.078, 0.042, 0.145), 0.02);

  // Combine Titanium Armor (ID 1.0)
  float armor = headArmor;
  armor = min(armor, piston1);
  armor = min(armor, collar);
  armor = min(armor, pec);
  armor = min(armor, ribs);
  armor = min(armor, pauldrons);
  armor = min(armor, upperArmArmor);
  armor = min(armor, forearm);
  armor = min(armor, hand);
  armor = min(armor, claws);
  armor = min(armor, pelvis);
  armor = min(armor, thigh);
  armor = min(armor, kneeGuard);
  armor = min(armor, shin);
  armor = min(armor, foot);

  // Combine Dark Inner Frame (ID 2.0)
  float dark = headInner;
  dark = min(dark, neckCore);
  dark = min(dark, piston2);
  dark = min(dark, torsoInner);
  dark = min(dark, upperArmInner);

  vec2 res = vec2(armor, 1.0);
  if(dark < res.x) res = vec2(dark, 2.0);
  if(glow < res.x) res = vec2(glow, 3.0);
  return res;
}

vec3 calcNormal(vec3 p){
  vec2 e = vec2(0.0018, -0.0018);
  return normalize(
    e.xyy * mapScene(p + e.xyy).x +
    e.yyx * mapScene(p + e.yyx).x +
    e.yxy * mapScene(p + e.yxy).x +
    e.xxx * mapScene(p + e.xxx).x
  );
}

// Procedural studio + fiery apocalyptic reflection environment
vec3 envReflection(vec3 r){
  float sky = clamp(r.y * 0.5 + 0.5, 0.0, 1.0);
  vec3 coldKey = vec3(0.75, 0.84, 0.96) * pow(max(0.0, dot(r, normalize(vec3(-0.5, 0.7, 0.5)))), 6.0);
  vec3 topStrip = vec3(0.95, 0.98, 1.0) * smoothstep(0.65, 0.96, r.y) * 0.9;
  vec3 fireBounce = vec3(1.0, 0.16, 0.06) * pow(clamp(-r.y + 0.25, 0.0, 1.0), 2.2) * 0.85;
  vec3 rimRed = vec3(0.95, 0.08, 0.14) * pow(max(0.0, dot(r, normalize(vec3(0.6, 0.1, -0.8)))), 4.0) * 0.95;
  return mix(vec3(0.04, 0.05, 0.07), vec3(0.18, 0.22, 0.28), sky) + coldKey + topStrip + fireBounce + rimRed;
}

void main(){
  vec2 uv = (gl_FragCoord.xy - 0.5 * uRes.xy) / uRes.y;

  // Camera framing: Full body Stand Mode vs Menacing Close-Up Sit Mode
  vec3 standCam = vec3(0.0, -0.08, 2.65 / uZoom);
  vec3 sitCam   = vec3(0.0, 0.76, 1.18 / uZoom);
  vec3 ro = mix(standCam, sitCam, uSit);

  vec3 target = mix(vec3(0.0, -0.08, 0.0), vec3(0.0, 0.78, 0.05), uSit);
  vec3 fwd = normalize(target - ro);
  vec3 right = normalize(cross(vec3(0.0, 1.0, 0.0), fwd));
  vec3 up = cross(fwd, right);
  vec3 rd = normalize(fwd + uv.x * right + uv.y * up);

  float t = 0.0;
  float hitMat = 0.0;
  float minGlowDist = 100.0;

  for(int i = 0; i < 88; i++){
    vec3 p = ro + rd * t;
    vec2 h = mapScene(p);
    // Track closest approach to red plasma cores for volumetric bloom
    float gDist = mapScene(p).y == 3.0 ? h.x : 1.0;
    minGlowDist = min(minGlowDist, max(0.002, h.x + (h.y == 3.0 ? 0.0 : 0.06)));

    if(h.x < 0.0018){
      hitMat = h.y;
      break;
    }
    if(t > 5.5) break;
    t += h.x * 0.88;
  }

  vec3 col = vec3(0.0);
  float alpha = 0.0;

  if(hitMat > 0.5){
    vec3 p = ro + rd * t;
    vec3 n = calcNormal(p);
    vec3 v = -rd;
    vec3 r = reflect(-v, n);

    // Ambient occlusion approximation
    float ao = clamp(0.5 + 0.5 * mapScene(p + n * 0.045).x / 0.045, 0.15, 1.0);
    float fresnel = pow(1.0 - max(dot(n, v), 0.0), 4.0);

    vec3 keyDir = normalize(vec3(-0.55, 0.75, 0.65));
    vec3 rimDir = normalize(vec3(0.65, 0.25, -0.72));
    float diffKey = max(dot(n, keyDir), 0.0);
    float diffRim = max(dot(n, rimDir), 0.0);

    if(hitMat < 1.5){
      // Brushed Vibranium/Titanium Armor
      vec3 baseMetal = vec3(0.46, 0.50, 0.56);
      vec3 env = envReflection(r);
      vec3 specKey = vec3(1.0, 0.98, 0.96) * pow(max(dot(r, keyDir), 0.0), 42.0) * 1.35;
      vec3 specRim = vec3(1.0, 0.14, 0.20) * pow(max(dot(r, rimDir), 0.0), 16.0) * 1.1;
      col = baseMetal * (0.14 + 0.45 * diffKey) * ao
          + env * mix(0.42, 0.95, fresnel) * ao
          + specKey + specRim
          + vec3(0.95, 0.10, 0.16) * diffRim * 0.35;
    } else if(hitMat < 2.5){
      // Dark Gunmetal Inner Chassis
      vec3 darkMetal = vec3(0.06, 0.075, 0.095);
      vec3 env = envReflection(r) * 0.32;
      vec3 spec = vec3(0.7, 0.78, 0.9) * pow(max(dot(r, keyDir), 0.0), 24.0) * 0.5;
      col = darkMetal * (0.25 + 0.5 * diffKey) * ao + env * (0.3 + 0.7 * fresnel) + spec;
    } else {
      // Incandescent Crimson Plasma (Eyes, Mouth Furnace, Arc Core)
      float pulse = 0.88 + 0.12 * sin(uTime * 3.5) + uTalk * 0.25;
      float coreHot = pow(max(dot(n, v), 0.0), 1.5);
      col = mix(vec3(1.0, 0.06, 0.12), vec3(1.0, 0.82, 0.85), coreHot) * (1.85 * pulse);
    }
    alpha = 1.0;
  }

  // Volumetric crimson plasma bloom around eyes, mouth & core
  float plasmaBloom = exp(-minGlowDist * 18.0) * (0.55 + 0.2 * uTalk);
  col += vec3(1.0, 0.08, 0.14) * plasmaBloom;
  alpha = max(alpha, clamp(plasmaBloom * 1.4, 0.0, 1.0));

  // Filmic tone-mapping & contrast punch
  col = col / (col + vec3(0.65));
  col = pow(max(col, 0.0), vec3(0.92));

  gl_FragColor = vec4(col, alpha);
}
</script>

<script>
const reply=document.getElementById('reply'),
      voiceStatus=document.getElementById('voiceStatus'),
      micStatus=document.getElementById('micStatus'),
      sitBtn=document.getElementById('sitBtn'),
      standBtn=document.getElementById('standBtn'),
      canvas=document.getElementById('glCanvas');

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

window.addEventListener('pointermove',e=>{
  state.px=Math.max(-1,Math.min(1,(e.clientX/window.innerWidth)*2-1));
  state.py=Math.max(-1,Math.min(1,(e.clientY/window.innerHeight)*2-1));
});

const gl=canvas.getContext('webgl',{alpha:true,antialias:true,premultipliedAlpha:false});
let prog,uRes,uTime,uZoom,uSit,uTalk,uLook;

function initGL(){
  if(!gl)return;
  function compile(type,src){
    const s=gl.createShader(type);
    gl.shaderSource(s,src);
    gl.compileShader(s);
    if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))console.error(gl.getShaderInfoLog(s));
    return s;
  }
  prog=gl.createProgram();
  gl.attachShader(prog,compile(gl.VERTEX_SHADER,document.getElementById('vs').textContent));
  gl.attachShader(prog,compile(gl.FRAGMENT_SHADER,document.getElementById('fs').textContent));
  gl.linkProgram(prog);
  gl.useProgram(prog);

  const buf=gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER,buf);
  gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,1,1]),gl.STATIC_DRAW);
  const aPos=gl.getAttribLocation(prog,'aPos');
  gl.enableVertexAttribArray(aPos);
  gl.vertexAttribPointer(aPos,2,gl.FLOAT,false,0,0);

  uRes=gl.getUniformLocation(prog,'uRes');
  uTime=gl.getUniformLocation(prog,'uTime');
  uZoom=gl.getUniformLocation(prog,'uZoom');
  uSit=gl.getUniformLocation(prog,'uSit');
  uTalk=gl.getUniformLocation(prog,'uTalk');
  uLook=gl.getUniformLocation(prog,'uLook');
}
initGL();

function resize(){
  const dpr=Math.min(window.devicePixelRatio||1,1.75);
  const w=Math.max(1,Math.floor(canvas.clientWidth*dpr));
  const h=Math.max(1,Math.floor(canvas.clientHeight*dpr));
  if(canvas.width!==w||canvas.height!==h){
    canvas.width=w;
    canvas.height=h;
  }
}
window.addEventListener('resize',resize);
resize();

function loop(now){
  const t=now*0.001;
  state.zoom+=(state.targetZoom-state.zoom)*0.12;
  state.sitBlend+=((state.sitMode?1:0)-state.sitBlend)*0.09;
  state.lookX+=(state.px-state.lookX)*0.08;
  state.lookY+=(state.py-state.lookY)*0.08;
  const targetTalk=state.speaking?(0.4+0.6*Math.abs(Math.sin(t*15))):0.0;
  state.talkAmp+=(targetTalk-state.talkAmp)*0.22;

  if(gl&&prog){
    resize();
    gl.viewport(0,0,canvas.width,canvas.height);
    gl.clearColor(0,0,0,0);
    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.uniform2f(uRes,canvas.width,canvas.height);
    gl.uniform1f(uTime,t);
    gl.uniform1f(uZoom,state.zoom);
    gl.uniform1f(uSit,state.sitBlend);
    gl.uniform1f(uTalk,state.talkAmp);
    gl.uniform2f(uLook,state.lookX,state.lookY);
    gl.drawArrays(gl.TRIANGLE_STRIP,0,4);
  }
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
