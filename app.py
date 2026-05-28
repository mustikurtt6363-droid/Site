from flask import Flask, request, render_template_string, redirect, url_for
import os

app = Flask(__name__)

USER="mustafa"
PASS="kurt"

login_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Login</title>
<style>
body{margin:0;height:100vh;display:flex;justify-content:center;align-items:center;background:#03152d;font-family:Arial;}
.box{width:90%;max-width:400px;background:#13233d;padding:25px;border-radius:20px;color:white;text-align:center;}
input,button{width:100%;padding:12px;margin-top:10px;border:none;border-radius:10px;}
button{background:#0d6efd;color:white;font-size:18px;}
.error{color:red;margin-top:10px;}
</style>
</head>
<body>
<div class="box">
<h2>Giriş</h2>
<form method="POST">
<input name="user">
<input type="password" name="pass">
<button>Giriş</button>
</form>
<p class="error">{{error}}</p>
</div>
</body>
</html>
"""

game_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">

<title>Game</title>

<style>
html,body{
margin:0;
padding:0;
overflow:hidden;
width:100%;
height:100%;
background:#444;
touch-action:none;
user-select:none;
}

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

#ekran{width:100%;padding:15px;font-size:22px;text-align:right;}

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

/* GAME */
#game{
display:none;
position:fixed;
top:0;left:0;
width:100%;height:100%;
}

#skor{
position:absolute;
top:10px;
left:10px;
color:white;
font-size:22px;
z-index:10;
}

#araba{
position:absolute;
bottom:120px;
left:50%;
width:55px;
height:95px;
background:red;
border-radius:10px;
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
top:-60px;
}

/* CONTROLS (İÇERİ ALINDI) */
#kontroller{
position:absolute;
bottom:40px;
width:100%;
display:flex;
justify-content:space-between;
padding:0 40px;
box-sizing:border-box;
}

.btn{
width:80px;
height:80px;
border-radius:50%;
border:none;
font-size:35px;
background:rgba(255,255,255,0.25);
color:white;
touch-action:none;
user-select:none;
}

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

<!-- CALC -->
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
<button onclick="calc()">=</button>
<button onclick="clearE()" style="grid-column:span 2;background:red;">C</button>
</div>
</div>

<!-- GAME -->
<div id="game">

<div id="skor">0</div>
<div id="araba"></div>

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
document.getElementById("ekran").value+=v;
}

function clearE(){
document.getElementById("ekran").value="";
}

function calc(){
let v=document.getElementById("ekran").value;
if(v==="0000"){ start(); return; }
try{document.getElementById("ekran").value=eval(v);}
catch{document.getElementById("ekran").value="ERROR";}
}

/* GAME */
let calcBox=document.getElementById("calc");
let game=document.getElementById("game");
let araba=document.getElementById("araba");
let over=document.getElementById("over");

let x=window.innerWidth/2;
let left=false,right=false;
let dead=false;
let skor=0;

/* START */
function start(){
calcBox.style.display="none";
game.style.display="block";
}

/* SKOR */
setInterval(()=>{
if(!dead && game.style.display==="block"){
skor++;
document.getElementById("skor").innerText=skor;
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

if(game.style.display==="none") return;

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

/* CONTROLS (TAKILMA FIX) */
function hold(btn,dir){
btn.addEventListener("touchstart",(e)=>{e.preventDefault(); if(dir==="l") left=true; else right=true;});
btn.addEventListener("touchend",(e)=>{e.preventDefault(); if(dir==="l") left=false; else right=false;});
}

hold(document.getElementById("left"),"l");
hold(document.getElementById("right"),"r");

/* MOVE (SMOOTH) */
function loop(){
if(game.style.display==="block"){
if(left)x-=7;
if(right)x+=7;

if(x<10)x=10;
if(x>window.innerWidth-70)x=window.innerWidth-70;

araba.style.left=x+"px";
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
    if request.method=="POST":
        u=request.form.get("user")
        p=request.form.get("pass")
        if u==USER and p==PASS:
            return redirect(url_for("game"))
        error="Hatalı giriş"
    return render_template_string(login_html,error=error)

@app.route("/game")
def game_route():
    return render_template_string(game_html)

if __name__=="__main__":
    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
