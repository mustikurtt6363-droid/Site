from flask import Flask, request, render_template_string, redirect, url_for
import os

app = Flask(__name__)

USER = "mustafa"
PASS = "kurt"

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
background:#03152d;
height:100vh;
display:flex;
justify-content:center;
align-items:center;
font-family:Arial;
}

.box{
width:90%;
max-width:400px;
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
<input name="user" placeholder="Kullanıcı">
<input type="password" name="pass" placeholder="Şifre">
<button>Giriş</button>
</form>
<p class="error">{{ error }}</p>
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
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">

<title>Car Game</title>

<style>

/* GENEL */
html,body{
margin:0;
padding:0;
width:100%;
height:100%;
overflow:hidden;
background:#444;
font-family:Arial;
touch-action:none;
position:fixed;
}

/* ================= CALC ================= */
#calc{
position:absolute;
top:50%;
left:50%;
transform:translate(-50%,-50%);
width:90%;
max-width:380px;
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
}

/* ================= GAME ================= */
#game{
display:none;
width:100%;
height:100%;
position:fixed;
top:0;
left:0;
}

/* SKOR */
#skor{
position:absolute;
top:10px;
left:10px;
color:white;
font-size:22px;
z-index:10;
}

/* ARABA */
#araba{
position:absolute;
bottom:120px;
left:50%;
width:55px;
height:95px;
background:red;
border-radius:10px;
border:3px solid darkred;
}

#araba:before{
content:"";
position:absolute;
top:10px;
left:12px;
width:30px;
height:20px;
background:#87ceeb;
border-radius:5px;
}

/* ENGEL */
.engel{
position:absolute;
width:55px;
height:25px;
background:yellow;
border-radius:6px;
top:-60px;
}

/* CONTROLS */
#kontroller{
position:absolute;
bottom:25px;
width:100%;
display:flex;
justify-content:space-between;
padding:0 20px;
}

.btn{
width:85px;
height:85px;
border-radius:50%;
border:none;
font-size:36px;
background:rgba(255,255,255,0.25);
color:white;
}

/* SKIN PANEL (İÇERİ ALINDI) */
#skinPanel{
position:absolute;
top:60px;
right:15px;
background:rgba(0,0,0,0.5);
padding:8px;
border-radius:10px;
z-index:20;
max-width:110px;
}

.skinBtn{
display:block;
margin:4px 0;
padding:6px;
border:none;
color:white;
font-size:12px;
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
z-index:50;
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
<button onclick="add('6')">6</button>
<button onclick="add('*')">*</button>

<button onclick="add('1')">1</button>
<button onclick="add('2')">2</button>
<button onclick="add('3')">3</button>
<button onclick="add('-')">-</button>

<button onclick="add('0')">0</button>
<button onclick="add('.')">.</button>
<button onclick="calc()">=</button>
<button onclick="add('+')">+</button>

<button onclick="clearE()" style="grid-column:span 4;background:red;">C</button>
</div>
</div>

<!-- ================= GAME ================= -->
<div id="game">

<div id="skor">SKOR: 0</div>
<div id="araba"></div>

<div id="skinPanel">
<button class="skinBtn" style="background:red" onclick="skin('red')">K</button>
<button class="skinBtn" style="background:blue" onclick="skin('blue')">M</button>
<button class="skinBtn" style="background:green" onclick="skin('green')">Y</button>
</div>

<div id="kontroller">
<button class="btn" id="left">◀</button>
<button class="btn" id="right">▶</button>
</div>

<div id="over">
<h1>GAME OVER</h1>
<button onclick="location.reload()">TEKRAR</button>
</div>

</div>

<script>

/* CALC */
function add(v){
document.getElementById("ekran").value += v;
}

function clearE(){
document.getElementById("ekran").value="";
}

function calc(){
let v=document.getElementById("ekran").value;
if(v==="0000"){
start();
return;
}
try{
document.getElementById("ekran").value=eval(v);
}catch{
document.getElementById("ekran").value="ERROR";
}
}

/* GAME */
let calcBox=document.getElementById("calc");
let game=document.getElementById("game");
let araba=document.getElementById("araba");
let over=document.getElementById("over");

let x=window.innerWidth/2;
let left=false,right=false;
let skor=0;
let dead=false;

/* START */
function start(){
calcBox.style.display="none";
game.style.display="block";
}

/* SKIN */
function skin(c){
araba.style.background=c;
}

/* SKOR */
setInterval(()=>{
if(dead) return;
if(game.style.display==="block"){
skor++;
document.getElementById("skor").innerHTML="SKOR: "+skor;
}
},100);

/* ENGEL */
function engel(){
let e=document.createElement("div");
e.className="engel";
e.style.left=Math.random()*(window.innerWidth-60)+"px";
document.body.appendChild(e);

let y=-50;

let m=setInterval(()=>{

y+=6;
e.style.top=y+"px";

let a=araba.getBoundingClientRect();
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

setInterval(()=>engel(),700);

/* CONTROLS */
document.getElementById("left").addEventListener("touchstart",()=>left=true);
document.getElementById("left").addEventListener("touchend",()=>left=false);

document.getElementById("right").addEventListener("touchstart",()=>right=true);
document.getElementById("right").addEventListener("touchend",()=>right=false);

/* MOVE */
function loop(){
if(!dead && game.style.display==="block"){
if(left)x-=7;
if(right)x+=7;

if(x<0)x=0;
if(x>window.innerWidth-60)x=window.innerWidth-60;

araba.style.left=x+"px";
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
        p=request.form.get("pass")

        if u==USER and p==PASS:
            return redirect(url_for("game"))
        else:
            error="Hatalı giriş!"

    return render_template_string(login_html, error=error)


@app.route("/game")
def game():
    return render_template_string(game_html)


if __name__=="__main__":
    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
