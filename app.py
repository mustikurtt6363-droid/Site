from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Neon Race</title>

<style>

body{
margin:0;
overflow:hidden;
background:#071014;
font-family:Arial;
touch-action:none;
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

/* MENU */
#menu{
position:absolute;
inset:0;
display:none;
justify-content:center;
align-items:center;
flex-direction:column;
background:#0b1220;
z-index:100;
}

.menuBtn{
width:260px;
padding:16px;
margin:10px;
border:none;
border-radius:14px;
font-size:22px;
background:#0891b2;
color:white;
}

/* ROAD */
#road{
position:absolute;
left:50%;
transform:translateX(-50%);
width:190px;
height:100%;
background:#1d1d1d;
border-left:3px solid #00d5ff;
border-right:3px solid #00d5ff;
display:none;
}

/* ROAD LINE */
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

/* PLAYER NAME */
#playerName{
position:absolute;
top:10px;
right:10px;
color:white;
font-size:20px;
z-index:50;
display:none;
}

/* CAR */
#car{
position:absolute;
bottom:120px;
width:50px;
height:85px;
border-radius:12px;
display:none;
background:
linear-gradient(
to bottom,
#ff00aa,
#ff66cc
);
box-shadow:0 0 15px #ff00aa;
}

/* CAR DESIGN */
#car::before{
content:'';
position:absolute;
left:8px;
top:12px;
width:34px;
height:18px;
background:#87cefa;
border-radius:6px;
}

#car::after{
content:'';
position:absolute;
left:12px;
bottom:10px;
width:26px;
height:8px;
background:#222;
border-radius:4px;
}

/* ENEMY */
.enemy{
position:absolute;
width:50px;
height:85px;
border-radius:12px;
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
width:26px;
height:26px;
border-radius:50%;
background:#00bfff;
box-shadow:0 0 15px #00bfff;
}

/* UI */
#ui{
position:absolute;
top:10px;
left:10px;
color:white;
font-size:20px;
z-index:50;
display:none;
}

/* CONTROLS */
#controls{
position:absolute;
bottom:25px;
width:100%;
display:none;
justify-content:space-between;
padding:0 20px;
box-sizing:border-box;
z-index:100;
}

.btn{
width:110px;
height:110px;
border:none;
border-radius:50%;
background:rgba(255,255,255,0.15);
backdrop-filter:blur(4px);
font-size:42px;
color:white;
}

/* GAME OVER */
#gameOver{
position:absolute;
inset:0;
display:none;
justify-content:center;
align-items:center;
flex-direction:column;
background:rgba(0,0,0,0.8);
z-index:300;
color:white;
}

</style>
</head>

<body>

<!-- LOGIN -->
<div id="login">
<h1 style="color:white">KULLANICI ADI</h1>

<input id="nameInput" placeholder="Musti">

<button class="loginBtn" onclick="login()">
OYUNA GİR
</button>
</div>

<!-- MENU -->
<div id="menu">
<h1 style="color:white">NEON RACE</h1>

<button class="menuBtn" onclick="startGame()">
BAŞLA
</button>

<button class="menuBtn" onclick="start1v1()">
1V1 BOT
</button>
</div>

<!-- UI -->
<div id="ui">
CAN: <span id="hp">3</span>
|
COIN: <span id="coin">0</span>
</div>

<div id="playerName"></div>

<div id="road"></div>
<div id="line"></div>

<div id="car"></div>

<div id="controls">
<button class="btn" id="left">◀</button>
<button class="btn" id="right">▶</button>
</div>

<!-- GAME OVER -->
<div id="gameOver">
<h1>GAME OVER</h1>

<button class="menuBtn" onclick="location.reload()">
TEKRAR OYNA
</button>
</div>

<script>

/* LOGIN */
function login(){

let name =
document.getElementById("nameInput").value;

if(name.trim()==""){
return;
}

document.getElementById("playerName")
.innerText=name;

document.getElementById("login")
.style.display="none";

document.getElementById("menu")
.style.display="flex";

}

/* VARIABLES */
let car=document.getElementById("car");

let x=window.innerWidth/2;

let left=false;
let right=false;

let hp=3;
let coin=0;
let dead=false;

/* START */
function startGame(){

document.getElementById("menu")
.style.display="none";

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

document.getElementById("playerName")
.style.display="block";

car.style.left=x+"px";

}

/* 1V1 */
function start1v1(){
startGame();
spawnBot();
}

/* CONTROLS */
/* TAKILMA AZALTILDI */

const leftBtn =
document.getElementById("left");

const rightBtn =
document.getElementById("right");

leftBtn.addEventListener(
"touchstart",
e=>{
e.preventDefault();
left=true;
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

rightBtn.addEventListener(
"touchstart",
e=>{
e.preventDefault();
right=true;
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

/* MOVE */
function loop(){

if(!dead){

if(left) x-=7;
if(right) x+=7;

if(x<window.innerWidth/2-85)
x=window.innerWidth/2-85;

if(x>window.innerWidth/2+35)
x=window.innerWidth/2+35;

car.style.left=x+"px";

}

requestAnimationFrame(loop);
}
loop();

/* ENEMY */
function spawnEnemy(){

if(dead)return;

let e=document.createElement("div");

e.className="enemy";

e.style.left=
(window.innerWidth/2-85+
Math.random()*120)+"px";

document.body.appendChild(e);

let y=-120;

let t=setInterval(()=>{

if(dead){
e.remove();
clearInterval(t);
return;
}

y+=7;

e.style.top=y+"px";

let a=car.getBoundingClientRect();
let b=e.getBoundingClientRect();

if(!(a.right<b.left||
a.left>b.right||
a.bottom<b.top||
a.top>b.bottom)){

hp--;

document.getElementById("hp")
.innerText=hp;

/* PATLAMA */
explosion(a.left,a.top);

e.remove();
clearInterval(t);

if(hp<=0){

dead=true;

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

setInterval(spawnEnemy,850);

/* COIN */
function spawnCoin(){

if(dead)return;

let c=document.createElement("div");

c.className="coin";

c.style.left=
(window.innerWidth/2-85+
Math.random()*120)+"px";

document.body.appendChild(c);

let y=-50;

let t=setInterval(()=>{

if(dead){
c.remove();
clearInterval(t);
return;
}

y+=6;

c.style.top=y+"px";

let a=car.getBoundingClientRect();
let b=c.getBoundingClientRect();

if(!(a.right<b.left||
a.left>b.right||
a.bottom<b.top||
a.top>b.bottom)){

coin++;

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

setInterval(spawnCoin,1200);

/* BOT */
function spawnBot(){

let bot=document.createElement("div");

bot.className="enemy";

bot.style.left=
(window.innerWidth/2+20)+"px";

bot.style.top=
(window.innerHeight-240)+"px";

document.body.appendChild(bot);

let by=window.innerHeight-240;
let bx=window.innerWidth/2+20;

setInterval(()=>{

if(dead)return;

by-=4;

bx+=(Math.random()-0.5)*3;

if(bx<window.innerWidth/2-85)
bx=window.innerWidth/2-85;

if(bx>window.innerWidth/2+35)
bx=window.innerWidth/2+35;

bot.style.top=by+"px";
bot.style.left=bx+"px";

},35);

}

/* EXPLOSION */
function explosion(x,y){

let ex=document.createElement("div");

ex.style.position="absolute";
ex.style.left=x+"px";
ex.style.top=y+"px";
ex.style.width="15px";
ex.style.height="15px";
ex.style.borderRadius="50%";
ex.style.background="orange";
ex.style.boxShadow="0 0 25px orange";
ex.style.zIndex="999";

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
