from flask import Flask, request, render_template_string, redirect, url_for
import os

app = Flask(__name__)

# ================= LOGIN =================
login_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Login</title>
<style>
body{
margin:0;
height:100vh;
display:flex;
justify-content:center;
align-items:center;
background:#0b1a2b;
font-family:Arial;
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

input,button{
width:100%;
padding:12px;
margin-top:10px;
border:none;
border-radius:10px;
}

button{
background:#0d6efd;
color:white;
font-size:18px;
}

.error{color:red;margin-top:10px;}
</style>
</head>
<body>

<div class="box">
<h2>Giriş Sistemi</h2>

<form method="POST">
<input name="user" placeholder="Kullanıcı adı">
<button>Giriş</button>
</form>

<p class="error">{{error}}</p>

</div>

</body>
</html>
"""

# ================= GAME =================
game_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>Game</title>

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
position:fixed;
inset:0;
display:flex;
justify-content:center;
align-items:center;
background:#111;
z-index:10;
}

#box{
width:92%;
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

#score{
position:absolute;
top:10px;
left:10px;
color:white;
font-size:22px;
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
padding:0 35px;
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

<!-- ================= LOGIN ================= -->
<div id="login" style="position:fixed;inset:0;display:flex;justify-content:center;align-items:center;background:#0b1a2b;z-index:20;">
<div style="width:90%;max-width:360px;background:#13233d;padding:25px;border-radius:20px;text-align:center;color:white;">
<h2>Giriş</h2>

<form method="POST">
<input name="user" style="width:100%;padding:12px;border:none;border-radius:10px;" placeholder="Kullanıcı adı">
<button style="width:100%;margin-top:10px;padding:12px;border:none;border-radius:10px;background:#0d6efd;color:white;">Giriş</button>
</form>

<p style="color:red;">{{error}}</p>

</div>
</div>

<!-- ================= CALC ================= -->
<div id="calc" style="display:none;">
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
<button onclick="restart()">RESTART</button>
</div>

</div>

<script>

/* LOGIN SWITCH (Musti) */
document.querySelector("form").addEventListener("submit",function(e){
let u=document.querySelector("input[name='user']").value;
if(u!=="Musti"){
e.preventDefault();
alert("Hatalı kullanıcı adı!");
}
else{
e.preventDefault();
document.getElementById("login").style.display="none";
document.getElementById("calc").style.display="flex";
}
});

/* CALC */
function add(v){
document.getElementById("ekran").value+=v;
}

function clearE(){
document.getElementById("ekran").value="";
}

/* 2727 */
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

/* GAME START */
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

/* RESTART */
function restart(){
dead=false;
score=0;
over.style.display="none";
x=window.innerWidth/2;
car.style.left=x+"px";
}

/* SCORE */
setInterval(()=>{
if(game.style.display==="block" && !dead){
score++;
document.getElementById("score").innerText=score;
}
},100);

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

@app.route("/", methods=["GET","POST"])
def login():
    error=""
    return render_template_string(game_html,error=error)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
