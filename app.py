import os
from flask import Flask, jsonify, render_template_string

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
.stage{position:absolute;inset:64px 0 92px;display:flex;align-items:center;justify-content:center}
.floor{position:absolute;bottom:0;width:min(900px,95vw);height:150px;background:radial-gradient(ellipse,rgba(255,52,20,.34),transparent 67%);border-radius:50%;transform:rotateX(65deg);pointer-events:none}
#threeMount{position:absolute;inset:0;z-index:2;touch-action:none}
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
@media(max-width:650px){.topbar{padding:16px}.stage{inset:62px 0 136px}.chat{top:68px;right:10px;width:155px;font-size:10px}.console{left:12px;bottom:142px;width:150px;font-size:8px}.mic-state{right:12px;bottom:142px;font-size:8px}.controls{bottom:13px;gap:6px}button{padding:11px 12px;font-size:9px}.zoom{padding:7px}.caption{bottom:4px;font-size:9px}}
</style>
<script type="importmap">
{
  "imports": {
    "three": "https://unpkg.com/three@0.168.0/build/three.module.js",
    "three/addons/": "https://unpkg.com/three@0.168.0/examples/jsm/"
  }
}
</script>
</head>
<body>
<div class="scene">
 <div class="city"></div><div class="flames"></div><div class="smoke"></div>
 <header class="topbar"><div class="brand">ULTRON<span>.</span>AI</div><div class="status"><i></i> SYSTEM ONLINE</div></header>
 <div class="chat"><small>ULTRON // RESPONSE</small><div id="reply">Awaiting your command, Shivam Sir.</div></div>
 <main class="stage">
  <div class="floor"></div>
  <div id="threeMount"></div>
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

<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';

const reply = document.getElementById('reply'),
      voiceStatus = document.getElementById('voiceStatus'),
      micStatus = document.getElementById('micStatus'),
      sitBtn = document.getElementById('sitBtn'),
      standBtn = document.getElementById('standBtn'),
      mount = document.getElementById('threeMount');

const state = {
  zoom: 1,
  targetZoom: 1,
  sitMode: false,
  sitBlend: 0,
  speaking: false,
  talkAmp: 0,
  px: 0,
  py: 0
};

window.addEventListener('pointermove', e => {
  state.px = Math.max(-1, Math.min(1, (e.clientX / window.innerWidth) * 2 - 1));
  state.py = Math.max(-1, Math.min(1, (e.clientY / window.innerHeight) * 2 - 1));
});

// ---------------- THREE.JS PBR SCENE & STUDIO ENV ----------------
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
renderer.setSize(mount.clientWidth, mount.clientHeight);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.25;
mount.appendChild(renderer.domElement);

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(34, mount.clientWidth / mount.clientHeight, 0.1, 40);
camera.position.set(0, 0.15, 5.2);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.06;
controls.enablePan = false;
controls.minDistance = 1.4;
controls.maxDistance = 7.5;
controls.minPolarAngle = Math.PI * 0.25;
controls.maxPolarAngle = Math.PI * 0.65;
controls.target.set(0, 0.05, 0);

// Procedural Studio Chrome HDRI-like Environment Map
const pmrem = new THREE.PMREMGenerator(renderer);
const envScene = new THREE.Scene();
envScene.background = new THREE.Color(0x0b0e14);
const strip1 = new THREE.Mesh(new THREE.PlaneGeometry(14, 3), new THREE.MeshBasicMaterial({ color: 0xeef6ff, side: THREE.DoubleSide }));
strip1.position.set(-4, 6, 5); strip1.lookAt(0, 0, 0); envScene.add(strip1);
const strip2 = new THREE.Mesh(new THREE.PlaneGeometry(14, 2.5), new THREE.MeshBasicMaterial({ color: 0x9bb4d4, side: THREE.DoubleSide }));
strip2.position.set(5, 4, 4); strip2.lookAt(0, 0, 0); envScene.add(strip2);
const fireStrip = new THREE.Mesh(new THREE.PlaneGeometry(18, 5), new THREE.MeshBasicMaterial({ color: 0xff2810, side: THREE.DoubleSide }));
fireStrip.position.set(0, -6, 2); fireStrip.lookAt(0, 0, 0); envScene.add(fireStrip);
const rimStrip = new THREE.Mesh(new THREE.PlaneGeometry(12, 8), new THREE.MeshBasicMaterial({ color: 0xff1e32, side: THREE.DoubleSide }));
rimStrip.position.set(4, 2, -6); rimStrip.lookAt(0, 0, 0); envScene.add(rimStrip);
scene.environment = pmrem.fromScene(envScene, 0.035).texture;

