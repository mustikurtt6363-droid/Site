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
position:fixed;
touch-action:none;
user-select:none;
}

/* ================= LOGIN ================= */
#login{
position:fixed;
inset:0;
display:flex;
justify-content:center;
align-items:center;
background:#0b1a2b;
z-index:100;
}

.loginBox{
width:90%;
max-width:360px;
background:#13233d;
padding:25px;
border-radius:20px;
color:white;
text-align:center;
}

/* ================= CALC ================= */
#calc{
position:fixed;
inset:0;
display:none;
justify-content:center;
align-items:center;
background:#111;
z-index:10;
}

#box{
width:92%;
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
border-radius:8px;
}

#startBtn{
display:none;
margin-top:10px;
width:100%;
padding:15px;
background:#0d6efd;
color:white;
border:none;
border-radius:10px;
font-size:18px;
}

/* ================= GAME ================= */
#game{
display:none;
position:fixed;
inset:0;
background:#555;
}

#road{
position:absolute;
left:50%;
transform:translateX(-50%);
width:140px;
height:100%;
background:#2b2b2b;
}

#car{
position:absolute;
bottom:120px;
left:50%;
width:50px;
height:90px;
background:red;
border-radius:8px;
}

.enemy{
position:absolute;
width:50px;
height:90px;
background:yellow;
top:-120px;
}

.coin{
position:absolute;
width:25px;
height:25px;
border-radius:50%;
background:gold;
top:-50px;
}

#score{
position:absolute;
top:10px;
left:10px;
color:white;
font-size:18px;
z-index:5;
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
}

.btn{
width:70px;
height:70px;
border-radius:50%;
border:none;
font-size:32px;
background:rgba(255,255,255,0.3);
color:white;
touch-action:none;
}

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

<!-- LOGIN -->
<div id="login">
<div class="loginBox">
<h2>Giriş</h2>
<input id="user" placeholder="Kullanıcı adı" style="width:100%;padding:12px;border:none;border-radius:10px;">
<button onclick="login()" style="width:100%;margin-top:10px;padding:12px;border:none;border-radius:10px;background:#0d6efd;color:white;">Giriş</button>
</div>
</div>

<!-- CALC -->
<div id="calc">
<div id="box">

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

<button id="startBtn" onclick="startGame()">START</button>

</div>
</div>

<!-- GAME -->
<div id="game">

<div id="road"></div>

<div id="score">Skor: 0 | Coin: 0 | HS: 0</div>
<div id="car"></div>

<div id="controls">
<button class="btn" id="left">◀</button>
<button class="btn" id="right">▶</button>
</div>

<div id="over">
<h1>GAME OVER</h1>
<button onclick="restart()">RESTART</button>
</div>

</div>

<script>

/* LOGIN */
function login(){
let u=document.getElementById("user").value;
if(u==="Musti"){
document.getElementById("login").style.display="none";
document.getElementById("calc").style.display="flex";
}else{
alert("Hatalı kullanıcı adı");
}
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
}

/* STATE */
let x=window.innerWidth/2;
let left=false,right=false;
let dead=false;

let score=0;
let coins=0;
let speed=6;
let highScore=localStorage.getItem("hs")||0;

/* UPDATE UI */
function updateUI(){
document.getElementById("score").innerText =
"Skor: "+score+" | Coin: "+coins+" | HS: "+highScore;
}

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

/* SCORE + SPEED */
setInterval(()=>{
if(game.style.display==="block" && !dead){
score++;
if(score%50===0) speed++;
updateUI();
}
},100);

/* COINS */
function spawnCoin(){
if(game.style.display!=="block") return;

let c=document.createElement("div");
c.className="coin";
c.style.left=Math.random()*(window.innerWidth-50)+"px";
document.body.appendChild(c);

let y=-50;

let m=setInterval(()=>{

if(dead){c.remove();clearInterval(m);return;}

y+=5;
c.style.top=y+"px";

let a=car.getBoundingClientRect();
let b=c.getBoundingClientRect();

if(!(a.right<b.left||a.left>b.right||a.bottom<b.top||a.top>b.bottom)){
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
function spawn(){
if(game.style.display!=="block") return;

let e=document.createElement("div");
e.className="enemy";
e.style.left=Math.random()*(window.innerWidth-60)+"px";
document.body.appendChild(e);

let y=-120;

let m=setInterval(()=>{

if(dead){e.remove();clearInterval(m);return;}

y+=speed;
e.style.top=y+"px";

let a=car.getBoundingClientRect();
let b=e.getBoundingClientRect();

if(!(a.right<b.left||a.left>b.right||a.bottom<b.top||a.top>b.bottom)){
dead=true;
if(score>highScore){
highScore=score;
localStorage.setItem("hs",highScore);
}
over.style.display="block";
}

if(y>window.innerHeight){
e.remove();
clearInterval(m);
}

},20);
}
setInterval(spawn,800);

/* CONTROLS */
function bind(btn,dir){
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

bind(document.getElementById("left"),"l");
bind(document.getElementById("right"),"r");

/* MOVE */
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
