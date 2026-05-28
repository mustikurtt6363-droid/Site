from flask import Flask, request, redirect, url_for, render_template_string
import os

app = Flask(__name__)

USER = "mustafa"
PASS = "kurt"

# ---------------- LOGIN ----------------
login_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Giriş</title>
</head>
<body style="background:#03152d;color:white;text-align:center;padding-top:100px;">

<h2>Giriş Yap</h2>

<form method="POST">
<input name="user" placeholder="Kullanıcı"><br><br>
<input name="pass" type="password" placeholder="Şifre"><br><br>
<button>Giriş</button>
</form>

<p style="color:red;">{{ error }}</p>

</body>
</html>
"""

# ---------------- CALCULATOR ----------------
calc_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Hesap Makinesi</title>
</head>
<body style="background:black;color:white;text-align:center;padding-top:50px;">

<h2>Hesap Makinesi</h2>

<input id="ekran" style="font-size:20px;padding:10px;width:200px;"><br><br>

<br>

<button onclick="ekle('7')">7</button>
<button onclick="ekle('8')">8</button>
<button onclick="ekle('9')">9</button>
<button onclick="ekle('/')">/</button><br>

<button onclick="ekle('4')">4</button>
<button onclick="ekle('5')">5</button>
<button onclick="ekle('6')">6</button>
<button onclick="ekle('*')">*</button><br>

<button onclick="ekle('1')">1</button>
<button onclick="ekle('2')">2</button>
<button onclick="ekle('3')">3</button>
<button onclick="ekle('-')">-</button><br>

<button onclick="ekle('0')">0</button>
<button onclick="ekle('.')">.</button>
<button onclick="hesapla()">=</button>
<button onclick="ekle('+')">+</button><br><br>

<button onclick="temizle()">C</button>

<script>
function ekle(x){
document.getElementById("ekran").value += x;
}

function temizle(){
document.getElementById("ekran").value = "";
}

function hesapla(){
let v = document.getElementById("ekran").value;

if(v === "0000"){
alert("Gizli mod açıldı!");
return;
}

try{
document.getElementById("ekran").value = eval(v);
}catch{
document.getElementById("ekran").value = "ERROR";
}
}
</script>

</body>
</html>
"""

# ---------------- ROUTES ----------------
@app.route("/", methods=["GET","POST"])
def login():
    error = ""

    if request.method == "POST":
        u = request.form.get("user")
        p = request.form.get("pass")

        if u == USER and p == PASS:
            return redirect(url_for("calc"))
        else:
            error = "Hatalı giriş!"

    return render_template_string(login_html, error=error)


@app.route("/calc")
def calc():
    return render_template_string(calc_html)


# ---------------- RENDER ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
