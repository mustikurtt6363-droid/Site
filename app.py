from flask import Flask, render_template_string
import os

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">

<title>Neon Car Game</title>

<style>

html,body{
margin:0;
padding:0;
width:100%;
height:100%;
overflow:hidden;
font-family:Arial;
position:fixed;
touch-action:none;
user-select:none;
background:radial-gradient(circle,#0f172a,#020617);
}

/* LOGIN */

#login{
position:fixed;
inset:0;
display:flex;
justify-content:center;
align-items:center;
background:#08111f;
z-index:100;
}

.loginBox{
width:90%;
max-width:360px;
background:#111827;
padding:25px;
border-radius:20px;
text-align:center;
color:white;
box-shadow:0 0 20px #00ffff;
}

.loginBox input{
width:100%;
padding:12px;
border:none;
border-radius:10px;
margin-top:10px;
background:#1f2937;
color:white;
}

.loginBox button{
width:100%;
padding:12px;
margin-top:10px;
border:none;
border-radius:10px;
background:#00bfff;
color:white;
font-size:18px;
}

/* CALC */

#calc{
position:fixed;
inset:0;
display:none;
justify-content:center;
align-items:center;
background:#050816;
z-index:50;
}

#calcBox{
width:92%;
max-width:380px;
background:#111827;
padding:20px;
border-radius:20px;
box-shadow:0 0 20px #00ffff;
}

#ekran{
width:100%;
padding:15px;
font-size:24px;
text-align:right;
border:none;
border-radius:10px;
background:#1f2937;
color:white;
outline:none;
}

.grid{
display:grid;
grid-template-columns:repeat(4,1fr);
gap:8px;
margin-top:10px;
}

.grid button{
padding:16px;
border:none;
border-radius:10px;
background:#1e293b;
color:white;
font-size:20px;
}

#startBtn{
display:none;
margin-top:10px;
width:100%;
padding:15px;
border:none;
border-radius:12px;
background:#00bfff;
color:white;
font-size:20px;
}

/* GAME */

#game{
display:none;
position:fixed;
inset:0;
background:#020617;
overflow:hidden;
}

/* ROAD */

#road{
position:absolute;
left:50%;
transform:translateX(-50%);
width:170px;
height:100%;
background:linear-gradient(#111,#000);
border-left:2px solid #00ffff;
border-right:2px solid #00ffff;
box-shadow:
0 0 20px #00ffff,
0 0 40px #00ffff inset;
overflow:hidden;
}

/* LANE */

.lane{
position:absolute;
left:50%;
transform:translateX(-50%);
width:5px;
height:70px;
background:#00ffff;
box-shadow:0 0 10px #00ffff;
animation:moveLine 0.5s linear infinite;
opacity:0.7;
}

@keyframes moveLine{
0%{transform:translate(-50%,-120px);}
100%{transform:translate(-50%,120vh);}
}

/* PLAYER CAR */

#car{
position:absolute;
bottom:120px;
left:50%;
width:45px;
height:80px;
background:linear-gradient(#ff00ff,#7e22ce);
border-radius:10px;
box-shadow:
0 0 15px #ff00ff,
0 0 30px #ff00ff;
border:2px solid #ffffff33;
}

/* WINDOW */

#car::before{
content:"";
position:absolute;
top:8px;
left:10px;
width:24px;
height:18px;
background:#87cefa;
border-radius:5px;
}

/* HEADLIGHT */

#car::after{
content:"";
position:absolute;
top:-40px;
left:-12px;
width:70px;
height:120px;
background:radial-gradient(rgba(255,255,180,0.35),transparent);
}

/* ENEMY */

.enemy{
position:absolute;
width:45px;
height:80px;
background:linear-gradient(#00ff99,#008f5a);
border-radius:10px;
box-shadow:
0 0 10px #00ff99,
0 0 20px #00ff99;
}

/* COIN */

.coin{
position:absolute;
width:22px;
height:22px;
border-radius:50%;
background:#ffff00;
box-shadow:
0 0 10px yellow,
0 0 20px gold;
}

/* SCORE */

#score{
position:absolute;
top:10px;
left:10px;
color:#00ffff;
font-size:15px;
text-shadow:0 0 10px #00ffff;
z-index:10;
}

