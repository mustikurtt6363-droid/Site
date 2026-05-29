from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">

<title>Neon Car Game</title>

<style>

html,body{
margin:0;
padding:0;
width:100%;
height:100%;
overflow:hidden;
background:#071014;
font-family:Arial;
touch-action:none;
user-select:none;
}

/* GAME */

#game{
position:fixed;
inset:0;
overflow:hidden;
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
background:#1a1a1a;
border-left:2px solid #00d5ff;
border-right:2px solid #00d5ff;
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
opacity:.5;
animation:moveLine .5s linear infinite;
}

@keyframes moveLine{
0%{transform:translate(-50%,-120px);}
100%{transform:translate(-50%,120vh);}
}

/* PLAYER */

#car{
position:absolute;
bottom:120px;
width:45px;
height:80px;
background:#ff00aa;
border-radius:10px;
box-shadow:0 0 10px #ff00aa;
}

/* ENEMY */

.enemy{
position:absolute;
width:45px;
height:80px;
background:#00aaff;
border-radius:10px;
box-shadow:0 0 10px #00aaff;
}

/* OBSTACLE */

.obstacle{
position:absolute;
width:45px;
height:45px;
background:red;
border-radius:8px;
}

/* COIN */

.coin{
position:absolute;
width:20px;
height:20px;
border-radius:50%;
background:gold;
box-shadow:0 0 10px gold;
}

/* EXPLOSION */

.explosion{
position:absolute;
width:80px;
height:80px;
border-radius:50%;
background:radial-gradient(circle,orange,red,transparent);
animation:boom .4s linear forwards;
pointer-events:none;
z-index:999;
}

@keyframes boom{

0%{
transform:scale(.3);
opacity:1;
}

100%{
transform:scale(2.5);
opacity:0;
}

}

/* UI */

#healthBar{
position:absolute;
top:10px;
left:10px;
color:#ff4444;
font-size:20px;
z-index:50;
}

#coinBar{
position:absolute;
top:40px;
left:10px;
color:gold;
font-size:20px;
z-index:50;
}

#botHealthBar{
position:absolute;
top:70px;
left:10px;
color:#00aaff;
font-size:20px;
z-index:50;
display:none;
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
width:95px;
height:95px;
border:none;
border-radius:50%;
background:rgba(255,255,255,0.12);
color:white;
font-size:40px;
touch-action:none;
}

/* GAME OVER */

#over{
display:none;
position:absolute;
inset:0;
background:rgba(0,0,0,.7);
justify-content:center;
align-items:center;
z-index:100;
}

.panel{
background:#111827;
padding:25px;
border-radius:20px;
width:80%;
max-width:320px;
text-align:center;
color:white;
}

.panel button{
width:100%;
padding:14px;
margin-top:10px;
border:none;
border-radius:12px;
background:#0891b2;
color:white;
font-size:18px;
}

</style>
</head>

<body>

<div id="game">

<div id="grassLeft"></div>
<div id="grassRight"></div>

<div id="road"></div>

<div id="healthBar">CAN: 3</div>
<div id="coinBar">COIN: 0</div>
<div id="botHealthBar">BOT CAN: 4</div>

<div id="car"></div>

<div id="controls">

<button class="btn" id="left">◀</button>
<button class="btn" id="right">▶</button>

</div>

<div id="over">

<div class="panel">

<h1 id="winnerText">GAME OVER</h1>

<button onclick="restart()">
TEKRAR OYNA
</button>

<button onclick="start1v1()">
1V1
</button>

<button onclick="normalMode()">
NORMAL OYUN
</button>

</div>

</div>

</div>

<script>

/* ROAD LINES */

for(let i=0;i<10;i++){

let line=document.createElement("div");

line.className="lane";

line.style.top=(i*120)+"px";

document.getElementById("road").appendChild(line);

}

/* VARIABLES */

let car=document.getElementById("car");

let x=window.innerWidth/2;

car.style.left=x+"px";

let left=false;
let right=false;

let dead=false;

let health=3;
let botHealth=4;

let coins=0;

let mode1v1=false;

let bot=null;

/* CONTROLS */

const leftBtn=document.getElementById("left");
const rightBtn=document.getElementById("right");

leftBtn.addEventListener("touchstart",(e)=>{
e.preventDefault();
left=true;
},{passive:false});

leftBtn.addEventListener("touchend",(e)=>{
e.preventDefault();
left=false;
},{passive:false});

rightBtn.addEventListener("touchstart",(e)=>{
e.preventDefault();
right=true;
},{passive:false});

rightBtn.addEventListener("touchend",(e)=>{
e.preventDefault();
right=false;
},{passive:false});

/* MOVE */

function loop(){

if(!dead){

if(left) x-=7;
if(right) x+=7;

if(x<20) x=20;
if(x>window.innerWidth-70) x=window.innerWidth-70;

car.style.left=x+"px";

}

requestAnimationFrame(loop);

}

loop();

/* EXPLOSION */

function explode(px,py){

let ex=document.createElement("div");

ex.className="explosion";

ex.style.left=(px-40)+"px";
ex.style.top=(py-40)+"px";

document.body.appendChild(ex);

setTimeout(()=>{
ex.remove();
},400);

}