// Postprocessing Bloom for real incandescent red eyes, core & vents
const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(mount.clientWidth, mount.clientHeight), 0.72, 0.45, 0.78);
composer.addPass(bloom);

// Cinematic 3-Point + Under-Fire Lighting
scene.add(new THREE.AmbientLight(0x283244, 0.9));
const keyLight = new THREE.DirectionalLight(0xf2f7ff, 2.8);
keyLight.position.set(-3, 5, 4);
scene.add(keyLight);
const fillLight = new THREE.DirectionalLight(0x7ca2d6, 1.4);
fillLight.position.set(4, 2, 3);
scene.add(fillLight);
const rimLight = new THREE.DirectionalLight(0xff2238, 3.2);
rimLight.position.set(2, 3, -4);
scene.add(rimLight);
const fireLight = new THREE.PointLight(0xff4214, 4.5, 8);
fireLight.position.set(0, -2.2, 1.2);
scene.add(fireLight);

// PBR Materials (Brushed Vibranium/Titanium, Dark Gunmetal Frame, Emissive Crimson Plasma)
const armorMat = new THREE.MeshStandardMaterial({
  color: 0x9aa4b2,
  metalness: 0.94,
  roughness: 0.22,
  envMapIntensity: 1.45
});
const brightArmorMat = new THREE.MeshStandardMaterial({
  color: 0xcbd4e0,
  metalness: 0.96,
  roughness: 0.16,
  envMapIntensity: 1.65
});
const darkFrameMat = new THREE.MeshStandardMaterial({
  color: 0x1a202a,
  metalness: 0.85,
  roughness: 0.42,
  envMapIntensity: 0.9
});
const plasmaMat = new THREE.MeshStandardMaterial({
  color: 0xff162c,
  emissive: 0xff162c,
  emissiveIntensity: 3.4,
  roughness: 0.1
});

function addPart(parent, geo, mat, pos = [0,0,0], rot = [0,0,0], scale = [1,1,1]) {
  const m = new THREE.Mesh(geo, mat);
  m.position.set(...pos);
  m.rotation.set(...rot);
  m.scale.set(...scale);
  parent.add(m);
  return m;
}

// ---------------- BUILD 3D AGE OF ULTRON PRIME ----------------
const ultron = new THREE.Group();
scene.add(ultron);

// 1. TORSO & INNER SKELETON
const torsoGroup = new THREE.Group();
ultron.add(torsoGroup);

// Dark inner ribcage & spine core
addPart(torsoGroup, new THREE.CylinderGeometry(0.32, 0.22, 0.82, 24), darkFrameMat, [0, 0.36, -0.02], [0, 0, 0], [1.15, 1, 0.72]);
addPart(torsoGroup, new THREE.CylinderGeometry(0.11, 0.12, 0.88, 16), brightArmorMat, [0, 0.36, -0.18]);

// Glowing internal plasma vents inside ribcage
for (const s of [-1, 1]) {
  addPart(torsoGroup, new THREE.BoxGeometry(0.035, 0.34, 0.04), plasmaMat, [s * 0.16, 0.28, 0.15], [0, s * 0.2, s * -0.15]);
  addPart(torsoGroup, new THREE.TorusGeometry(0.11, 0.016, 12, 28), plasmaMat, [s * 0.34, 0.56, 0.02], [0, s * 1.15, 0]);
  addPart(torsoGroup, new THREE.TorusGeometry(0.12, 0.026, 12, 28), darkFrameMat, [s * 0.34, 0.56, 0.02], [0, s * 1.15, 0]);
}
// Central Arc Reactor Slit
addPart(torsoGroup, new THREE.CapsuleGeometry(0.024, 0.18, 8, 16), plasmaMat, [0, 0.52, 0.245], [0.12, 0, 0]);
addPart(torsoGroup, new THREE.BoxGeometry(0.09, 0.28, 0.08), darkFrameMat, [0, 0.52, 0.20], [0.12, 0, 0]);

