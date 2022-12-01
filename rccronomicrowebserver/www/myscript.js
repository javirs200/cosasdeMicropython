// Let us open a web socket
var ws = new WebSocket("ws://192.168.4.1/wstest");

var received_msg = "";
var hasTime = false;

function WebSocketTest() {
   if ("WebSocket" in window) {
      alert("WebSocket is supported by your Browser!");

      ws.onopen = function () {
         // Web Socket is connected, send data using send()
         //alert("WS is connected");
         alert("WS is connected");
      };

      ws.onmessage = function (evt) {
         received_msg = evt.data;
         hasTime = true;
         document.getElementById("dop").innerHTML = received_msg;
      };

      ws.onclose = function () {
         // websocket is closed.
         alert("Connection is closed...");
      };
   } else {
      // The browser doesn't support WebSocket
      alert("WebSocket NOT supported by your Browser!");
   }
}