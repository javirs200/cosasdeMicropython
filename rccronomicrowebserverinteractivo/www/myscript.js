// Let us open a web socket
var ws = new WebSocket("ws://"+ location.host +"/ws");

var received_msg = "";

var tabletime

var timeToStore = "";

var lap = 0;

var timeSelected = false;
var timeSelected_id

document.addEventListener('click', function(e) {
   e = e || window.event;
   var target = e.target;
   if(target.id.includes('lap')){
      target.style.backgroundColor = "red";
      if(timeSelected){
         if(target.id != timeSelected_id){
            document.getElementById(timeSelected_id).style.backgroundColor = "yellow"
         }
      }
      timeSelected_id = target.id;
      timeSelected = true;
   }
}, false);


function WebSocketTest() {

   tabletime = document.getElementById('timetable')

   console.log(tabletime)

   if ("WebSocket" in window) {
      alert("WebSocket is supported by your Browser!");

      ws.onopen = function () {
         alert("WS is connected");
      };

      ws.onmessage = function (evt) {
         received_msg = evt.data;
         console.log("ws recivido : " + received_msg)
         if(received_msg.includes(':')){
            lap += 1;
            timeToStore = received_msg;
            var row = tabletime.insertRow(0)
            var cell = row.insertCell(0);
            cell.id = "lap" + lap
            cell.innerHTML = received_msg;
         }
      };

      ws.onclose = function () {
         alert("Connection is closed...");
      };
   } else {
      alert("WebSocket NOT supported by your Browser!");
   }
}

function save() {
   var cell = document.getElementById(timeSelected_id)
   console.log(timeSelected_id)
   var timetext = cell.innerHTML;
   cell.style.backgroundColor = "green";
   var storeString = "store " + cell.id + " " + timetext;
   console.log(storeString)
   ws.send(storeString)
   timeSelected_id = undefined
   timeSelected = false;
   
}



