from flask import Flask, request, render_template_string, redirect, url_for
import os

app = Flask(__name__)

USER = "mustafa"
PASS = "kurt"

# =========================
# LOGIN
# =========================
login_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Login</title>
</head>
<body style="margin:0;background:#03152d;color:white;font-family:Arial;display:flex;justify-content:center;align-items:center;height:100vh;">

<div style="width:90%;max-width:400px;background:#13233d;padding:25px;border-radius:15px;text-align:center;">
<h2>Giriş</h2>

<form method="POST">
<input name="user" placeholder="Kullanıcı" style="width:100%;padding:10px;margin:5px 0;"><br>
<input type="password" name="pass" placeholder="Şifre" style="width:100%;padding:10px;margin:5px 0;"><br>
<button style="width:100%;padding:10px;background:#0d6efd;color:white;border:none;">Giriş</button>
</form>

<p style="color:red;">{{ error }}</p>
</div>

</body>
</html>
"""

# =========================
# SMOOTH JOYSTICK GAME
# =========================
game_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Smooth Car Game</title>

<style>
body{
margin:0;
background:#444;
overflow:hidden;
font-family:Arial;
}

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
transition:transform 0.05s linear;
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

/* JOYSTICK */
#joyArea{
position:absolute;
bottom:30px;
left:30px;
width:120px;
height:120px;
background:rgba(255,255,255,0.1);
border-radius:50%;
}

#stick{
position:absolute;
top:40px;
left:40px;
width:40px;
height:40px;
background:white;
border-radius:50%;
}
</style>
</head>

<body>

<div id="skor">SKOR: 0</div>
<div id="araba"></div>

<div id="joyArea">
<div id="stick"></div>
</div>

<script>

let araba = document.getElementById("araba");
let skorText = document.getElementById("skor");
let stick = document.getElementById("stick");
let area = document.getElementById("joyArea");

let targetX = window.innerWidth / 2;
let posX = targetX;
let velocity = 0;

let skor = 0;

/* SKOR */
setInterval(()=>{
skor++;
skorText.innerHTML = "SKOR: " + skor;
},100);

/* ENGEL */
function engel(){
let e = document.createElement("div");
e.className = "engel";
e.style.left = Math.random() * (window.innerWidth - 60) + "px";
document.body.appendChild(e);

let y = -50;

let move = setInterval(()=>{

y += 6;
e.style.top = y + "px";

let a = araba.getBoundingClientRect();
let b = e.getBoundingClientRect();

if(!(a.right < b.left || a.left > b.right || a.bottom < b.top || a.top > b.bottom)){
alert("GAME OVER");
location.reload();
}

if(y > window.innerHeight){
e.remove();
clearInterval(move);
}

},20);
}

setInterval(()=>engel(), 600);

/* 🔥 SMOOTH PHYSICS LOOP */
function loop(){

// easing (çok akıcı geçiş)
velocity += (targetX - posX) * 0.15;
velocity *= 0.75;
posX += velocity;

araba.style.left = posX + "px";

requestAnimationFrame(loop);
}
loop();

/* JOYSTICK */
let active = false;

area.addEventListener("touchstart", ()=> active = true);

area.addEventListener("touchend", ()=>{
active = false;
targetX = posX;
stick.style.left = "40px";
stick.style.top = "40px";
});

area.addEventListener("touchmove", (e)=>{

let rect = area.getBoundingClientRect();
let t = e.touches[0];

let dx = t.clientX - rect.left - 60;

if(dx > 50) dx = 50;
if(dx < -50) dx = -50;

targetX = window.innerWidth/2 + dx * 6;

// stick hareket
stick.style.left = (40 + dx) + "px";

});

</script>

</body>
</html>
"""

# =========================
# ROUTES
# =========================
@app.route("/", methods=["GET","POST"])
def login():
    error = ""

    if request.method == "POST":
        u = request.form.get("user")
        p = request.form.get("pass")

        if u == USER and p == PASS:
            return redirect(url_for("game"))
        else:
            error = "Hatalı giriş!"

    return render_template_string(login_html, error=error)


@app.route("/game")
def game():
    return render_template_string(game_html)


# =========================
# RENDER START
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
