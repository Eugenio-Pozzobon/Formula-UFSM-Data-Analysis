import processing.serial.*; //Biblioteca importante para essa aplicação
Serial serial; //Funcionalidade serial

void chamarOnline() {//chama o cartão SD, inicializando a porta Serial
  if (!online && !clientSelected) {
    String portName = Serial.list()[0]; //configura a porta serial
    serial = new Serial(this, portName, 115200); //Configura a porta serial 2400000 maior velocidade porém carregando erros
    for (int i=0; i<2; i++) {
      delay(1000);
      serial.write(1);
    }
    online=true;
    println("online");
    nutValuesConter=0;
    valuesCounter=0;
    timeCall=millis();
    if (serverSelected) {
      setupServer();
    }
  } 
  if (clientSelected) {
    println("online");
    setupClient();
  }
}

Serial chamarOnline(Serial input, int index) {
  if (!online && !clientSelected) {
    String portName = Serial.list()[index]; //configura a porta serial
    input = new Serial(this, portName, 115200); //Configura a porta serial 2400000 maior velocidade porém carregando erros
    serial= input;
    for (int i=0; i<3; i++) {
      delay(1000);
      input.write(1);
    }
    online=true;
    println("online");
    println(portName);
    println(index);
    nutValuesConter=0;
    valuesCounter=0;
    timeCall=millis();
    if (serverSelected) {
      setupServer();
    }
  }  
  if (!online && clientSelected) {
    setupClient();
    nutValuesConter=0;
    valuesCounter=0;
    timeCall=millis();

    online=true;
  }
  return input;
}

void ressetSerial(Serial input){
  input.stop();
  println("RESSETED");
  online=false;
}

boolean online=false;
int linhaDados;
String[] Values;
String[] nutValues;
int nutValuesConter; 
long valuesCounter=0;
long timeCall=0;

boolean onlineReading(int i, Serial input, int header, boolean callback) {
  if (input.available() > 0 ) { //Se receber um valor na porta serial
    String value = input.readStringUntil('\n'); //Le o valor recebido até a quebra de linha do arquivo
    //se o valor recebido não for nulo, separa a linha com os dados entre virgulas, em dados separados.
    println("Value = "+value);
    valuesCounter++;
    if (value != null ) {
      if (valuesCounter >= header) {
        valuesCounter--;
        nutValues = split(value, ';');
        if (nutValues.length==i) {
          if (serverSelected) {
            ws.sendMessage(value);
          }
          Values = split(value, ';');
          return true;
        } else {
          nutValuesConter++;
          println(nutValues.length + ": nutvalues problem");
          return false;
        }
      } else {
        
        return false;
      }
    } else {
      return false;
    }
  } else {
    if (((millis() - timeCall) >5000)) {
      input.clear();
      input.write(1);
      //println("callback  " + (millis()-timeCall));
      timeCall=millis();
    }
    return false;
  }
} 

void comandSerialButton(Serial input, int send, float x, float y, float tam) {
  fill(150, 150, 0);
  rect(x, y, tam, tam);
  if (mousePressed) {
    if (mouseX>x && mouseX<x+tam && mouseY>y && mouseY<y+tam) {
      input.write(send);
      delay(10);
    }
  }
}

void checkCom(Serial input) {
  //println("Checking COM: " + nutValuesConter + " nutValues Problem");
  if (nutValuesConter>50 &&(NCU.display || telemetry.display || datalogger.display || scales.display)) {
    input.clear();
    input.write(0);
    input.clear();
    input.stop();
    tela=0;
    online=false;
    //print("END SERIAL");
    NCU.display=false;
    telemetry.display=false;
    datalogger.display=false;
    scales.display=false;

    cronometers.isSelected=false;
    NCU.isSelected=false;
    telemetry.isSelected=false;
    datalogger.isSelected=false;
    scales.isSelected=false;

    cronometers.load=false;
    NCU.load=false;
    telemetry.load=false;
    datalogger.load=false;
    scales.load=false;
    nutValuesConter=0;
  }
}
