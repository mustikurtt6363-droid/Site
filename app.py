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
}

/* CAR */
#car{
position:absolute;
bottom:120px;
width:45px;
height:80px;
background:#ff00aa;
border-radius:10px;
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
width:20px;
height:20px;
border-radius:50%;
background:gold;
box-shadow:0 0 10px gold;
}

/* UI */
#ui{
position:absolute;
top:10px;
left:10px;
color:white;
z-index:10;
}

/* CONTROLS */
#controls{
position:absolute;
bottom:20px;
width:100%;
display:flex;
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
</style>
</head>

<body>

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

<script>

let car=document.getElementById("car");
let x=window.innerWidth/2;
car.style.left=x+"px";

let left=false;
let right=false;

let hp=3;
let coin=0;
let dead=false;

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

/* ENEMY */
function spawnEnemy(){
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

e.remove();
clearInterval(t);

if(hp<=0){
dead=true;
alert("GAME OVER");
location.reload();
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

if(!(a.right<b.left||a.left>b.right||a.bottom<b.top||a.top>b.bottom)){

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