/* CONTROLS */

#controls{
position:absolute;
bottom:15px;
left:0;
width:100%;
display:flex;
justify-content:space-between;
padding:0 30px;
box-sizing:border-box;
z-index:20;
}

.btn{
width:70px;
height:70px;
border:none;
border-radius:50%;
background:rgba(255,255,255,0.15);
backdrop-filter:blur(5px);
color:white;
font-size:30px;
touch-action:none;
}

/* GAME OVER */

#over{
display:none;
position:absolute;
inset:0;
background:rgba(0,0,0,0.7);
justify-content:center;
align-items:center;
z-index:50;
}

.panel{
background:#111827;
padding:25px;
border-radius:20px;
text-align:center;
width:80%;
max-width:320px;
color:white;
box-shadow:0 0 25px #00ffff;
}

.panel h1{
color:#ff4d4d;
text-shadow:0 0 10px red;
}

.panel p{
margin:10px 0;
font-size:18px;
}

.panel button{
width:100%;
padding:14px;
border:none;
border-radius:12px;
background:#00bfff;
color:white;
font-size:18px;
}

</style>
</head>

<body>

<!-- LOGIN -->

<div id="login">
<div class="loginBox">

<h2>NEON LOGIN</h2>

<input id="user" placeholder="Kullanıcı adı">

<button onclick="login()">
Giriş
</button>

</div>
</div>

<!-- CALC -->

<div id="calc">
<div id="calcBox">

<input id="ekran">

<div class="grid">

<button onclick="add('7')">7</button>
<button onclick="add('8')">8</button>
<button onclick="add('9')">9</button>
<button onclick="add('/')">/</button>

<button onclick="add('4')">4</button>
<button onclick="add('5')">5</button>
<button onclick="add('*')">*</button>
<button onclick="add('-')">-</button>

<button onclick="add('1')">1</button>
<button onclick="add('2')">2</button>
<button onclick="add('3')">3</button>
<button onclick="add('+')">+</button>

<button onclick="add('0')">0</button>
<button onclick="check()">OK</button>

<button onclick="clearE()"
style="grid-column:span 2;background:red;">
C
</button>

</div>

<button id="startBtn"
onclick="startGame()">

START GAME

</button>

</div>
</div>

<!-- GAME -->

<div id="game">

<div id="road"></div>

<div id="score">
Skor:0 Coin:0 HS:0
</div>

<div id="car"></div>

<div id="controls">

<button class="btn" id="left">
◀
</button>

<button class="btn" id="right">
▶
</button>

</div>

<div id="over">

<div class="panel">

<h1>GAME OVER</h1>

<p>
YAPILAN SKOR:
<span id="fs"></span>
</p>

<p>
KAZANILAN PARA:
<span id="fc"></span>
</p>

<p>
YÜKSEK SKOR:
<span id="fh"></span>
</p>

<button onclick="restart()">
TEKRAR OYNA
</button>

</div>

</div>

</div>

<!-- AUDIO -->

<audio id="menuMusic" loop>
<source src="https://cdn.pixabay.com/download/audio/2022/02/22/audio_d1718ab41b.mp3?filename=relaxing-vlog-night-street-131746.mp3">
</audio>

<audio id="bgm" loop>
<source src="https://cdn.pixabay.com/download/audio/2022/03/15/audio_c8c8a73467.mp3?filename=cyberpunk-moonlight-sonata-ambient-11113.mp3">
</audio>

<audio id="coinSound">
<source src="https://cdn.pixabay.com/download/audio/2022/03/15/audio_4c999d6cb1.mp3?filename=game-coin-collection-123.wav">
</audio>

<audio id="crashSound">
<source src="https://cdn.pixabay.com/download/audio/2022/03/15/audio_8f4c8f4f11.mp3?filename=impact-crash-1-81462.mp3">
</audio>

<script>

/* MUSIC */

window.onload=()=>{
document.getElementById("menuMusic").play();
}

/* LOGIN */

function login(){

let u=document.getElementById("user").value;

if(u!=="Musti"){
alert("Hatalı kullanıcı");
return;
}

document.getElementById("login").style.display="none";
document.getElementById("calc").style.display="flex";

}

/* CALC */

