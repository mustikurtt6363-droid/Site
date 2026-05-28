from flask import Flask, request, render_template_string, redirect, url_for
import os

app = Flask(__name__)

USER = "Musti"

# ================= LOGIN =================
login_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Giriş</title>
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
<h2>Giriş</h2>

<form method="POST">
<input name="user" placeholder="Kullanıcı adı">
<button>Giriş</button>
</form>

<p class="error">{{error}}</p>
</div>

</body>
</html>
"""

# ================= CALC + GAME =================
game_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">

<title>System</title>

<style>
html,body{
margin:0;
padding:0;
width:100%;
height:100%;
overflow:hidden;
background:#333;
font-family:Arial;
touch-action:none;
user-select:none;
position:fixed;
}

/* ================= CALC ================= */
#calc{
position:absolute;
top:50%;
left:50%;
transform:translate(-50%,-50%);
width:90%;
max-width:360px;
background:#111;
padding:20px;
border-radius:15px;
}

#ekran{
width:100%;
padding:15px;
font-size:22px;
text-align:right;
}

.grid{
display:grid;
grid-template-columns:repeat(4,1fr);
gap:6px;
}

.grid button{
padding:15px;
border:none;
background:#222;
color:white;
font-size:18px;
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
.road{
position:absolute;
left:50%;
transform:translateX(-50%);
width:140px;
height:100%;
background:#2b2b2b;
}

/* LINES */
.line{
position:absolute;
left:50%;
transform:translateX(-50%);
width:6px;
height:80px;
background:white;
animation:move 1s linear infinite;
}

@keyframes move{
0%{top:-100px;}
100%{top:120vh;}
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
border-radius:8px;
}

/* SCORE */
#score{
position:absolute;
top:10px;
left:10px;
color:white;
font-size:22px;
}

/* CONTROLS (BOTTOM FIXED) */
#controls{
position:absolute;
bottom:0;
left:0;
width:100%;
display:flex;
justify-content:space-between;
padding:15px 25px;
box-sizing:border-box;
}

.btn{
width:90px;
height:90px;
border-radius:50%;
border:none;
background:rgba(255,255,255,0.25);
color:white;
font-size:40px;
touch-action:none;
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
}
</style>
</head>

<body>

<!-- ================= CALC ================= -->
<div id="calc">
<input id="ekran">

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
<button onclick="run()">ENTER</button>
<button onclick="clearE()" style="grid-column:span 2;background:red;">C</button>
</div>
</div>

<!-- ================= GAME ================= -->
<div id="game">

<div class="road"></div>

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

/* CALC */
function add(v){
document.getElementById("ekran").value+=v;
}

function clearE(){
document.getElementById("ekran").value="";
}

function run(){
let v=document.getElementById("ekran").value;

if(v==="2727"){
startGame();
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

let x=window.innerWidth/2;
let left=false,right=false;
let dead=false;
let score=0;

/* START */
function startGame(){
calc.style.display="none";
game.style.display="block";
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

/* CONTROLS (HOLD SMOOTH) */
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

# ================= ROUTES =================
@app.route("/", methods=["GET","POST"])
def login():
    error=""
    if request.method=="POST":
        u=request.form.get("user")

        if u=="Musti":
            return redirect(url_for("game"))
        else:
            error="Hatalı kullanıcı adı"

    return render_template_string(login_html,error=error)

@app.route("/game")
def game():
    return render_template_string(game_html)

if __name__=="__main__":
    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
