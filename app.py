# requirements.txt
# flask
# flask-socketio
# eventlet

from flask import Flask, render_template_string, request
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# ONLINE PLAYERS
players = {}
counter = 1

html = """

<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Neon Multiplayer</title>

<script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>

<style>

body{
margin:0;
background:#071014;
font-family:Arial;
overflow:hidden;
color:white;
}

#nameBox{
position:absolute;
top:10px;
left:10px;
font-size:22px;
z-index:20;
}

#menu{
position:absolute;
top:50%;
left:50%;
transform:translate(-50%,-50%);
background:#111827;
padding:20px;
border-radius:20px;
width:300px;
text-align:center;
z-index:20;
}

.btn{
width:100%;
padding:15px;
margin-top:10px;
border:none;
border-radius:12px;
background:#0891b2;
color:white;
font-size:18px;
}

#playersPanel{
display:none;
position:absolute;
top:50%;
left:50%;
transform:translate(-50%,-50%);
background:#111827;
padding:20px;
border-radius:20px;
width:300px;
z-index:30;
}

.playerRow{
display:flex;
justify-content:space-between;
align-items:center;
margin-top:10px;
background:#1f2937;
padding:10px;
border-radius:10px;
}

#inviteBox{
display:none;
position:absolute;
top:20px;
left:50%;
transform:translateX(-50%);
background:#1f2937;
padding:20px;
border-radius:15px;
z-index:50;
text-align:center;
}

#countdown{
display:none;
position:absolute;
top:50%;
left:50%;
transform:translate(-50%,-50%);
font-size:120px;
font-weight:bold;
z-index:100;
}

</style>
</head>

<body>

<div id="nameBox">
YÜKLENİYOR...
</div>

<div id="menu">

<h1>NEON RACE</h1>

<button class="btn">
TEKRAR OYNA
</button>

<button class="btn">
1V1
</button>

<button class="btn" onclick="openPlayers()">
MULTIPLAYER
</button>

</div>

<div id="playersPanel">

<h2>AKTİF OYUNCULAR</h2>

<div id="playersList"></div>

</div>

<div id="inviteBox">

<h2 id="inviteText"></h2>

<button class="btn" onclick="acceptInvite()">
KABUL ET
</button>

<button class="btn" onclick="rejectInvite()">
REDDET
</button>

</div>

<div id="countdown">
5
</div>

<script>

const socket = io();

let myName = "";
let inviteFrom = null;

/* JOIN */

socket.on("welcome",(data)=>{

myName = data.name;

document.getElementById("nameBox").innerText =
myName;

});

/* PLAYERS */

socket.on("players",(list)=>{

let box = document.getElementById("playersList");

box.innerHTML = "";

let count = 0;

for(let id in list){

if(list[id].name !== myName){

count++;

box.innerHTML += `
<div class="playerRow">

<span>${list[id].name}</span>

<button onclick="invitePlayer('${id}')">
DAVET ET
</button>

</div>
`;

}

}

if(count===0){

box.innerHTML = "<h3>NO FRIEND</h3>";

}

});

/* OPEN PANEL */

function openPlayers(){

document.getElementById("playersPanel").style.display =
"block";

socket.emit("get_players");

}

/* INVITE */

function invitePlayer(id){

socket.emit("invite",{
target:id
});

}

/* RECEIVE INVITE */

socket.on("invite_received",(data)=>{

inviteFrom = data.id;

document.getElementById("inviteBox").style.display =
"block";

document.getElementById("inviteText").innerText =
data.name + " seni VS çağırıyor";

});

/* ACCEPT */

function acceptInvite(){

socket.emit("accept_invite",{
target:inviteFrom
});

document.getElementById("inviteBox").style.display =
"none";

}

/* REJECT */

function rejectInvite(){

socket.emit("reject_invite",{
target:inviteFrom
});

document.getElementById("inviteBox").style.display =
"none";

}

/* REJECTED */

socket.on("invite_rejected",(data)=>{

alert(data.name + " reddetti");

});

/* START MATCH */

socket.on("start_match",()=>{

startCountdown();

});

/* COUNTDOWN */

function startCountdown(){

let cd = document.getElementById("countdown");

cd.style.display = "block";

let n = 5;

cd.innerText = n;

let timer = setInterval(()=>{

n--;

cd.innerText = n;

if(n<=0){

clearInterval(timer);

cd.innerText = "GO!";

setTimeout(()=>{

cd.style.display="none";

startGame();

},1000);

}

},1000);

}

/* GAME */

function startGame(){

alert("15 CANLIK MULTIPLAYER BAŞLADI");

}

</script>

</body>
</html>

"""

@app.route("/")
def home():
    return render_template_string(html)

@socketio.on("connect")
def connect():

    global counter

    name = f"Nome {counter}"

    players[request.sid] = {
        "name": name
    }

    counter += 1

    emit("welcome",{
        "name": name
    })

    socketio.emit("players", players)

@socketio.on("disconnect")
def disconnect():

    if request.sid in players:
        del players[request.sid]

    socketio.emit("players", players)

@socketio.on("get_players")
def get_players():

    emit("players", players)

@socketio.on("invite")
def invite(data):

    target = data["target"]

    if target in players:

        socketio.emit(
            "invite_received",
            {
                "id": request.sid,
                "name": players[request.sid]["name"]
            },
            room=target
        )

@socketio.on("accept_invite")
def accept_invite(data):

    target = data["target"]

    socketio.emit(
        "start_match",
        room=target
    )

    emit("start_match")

@socketio.on("reject_invite")
def reject_invite(data):

    target = data["target"]

    socketio.emit(
        "invite_rejected",
        {
            "name": players[request.sid]["name"]
        },
        room=target
    )

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    socketio.run(
        app,
        host="0.0.0.0",
        port=port
    )
