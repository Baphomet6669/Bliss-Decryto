import os
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

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
.robot-wrap{position:relative;width:min(62vw,510px);height:min(76vh,700px);min-height:410px;display:flex;align-items:center;justify-content:center;transform:scale(var(--zoom,1));transform-origin:center 58%;transition:transform .35s ease,opacity .35s}
.robot{height:100%;width:100%;filter:drop-shadow(0 0 24px rgba(255,28,45,.23))}
.robot .metal{fill:url(#steel);stroke:#7e8793;stroke-width:2}
.robot .dark{fill:#10151d;stroke:#68717d;stroke-width:2}
.robot .red{fill:#ff1e36;filter:url(#glow)}
.robot .line{fill:none;stroke:#aeb7c2;stroke-width:3;opacity:.7}
.robot .joint{fill:#080b10;stroke:#929ca8;stroke-width:3}
.robot .eye{fill:#ff2638;filter:url(#glow)}
.robot .chest{fill:#111820;stroke:#87919e;stroke-width:3}
.robot .core{fill:#ff2439;filter:url(#glow)}
.sit-face{position:absolute;width:min(88vw,820px);height:auto;opacity:0;transform:scale(.72);transition:all .45s ease;filter:drop-shadow(0 0 35px rgba(255,20,42,.45));pointer-events:none}
.sit-face.active{opacity:1;transform:scale(1)}
.robot-wrap.hidden{opacity:0;transform:scale(.3)}
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
   <svg class="robot" viewBox="0 0 420 700" role="img" aria-label="Original futuristic armored robot">
    <defs>
     <linearGradient id="steel" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#f0f2f3"/><stop offset=".22" stop-color="#737d89"/><stop offset=".48" stop-color="#252d38"/><stop offset=".72" stop-color="#aeb7c1"/><stop offset="1" stop-color="#333b47"/></linearGradient>
     <filter id="glow"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    </defs>
    <!-- head -->
    <path class="metal" d="M143 34 L174 10 246 10 277 34 292 91 276 151 245 177 175 177 144 151 128 91Z"/>
    <path class="dark" d="M157 47 L183 28 237 28 263 47 271 91 252 130 228 151 192 151 168 130 149 91Z"/>
    <path class="metal" d="M169 52 L190 38 230 38 251 52 259 88 241 111 210 123 179 111 161 88Z"/>
    <path class="dark" d="M166 78 L197 67 210 75 223 67 254 78 243 100 218 110 202 110 177 100Z"/>
    <path class="eye" d="M169 82 L197 76 203 86 178 94Z M251 82 L223 76 217 86 242 94Z"/>
    <path class="dark" d="M195 115 L210 105 225 115 221 136 210 143 199 136Z"/>
    <path class="line" d="M143 93 L119 111 130 144 157 161 M277 93 L301 111 290 144 263 161"/>
    <path class="metal" d="M174 160 L246 160 263 203 244 239 176 239 157 203Z"/>
    <path class="dark" d="M181 174 L239 174 249 203 231 224 189 224 171 203Z"/>
    <!-- shoulders and torso -->
    <path class="metal" d="M158 205 L105 221 72 265 90 318 144 309 169 270Z M262 205 L315 221 348 265 330 318 276 309 251 270Z"/>
    <path class="dark" d="M105 244 L145 228 163 266 143 295 99 298 86 270Z M315 244 L275 228 257 266 277 295 321 298 334 270Z"/>
    <path class="chest" d="M160 226 L260 226 287 300 267 412 244 449 176 449 153 412 133 300Z"/>
    <path class="metal" d="M178 241 L242 241 266 296 251 363 210 392 169 363 154 296Z"/>
    <path class="dark" d="M184 255 L236 255 252 301 239 350 210 372 181 350 168 301Z"/>
    <path class="core" d="M210 278 L232 307 210 337 188 307Z"/>
    <path class="line" d="M147 319 L177 386 210 404 243 386 273 319 M160 409 L210 430 260 409"/>
    <!-- arms -->
    <path class="metal" d="M78 286 L48 311 34 389 52 428 83 413 100 339Z M342 286 L372 311 386 389 368 428 337 413 320 339Z"/>
    <path class="dark" d="M48 327 L70 317 84 354 70 399 51 407 43 384Z M372 327 L350 317 336 354 350 399 369 407 377 384Z"/>
    <path class="joint" d="M46 417 L84 411 96 445 75 470 42 456Z M374 417 L336 411 324 445 345 470 378 456Z"/>
    <path class="metal" d="M42 464 L76 468 87 530 68 562 37 546 25 501Z M378 464 L344 468 333 530 352 562 383 546 395 501Z"/>
    <path class="dark" d="M39 488 L70 493 75 529 55 544 35 530Z M381 488 L350 493 345 529 365 544 385 530Z"/>
    <!-- hips and legs -->
    <path class="metal" d="M163 430 L257 430 275 488 245 523 175 523 145 488Z"/>
    <path class="dark" d="M180 451 L240 451 251 486 230 505 190 505 169 486Z"/>
    <path class="metal" d="M166 505 L205 514 198 596 179 637 142 625 145 561Z M254 505 L215 514 222 596 241 637 278 625 275 561Z"/>
    <path class="dark" d="M157 535 L193 541 187 591 168 615 148 604Z M263 535 L227 541 233 591 252 615 272 604Z"/>
    <path class="metal" d="M143 622 L180 632 193 674 178 690 111 690 103 675 119 642Z M277 622 L240 632 227 674 242 690 309 690 317 675 301 642Z"/>
    <path class="line" d="M128 660 L179 665 M292 660 L241 665"/>
    <path class="red" d="M210 14 L210 25 M110 266 L124 276 M310 266 L296 276"/>
   </svg>
  </div>
  <svg class="sit-face" id="sitFace" viewBox="0 0 900 430" aria-label="Ultron face close-up">
   <defs><linearGradient id="faceSteel" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#f2f4f6"/><stop offset=".3" stop-color="#626e7a"/><stop offset=".65" stop-color="#202833"/><stop offset="1" stop-color="#b4bdc7"/></linearGradient><filter id="faceGlow"><feGaussianBlur stdDeviation="8" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
   <path fill="url(#faceSteel)" stroke="#aeb8c2" stroke-width="7" d="M105 85 L210 24 450 8 690 24 795 85 850 210 790 330 680 394 450 420 220 394 110 330 50 210Z"/>
   <path fill="#101720" stroke="#87939f" stroke-width="6" d="M170 105 L275 58 450 43 625 58 730 105 775 207 720 300 630 350 450 380 270 350 180 300 125 207Z"/>
   <path fill="url(#faceSteel)" d="M205 116 L320 79 450 69 580 79 695 116 730 205 675 280 580 330 450 355 320 330 225 280 170 205Z"/>
   <path fill="#080d14" d="M205 166 L365 130 420 160 450 145 480 160 535 130 695 166 655 220 520 245 450 230 380 245 245 220Z"/>
   <path fill="#ff243a" filter="url(#faceGlow)" d="M220 174 L365 151 405 176 265 207Z M680 174 L535 151 495 176 635 207Z"/>
   <path fill="#111923" stroke="#aeb8c2" stroke-width="5" d="M405 245 L450 220 495 245 482 310 450 330 418 310Z"/>
   <path fill="none" stroke="#d4dbe2" stroke-width="7" d="M260 285 L360 310 450 320 540 310 640 285"/>
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