// Sculpted Pectoral Armor & Swept Rib Wings
for (const s of [-1, 1]) {
  // Upper Pectoral Shell
  const pec = addPart(torsoGroup, new THREE.SphereGeometry(0.24, 28, 20), brightArmorMat, [s * 0.21, 0.58, 0.11], [0.15, s * 0.35, s * -0.18], [1.18, 0.72, 0.65]);
  // Swept Rib Armor Plates (4 tiered curved ribs)
  for (let r = 0; r < 4; r++) {
    const ry = 0.40 - r * 0.095;
    const rw = 0.25 - r * 0.024;
    addPart(torsoGroup, new THREE.BoxGeometry(rw, 0.042, 0.16), armorMat, [s * (0.14 - r * 0.01), ry, 0.14 - r * 0.012], [0.12, s * 0.45, s * -0.22]);
  }
  // Collarbone & Trapezius Armor
  addPart(torsoGroup, new THREE.CapsuleGeometry(0.055, 0.26, 10, 16), armorMat, [s * 0.20, 0.75, 0.05], [0.25, 0, s * 1.18]);
}

// 2. NECK & HYDRAULICS
addPart(torsoGroup, new THREE.CylinderGeometry(0.11, 0.13, 0.24, 20), darkFrameMat, [0, 0.84, -0.01]);
for (const s of [-1, 1]) {
  addPart(torsoGroup, new THREE.CylinderGeometry(0.022, 0.026, 0.24, 12), brightArmorMat, [s * 0.075, 0.84, 0.05], [0.1, 0, s * -0.12]);
  addPart(torsoGroup, new THREE.CylinderGeometry(0.018, 0.022, 0.23, 12), armorMat, [s * 0.10, 0.84, -0.04], [-0.08, 0, s * -0.16]);
  addPart(torsoGroup, new THREE.BoxGeometry(0.016, 0.14, 0.016), plasmaMat, [s * 0.095, 0.83, 0.02], [0, 0, s * -0.14]);
}

// 3. HEAD & ARTICULATED JAW (SCULPTED ULTRON PRIME SKULL)
const headGroup = new THREE.Group();
headGroup.position.set(0, 1.08, 0.03);
torsoGroup.add(headGroup);

// Sleek Titanium Cranium
addPart(headGroup, new THREE.SphereGeometry(0.21, 32, 28), brightArmorMat, [0, 0.05, -0.02], [0, 0, 0], [0.92, 1.16, 1.08]);
// Central Forehead Crest
addPart(headGroup, new THREE.CapsuleGeometry(0.022, 0.20, 8, 16), brightArmorMat, [0, 0.14, 0.13], [0.68, 0, 0]);
// Brow Ridge & Menacing Glowing Red Brow Lines
for (const s of [-1, 1]) {
  addPart(headGroup, new THREE.BoxGeometry(0.12, 0.036, 0.11), brightArmorMat, [s * 0.095, 0.065, 0.155], [0.18, s * 0.36, s * -0.24]);
  // Iconic red forehead V-slits
  addPart(headGroup, new THREE.BoxGeometry(0.085, 0.011, 0.02), plasmaMat, [s * 0.095, 0.11, 0.185], [-0.35, s * 0.35, s * -0.32]);
  // Ear Rotary Pods
  addPart(headGroup, new THREE.CylinderGeometry(0.058, 0.052, 0.05, 20), armorMat, [s * 0.195, 0.01, -0.02], [0, 0, Math.PI * 0.5]);
  addPart(headGroup, new THREE.BoxGeometry(0.015, 0.045, 0.015), plasmaMat, [s * 0.222, 0.01, -0.01]);
  // High Sculpted Cheekbones
  addPart(headGroup, new THREE.BoxGeometry(0.085, 0.11, 0.13), armorMat, [s * 0.125, -0.035, 0.11], [0.15, s * 0.52, s * 0.28]);
}
// Dark Ocular Cavity + Predator Red Eyes
addPart(headGroup, new THREE.BoxGeometry(0.22, 0.065, 0.12), darkFrameMat, [0, 0.025, 0.135]);
for (const s of [-1, 1]) {
  addPart(headGroup, new THREE.BoxGeometry(0.072, 0.018, 0.03), plasmaMat, [s * 0.078, 0.025, 0.185], [0, s * 0.32, s * -0.22]);
}
// Nasal Bridge
addPart(headGroup, new THREE.BoxGeometry(0.032, 0.085, 0.055), brightArmorMat, [0, -0.015, 0.195], [-0.18, 0, 0]);

