from flask import Flask, render_template_string
import os

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Neon 1V1 Race</title>

<style>

html,body{
margin:0;
padding:0;
width:100%;
height:100%;
overflow:hidden;
font-family:Arial;
background:#071014;
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
border-left:2px solid #00bcd4;
border-right:2px solid #00bcd4;
overflow:hidden;
}

/* LINES */

.lane{
position:absolute;
left:50%;
transform:translateX(-50%);
width:5px;
height:70px;
background:#00d5ff;
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
width:45px;
height:80px;
background:#ff00aa;
border-radius:10px;
}

/* BOT */

.enemy{
position:absolute;
width:45px;
height:80px;
background:#00aaff;
border-radius:10px;
}

/* MINI OBSTACLE */

.miniObstacle{
position:absolute;
width:18px;
height:18px;
background:red;
border-radius:4px;
}

/* HEALTH */

#healthBar{
position:absolute;
top:10px;
left:10px;
color:#ff4444;
font-size:20px;
z-index:50;
}

#botHealthBar{
position:absolute;
top:40px;
left:10px;
color:#00aaff;
font-size:20px;
z-index:50;
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
will-change:transform;
transform:translateZ(0);
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

<div id="game">

<div id="grassLeft"></div>
<div id="grassRight"></div>

<div id="road"></div>

<div id="healthBar">
CAN: 4
</div>

<div id="botHealthBar">
BOT CAN: 4
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

<h1 id="winnerText">
GAME OVER
</h1>

<button onclick="restart()">
TEKRAR OYNA
</button>

<button onclick="normalMode()">
NORMAL OYUNA DÖN
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

/* PLAYER */

let car=document.getElementById("car");

let x=(window.innerWidth/2)-60;

car.style.left=x+"px";

/* BOT */

let bot=document.createElement("div");

bot.className="enemy";

bot.style.left=(window.innerWidth/2)+15+"px";

bot.style.top=(window.innerHeight-220)+"px";

document.body.appendChild(bot);

/* STATE */

let left=false;
let right=false;

let dead=false;

let health=4;
let botHealth=4;

/* BOT MOVE */

let botY=window.innerHeight-220;

let botX=(window.innerWidth/2)+15;

setInterval(()=>{

if(dead)return;

/* SPEED */
botY-=3.5;

/* RANDOM */
botX += (Math.random()-0.5)*6;

/* LIMIT */

if(botX<(window.innerWidth/2)+5)
botX=(window.innerWidth/2)+5;

if(botX>(window.innerWidth/2)+45)
botX=(window.innerWidth/2)+45;

bot.style.left=botX+"px";

bot.style.top=botY+"px";

},40);

/* CONTROLS */

const leftBtn=document.getElementById("left");
const rightBtn=document.getElementById("right");

function pressLeft(e){
e.preventDefault();
left=true;
}

function releaseLeft(e){
e.preventDefault();
left=false;
}

function pressRight(e){
e.preventDefault();
right=true;
}

function releaseRight(e){
e.preventDefault();
right=false;
}

/* LEFT */

leftBtn.addEventListener(
"touchstart",
pressLeft,
{passive:false}
);

leftBtn.addEventListener(
"touchend",
releaseLeft,
{passive:false}
);

/* RIGHT */

rightBtn.addEventListener(
"touchstart",
pressRight,
{passive:false}
);

rightBtn.addEventListener(
"touchend",
releaseRight,
{passive:false}
);

/* EXTRA FIX */

window.addEventListener("touchend",()=>{

left=false;
right=false;

});

/* MOVE */

function loop(){

if(!dead){

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

/* MINI OBSTACLE */

function spawnMiniObstacle(){

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

y+=7;

o.style.top=y+"px";

/* PLAYER HIT */

let a=car.getBoundingClientRect();
let b=o.getBoundingClientRect();

if(!(a.right<b.left||
a.left>b.right||
a.bottom<b.top||
a.top>b.bottom)){

health--;

document.getElementById("healthBar").innerText=
"CAN: "+health;

o.remove();

clearInterval(m);

if(health<=0){

gameOver("BOT KAZANDI");

}

}

/* BOT HIT */

let bb=bot.getBoundingClientRect();

if(!(bb.right<b.left||
bb.left>b.right||
bb.bottom<b.top||
bb.top>b.bottom)){

botHealth--;

document.getElementById("botHealthBar").innerText=
"BOT CAN: "+botHealth;

o.remove();

clearInterval(m);

if(botHealth<=0){

gameOver("SEN KAZANDIN");

}

}

if(y>window.innerHeight){

o.remove();

clearInterval(m);

}

},20);

}

setInterval(spawnMiniObstacle,500);

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

location.reload();

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
