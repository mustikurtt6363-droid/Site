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
background:#071014;
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
box-shadow:0 0 10px #00bcd4;
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
background:#0891b2;
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
box-shadow:0 0 10px #00bcd4;
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
background:#0891b2;
color:white;
font-size:20px;
}

/* GAME */

#game{
display:none;
position:fixed;
inset:0;
overflow:hidden;
background:#0a0f12;
}

/* GRASS */

#grassLeft{
position:absolute;
left:0;
top:0;
width:calc(50% - 85px);
height:100%;
background:#14532d;
}

#grassRight{
position:absolute;
right:0;
top:0;
width:calc(50% - 85px);
height:100%;
background:#14532d;
}

/* ROAD */

#road{
position:absolute;
left:50%;
transform:translateX(-50%);
width:170px;
height:100%;
background:linear-gradient(#222,#111);
border-left:1px solid #00bcd4;
border-right:1px solid #00bcd4;
box-shadow:
0 0 6px #00bcd4,
0 0 10px #00bcd4 inset;
overflow:hidden;
}

/* ROAD LINE */

.lane{
position:absolute;
left:50%;
transform:translateX(-50%);
width:5px;
height:70px;
background:#00d5ff;
box-shadow:0 0 4px #00d5ff;
opacity:0.5;
animation:moveLine 0.5s linear infinite;
}

@keyframes moveLine{
0%{transform:translate(-50%,-120px);}
100%{transform:translate(-50%,120vh);}
}

/* PLAYER */

#car{
position:absolute;
bottom:120px;
left:50%;
width:45px;
height:80px;
background:linear-gradient(#ff00aa,#6d1b7b);
border-radius:10px;
box-shadow:0 0 6px #ff00aa;
border:1px solid #ffffff22;
}

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

/* ENEMY */

.enemy{
position:absolute;
width:45px;
height:80px;
background:linear-gradient(#00d084,#007a50);
border-radius:10px;
box-shadow:0 0 5px #00d084;
}

/* COIN */

.coin{
position:absolute;
width:20px;
height:20px;
border-radius:50%;
background:gold;
}

/* MINI */

.miniObstacle{
position:absolute;
width:18px;
height:18px;
background:red;
border-radius:4px;
}

/* SCORE */

#score{
position:absolute;
top:10px;
left:10px;
color:#00d5ff;
font-size:15px;
z-index:20;
}

/* CONTROLS */

#controls{
position:absolute;
bottom:15px;
left:0;
width:100%;
display:flex;
justify-content:space-between;
padding:0 20px;
box-sizing:border-box;
z-index:50;
}

.btn{
width:90px;
height:90px;
border:none;
border-radius:50%;
background:rgba(255,255,255,0.12);
color:white;
font-size:38px;
touch-action:none;
-webkit-user-select:none;
user-select:none;
-webkit-touch-callout:none;
}

/* GAME OVER */

#over{
display:none;
position:absolute;
inset:0;
background:rgba(0,0,0,0.7);
justify-content:center;
align-items:center;
z-index:100;
}

.panel{
background:#111827;
padding:25px;
border-radius:20px;
text-align:center;
width:80%;
max-width:320px;
color:white;
box-shadow:0 0 10px #00bcd4;
}

.panel button{
width:100%;
padding:14px;
border:none;
border-radius:12px;
background:#0891b2;
color:white;
font-size:18px;
margin-top:10px;
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

<div id="grassLeft"></div>
<div id="grassRight"></div>

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

<button onclick="start1v1()">
1V1
</button>

</div>

</div>

</div>

<script>

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

let mode1v1=false;

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

if(mode1v1)return;

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

gameOver();

}

if(y>window.innerHeight){

e.remove();

clearInterval(m);

}

},20);

}

setInterval(spawnEnemy,800);

/* GAME OVER */

function gameOver(){

dead=true;

if(score>highScore){

highScore=score;

localStorage.setItem("hs",highScore);

}

document.getElementById("fs").innerText=score;
document.getElementById("fc").innerText=coins;
document.getElementById("fh").innerText=highScore;

over.style.display="flex";

}

/* CONTROLS */

function bind(btn,dir){

btn.addEventListener("pointerdown",(e)=>{

e.preventDefault();

if(dir==="l")
left=true;
else
right=true;

});

btn.addEventListener("pointerup",(e)=>{

e.preventDefault();

if(dir==="l")
left=false;
else
right=false;

});

btn.addEventListener("pointercancel",(e)=>{

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

mode1v1=false;

dead=false;

score=0;
coins=0;

over.style.display="none";

x=window.innerWidth/2;

car.style.left=x+"px";

}

/* 1V1 */

function start1v1(){

mode1v1=true;

dead=false;

score=0;

coins=0;

over.style.display="none";

spawnBots();

}

/* BOTS */

function spawnBots(){

for(let i=0;i<2;i++){

let bot=document.createElement("div");

bot.className="enemy";

bot.style.background=
i==0 ? "#00aaff" : "#ff6600";

bot.style.left=
i==0 ?
(window.innerWidth/2)-55+"px"
:
(window.innerWidth/2)+10+"px";

document.body.appendChild(bot);

let y=window.innerHeight-220;

setInterval(()=>{

if(dead)return;

y-=2;

bot.style.top=y+"px";

},20);

}

}

/* MINI OBSTACLE */

function spawnMiniObstacle(){

if(!mode1v1)return;

let o=document.createElement("div");

o.className="miniObstacle";

o.style.left=
Math.random()*
(window.innerWidth-40)+"px";

document.body.appendChild(o);

let y=-20;

let m=setInterval(()=>{

if(dead){

o.remove();

clearInterval(m);

return;

}

y+=5;

o.style.top=y+"px";

let a=car.getBoundingClientRect();
let b=o.getBoundingClientRect();

if(!(a.right<b.left||
a.left>b.right||
a.bottom<b.top||
a.top>b.bottom)){

speed=2;

setTimeout(()=>{
speed=6;
},1000);

o.remove();

clearInterval(m);

}

if(y>window.innerHeight){

o.remove();

clearInterval(m);

}

},20);

}

setInterval(spawnMiniObstacle,1200);

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
