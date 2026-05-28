from flask import Flask, request, render_template_string, redirect, url_for
import os

app = Flask(__name__)

DOGRU_KULLANICI = "mustafa"
DOGRU_SIFRE = "kurt"

# =========================
# LOGIN EKRANI
# =========================
login_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Giriş</title>
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
<h2>Giriş Yap</h2>
<form method="POST">
<input name="kullanici" placeholder="Kullanıcı">
<input type="password" name="sifre" placeholder="Şifre">
<button>Giriş</button>
</form>
<p class="error">{{ hata }}</p>
</div>

</body>
</html>
"""

# =========================
# OYUN + HESAP MAKİNESİ (SENİN KODUN)
# =========================
calc_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Oyun</title>

<style>
body{
margin:0;
background:black;
overflow:hidden;
font-family:Arial;
user-select:none;
}

.box{
position:absolute;
top:50%;
left:50%;
transform:translate(-50%,-50%);
width:95%;
max-width:420px;
background:#111;
padding:20px;
border-radius:20px;
}

input{
width:100%;
padding:15px;
font-size:22px;
text-align:right;
border:none;
border-radius:10px;
margin-bottom:15px;
}

.grid{
display:grid;
grid-template-columns:repeat(4,1fr);
gap:8px;
}

button{
padding:18px;
font-size:20px;
border:none;
border-radius:10px;
background:#222;
color:white;
}

/* OYUN */
#oyun{
display:none;
position:fixed;
top:0;
left:0;
width:100%;
height:100%;
background:#555;
}

.serit{
position:absolute;
left:47%;
width:20px;
height:180px;
background:white;
animation:yol 1s linear infinite;
}

@keyframes yol{
from{transform:translateY(-300px);}
to{transform:translateY(120vh);}
}

#araba{
position:absolute;
bottom:120px;
left:45%;
width:45px;
height:80px;
background:red;
border-radius:10px;
}

.engel{
position:absolute;
width:50px;
height:20px;
background:yellow;
border-radius:6px;
top:-50px;
}

#skor{
position:absolute;
top:20px;
left:20px;
color:white;
font-size:25px;
}
</style>
</head>

<body>

<!-- HESAP MAKİNESİ -->
<div class="box" id="hesap">
<h2 style="color:white">Hesap Makinesi</h2>

<input id="ekran">

<div class="grid">
<button onclick="ekle('7')">7</button>
<button onclick="ekle('8')">8</button>
<button onclick="ekle('9')">9</button>
<button onclick="ekle('/')">/</button>

<button onclick="ekle('4')">4</button>
<button onclick="ekle('5')">5</button>
<button onclick="ekle('6')">6</button>
<button onclick="ekle('*')">*</button>

<button onclick="ekle('1')">1</button>
<button onclick="ekle('2')">2</button>
<button onclick="ekle('3')">3</button>
<button onclick="ekle('-')">-</button>

<button onclick="ekle('0')">0</button>
<button onclick="ekle('.')">.</button>
<button onclick="hesapla()">=</button>
<button onclick="ekle('+')">+</button>

<button onclick="temizle()" style="grid-column:span 4;background:red;">C</button>
</div>
</div>

<!-- OYUN -->
<div id="oyun">

<div class="serit"></div>
<div class="serit" style="top:-200px;"></div>

<div id="skor">SKOR: 0</div>

<div id="araba"></div>

</div>

<script>

let araba = document.getElementById("araba");
let skorText = document.getElementById("skor");
let oyun = document.getElementById("oyun");
let hesap = document.getElementById("hesap");

let skor = 0;
let bitti = false;
let x = window.innerWidth/2;

function ekle(v){
document.getElementById("ekran").value += v;
}

function temizle(){
document.getElementById("ekran").value = "";
}

function hesapla(){
let v = document.getElementById("ekran").value;

if(v === "0000"){
oyunBaslat();
return;
}

try{
document.getElementById("ekran").value = eval(v);
}catch{
document.getElementById("ekran").value = "ERROR";
}
}

function oyunBaslat(){
hesap.style.display = "none";
oyun.style.display = "block";

setInterval(()=>{
if(bitti) return;

skor++;
skorText.innerHTML = "SKOR: " + skor;

},100);
}

</script>

</body>
</html>
"""

# =========================
# ROUTES
# =========================
@app.route("/", methods=["GET","POST"])
def login():
    hata = ""

    if request.method == "POST":
        k = request.form.get("kullanici")
        s = request.form.get("sifre")

        if k == DOGRU_KULLANICI and s == DOGRU_SIFRE:
            return redirect(url_for("calc"))
        else:
            hata = "Hatalı giriş!"

    return render_template_string(login_html, hata=hata)


@app.route("/calc")
def calc():
    return render_template_string(calc_html)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
