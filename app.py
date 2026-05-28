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
body{margin:0;background:#03152d;height:100vh;display:flex;justify-content:center;align-items:center;font-family:Arial;}
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
body{
margin:0;
background:#444;
overflow:hidden;
touch-action:none;
position:fixed;
width:100%;
height:100%;
font-family:Arial;
}

/* MENU */
#menu{
position:absolute;
top:0;left:0;
width:100%;height:100%;
background:#111;
display:flex;
flex-direction:column;
justify-content:center;
align-items:center;
color:white;
}

.menuBtn{
width:200px;
padding:15px;
margin:10px;
font-size:18px;
border:none;
border-radius:10px;
background:#0d6efd;
color:white;
}

/* GAME */
#game{display:none;width:100%;height:100%;}

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

/* BUTTONS */
#kontroller{
position:absolute;
bottom:25px;
width:100%;
display:flex;
justify-content:space-between;
padding:0 30px;
}

.btn{
width:90px;
height:90px;
border-radius:50%;
border:none;
font-size:40px;
background:rgba(255,255,255,0.25);
color:white;
}

/* SKIN */
#skinPanel{
position:absolute;
top:60px;
right:10px;
background:rgba(0,0,0,0.5);
padding:10px;
border-radius:10px;
}
.skinBtn{
display:block;
margin:5px 0;
padding:6px;
border:none;
color:white;
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

<!-- MENU -->
<div id="menu">
<h1>🚗 CAR GAME</h1>
<button class="menuBtn" onclick="start()">BAŞLA</button>
</div>

<!-- GAME -->
<div id="game">

<div id="skor">SKOR: 0</div>
<div id="araba"></div>

<div id="skinPanel">
<button onclick="skin('red')" style="background:red;color:white;">Kırmızı</button>
<button onclick="skin('blue')" style="background:blue;color:white;">Mavi</button>
<button onclick="skin('green')" style="background:green;color:white;">Yeşil</button>
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

let menu=document.getElementById("menu");
let game=document.getElementById("game");
let araba=document.getElementById("araba");
let over=document.getElementById("over");

let x=window.innerWidth/2;
let left=false,right=false;
let skor=0;
let dead=false;

/* CALC START */
function start(){
menu.style.display="none";
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
