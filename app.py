from flask import Flask, render_template_string
import os

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>Car Game</title>

<style>
html,body{
margin:0;
padding:0;
width:100%;
height:100%;
overflow:hidden;
font-family:Arial;
background:#222;
touch-action:none;
user-select:none;
position:fixed;
}

/* ================= CALC ================= */
#calc{
position:absolute;
width:100%;
height:100%;
display:flex;
justify-content:center;
align-items:center;
background:#111;
z-index:10;
}

#box{
width:90%;
max-width:360px;
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
outline:none;
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
font-size:18px;
border-radius:8px;
}

#startBtn{
display:none;
margin-top:10px;
padding:15px;
width:100%;
background:#0d6efd;
border:none;
color:white;
font-size:18px;
border-radius:10px;
}

/* ================= GAME ================= */
#game{
display:none;
position:fixed;
top:0;
left:0;
width:100%;
height:100%;
background:#555;
}

/* ROAD */
#road{
position:absolute;
left:50%;
transform:translateX(-50%);
width:140px;
height:100%;
background:#2b2b2b;
}

/* CAR */
#car{
position:absolute;
bottom:120px;
left:50%;
width:50px;
height:90px;
background:red;
border-radius:8px;
}

/* ENEMY */
.enemy{
position:absolute;
width:50px;
height:90px;
background:yellow;
top:-120px;
}

/* SCORE */
#score{
position:absolute;
top:10px;
left:10px;
color:white;
font-size:22px;
z-index:5;
}

/* ================= CONTROLS FIX ================= */
#controls{
position:absolute;
bottom:15px;
left:0;
width:100%;
display:flex;
justify-content:space-between;
align-items:center;
padding:0 15px;
box-sizing:border-box;
z-index:50;
}

.btn{
width:75px;
height:75px;
border-radius:50%;
border:none;
font-size:32px;
background:rgba(255,255,255,0.3);
color:white;
touch-action:none;
display:flex;
justify-content:center;
align-items:center;
}

/* GAME OVER */
#over{
display:none;
position:absolute;
top:50%;
left:50%;
transform:translate(-50%,-50%);
color:white;
text-align:center;
z-index:100;
}
</style>
</head>

<body>

<!-- ================= CALC ================= -->
<div id="calc">
<div id="box">

<input id="ekran" placeholder="Hesap">

<div class="grid">

<button onclick="add('7')">7</button>
<button onclick="add('8')">8</button>
<button onclick="add('9')">9</button>
<button onclick="add('/')">/</button>

<button onclick="add('4')">4</button>
<button onclick="add('5')">5</button>
<button onclick="add('6')">*</button>
<button onclick="add('-')">-</button>

<button onclick="add('1')">1</button>
<button onclick="add('2')">2</button>
<button onclick="add('3')">3</button>
<button onclick="add('+')">+</button>

<button onclick="add('0')">0</button>
<button onclick="run()">OK</button>
<button onclick="clearE()" style="grid-column:span 2;background:red;">C</button>

</div>

<button id="startBtn" onclick="startGame()">START</button>

</div>
</div>

<!-- ================= GAME ================= -->
<div id="game">

<div id="road"></div>

<div id="score">0</div>
<div id="car"></div>

<div id="controls">
<button class="btn" id="left">◀</button>
<button class="btn" id="right">▶</button>
</div>

<div id="over">
<h1>GAME OVER</h1>
<button onclick="location.reload()">RESTART</button>
</div>

</div>

<script>

/* ================= CALC ================= */
function add(v){
document.getElementById("ekran").value+=v;
}

function clearE(){
document.getElementById("ekran").value="";
}

/* 2727 SYSTEM */
function run(){
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

/* START GAME */
let calc=document.getElementById("calc");
let game=document.getElementById("game");
let car=document.getElementById("car");
let over=document.getElementById("over");

function startGame(){
calc.style.display="none";
game.style.display="block";
}

/* ================= GAME LOGIC ================= */
let x=window.innerWidth/2;
let left=false,right=false;
let dead=false;
let score=0;

/* SCORE */
setInterval(()=>{
if(game.style.display==="block" && !dead){
score++;
document.getElementById("score").innerText=score;
}
},100);

/* ENEMIES */
function spawn(){
let e=document.createElement("div");
e.className="enemy";
e.style.left=Math.random()*(window.innerWidth-60)+"px";
document.body.appendChild(e);

let y=-120;

let m=setInterval(()=>{

y+=6;
e.style.top=y+"px";

let a=car.getBoundingClientRect();
let b=e.getBoundingClientRect();

if(!(a.right<b.left||a.left>b.right||a.bottom<b.top||a.top>b.bottom)){
dead=true;
over.style.display="block";
}

if(y>window.innerHeight){
e.remove();
clearInterval(m);
}

},20);
}

setInterval(spawn,800);

/* CONTROLS FIX (NO OUTSIDE) */
function hold(btn,dir){
btn.addEventListener("touchstart",(e)=>{
e.preventDefault();
if(dir==="l")left=true;
else right=true;
});

btn.addEventListener("touchend",(e)=>{
e.preventDefault();
if(dir==="l")left=false;
else right=false;
});
}

hold(document.getElementById("left"),"l");
hold(document.getElementById("right"),"r");

/* MOVE LOOP */
function loop(){
if(game.style.display==="block"){
if(left)x-=7;
if(right)x+=7;

if(x<20)x=20;
if(x>window.innerWidth-70)x=window.innerWidth-70;

car.style.left=x+"px";
}
requestAnimationFrame(loop);
}
loop();

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