function add(v){
document.getElementById("ekran").value+=v;
}

function clearE(){
document.getElementById("ekran").value="";
}

function check(){

let v=document.getElementById("ekran").value;

if(v==="2727"){
document.getElementById("startBtn").style.display="block";
return;
}

try{
document.getElementById("ekran").value=eval(v);
}catch{
document.getElementById("ekran").value="ERROR";
}

}

/* GAME */

let calc=document.getElementById("calc");
let game=document.getElementById("game");
let car=document.getElementById("car");
let over=document.getElementById("over");

function startGame(){

document.getElementById("menuMusic").pause();
document.getElementById("bgm").play();

calc.style.display="none";
game.style.display="block";

createLines();

}

/* ROAD LINES */

function createLines(){

for(let i=0;i<10;i++){

let line=document.createElement("div");

line.className="lane";

line.style.top=(i*120)+"px";

document.getElementById("road").appendChild(line);

}

}

/* STATE */

let x=window.innerWidth/2;

let left=false;
let right=false;

let dead=false;

let score=0;
let coins=0;
let speed=6;

let highScore=
localStorage.getItem("hs") || 0;

/* UI */

function updateUI(){

document.getElementById("score").innerText=
"Skor:"+score+
" Coin:"+coins+
" HS:"+highScore;

}

/* SCORE */

setInterval(()=>{

if(game.style.display==="block" && !dead){

score++;

if(score%50===0)
speed++;

updateUI();

}

},100);

/* COINS */

function spawnCoin(){

if(game.style.display!=="block")
return;

let c=document.createElement("div");

c.className="coin";

c.style.left=
Math.random()*
(window.innerWidth-50)+"px";

document.body.appendChild(c);

let y=-50;

let m=setInterval(()=>{

if(dead){

c.remove();
clearInterval(m);

return;

}

y+=5;

c.style.top=y+"px";

let a=car.getBoundingClientRect();
let b=c.getBoundingClientRect();

if(!(a.right<b.left||
a.left>b.right||
a.bottom<b.top||
a.top>b.bottom)){

coins++;

document.getElementById("coinSound").play();

c.remove();

clearInterval(m);

updateUI();

}

if(y>window.innerHeight){

c.remove();

clearInterval(m);

}

},20);

}

setInterval(spawnCoin,1200);

/* ENEMY */

function spawnEnemy(){

if(game.style.display!=="block")
return;

let e=document.createElement("div");

e.className="enemy";

e.style.left=
Math.random()*
(window.innerWidth-60)+"px";

document.body.appendChild(e);

let y=-120;

let m=setInterval(()=>{

if(dead){

e.remove();

clearInterval(m);

return;

}

y+=speed;

e.style.top=y+"px";

let a=car.getBoundingClientRect();
let b=e.getBoundingClientRect();

if(!(a.right<b.left||
a.left>b.right||
a.bottom<b.top||
a.top>b.bottom)){

dead=true;

document.getElementById("crashSound").play();

if(score>highScore){

highScore=score;

localStorage.setItem("hs",highScore);

}

document.getElementById("fs").innerText=score;
document.getElementById("fc").innerText=coins;
document.getElementById("fh").innerText=highScore;

over.style.display="flex";

}

if(y>window.innerHeight){

e.remove();

clearInterval(m);

}

},20);

}

setInterval(spawnEnemy,800);

/* CONTROLS */

function bind(btn,dir){

btn.addEventListener("touchstart",(e)=>{

e.preventDefault();

if(dir==="l")
left=true;
else
right=true;

});

btn.addEventListener("touchend",(e)=>{

e.preventDefault();

if(dir==="l")
left=false;
else
right=false;

});

}

bind(document.getElementById("left"),"l");
bind(document.getElementById("right"),"r");

/* MOVE */

function loop(){

if(game.style.display==="block"){

if(left)
x-=7;

if(right)
x+=7;

if(x<20)
x=20;

if(x>window.innerWidth-70)
x=window.innerWidth-70;

car.style.left=x+"px";

}

requestAnimationFrame(loop);

}

loop();

/* RESTART */

function restart(){

dead=false;

score=0;
coins=0;
speed=6;

over.style.display="none";

x=window.innerWidth/2;

car.style.left=x+"px";

}

</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(html)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
