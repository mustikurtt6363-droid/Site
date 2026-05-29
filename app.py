from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>Neon Race</title>

<style>

body{
margin:0;
overflow:hidden;
background:#071014;
font-family:Arial;
touch-action:none;
width:100vw;
height:100vh;
}

/* LOGIN */

#login{
position:absolute;
inset:0;
display:flex;
justify-content:center;
align-items:center;
flex-direction:column;
background:#0b1220;
z-index:200;
}

#nameInput{
padding:15px;
font-size:20px;
border:none;
border-radius:10px;
outline:none;
text-align:center;
width:220px;
}

.loginBtn{
margin-top:15px;
padding:14px 30px;
border:none;
border-radius:12px;
background:#00aaff;
color:white;
font-size:20px;
}

/* ROAD */

#road{
position:absolute;
left:50%;
transform:translateX(-50%);
width:min(92vw,430px);
height:100%;
background:#1d1d1d;
border-left:3px solid #00d5ff;
border-right:3px solid #00d5ff;
display:none;
}

/* LINE */

#line{
position:absolute;
left:50%;
transform:translateX(-50%);
width:6px;
height:100%;
background:
repeating-linear-gradient(
to bottom,
white 0px,
white 35px,
transparent 35px,
transparent 70px
);
display:none;
opacity:0.7;
}

/* UI */

#ui{
position:absolute;
top:10px;
left:10px;
color:white;
font-size:18px;
z-index:50;
display:none;
line-height:32px;
}

/* PLAYER */

#playerName{
position:absolute;
top:10px;
right:10px;
color:white;
font-size:18px;
z-index:50;
display:none;
}

/* CAR */

#car{
position:absolute;
bottom:120px;
width:60px;
height:88px;
border-radius:14px;
display:none;

background:
linear-gradient(
to bottom,
#ff00aa,
#ff66cc
);

box-shadow:0 0 20px #ff00aa;

transition:
transform 0.15s,
rotate 0.15s;
}

#car::before{
content:'';
position:absolute;
left:10px;
top:12px;
width:40px;
height:18px;
background:#87cefa;
border-radius:6px;
}

#car::after{
content:'';
position:absolute;
left:18px;
bottom:10px;
width:25px;
height:8px;
background:#222;
border-radius:4px;
}

/* ENEMY */

.enemy{
position:absolute;
width:30px;
height:50px;
border-radius:10px;

background:
linear-gradient(
to bottom,
#00aaff,
#66ddff
);
}

/* COIN */

.coin{
position:absolute;
width:24px;
height:24px;
border-radius:50%;
background:gold;
box-shadow:0 0 15px gold;
}

/* CONTROLS */

#controls{
position:fixed;
bottom:20px;
left:0;
width:100%;
display:none;
justify-content:space-between;
align-items:flex-end;
padding:0 18px;
box-sizing:border-box;
z-index:100;
pointer-events:none;
}

.leftArea{
display:flex;
flex-direction:column;
align-items:center;
gap:8px;
pointer-events:auto;
}

.btn{
width:82px;
height:82px;
border:none;
border-radius:50%;
background:rgba(255,255,255,0.15);
font-size:34px;
color:white;
pointer-events:auto;
}

#jump{
width:58px;
height:58px;
font-size:26px;
}

/* GAME OVER */

#gameOver{
position:absolute;
inset:0;
display:none;
justify-content:center;
align-items:center;
flex-direction:column;
background:rgba(0,0,0,0.85);
z-index:300;
color:white;
}

</style>
</head>

<body>

<!-- LOGIN -->

<div id="login">

<h1 style="color:white">
KULLANICI ADI
</h1>

<input id="nameInput"
placeholder="Gir...">

<button class="loginBtn"
onclick="login()">
GİRİŞ
</button>

</div>

<!-- UI -->

<div id="ui">

❤️ CAN:
<span id="hp">5</span>

<br>

🏆 SKOR:
<span id="score">0</span>

<br>

🪙 COIN:
<span id="coin">0</span>

</div>

<div id="playerName"></div>

<div id="road"></div>
<div id="line"></div>

<div id="car"></div>

<!-- CONTROLS -->

<div id="controls">

<div class="leftArea">

<button class="btn"
id="jump">
⬆
</button>

