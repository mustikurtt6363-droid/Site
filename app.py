from flask import Flask, render_template_string
import os

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>Night Car Game</title>

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
background:#000;
}

/* LOGIN */
#login{
position:fixed;
inset:0;
display:flex;
justify-content:center;
align-items:center;
background:#0b1a2b;
z-index:100;
}

.box{
width:90%;
max-width:360px;
background:#13233d;
padding:25px;
border-radius:20px;
color:white;
text-align:center;
}

/* CALC */
#calc{
position:fixed;
inset:0;
display:none;
justify-content:center;
align-items:center;
background:#111;
z-index:10;
}

#panel{
width:90%;
max-width:380px;
background:#222;
padding:20px;
border-radius:15px;
}

#ekran{
width:100%;
padding:15px;
font-size:22px;
text-align:right;
border:none;
}

.grid{
display:grid;
grid-template-columns:repeat(4,1fr);
gap:6px;
margin-top:10px;
}

.grid button{
padding:15px;
border:none;
background:#444;
color:white;
}

/* GAME */
#game{
display:none;
position:fixed;
inset:0;
background:#05070d;
}

#road{
position:absolute;
left:50%;
transform:translateX(-50%);
width:160px;
height:100%;
background:linear-gradient(#1a1a1a,#000);
box-shadow:inset 0 0 20px black;
overflow:hidden;
}

/* LANE */
.lane{
position:absolute;
left:50%;
transform:translateX(-50%);
width:4px;
height:70px;
background:white;
opacity:0.6;
animation:move 0.5s linear infinite;
}

@keyframes move{
0%{transform:translate(-50%,-120px);}
100%{transform:translate(-50%,120vh);}
}

/* CAR */
#car{
position:absolute;
bottom:120px;
left:50%;
width:45px;
height:80px;
background:linear-gradient(red,darkred);
border-radius:10px;
}

#car::before{
content:"";
position:absolute;
top:-40px;
left:-10px;
width:70px;
height:120px;
background:radial-gradient(rgba(255,255,180,0.4),transparent);
}

/* ENEMY CAR */
.enemy{
position:absolute;
width:45px;
height:80px;
background:gold;
border-radius:8px;
}

/* COIN */
.coin{
position:absolute;
width:20px;
height:20px;
background:gold;
border-radius:50%;
top:-40px;
}

/* SCORE */
#score{
position:absolute;
top:10px;
left:10px;
color:white;
font-size:14px;
}

/* LEADERBOARD */
#board{
position:absolute;
top:10px;
right:10px;
width:160px;
background:rgba(0,0,0,0.4);
color:white;
font-size:11px;
padding:8px;
border-radius:10px;
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
}

.btn{
width:70px;
height:70px;
border-radius:50%;
background:rgba(255,255,255,0.2);
border:none;
color:white;
font-size:30px;
}

/* GAME OVER */
#over{
display:none;
position:absolute;
inset:0;
background:rgba(0,0,0,0.7);
justify-content:center;
align-items:center;
}

.card{
background:#1e1e1e;
padding:20px;
border-radius:15px;
color:white;
text-align:center;
width:80%;
}

</style>
</head>

<body>

<!-- LOGIN -->
<div id="login">
<div class="box">
<h2>Giriş</h2>
<input id="user" placeholder="Musti yaz">
<button onclick="login()" style="width:100%;margin-top:10px;padding:10px;background:#0d6efd;color:white;">Giriş</button>
</div>
</div>

<!-- CALC -->
<div id="calc">
<div id="panel">

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
<button onclick="clearE()" style="grid-column:span 2;background:red;">C</button>
</div>

</div>
</div>

<!-- GAME -->
<div id="game">

<div id="road"></div>

<div id="score"></div>

<div id="board"></div>

<div id="car"></div>

<div id="controls">
<button class="btn" id="left">◀</button>
<button class="btn" id="right">▶</button>
</div>

<div id="over">
<div class="card">
<h2>GAME OVER</h2>
<p id="fs"></p>
<p id="fc"></p>
<p id="fh"></p>
<button onclick="restart()">Tekrar</button>
</div>
</div>

</div>

<script>

/* LOGIN */
function login(){
if(document.getElementById("user").value==="Musti"){
document.getElementById("login").style.display="none";
document.getElementById("calc").style.display="flex";
}else alert("Hatalı");
}

/* CALC */
function add(v){ekran.value+=v;}
function clearE(){ekran.value="";}

let startBtn=false;

function check(){
let v=ekran.value;
if(v==="2727") startBtn=true;
}

/* GAME */
let calc=document.getElementById("calc");
let game=document.getElementById("game");
let car=document.getElementById("car");

let x=window.innerWidth/2;
let left=false,right=false;

let score=0,coins=0,speed=6;
let dead=false;

let hs=localStorage.getItem("hs")||0;

/* START GAME */
function start(){
calc.style.display="none";
game.style.display="block";
createLanes();
board();
}

/* LANES */
function createLanes(){
for(let i=0;i<12;i++){
let l=document.createElement("div");
l.className="lane";
l.style.top=(i*120)+"px";
document.getElementById("game").appendChild(l);
}
}

/* SCORE */
setInterval(()=>{
if(game.style.display==="block" && !dead){
score++;
if(score%50===0)speed++;
document.getElementById("score").innerText="Score:"+score+" Coin:"+coins+" HS:"+hs;
}
},100);

/* ENEMY */
function enemy(){
if(game.style.display!=="block")return;

let e=document.createElement("div");
e.className="enemy";
e.style.left=Math.random()*(window.innerWidth-60)+"px";
document.body.appendChild(e);

let y=-100;

let m=setInterval(()=>{
if(dead){e.remove();clearInterval(m);return;}

y+=speed;
e.style.top=y+"px";

let a=car.getBoundingClientRect();
let b=e.getBoundingClientRect();

if(!(a.right<b.left||a.left>b.right||a.bottom<b.top||a.top>b.bottom)){
dead=true;

document.getElementById("fs").innerText="Skor:"+score;
document.getElementById("fc").innerText="Coin:"+coins;

if(score>hs){
hs=score;
localStorage.setItem("hs",hs);
}
document.getElementById("fh").innerText="HS:"+hs;

document.getElementById("over").style.display="flex";
}

if(y>window.innerHeight){
e.remove();
clearInterval(m);
}

},20);
}
setInterval(enemy,800);

/* MOVE */
function bind(btn,d){
btn.addEventListener("touchstart",()=>d==="l"?left=true:right=true);
btn.addEventListener("touchend",()=>d==="l"?left=false:right=false);
}

bind(leftBtn=document.getElementById("left"),"l");
bind(rightBtn=document.getElementById("right"),"r");

function loop(){
if(game.style.display==="block"){
if(left)x-=7;
if(right)x+=7;

car.style.left=x+"px";
}
requestAnimationFrame(loop);
}
loop();

/* RESTART */
function restart(){
location.reload();
}

/* AUTO START */
setInterval(()=>{
if(startBtn){
startBtn=false;
start();
}
},500);

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
