import os
from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

DOGRU_KULLANICI = "mustafa"
DOGRU_SIFRE = "kurt"

# GİRİŞ SAYFASI
login_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Giriş</title>
</head>
<body style="background:#03152d;color:white;text-align:center;padding-top:100px;">

<h1>Giriş</h1>

<form method="POST">
<input name="kullanici" placeholder="Kullanıcı"><br><br>
<input name="sifre" type="password" placeholder="Şifre"><br><br>
<button type="submit">Giriş</button>
</form>

<p style="color:red;">{{ hata }}</p>

</body>
</html>
"""

# OYUN SAYFASI
calc_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Oyun</title>
</head>
<body style="background:black;color:white;text-align:center;">

<h1>Hesap Makinası + Oyun</h1>

<input id="ekran">
<br><br>

<button onclick="t('1')">1</button>
<button onclick="t('2')">2</button>
<button onclick="t('+')">+</button>
<button onclick="h()">=</button>

<script>
function t(x){
document.getElementById("ekran").value += x;
}

function h(){
let v = document.getElementById("ekran").value;
if(v == "0000"){
alert("Oyun Açılıyor!");
}
else{
document.getElementById("ekran").value = eval(v);
}
}
</script>

</body>
</html>
"""

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