<button class="btn"
id="left">
◀
</button>

</div>

<button class="btn"
id="right">
▶
</button>

</div>

<!-- GAME OVER -->

<div id="gameOver">

<h1>GAME OVER</h1>

<h2>
TOPLAM COİN:
<span id="finalCoin">0</span>
</h2>

<h2>
SKOR:
<span id="finalScore">0</span>
</h2>

<h2>
SKOR REKOR:
<span id="highScoreText">0</span>
</h2>

<button class="loginBtn"
onclick="restartGame()">
TEKRAR OYNA
</button>

<button class="loginBtn"
onclick="start1v1()">
1V1 OYNA
</button>

</div>

<script>

/* SOUND */

function playSound(freq,duration){

let audio =
new(window.AudioContext||
window.webkitAudioContext)();

let osc =
audio.createOscillator();

let gain =
audio.createGain();

osc.connect(gain);
gain.connect(audio.destination);

osc.frequency.value=freq;
osc.type="square";

osc.start();

gain.gain.setValueAtTime(
0.1,
audio.currentTime
);

gain.gain.exponentialRampToValueAtTime(
0.0001,
audio.currentTime+duration
);

osc.stop(audio.currentTime+duration);

}

/* LOGIN */

function login(){

let name =
document.getElementById("nameInput").value;

if(name.trim()==""){
return;
}

document.getElementById("playerName")
.innerText=name;

document.getElementById("playerName")
.style.display="block";

document.getElementById("login")
.style.display="none";

startGame();

}

/* VARIABLES */

let car =
document.getElementById("car");

let x =
window.innerWidth/2;

let left=false;
let right=false;

let hp=5;
let coin=0;

let score=0;
let highScore=0;

let dead=false;

let jumping=false;
let jumpY=0;

let lastLeftTap=0;
let lastRightTap=0;

/* START */

function startGame(){

dead=false;

hp=5;
coin=0;
score=0;

document.getElementById("hp")
.innerText=hp;

document.getElementById("coin")
.innerText=coin;

document.getElementById("score")
.innerText=score;

document.getElementById("road")
.style.display="block";

document.getElementById("line")
.style.display="block";

document.getElementById("car")
.style.display="block";

document.getElementById("controls")
.style.display="flex";

document.getElementById("ui")
.style.display="block";

document.getElementById("gameOver")
.style.display="none";

car.style.left=x+"px";

}

/* RESTART */

function restartGame(){

document.getElementById("gameOver")
.style.display="none";

startGame();

}

/* 1V1 */

function start1v1(){

startGame();

spawnBot();

}

/* BUTTONS */

const leftBtn =
document.getElementById("left");

const rightBtn =
document.getElementById("right");

const jumpBtn =
document.getElementById("jump");

/* LEFT */

leftBtn.addEventListener(
"touchstart",
e=>{

e.preventDefault();

playSound(220,0.08);

left=true;

let now=Date.now();

if(now-lastLeftTap<250){

playSound(120,0.2);

car.style.transform=
"rotate(-25deg)";

setTimeout(()=>{
car.style.transform=
"rotate(0deg)";
},300);

x-=50;

}

lastLeftTap=now;

},
{passive:false}
);

leftBtn.addEventListener(
"touchend",
e=>{
e.preventDefault();
left=false;
},
{passive:false}
);

/* RIGHT */

rightBtn.addEventListener(
"touchstart",
e=>{

e.preventDefault();

playSound(220,0.08);

right=true;

let now=Date.now();

if(now-lastRightTap<250){

playSound(120,0.2);

car.style.transform=
"rotate(25deg)";

setTimeout(()=>{
car.style.transform=
"rotate(0deg)";
},300);

x+=50;

}

lastRightTap=now;

},
{passive:false}
);

rightBtn.addEventListener(
"touchend",
e=>{
e.preventDefault();
right=false;
},
{passive:false}
);

/* JUMP */

jumpBtn.addEventListener(
"touchstart",
e=>{

e.preventDefault();

playSound(700,0.15);

if(!jumping){

jumping=true;

jump();

}

},
{passive:false}
);