// Animated Lower Jaw + Mouth Furnace Grille
const jawGroup = new THREE.Group();
jawGroup.position.set(0, -0.085, 0.04);
headGroup.add(jawGroup);
addPart(jawGroup, new THREE.BoxGeometry(0.15, 0.085, 0.16), armorMat, [0, -0.025, 0.045]);
addPart(jawGroup, new THREE.BoxGeometry(0.085, 0.042, 0.08), brightArmorMat, [0, -0.062, 0.095]);
// Internal red furnace glow inside mouth
const mouthGlowMesh = addPart(jawGroup, new THREE.BoxGeometry(0.11, 0.042, 0.03), plasmaMat, [0, 0.005, 0.118]);
// Titanium mouth grille bars
for (const gx of [-0.042, -0.021, 0, 0.021, 0.042]) {
  addPart(jawGroup, new THREE.BoxGeometry(0.008, 0.052, 0.018), brightArmorMat, [gx, 0.005, 0.132]);
}

// 4. LAYERED SHOULDER PAULDRONS, ARMS & CLAWS
const armGroups = [];
for (const s of [-1, 1]) {
  const armPivot = new THREE.Group();
  armPivot.position.set(s * 0.44, 0.64, 0);
  torsoGroup.add(armPivot);
  armGroups.push({ group: armPivot, side: s });

  // Outer curved shoulder pauldron
  addPart(armPivot, new THREE.SphereGeometry(0.17, 24, 20), brightArmorMat, [s * 0.04, 0.02, 0], [0, 0, s * -0.35], [1.1, 0.92, 1.05]);
  addPart(armPivot, new THREE.SphereGeometry(0.145, 20, 16), armorMat, [s * 0.07, -0.08, 0.01], [0, 0, s * -0.25], [1.0, 0.85, 0.95]);
  // Upper arm / bicep
  addPart(armPivot, new THREE.CylinderGeometry(0.075, 0.065, 0.34, 18), darkFrameMat, [s * 0.08, -0.26, 0.01], [0, 0, s * 0.12]);
  addPart(armPivot, new THREE.CapsuleGeometry(0.072, 0.22, 10, 16), armorMat, [s * 0.095, -0.26, 0.02], [0, 0, s * 0.12]);
  // Elbow joint
  addPart(armPivot, new THREE.SphereGeometry(0.076, 18, 14), darkFrameMat, [s * 0.11, -0.45, 0.03]);
  // Forearm gauntlet
  addPart(armPivot, new THREE.CylinderGeometry(0.082, 0.058, 0.36, 18), brightArmorMat, [s * 0.12, -0.65, 0.09], [-0.28, 0, s * 0.06]);
  addPart(armPivot, new THREE.BoxGeometry(0.015, 0.16, 0.015), plasmaMat, [s * 0.175, -0.63, 0.11], [-0.28, 0, s * 0.06]);
  // Mechanical Hand & Claws
  addPart(armPivot, new THREE.BoxGeometry(0.065, 0.09, 0.085), darkFrameMat, [s * 0.12, -0.86, 0.15], [-0.25, 0, 0]);
  for (let f = -1; f <= 1; f++) {
    addPart(armPivot, new THREE.ConeGeometry(0.012, 0.09, 8), brightArmorMat, [s * (0.11 + f * 0.015), -0.94, 0.16 + f * 0.022], [Math.PI + 0.35, 0, s * -0.2]);
  }
}

// 5. PELVIS, HEAVY ARMORED THIGHS, KNEES, SHINS & FEET
addPart(ultron, new THREE.CylinderGeometry(0.22, 0.16, 0.22, 20), armorMat, [0, -0.12, 0.01], [0, 0, 0], [1.15, 1, 0.78]);
addPart(ultron, new THREE.BoxGeometry(0.11, 0.24, 0.16), brightArmorMat, [0, -0.13, 0.08]);

