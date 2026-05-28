from flask import Flask, request, render_template_string, redirect, url_for
import os

app = Flask(__name__)

DOGRU_KULLANICI = "mustafa"
DOGRU_SIFRE = "kurt"

# =========================
# GİRİŞ SAYFASI
# =========================
login_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Giriş</title>
<style>
body{margin:0;font-family:Arial;background:#03152d;display:flex;justify-content:center;align-items:center;height:100vh;}
.box{background:#13233d;padding:25px;border-radius:15px;width:90%;max-width:400px;color:white;text-align:center;}
input,button{width:100%;padding:12px;margin-top:10px;border:none;border-radius:8px;}
button{background:#0d6efd;color:white;font-size:16px;}
.error{color:red;margin-top:10px;}
</style>
</head>
<body>

<div class="box">
<h2>Giriş Yap</h2>

<form method="POST">
<input name="kullanici" placeholder="Kullanıcı">
<input type="password" name="sifre" placeholder="Şifre">
<button type="submit">Giriş</button>
</form>

<p class="error">{{ hata }}</p>
</div>

</body>
</html>
"""

# =========================
# OYUN + HESAP MAKİNESİ
# =========================
calc_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Oyun</title>
<style>
body{margin:0;background:black;color:white;font-family:Arial;text-align:center;}
#box{margin-top:50px;}
input{padding:10px;font-size:20px;width:80%;}
button{padding:10px;margin:5px;font-size:18px;}
</style>
</head>
<body>

<div id="box">
<h2>Hesap Makinesi</h2>

<input id="ekran">

<br>

<button onclick="ekle('1')">1</button>
<button onclick="ekle('2')">2</button>
<button onclick="ekle('+')">+</button>
<button onclick="hesapla()">=</button>

<script>
function ekle(x){
document.getElementById("ekran").value += x;
}

function hesapla(){
let v = document.getElementById("ekran").value;

if(v == "0000"){
alert("Gizli oyun açılıyor!");
return;
}

try{
document.getElementById("ekran").value = eval(v);
}catch{
document.getElementById("ekran").value = "HATA";
}
}
</script>

</div>

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


# =========================
# RENDER UYUMLU START
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