function jump(){

let up=true;

let t=setInterval(()=>{

if(up){

jumpY+=16;

if(jumpY>=190){
up=false;
}

}else{

jumpY-=16;

if(jumpY<=0){

jumpY=0;

jumping=false;

clearInterval(t);

}

}

car.style.transform=
"translateY(-"+jumpY+"px)";

},16);

}

/* MOVE */

function loop(){

if(!dead){

if(left) x-=7;
if(right) x+=7;

if(x<window.innerWidth/2-205)
x=window.innerWidth/2-205;

if(x>window.innerWidth/2+150)
x=window.innerWidth/2+150;

car.style.left=x+"px";

}

requestAnimationFrame(loop);

}

loop();

/* SCORE */

setInterval(()=>{

if(!dead){

score++;

document.getElementById("score")
.innerText=score;

}

},500);

/* EXPLOSION */

function explosion(x,y){

playSound(80,0.4);

let ex =
document.createElement("div");

ex.style.position="absolute";
ex.style.left=x+"px";
ex.style.top=y+"px";

ex.style.width="15px";
ex.style.height="15px";

ex.style.borderRadius="50%";

ex.style.background="orange";

ex.style.boxShadow=
"0 0 25px orange";

document.body.appendChild(ex);

let s=1;

let t=setInterval(()=>{

s+=0.5;

ex.style.transform=
"scale("+s+")";

ex.style.opacity=
1-(s/6);

if(s>6){

clearInterval(t);

ex.remove();

}

},16);

}

/* ENEMY */

function spawnEnemy(){

if(dead)return;

let e =
document.createElement("div");

e.className="enemy";

e.style.left=
(window.innerWidth/2-205+
Math.random()*350)+"px";

document.body.appendChild(e);

let y=-120;

let t=setInterval(()=>{

if(dead){

e.remove();
clearInterval(t);

return;

}

y+=5;

e.style.top=y+"px";

let a =
car.getBoundingClientRect();

let b =
e.getBoundingClientRect();

if(
!jumping &&
!(a.right<b.left||
a.left>b.right||
a.bottom<b.top||
a.top>b.bottom)
){

hp--;

document.getElementById("hp")
.innerText=hp;

explosion(a.left,a.top);

e.remove();

clearInterval(t);

if(hp<=0){

dead=true;

if(score>highScore){
highScore=score;
}

document.getElementById("finalCoin")
.innerText=coin;

document.getElementById("finalScore")
.innerText=score;

document.getElementById("highScoreText")
.innerText=highScore;

document.getElementById("gameOver")
.style.display="flex";

}

}

if(y>window.innerHeight){

e.remove();

clearInterval(t);

}

},16);

}

setInterval(spawnEnemy,1000);

/* COIN */

function spawnCoin(){

if(dead)return;

let c =
document.createElement("div");

c.className="coin";

c.style.left=
(window.innerWidth/2-205+
Math.random()*350)+"px";

document.body.appendChild(c);

let y=-50;

let t=setInterval(()=>{

if(dead){

c.remove();

clearInterval(t);

return;

}

y+=4;

c.style.top=y+"px";

let a =
car.getBoundingClientRect();

let b =
c.getBoundingClientRect();

if(!(a.right<b.left||
a.left>b.right||
a.bottom<b.top||
a.top>b.bottom)){

coin++;

playSound(900,0.08);

document.getElementById("coin")
.innerText=coin;

c.remove();

clearInterval(t);

}

if(y>window.innerHeight){

c.remove();

clearInterval(t);

}

},16);

}

setInterval(spawnCoin,1400);

/* BOT */

function spawnBot(){

let bot =
document.createElement("div");

bot.className="enemy";

bot.style.left=
(window.innerWidth/2+80)+"px";

bot.style.top=
(window.innerHeight-240)+"px";

document.body.appendChild(bot);

let by=
window.innerHeight-240;

let bx=
window.innerWidth/2+80;

setInterval(()=>{

if(dead){

bot.remove();

return;

}

by-=0.7;

bx+=(Math.random()-0.5)*0.3;

if(bx<window.innerWidth/2-205)
bx=window.innerWidth/2-205;

if(bx>window.innerWidth/2+150)
bx=window.innerWidth/2+150;

bot.style.top=by+"px";
bot.style.left=bx+"px";

},35);

}

</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    port = int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0", port=port)
