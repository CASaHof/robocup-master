// TODO: Implement multiple balls.
// TODO: Implement current state (running, paused, etc.) - maybe some overlays?
// TODO: Implement goals? Display score / Display GOAL EFFECT WITH NUCLEAR BOMB EXPLOSION
// TBC: GOAL DETECTION MANUALLY?AUTOMATICALLY?

var ws = new WebSocket("ws://localhost:8765");
var local_robots = [];

ws.onopen = function () {
  ws.send(JSON.stringify({ type: "auth", token: "61OfXnt2prlDjM2xUb3S" }));
  console.log("Message is sent...");
};

wasUpdated = false;
ws.onmessage = function (evt) {
  // if(wasUpdated) return
  wasUpdated = true;
  var received_msg = JSON.parse(evt.data);
  if ("time_remaining" in received_msg) {
    document.getElementById("time").innerHTML = new Date(
      received_msg.time_remaining
    ).toLocaleTimeString();
  }
  removeDynObjects();
  for (let i = 0; i < received_msg.balls.length; i++) {
    var ball = document.createElement("div");
    ball.classList.add("ball");
    document.getElementsByClassName("field")[0].append(ball);
    ball.style.left = received_msg.balls[i].x * 100 + "%";
    ball.style.top = 100 - received_msg.balls[i].y * 100 + "%";
  }
  console.log("Message is received...", received_msg);

  for (let i = 0; i < received_msg.robots.length; i++) {
    local_robots[i] = document.createElement("div");
    local_robots[i].classList.add("robot");
    // robot.style.background = received_msg.robots[i].id;
    document.getElementsByClassName("field")[0].append(local_robots[i]);
    local_robots[i].style.left = received_msg.robots[i].x * 100 + "%";
    local_robots[i].style.top = 100 - received_msg.robots[i].y * 100 + "%";
    local_robots[
      i
    ].style.transform = `rotate(${received_msg.robots[i].angle}deg)`;
  }

  document.getElementsByClassName;
  // if(Math.random() < 0.9){
  //     document.getElementById("message").style.display = "unset"
  // }
};

//TODO

ws.onclose = function () {
  console.log("Connection is closed...");
};

function removeDynObjects() {
  var oldball = document.getElementsByClassName("ball");
  for (let i = 0; i < oldball.length; i++) {
    oldball[i].remove();
  }
  for (let i = 0; i < local_robots.length; i++) {
    local_robots[i].remove();
  }

  document.getElementById("message").style.display = "none";
}