for (const s of [-1, 1]) {
  // Hip joint
  addPart(ultron, new THREE.SphereGeometry(0.095, 18, 14), darkFrameMat, [s * 0.17, -0.20, 0.01]);
  // Thigh armor
  addPart(ultron, new THREE.CapsuleGeometry(0.105, 0.38, 12, 20), brightArmorMat, [s * 0.20, -0.45, 0.02], [0.03, 0, s * 0.06], [0.95, 1, 1.08]);
  addPart(ultron, new THREE.BoxGeometry(0.09, 0.34, 0.12), darkFrameMat, [s * 0.16, -0.45, 0.0], [0.03, 0, s * 0.06]);
  // Knee guard
  addPart(ultron, new THREE.BoxGeometry(0.11, 0.12, 0.11), armorMat, [s * 0.22, -0.70, 0.06]);
  // Shin / Greave
  addPart(ultron, new THREE.CapsuleGeometry(0.085, 0.42, 12, 20), brightArmorMat, [s * 0.23, -0.98, 0.01], [-0.04, 0, s * 0.03], [0.92, 1, 1.12]);
  addPart(ultron, new THREE.BoxGeometry(0.014, 0.20, 0.014), plasmaMat, [s * 0.235, -0.96, 0.095]);
  // Armored Foot & Claws
  addPart(ultron, new THREE.BoxGeometry(0.13, 0.075, 0.26), armorMat, [s * 0.24, -1.24, 0.07]);
  for (let t = -1; t <= 1; t++) {
    addPart(ultron, new THREE.BoxGeometry(0.032, 0.045, 0.11), brightArmorMat, [s * 0.24 + t * 0.04, -1.255, 0.19], [0.15, 0, 0]);
  }
}

// ---------------- ANIMATION & CAMERA LOOP ----------------
const clock = new THREE.Clock();

function animate() {
  requestAnimationFrame(animate);
  const t = clock.getElapsedTime();

  state.zoom += (state.targetZoom - state.zoom) * 0.12;
  state.sitBlend += ((state.sitMode ? 1 : 0) - state.sitBlend) * 0.09;
  const targetTalk = state.speaking ? (0.45 + 0.55 * Math.abs(Math.sin(t * 14))) : 0.0;
  state.talkAmp += (targetTalk - state.talkAmp) * 0.24;

  // Idle breathing & subtle heroic sway
  const breath = Math.sin(t * 2.1);
  torsoGroup.position.y = breath * 0.016;
  torsoGroup.rotation.y = Math.sin(t * 0.7) * 0.04 + state.px * 0.18;

  // Head tracks cursor/touch smoothly
  headGroup.rotation.y += ((state.px * 0.45) - headGroup.rotation.y) * 0.09;
  headGroup.rotation.x += ((state.py * 0.26) - headGroup.rotation.x) * 0.09;

  // Jaw moves when speaking
  jawGroup.position.y = -0.085 - state.talkAmp * 0.026;
  jawGroup.rotation.x = state.talkAmp * 0.18;
  mouthGlowMesh.scale.y = 1 + state.talkAmp * 0.85;

  // Subtle arm breathing motion
  for (const a of armGroups) {
    a.group.rotation.z = a.side * (0.04 + breath * 0.018);
  }

  // Pulse emissive red glow
  plasmaMat.emissiveIntensity = 3.1 + Math.sin(t * 3.4) * 0.45 + state.talkAmp * 1.1;

  // Smooth camera transition between full-body Stand Mode & close-up Sit Mode
  const standCamZ = 4.55 / state.zoom;
  const sitCamZ = 1.68 / state.zoom;
  const desiredZ = standCamZ + (sitCamZ - standCamZ) * state.sitBlend;
  const desiredY = -0.08 + (1.02 - (-0.08)) * state.sitBlend;

  camera.position.z += (desiredZ - camera.position.z) * 0.08;
  camera.position.y += (desiredY - camera.position.y) * 0.08;
  controls.target.y += (desiredY - controls.target.y) * 0.08;

  controls.update();
  composer.render();
}
animate();

