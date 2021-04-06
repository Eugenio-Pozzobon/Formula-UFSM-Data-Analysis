int telemetryMonitor=0;  //0 = geral, 1 = Suspensão, 2=Simplificado;
int stepTeleConfig=0; //0=inactive, 1=select Monitor, 2=start;

boolean changeTelemetryMonitor=false;

color backgroundTele = color(255);
boolean warningState = false;

void telaTelemetry() {

  String[] nameChannelsTele = new String[]{
    "Lost Packets", //0
    "RPM", //1
    "Speed", //2
    "Engine Temp", //3
    "Gear", //4
    "MAP", //5
    "TPS", //6
    "Fuel Pressure", //7
    "Oil Pressure", //8
    "Brake Pressure", //9
    "Air temp", //10 
    "Bat V", //11
    "Lambda", //12
    "Oil Temp", //13
    "Steering Angle", //14
    "Acelerometer", //15
    "Gyroscope", //16
    "GPS Lat", 
    "GPS Long", //17,18
    "Tire1Atemp", "Tire1Atemp", "Tire1Atemp", "Tire1Atemp", "Tire1Atemp", "Tire1Atemp", "Tire1Atemp", "Tire1Atemp", "Tire1Atemp", "Tire1Atemp", "Tire1Atemp", "Tire1Atemp", 
    "Can State", //31
    "RSSI", //32
    "SNR"//33
  };

  //RPM Tentar shift light
  //Oil temp fazer um indicador de painel colorido, para saber a faixa operacional
  //Engine temp alarme visual 
  //SEPA St angle vai o proprio volante
  // Telemetria todos os valores de temperatura do pneu
  //Inserir lap time calculado
  //Inserir botão do lap time
  //Can State
  //Cone
  //colocar botão do cone e start

  float[] optionChannelsTele = new float[]{
    9, //0
    8, 
    8.3, 
    8.1, 
    9, //4
    8.5, //5
    8.2, 
    8.5, 
    8.5, 
    8.5, //
    8.1, //10
    9, 
    8, 
    8.1, 
    0, 
    3, //15
    3, 
    0, 
    0, 
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // Temperatura do Pneu
    4, 
    9, 
    9
  };

  float[] minChannelsTele = new float[]{
    0, //0
    0, 
    0, 
    0, 
    0, 
    0, //5 map
    0, 
    0, 
    0, 
    0, 
    -5, //10
    12, 
    0, 
    0, 
    -120, 
    -2, //15
    -90, 
    00000, 00000, 
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // Temperatura do Pneu
    0, 
    -140, 
    -100
  };

  float[] maxChannelsTele = new float[]{
    500, //0
    13000, 
    120, 
    130, 
    6, 
    100, //5 map
    100, 
    6, 
    15, 
    250, 
    130, //10
    14.9, 
    1, 
    130, 
    120, 
    2, //15
    90, 
    00000, 00000, 
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, // Temperatura do Pneu
    0, 
    0, 
    0
  };

  //confirmar range do fuel pressure
  //range do Air Temp
  //

  String[] unitsTele = new String[]{
    "", 
    "rpm", 
    "km/h", 
    "°C", 
    "", 
    "kpa", 
    "%", 
    "Bar", 
    "Bar", 
    "Bar", 
    "°C", 
    "V", 
    "", 
    "°C", 
    "°", 
    "g", 
    "°", 
    "", 
    "", 
    "°C", "°C", "°C", "°C", "°C", "°C", "°C", "°C", "°C", "°C", "°C", "°C", 
    "", 
    "dB", 
    "dBm"
  };

  //option 0 = canal desativado
  //option==1 pannel DIAL indicator 
  //option==2 horizontal bar completed
  //option==3) {  //horizontal bar circle
  //option==4) { //warning
  //option==5) { //vertical bar completed
  //option==6) {  //vertical bar circle
  //option==7) { //digital
  //option==8) { //timelapse
  //option == 9) {// just value
  //option == 10) {//Mapa de temperatura
  
  float[] wxChannelsTele = new float[]{
    width*12/20, //0
    1*width/40, 
    1*width/40, 
    width*12/20, 
    width*9/20, 
    1*width/40, //5 map
    1*width/40, //tps
    width*12/20, 
    width*12/20, 
    width*12/20, 
    width*12/20, //10
    width*9/20, 
    1*width/40, //lambda
    width*12/20, //oil temp
    0, //stangle
    (width-width/7)/2, //15
    (width-width/7)/2, 
    000, 000, 
    //"Tire1Atemp", "Tire1Atemp", "Tire1Atemp", "Tire1Atemp", "Tire1Atemp", "Tire1Atemp", "Tire1Atemp", "Tire1Atemp", "Tire1Atemp", "Tire1Atemp", "Tire1Atemp", "Tire1Atemp", 
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
    width/2, 
    width*14.5/20, 
    width*17/20
  }; 

  float[] wyChannelsTele = new float[]{
    height*11/12, //0
    3*height/20, 
    5.5*height/20, 
    10.5*height/20, 
    height*7.2/12, 
    8*height/20, //5 map
    13*height/20, //tps
    3*height/20, 
    5.5*height/20, 
    8*height/20, 
    height*13/20, //10
    height*8/12, 
    height*10.5/20, //lambda
    15.5*height/20, //oil
    0, //st angle
    height*5/12, //15
    height*6/12, 
    000, 000, 
    //"Tire1Atemp", "Tire1Atemp", "Tire1Atemp", "Tire1Atemp", "Tire1Atemp", "Tire1Atemp", "Tire1Atemp", "Tire1Atemp", "Tire1Atemp", "Tire1Atemp", "Tire1Atemp", "Tire1Atemp", 
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
    height*10.5/12, 
    height*11/12, 
    height*11/12    
  };

  Block engTempWarning, oilpressWarning, oiltempWarning;
  telemetry.callSerial();
  if (telemetry.read(34)) {

    telemetry.loadTela(nameChannelsTele, minChannelsTele, maxChannelsTele, optionChannelsTele, wxChannelsTele, wyChannelsTele, unitsTele);

    background(backgroundTele);
    telemetry.updateDevice(Values);
    float min, max;
    channel engtemp = blocks.get(3).ch;
    max=engtemp.maxValue;
    min=engtemp.minValue;
    engtemp.maxValue=110;
    engtemp.minValue=30;
    engTempWarning = new Block(4, width/2-width/14, height*10.5/12, -1, engtemp, "°C");
    engTempWarning.ch.update(float(Values[3]));
    engTempWarning.display();
    engtemp.maxValue=max;
    engtemp.minValue=min;

    channel oiltemp = blocks.get(13).ch;
    max=oiltemp.maxValue;
    min=oiltemp.minValue;
    oiltemp.maxValue=110;
    oiltemp.minValue=30;
    oiltempWarning = new Block(4, width/2-width/14, height*9/12, -1, oiltemp, "°C");
    oiltempWarning.ch.update(float(Values[13]));
    oiltempWarning.display();
    oiltemp.maxValue=max;
    oiltemp.minValue=min;

    channel oilpress = blocks.get(8).ch;
    max=oilpress.maxValue;
    min=oilpress.minValue;
    oilpress.maxValue=110;
    oilpress.minValue=30;
    oilpressWarning = new Block(4, width/2, height*9/12, -1, oilpress, "°C");
    oilpressWarning.ch.update(float(Values[8]));
    oilpressWarning.display();
    oilpress.maxValue=max;
    oilpress.minValue=min;

    //VOLANTE
    imageMode(CENTER);
    pushMatrix();
    translate(width/2, 4*height/15);
    fill(0, 255, 0);
    rotate(radians(float(Values[14])));
    image(steeringImage, 0, 0, 207*width*height/1250000, 150*width*height/1250000);
    textAlign(CENTER);
    textSize(25);
    text(int(float(Values[14])), 0, 0);
    rotate(-radians(float(Values[14])));
    fill(0, 0, 0);
    text("Steering Angle: " + float(Values[14]), 0, -95*width*height/1250000);
    popMatrix();

    //GPS Track
    PVector GPS = new PVector(float(Values[17]), float(Values[18]));

    gpsTrack(GPS, 2*width/40, height*10.5/13, width/3, height/5.5);


    //Color MAP


    for (int i=0; i<blocks.size(); i++) {
      Block part = blocks.get(i);
      part.display();
      //print("update block " + i);
    }


    if (logTelemetry) {
      for (int i=0; i<Values.length; i++) {
        telemetryLog.print(Values[i]);
        if (i<Values.length-1) {
          telemetryLog.print(",");
        }
      }
      //telemetryLog.println();
    }

    float textsize= width*height/30000;
    textSize(textsize);
    textAlign(CENTER);
    fill(200, 100, 0);
    text("Telemetry", width/4, height/10);
    textSize(textsize);
    textAlign(CENTER);
    fill(200, 100, 0);
    text("Wireless Data Unit", 3*width/4-10, height/10);
    imageMode(CORNER);
    if (!logTelemetry) {
    } else {
      image(download, width-width/30-3.5*width/40, height/50, width/45, width/45);
    }
    image(save, width-width/30-3.5*width/40, height/18, width/45, width/45);
    if (mousePressed) {
      if (mouseX>width-width/30-3.5*width/40 && mouseX<width-width/30-3.5*width/40 +width/45 && mouseY>height/18&& mouseY<height/18+width/45) {
        logTelemetry=!logTelemetry;
      }
    }

    ////image()// Enter second screen
    //if (mousePressed) {
    //  if (mouseX>width-width/30-3.5*width/40 && mouseX<width-width/30-3.5*width/40 +width/45 && mouseY>height/18&& mouseY<height/18+width/45) {
    //    //toggleSketch(Tele2);
    //  }
    //}

    //button("Cone", 4*width/5, height-100, 50);
  } else if (loading) {
    telaTrasiction() ;
  }
  cabecalho(telemetry.mySerial);
}

boolean logTelemetry = false;
