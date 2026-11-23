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
.floor{position:absolute;bottom:0;width:min(900px,95vw);height:150px;background:radial-gradient(ellipse,rgba(255,52,20,.3),transparent 67%);border-radius:50%;transform:rotateX(65deg)}
.robot-wrap{position:relative;width:min(62vw,510px);height:min(76vh,700px);min-height:410px;display:flex;align-items:center;justify-content:center;transform:scale(var(--zoom,1));transform-origin:center 58%;transition:transform .35s ease,opacity .35s;animation:ultronIdle 4.2s ease-in-out infinite}
.robot{height:100%;width:100%;filter:drop-shadow(0 0 28px rgba(255,24,42,.3))}
.robot .metal{fill:url(#steel);stroke:#8a94a0;stroke-width:1.8;stroke-linejoin:round}
.robot .metal-hi{fill:url(#steelHi);stroke:#b6c0ca;stroke-width:1.6;stroke-linejoin:round}
.robot .dark{fill:#0d1218;stroke:#5d6672;stroke-width:1.6;stroke-linejoin:round}
.robot .frame{fill:#181f29;stroke:#48505b;stroke-width:1.5;stroke-linejoin:round}
.robot .red{fill:#ff1e36;filter:url(#glow)}
.robot .line{fill:none;stroke:#9aa4b0;stroke-width:2;opacity:.75;stroke-linecap:round;stroke-linejoin:round}
.robot .seam{fill:none;stroke:#07090d;stroke-width:2.2;opacity:.85;stroke-linecap:round}
.robot .joint{fill:#070a0f;stroke:#86909c;stroke-width:2.4;stroke-linejoin:round}
.robot .eye{fill:#ff2237;filter:url(#glow);animation:eyePulse 2.8s ease-in-out infinite}
.robot .chest{fill:#0e141c;stroke:#7b8591;stroke-width:2.2;stroke-linejoin:round}
.robot .core{fill:#ff1e36;filter:url(#glow);animation:corePulse 2.8s ease-in-out infinite}
.sit-face{position:absolute;width:min(88vw,820px);height:auto;opacity:0;transform:scale(.72);transition:all .45s ease;filter:drop-shadow(0 0 38px rgba(255,20,42,.48));pointer-events:none}
.sit-face.active{opacity:1;transform:scale(1)}
.robot-wrap.hidden{opacity:0;transform:scale(.3)}
@keyframes ultronIdle{0%,100%{translate:0 0}50%{translate:0 -5px}}
@keyframes eyePulse{0%,100%{opacity:1}50%{opacity:.78}}
@keyframes corePulse{0%,100%{opacity:.95}50%{opacity:.55}}
.caption{position:absolute;bottom:12px;text-align:center;letter-spacing:.28em;font-size:11px;color:#c6c8ce;text-shadow:0 0 12px #f22}
.controls{position:absolute;left:50%;bottom:22px;transform:translateX(-50%);width:min(720px,94vw);display:flex;align-items:center;justify-content:center;gap:10px;flex-wrap:wrap;z-index:5}
button{border:1px solid #76303a;background:rgba(15,10,15,.88);color:#f5f5f7;padding:12px 17px;letter-spacing:.12em;font-size:10px;font-weight:700;cursor:pointer;transition:.2s}
button:hover,button:focus{border-color:#ff3448;box-shadow:0 0 18px #ff263844;outline:none}
button.primary{background:linear-gradient(135deg,#a50c20,#4d0913);border-color:#ff3348}
button.active{background:#64101c;border-color:#ff3348}
.zoom{display:flex;align-items:center;gap:9px;border:1px solid #59212a;background:#100b10;padding:8px 12px;color:#bbb;font-size:10px}
input[type=range]{width:95px;accent-color:#ff2638}
.console{position:absolute;left:24px;bottom:115px;width:230px;color:#d6a4a8;font:10px/1.8 monospace;letter-spacing:.05em;opacity:.8}
.console strong{color:#ff5261}
.mic-state{position:absolute;right:24px;bottom:115px;text-align:right;font:10px/1.8 monospace;color:#c7c7cc}
.mic-state strong{color:#ff5261}
.chat{position:absolute;top:82px;right:22px;width:min(280px,42vw);padding:13px;background:rgba(5,7,11,.62);border:1px solid #57232c;backdrop-filter:blur(8px);font-size:12px;z-index:4}
.chat small{display:block;color:#ff6876;letter-spacing:.18em;margin-bottom:7px}
#reply{color:#eee;min-height:30px;line-height:1.5}
@media(max-width:650px){.topbar{padding:16px}.stage{inset:70px 0 145px}.robot-wrap{width:95vw;height:65vh;min-height:390px}.chat{top:68px;right:10px;width:155px;font-size:10px}.console{left:12px;bottom:142px;width:150px;font-size:8px}.mic-state{right:12px;bottom:142px;font-size:8px}.controls{bottom:13px;gap:6px}button{padding:11px 12px;font-size:9px}.zoom{padding:7px}.caption{bottom:5px}}
</style>
</head>
<body>
<div class="scene">
 <div class="city"></div><div class="flames"></div><div class="smoke"></div>
 <header class="topbar"><div class="brand">ULTRON<span>.</span>AI</div><div class="status"><i></i> SYSTEM ONLINE</div></header>
 <div class="chat"><small>ULTRON // RESPONSE</small><div id="reply">Awaiting your command, Shivam Sir.</div></div>
 <main class="stage">
  <div class="floor"></div>
  <div class="robot-wrap" id="robotWrap">
   <svg class="robot" viewBox="0 0 420 700" role="img" aria-label="Ultron armored prime">
    <defs>
     <linearGradient id="steel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#e5eaef"/>
      <stop offset="20%" stop-color="#7a8490"/>
      <stop offset="46%" stop-color="#222a35"/>
      <stop offset="74%" stop-color="#9aa4b0"/>
      <stop offset="100%" stop-color="#2b333f"/>
     </linearGradient>
     <linearGradient id="steelHi" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#f5f7f9"/>
      <stop offset="35%" stop-color="#8b95a2"/>
      <stop offset="75%" stop-color="#343d4a"/>
      <stop offset="100%" stop-color="#192029"/>
     </linearGradient>
     <filter id="glow"><feGaussianBlur stdDeviation="4.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    </defs>

    <!-- Rear/inner neck & spine support -->
    <path class="frame" d="M182 158 L238 158 L248 228 L172 228 Z"/>
    <path class="seam" d="M192 172 L228 172 M190 186 L230 186 M188 200 L232 200 M186 214 L234 214"/>

    <!-- Ultron Head: sculpted crown, brow ridge, cheeks, jaw -->
    <path class="metal" d="M148 38 L175 13 L210 8 L245 13 L272 38 L289 88 L275 144 L244 172 L176 172 L145 144 L131 88 Z"/>
    <!-- Crown & brow armor plate -->
    <path class="metal-hi" d="M168 24 L210 15 L252 24 L268 58 L244 73 L210 64 L176 73 L152 58 Z"/>
    <path class="seam" d="M210 15 L210 64 M176 73 L163 92 M244 73 L257 92"/>
    <!-- Cheekbone plates -->
    <path class="metal" d="M146 74 L174 84 L182 122 L162 146 L142 122 Z"/>
    <path class="metal" d="M274 74 L246 84 L238 122 L258 146 L278 122 Z"/>
    <!-- Dark face cavity & fierce Ultron eyes -->
    <path class="dark" d="M164 76 L196 68 L210 77 L224 68 L256 76 L246 106 L222 115 L198 115 L174 106 Z"/>
    <path class="eye" d="M170 82 L199 77 L203 87 L177 95 Z"/>
    <path class="eye" d="M250 82 L221 77 L217 87 L243 95 Z"/>
    <!-- Nose bridge & grimacing mouth plate -->
    <path class="metal-hi" d="M204 76 L216 76 L219 108 L210 114 L201 108 Z"/>
    <path class="dark" d="M186 118 L234 118 L228 152 L210 163 L192 152 Z"/>
    <path class="metal" d="M192 122 L228 122 L224 148 L210 157 L196 148 Z"/>
    <path class="seam" d="M197 130 L223 130 M198 137 L222 137 M200 144 L220 144 M210 122 L210 156"/>
    <!-- Ear / temple audio ports -->
    <path class="dark" d="M132 82 L145 86 L146 122 L133 118 Z"/>
    <path class="dark" d="M288 82 L275 86 L274 122 L287 118 Z"/>
    <path class="red" d="M136 96 L141 98 L141 108 L136 106 Z"/>
    <path class="red" d="M284 96 L279 98 L279 108 L284 106 Z"/>

    <!-- Neck armor & collar -->
    <path class="metal" d="M172 166 L248 166 L262 204 L242 232 L178 232 L158 204 Z"/>
    <path class="dark" d="M183 175 L237 175 L246 202 L230 220 L190 220 L174 202 Z"/>
    <path class="line" d="M186 186 L234 186 M188 198 L232 198"/>

    <!-- Broad layered shoulders (pauldrons) -->
    <path class="metal-hi" d="M160 206 L104 218 L68 258 L84 312 L138 306 L168 268 Z"/>
    <path class="metal" d="M98 225 L142 216 L158 255 L134 294 L86 298 L74 262 Z"/>
    <path class="dark" d="M84 246 L124 238 L134 268 L112 288 L82 286 Z"/>
    <path class="seam" d="M104 224 L86 298 M124 220 L108 295"/>

    <path class="metal-hi" d="M260 206 L316 218 L352 258 L336 312 L282 306 L252 268 Z"/>
    <path class="metal" d="M322 225 L278 216 L262 255 L286 294 L334 298 L346 262 Z"/>
    <path class="dark" d="M336 246 L296 238 L286 268 L308 288 L338 286 Z"/>
    <path class="seam" d="M316 224 L334 298 M296 220 L312 295"/>

    <!-- Sculpted Torso, Pectorals, Ribbed Abdomen & Reactor Slit -->
    <path class="chest" d="M158 224 L262 224 L288 298 L266 414 L242 450 L178 450 L154 414 L132 298 Z"/>
    <!-- Left & Right Pectoral Plates -->
    <path class="metal-hi" d="M164 234 L206 238 L206 296 L154 302 L148 266 Z"/>
    <path class="metal-hi" d="M256 234 L214 238 L214 296 L266 302 L272 266 Z"/>
    <!-- Central sternum & red energy core -->
    <path class="dark" d="M196 244 L224 244 L228 336 L210 352 L192 336 Z"/>
    <path class="core" d="M206 274 L214 274 L216 322 L204 322 Z"/>
    <!-- Segmented abdominal / rib plates -->
    <path class="metal" d="M164 316 L198 322 L202 340 L168 336 Z"/>
    <path class="metal" d="M256 316 L222 322 L218 340 L252 336 Z"/>
    <path class="metal" d="M168 344 L202 348 L205 366 L172 362 Z"/>
    <path class="metal" d="M252 344 L218 348 L215 366 L248 362 Z"/>
    <path class="metal" d="M173 370 L205 374 L208 392 L177 388 Z"/>
    <path class="metal" d="M247 370 L215 374 L212 392 L243 388 Z"/>
    <path class="dark" d="M176 396 L244 396 L236 438 L184 438 Z"/>
    <path class="line" d="M184 408 L236 408 M188 422 L232 422"/>

    <!-- Upper Arms, Elbow Joints, Forearms & Articulated Claws -->
    <path class="metal" d="M78 286 L46 310 L33 388 L50 426 L82 412 L99 338 Z"/>
    <path class="dark" d="M48 325 L70 316 L82 356 L68 398 L50 405 L42 380 Z"/>
    <path class="seam" d="M58 322 L54 402 M72 328 L66 396"/>
    <path class="joint" d="M45 415 L84 410 L96 444 L75 470 L41 455 Z"/>
    <path class="metal-hi" d="M41 463 L76 467 L88 530 L67 564 L35 546 L23 500 Z"/>
    <path class="dark" d="M36 486 L68 490 L74 528 L54 545 L33 529 Z"/>
    <!-- Left mechanical fingers -->
    <path class="metal" d="M38 548 L50 554 L42 582 L31 577 Z"/>
    <path class="metal" d="M52 555 L64 558 L60 587 L48 584 Z"/>
    <path class="metal" d="M66 558 L77 554 L78 581 L67 583 Z"/>

    <path class="metal" d="M342 286 L374 310 L387 388 L370 426 L338 412 L321 338 Z"/>
    <path class="dark" d="M372 325 L350 316 L338 356 L352 398 L370 405 L378 380 Z"/>
    <path class="seam" d="M362 322 L366 402 M348 328 L354 396"/>
    <path class="joint" d="M375 415 L336 410 L324 444 L345 470 L379 455 Z"/>
    <path class="metal-hi" d="M379 463 L344 467 L332 530 L353 564 L385 546 L397 500 Z"/>
    <path class="dark" d="M384 486 L352 490 L346 528 L366 545 L387 529 Z"/>
    <!-- Right mechanical fingers -->
    <path class="metal" d="M382 548 L370 554 L378 582 L389 577 Z"/>
    <path class="metal" d="M368 555 L356 558 L360 587 L372 584 Z"/>
    <path class="metal" d="M354 558 L343 554 L342 581 L353 583 Z"/>

    <!-- Pelvis, Thighs, Knee Guards & Heavy Armored Greaves -->
    <path class="metal" d="M162 430 L258 430 L276 486 L244 522 L176 522 L144 486 Z"/>
    <path class="dark" d="M180 448 L240 448 L252 484 L230 506 L190 506 L168 484 Z"/>
    <path class="metal-hi" d="M198 442 L222 442 L226 492 L210 502 L194 492 Z"/>

    <!-- Left leg -->
    <path class="metal" d="M165 504 L205 513 L198 594 L179 636 L141 624 L144 560 Z"/>
    <path class="dark" d="M156 532 L192 538 L186 588 L167 612 L147 602 Z"/>
    <path class="metal-hi" d="M152 586 L186 592 L182 624 L148 618 Z"/>
    <path class="metal" d="M142 622 L180 632 L194 674 L178 691 L109 691 L101 675 L118 642 Z"/>
    <path class="line" d="M124 656 L178 662 M118 672 L182 676"/>

    <!-- Right leg -->
    <path class="metal" d="M255 504 L215 513 L222 594 L241 636 L279 624 L276 560 Z"/>
    <path class="dark" d="M264 532 L228 538 L234 588 L253 612 L273 602 Z"/>
    <path class="metal-hi" d="M268 586 L234 592 L238 624 L272 618 Z"/>
    <path class="metal" d="M278 622 L240 632 L226 674 L242 691 L311 691 L319 675 L302 642 Z"/>
    <path class="line" d="M296 656 L242 662 M302 672 L238 676"/>

    <!-- Subtle red indicator accents -->
    <path class="red" d="M208 12 L212 12 L211 23 L209 23 Z M106 264 L118 272 L115 277 L103 269 Z M314 264 L302 272 L305 277 L317 269 Z"/>
   </svg>
  </div>

  <svg class="sit-face" id="sitFace" viewBox="0 0 900 430" aria-label="Ultron face close-up">
   <defs>
    <linearGradient id="faceSteel" x1="0" y1="0" x2="1" y2="1">
     <stop offset="0%" stop-color="#f2f4f7"/>
     <stop offset="26%" stop-color="#6e7986"/>
     <stop offset="58%" stop-color="#1d242f"/>
     <stop offset="82%" stop-color="#9aa4b0"/>
     <stop offset="100%" stop-color="#262f3b"/>
    </linearGradient>
    <linearGradient id="faceCrown" x1="0" y1="0" x2="0" y2="1">
     <stop offset="0%" stop-color="#ffffff"/>
     <stop offset="40%" stop-color="#8993a0"/>
     <stop offset="100%" stop-color="#222a35"/>
    </linearGradient>
    <filter id="faceGlow"><feGaussianBlur stdDeviation="8" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
   </defs>
   <!-- Outer armored skull & jaw -->
   <path fill="url(#faceSteel)" stroke="#b4bec8" stroke-width="6.5" stroke-linejoin="round" d="M105 85 L210 24 L450 8 L690 24 L795 85 L850 210 L790 330 L680 394 L450 420 L220 394 L110 330 L50 210 Z"/>
   <!-- Sculpted upper crown & brow ridges -->
   <path fill="url(#faceCrown)" stroke="#c7d0d9" stroke-width="4" stroke-linejoin="round" d="M235 42 L450 22 L665 42 L725 112 L645 142 L535 122 L450 148 L365 122 L255 142 L175 112 Z"/>
   <path fill="none" stroke="#080c12" stroke-width="5" d="M450 22 L450 148 M365 122 L320 158 M535 122 L580 158"/>
   <!-- Dark inner face recess -->
   <path fill="#090e15" stroke="#5d6774" stroke-width="4" stroke-linejoin="round" d="M178 126 L362 128 L420 158 L450 142 L480 158 L538 128 L722 126 L755 215 L685 315 L560 362 L450 385 L340 362 L215 315 L145 215 Z"/>
   <!-- Cheekbone armor -->
   <path fill="url(#faceSteel)" stroke="#9aa4b0" stroke-width="4.5" stroke-linejoin="round" d="M142 138 L225 152 L245 235 L195 292 L128 232 Z"/>
   <path fill="url(#faceSteel)" stroke="#9aa4b0" stroke-width="4.5" stroke-linejoin="round" d="M758 138 L675 152 L655 235 L705 292 L772 232 Z"/>
   <!-- Fierce glowing red eyes -->
   <path fill="#ff2238" filter="url(#faceGlow)" d="M222 172 L368 148 L406 176 L264 210 Z"/>
   <path fill="#ff2238" filter="url(#faceGlow)" d="M678 172 L532 148 L494 176 L636 210 Z"/>
   <!-- Bridge of nose & mouth grille -->
   <path fill="url(#faceCrown)" stroke="#aeb8c2" stroke-width="4.5" stroke-linejoin="round" d="M426 154 L474 154 L482 224 L450 242 L418 224 Z"/>
   <path fill="#111822" stroke="#aeb8c2" stroke-width="5" stroke-linejoin="round" d="M368 248 L532 248 L516 332 L450 366 L384 332 Z"/>
   <path fill="none" stroke="#cfd6de" stroke-width="6" stroke-linecap="round" d="M382 268 L518 268 M386 289 L514 289 M392 310 L508 310 M404 330 L496 330"/>
   <path fill="none" stroke="#080c12" stroke-width="4.5" d="M450 248 L450 364"/>
  </svg>

  <div class="caption">ARTIFICIAL INTELLIGENCE // SUPERIOR MACHINE INTELLIGENCE</div>
 </main>
 <div class="console">CORE STATUS: <strong>STABLE</strong><br>THREAT LEVEL: <strong>MAXIMUM</strong><br>LANGUAGE: <strong>EN / HI</strong></div>
 <div class="mic-state">VOICE LINK: <strong id="voiceStatus">STANDBY</strong><br>MIC: <strong id="micStatus">READY</strong></div>
 <nav class="controls">
  <button class="primary" id="micBtn">🎙 SPEAK</button>
  <button id="sitBtn">SIT MODE</button>
  <button id="standBtn">STAND</button>
  <div class="zoom">ZOOM <input id="zoom" type="range" min=".65" max="1.65" step=".05" value="1"><span id="zoomVal">100%</span></div>
  <button id="resetBtn">RESET VIEW</button>
 </nav>
</div>
<script>
const reply=document.getElementById('reply'), robot=document.getElementById('robotWrap'), face=document.getElementById('sitFace');
const voiceStatus=document.getElementById('voiceStatus'), micStatus=document.getElementById('micStatus');
function say(text,lang='en-IN'){
 reply.textContent=text;
 if(!('speechSynthesis' in window)){voiceStatus.textContent='VOICE UNAVAILABLE';return}
 speechSynthesis.cancel();
 const u=new SpeechSynthesisUtterance(text);u.lang=lang;u.rate=.92;u.pitch=.72;u.volume=1;
 const voices=speechSynthesis.getVoices();
 const match=voices.find(v=>lang.startsWith('hi')?v.lang.toLowerCase().includes('hi'):v.lang.toLowerCase().includes('en'));
 if(match)u.voice=match;
 u.onstart=()=>voiceStatus.textContent='SPEAKING';u.onend=()=>voiceStatus.textContent='STANDBY';
 speechSynthesis.speak(u);
}
function sit(){robot.classList.add('hidden');face.classList.add('active');reply.textContent='Sitting mode engaged. I am watching, Shivam Sir.';say('Sitting mode engaged. I am watching, Shivam Sir.');}
function stand(){face.classList.remove('active');robot.classList.remove('hidden');say('Standing by, Shivam Sir.');}
document.getElementById('sitBtn').onclick=sit;document.getElementById('standBtn').onclick=stand;
document.getElementById('zoom').oninput=e=>{const z=Number(e.target.value);robot.style.setProperty('--zoom',z);face.style.width=(Math.min(88*z,100))+'vw';document.getElementById('zoomVal').textContent=Math.round(z*100)+'%';};
document.getElementById('resetBtn').onclick=()=>{document.getElementById('zoom').value=1;robot.style.setProperty('--zoom',1);face.style.width='min(88vw,820px)';document.getElementById('zoomVal').textContent='100%';stand();};
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