window.addEventListener('resize', () => {
  const w = mount.clientWidth, h = mount.clientHeight;
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
  renderer.setSize(w, h);
  composer.setSize(w, h);
});

// ---------------- VOICE & UI CONTROLS ----------------
function say(text, lang = 'en-IN') {
  reply.textContent = text;
  if (!('speechSynthesis' in window)) { voiceStatus.textContent = 'VOICE UNAVAILABLE'; return; }
  speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.lang = lang; u.rate = 0.9; u.pitch = 0.65; u.volume = 1;
  const voices = speechSynthesis.getVoices();
  const match = voices.find(v => lang.startsWith('hi') ? v.lang.toLowerCase().includes('hi') : v.lang.toLowerCase().includes('en'));
  if (match) u.voice = match;
  u.onstart = () => { voiceStatus.textContent = 'SPEAKING'; state.speaking = true; };
  u.onend = () => { voiceStatus.textContent = 'STANDBY'; state.speaking = false; };
  u.onerror = () => { voiceStatus.textContent = 'STANDBY'; state.speaking = false; };
  speechSynthesis.speak(u);
}

function sit() {
  state.sitMode = true;
  sitBtn.classList.add('active');
  standBtn.classList.remove('active');
  say('Sitting mode engaged. I am watching, Shivam Sir.');
}

function stand() {
  state.sitMode = false;
  standBtn.classList.add('active');
  sitBtn.classList.remove('active');
  say('Standing by, Shivam Sir.');
}

sitBtn.onclick = sit;
standBtn.onclick = stand;

document.getElementById('zoom').oninput = e => {
  const z = Number(e.target.value);
  state.targetZoom = z;
  document.getElementById('zoomVal').textContent = Math.round(z * 100) + '%';
};

document.getElementById('resetBtn').onclick = () => {
  document.getElementById('zoom').value = 1;
  state.targetZoom = 1;
  document.getElementById('zoomVal').textContent = '100%';
  camera.position.set(0, -0.08, 4.55);
  controls.target.set(0, -0.08, 0);
  stand();
};

function processCommand(text) {
  const t = text.toLowerCase().trim();
  if (/\b(hello|hi|hey)\b/.test(t) || t.includes('नमस्ते') || t.includes('हेलो')) { say('Hello Shivam Sir. I am Ultron.'); return; }
  if (t.includes('sit') || t.includes('बैठ')) { sit(); return; }
  if (t.includes('stand') || t.includes('खड़े') || t.includes('खड़ा')) { stand(); return; }
  if (t.includes('zoom in')) { const el = document.getElementById('zoom'); el.value = Math.min(1.65, Number(el.value) + 0.15); el.dispatchEvent(new Event('input')); say('Zooming in.'); return; }
  if (t.includes('zoom out')) { const el = document.getElementById('zoom'); el.value = Math.max(0.65, Number(el.value) - 0.15); el.dispatchEvent(new Event('input')); say('Zooming out.'); return; }
  say('Command received, Shivam Sir. My full command system will be added in the next phase.');
}

let recognition;
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
if (SpeechRecognition) {
  recognition = new SpeechRecognition();
  recognition.continuous = false; recognition.interimResults = false; recognition.lang = 'en-IN';
  recognition.onstart = () => { micStatus.textContent = 'LISTENING'; voiceStatus.textContent = 'VOICE LINK ACTIVE'; };
  recognition.onend = () => { micStatus.textContent = 'READY'; };
  recognition.onerror = () => { micStatus.textContent = 'MIC ERROR'; reply.textContent = 'Microphone unavailable. Check browser permission.'; };
  recognition.onresult = e => { const spoken = e.results[0][0].transcript; reply.textContent = 'You: ' + spoken; processCommand(spoken); };
} else { micStatus.textContent = 'USE CHROME'; }

document.getElementById('micBtn').onclick = () => {
  if (!recognition) { reply.textContent = 'Voice recognition is not supported in this browser. Try Chrome.'; return; }
  try { recognition.lang = 'en-IN'; recognition.start(); } catch (e) { micStatus.textContent = 'WAIT'; }
};

window.addEventListener('keydown', e => { if (e.key === 'Escape') document.getElementById('resetBtn').click(); });
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
