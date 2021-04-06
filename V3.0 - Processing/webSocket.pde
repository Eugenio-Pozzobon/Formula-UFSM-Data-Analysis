import websockets.*;

import processing.net.*;

int port = 10004;
Server myServer;

WebsocketServer ws;

boolean serverSelected=false;
boolean clientSelected=false;

void setupServer() {
  localIP = myServer.ip();
  ws= new WebsocketServer(this, 8025, "/formulaUfsm");
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
WebsocketClient wsc;

String localIP;

void setupClient() {
  if (!online) {
    wsc= new WebsocketClient(this, "ws://"+localIP+":8025/formulaUfsm");
    online=true;
  }
}

String serverMsg;
boolean msgIncomming;

void webSocketEvent(String msg) {
  serverMsg=msg;
  msgIncomming = true;

  println(true);
}

boolean clientReading(int i, int header) {
  if (msgIncomming) {
    msgIncomming=false;
    valuesCounter++;
    if (serverMsg != null ) {
      if (valuesCounter >= header) {
        valuesCounter--;
        nutValues = split(serverMsg, ';');
        if (nutValues.length==i) {
          Values = split(serverMsg, ';');
        return true;
      } else {
        nutValuesConter++;
        println(nutValues.length + ": nutvalues problem in client - - " + i);
        return false;
      }
    } else {
      loading=true;
      return false;
    }
  } else {
    return false;
  }
} else {
  return false;
}
} 


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
