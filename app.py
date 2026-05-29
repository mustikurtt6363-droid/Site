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
user-select:none;
}

/* MENU */
#menu{
position:absolute;
inset:0;
display:flex;
flex-direction:column;
justify-content:center;
align-items:center;
background:#0b1220;
z-index:100;
}

.menuBtn{
width:250px;
padding:15px;
margin:10px;
border:none;
border-radius:12px;
font-size:20px;
background:#0891b2;
color:white;
}

/* ROAD */
#road{
position:absolute;
left:50%;
transform:translateX(-50%);
width:180px;
height:100%;
background:#1a1a1a;
border-left:2px solid #00d5ff;
border-right:2px solid #00d5ff;
display:none;
}

/* CAR */
#car{
position:absolute;
bottom:120px;
width:45px;
height:80px;
background:#ff00aa;
border-radius:10px;
display:none;
}

/* ENEMY */
.enemy{
position:absolute;
width:45px;
height:80px;
background:#00aaff;
border-radius:10px;
}

/* COIN */
.coin{
position:absolute;
width:25px;
height:25px;
border-radius:50%;
background:#00bfff;
box-shadow:0 0 12px #00bfff;
}

/* EXPLOSION 💥 */
.explosion{
position:absolute;
width:10px;
height:10px;
border-radius:50%;
background:orange;
box-shadow:0 0 20px orange;
animation:boom 0.4s linear forwards;
z-index:999;
}

@keyframes boom{
0%{transform:scale(1);opacity:1;}
100%{transform:scale(6);opacity:0;}
}

/* UI */
#ui{
position:absolute;
top:10px;
left:10px;
color:white;
z-index:20;
display:none;
}

/* CONTROLS */
#controls{
position:absolute;
bottom:20px;
width:100%;
display:none;
justify-content:space-between;
padding:0 20px;
box-sizing:border-box;
}

.btn{
width:90px;
height:90px;
border-radius:50%;
border:none;
background:rgba(255,255,255,0.2);
font-size:40px;
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
color:white;
z-index:200;
}

</style>
</head>

<body>

<!-- MENU -->
<div id="menu">
<h1 style="color:white">NEON RACE</h1>
<button class="menuBtn" onclick="startGame()">BAŞLA</button>
</div>

<!-- UI -->
<div id="ui">
CAN: <span id="hp">3</span> |
COIN: <span id="coin">0</span>
</div>

<div id="road"></div>
<div id="car"></div>

<div id="controls">
<button class="btn" id="left">◀</button>
<button class="btn" id="right">▶</button>
</div>

<div id="gameOver">
<h1>GAME OVER</h1>
<button class="menuBtn" onclick="location.reload()">TEKRAR OYNA</button>
</div>

<script>

let car=document.getElementById("car");
let x=window.innerWidth/2;

let left=false;
let right=false;

let hp=3;
let coin=0;
let dead=false;

/* START */
function startGame(){
document.getElementById("menu").style.display="none";
document.getElementById("road").style.display="block";
document.getElementById("car").style.display="block";
document.getElementById("ui").style.display="block";
document.getElementById("controls").style.display="flex";

car.style.left=x+"px";
}

/* CONTROLS */
document.getElementById("left").ontouchstart=()=>left=true;
document.getElementById("left").ontouchend=()=>left=false;

document.getElementById("right").ontouchstart=()=>right=true;
document.getElementById("right").ontouchend=()=>right=false;

/* MOVE */
function loop(){
if(!dead){

if(left) x-=6;
if(right) x+=6;

if(x<30) x=30;
if(x>window.innerWidth-80) x=window.innerWidth-80;

car.style.left=x+"px";
}
requestAnimationFrame(loop);
}
loop();

/* 💥 EXPLOSION */
function explosion(x,y){
let ex=document.createElement("div");
ex.className="explosion";
ex.style.left=x+"px";
ex.style.top=y+"px";
document.body.appendChild(ex);

setTimeout(()=>ex.remove(),400);
}

/* ENEMY */
function spawnEnemy(){
if(dead) return;

let e=document.createElement("div");
e.className="enemy";
e.style.left=Math.random()*(window.innerWidth-60)+"px";
document.body.appendChild(e);

let y=-100;

let t=setInterval(()=>{

if(dead){e.remove();clearInterval(t);return;}

y+=6;
e.style.top=y+"px";

let a=car.getBoundingClientRect();
let b=e.getBoundingClientRect();

if(!(a.right<b.left||a.left>b.right||a.bottom<b.top||a.top>b.bottom)){

hp--;
document.getElementById("hp").innerText=hp;

/* 💥 PATLAMA */
explosion(a.left,a.top);

e.remove();
clearInterval(t);

if(hp<=0){
dead=true;
document.getElementById("gameOver").style.display="flex";
explosion(a.left,a.top);
}

}

if(y>window.innerHeight){
e.remove();
clearInterval(t);
}

},20);
}
setInterval(spawnEnemy,900);

/* COIN */
function spawnCoin(){
if(dead) return;

let c=document.createElement("div");
c.className="coin";
c.style.left=Math.random()*(window.innerWidth-40)+"px";
document.body.appendChild(c);

let y=-50;

let t=setInterval(()=>{

if(dead){c.remove();clearInterval(t);return;}

y+=5;
c.style.top=y+"px";

let a=car.getBoundingClientRect();
let b=c.getBoundingClientRect();

if(!(a.right<b.left||a.left>b.right||a.bottom<b.top||a.top>b.top)){

coin++;
document.getElementById("coin").innerText=coin;

c.remove();
clearInterval(t);

}

if(y>window.innerHeight){
c.remove();
clearInterval(t);
}

},20);
}
setInterval(spawnCoin,1200);

</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    port = int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