/* GAME OVER */

function gameOver(text){

dead=true;

document.getElementById("winnerText").innerText=text;

document.getElementById("over").style.display="flex";

}

/* RESTART */

function restart(){

location.reload();

}

/* NORMAL MODE */

function normalMode(){

mode1v1=false;

dead=false;

health=3;

document.getElementById("healthBar").innerText="CAN: 3";

document.getElementById("botHealthBar").style.display="none";

document.getElementById("over").style.display="none";

if(bot){
bot.remove();
bot=null;
}

}

/* ENEMY */

function spawnEnemy(){

if(mode1v1) return;

let e=document.createElement("div");

e.className="enemy";

e.style.left=Math.random()*(window.innerWidth-60)+"px";

document.body.appendChild(e);

let y=-100;

let move=setInterval(()=>{

if(dead){

e.remove();
clearInterval(move);
return;

}

y+=6;

e.style.top=y+"px";

let a=car.getBoundingClientRect();
let b=e.getBoundingClientRect();

if(!(a.right<b.left ||
a.left>b.right ||
a.bottom<b.top ||
a.top>b.bottom)){

health--;

document.getElementById("healthBar").innerText=
"CAN: "+health;

explode(
a.left+a.width/2,
a.top+a.height/2
);

e.remove();

clearInterval(move);

if(health<=0){

gameOver("GAME OVER");

}

}

if(y>window.innerHeight){

e.remove();
clearInterval(move);

}

},20);

}

setInterval(spawnEnemy,1000);

/* COIN */

function spawnCoin(){

let c=document.createElement("div");

c.className="coin";

c.style.left=
Math.random()*(window.innerWidth-40)+"px";

document.body.appendChild(c);

let y=-20;

let move=setInterval(()=>{

if(dead){

c.remove();
clearInterval(move);
return;

}

y+=5;

c.style.top=y+"px";

let a=car.getBoundingClientRect();
let b=c.getBoundingClientRect();

if(!(a.right<b.left ||
a.left>b.right ||
a.bottom<b.top ||
a.top>b.bottom)){

coins++;

document.getElementById("coinBar").innerText=
"COIN: "+coins;

c.remove();

clearInterval(move);

}

if(y>window.innerHeight){

c.remove();
clearInterval(move);

}

},20);

}

setInterval(spawnCoin,1200);

/* 1V1 */

function start1v1(){

mode1v1=true;

dead=false;

health=3;
botHealth=4;

document.getElementById("healthBar").innerText=
"CAN: 3";

document.getElementById("botHealthBar").style.display=
"block";

document.getElementById("botHealthBar").innerText=
"BOT CAN: 4";

document.getElementById("over").style.display="none";

/* BOT */

bot=document.createElement("div");

bot.className="enemy";

bot.style.left=(window.innerWidth/2)+15+"px";

bot.style.top=(window.innerHeight-220)+"px";

document.body.appendChild(bot);

/* PLAYER */

x=(window.innerWidth/2)-60;

car.style.left=x+"px";

let botY=window.innerHeight-220;

let botX=(window.innerWidth/2)+15;

let botMove=setInterval(()=>{

if(dead || !mode1v1){

clearInterval(botMove);
return;

}

botY-=3.5;

botX += (Math.random()-0.5)*6;

if(botX<(window.innerWidth/2)+5)
botX=(window.innerWidth/2)+5;

if(botX>(window.innerWidth/2)+45)
botX=(window.innerWidth/2)+45;

if(bot){

bot.style.left=botX+"px";
bot.style.top=botY+"px";

}

},40);

}

/* OBSTACLE */

function spawnObstacle(){

if(!mode1v1) return;

let o=document.createElement("div");

o.className="obstacle";

o.style.left=
Math.random()*(window.innerWidth-50)+"px";

document.body.appendChild(o);

let y=-40;

let move=setInterval(()=>{

if(dead){

o.remove();
clearInterval(move);
return;

}

y+=7;

o.style.top=y+"px";

let a=car.getBoundingClientRect();
let b=o.getBoundingClientRect();

/* PLAYER HIT */

if(!(a.right<b.left ||
a.left>b.right ||
a.bottom<b.top ||
a.top>b.bottom)){

health--;

document.getElementById("healthBar").innerText=
"CAN: "+health;

explode(
a.left+a.width/2,
a.top+a.height/2
);

o.remove();

clearInterval(move);

if(health<=0){

gameOver("BOT KAZANDI");

}

}

/* BOT HIT */

if(bot){

let bb=bot.getBoundingClientRect();

if(!(bb.right<b.left ||
bb.left>b.right ||
bb.bottom<b.top ||
bb.top>b.bottom)){

botHealth--;

document.getElementById("botHealthBar").innerText=
"BOT CAN: "+botHealth;

explode(
bb.left+bb.width/2,
bb.top+bb.height/2
);

o.remove();

clearInterval(move);

if(botHealth<=0){

gameOver("SEN KAZANDIN");

}

}

}

if(y>window.innerHeight){

o.remove();
clearInterval(move);

}

},20);

}

setInterval(spawnObstacle,500);

</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
