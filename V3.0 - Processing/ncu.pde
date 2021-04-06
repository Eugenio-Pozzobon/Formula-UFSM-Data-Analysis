String[] nameChannelsNCU = new String[]{
  "X Acel.", 
  "Y Acel.", 
  "Z Acel.", 
  "NCU Temp.", 
  "LVDT DE", 
  "LVDT DD", 
  "LVDT TD", 
  "LVDT TE", 
  "Speed Left", 
  "Speed Righ", 
  "UP Shift", 
  "DOWN Shift", 
  "Launch Control", 
  "Traction C.", 
  "Start", 
  "Stop"
};

float[] optionChannelsNCU = new float[]{
  3, 
  3, 
  3, 
  9, 
  2, 
  2, 
  2, 
  2, 
  2, 
  1, 
  7, 
  7, 
  7, 
  1, 
  7, 
  7
};

float[] minChannelsNCU = new float[]{
  -4, 
  -4, 
  -4, 
  0, 
  0, 
  0, 
  0, 
  0, 
  0, 
  0, 
  0, 
  0, 
  0, 
  0, 
  0, 
  0
};

float[] maxChannelsNCU = new float[]{
  4, 
  4, 
  4, 
  100, 
  1023, 
  1023, 
  1023, 
  1023, 
  100, 
  100, 
  1, 
  1, 
  1, 
  3, 
  1, 
  1
};

String[] unitsNCU = new String[]{
  "G", 
  "G", 
  "G", 
  "C", 
  "unit", 
  "unit", 
  "unit", 
  "unit", 
  "km/h", 
  "km/h", 
  "", 
  "", 
  "", 
  "", 
  "", 
  ""
};

void telaNCU() {
  float[] wxChannelsNCU = new float[]{
    width/2-width/14, 
    width/2-width/14, 
    width/2-width/14, // Acelerometro
    23*width/30, 
    width/5, 
    width/5, 
    width/5, 
    width/5-width/12, //SENSORES
    2*width/5-width/12, 
    3*width/5-width/12, //speed
    7*width/11, 
    23*width/30, 
    7*width/11, //shift
    4*width/5-width/12, 
    7*width/11, 
    23*width/30 //painel
  }; 

  float[] wyChannelsNCU = new float[]{
    height/2+height/10, 
    height/2+2*height/10, 
    height/2+3*height/10, // Acelerometro
    height/2+2*height/10+7, 
    height/2+height/10, 
    height/2+2*height/10, 
    height/2+3*height/10, 
    height/4, //SENSORES
    height/4, 
    height/4, //speed
    height/2+height/10, 
    height/2+height/10, 
    height/2+2*height/10, //shift
    height/4, 
    height/2+3*height/10, 
    height/2+3*height/10//painel
  };


  NCU.callSerial();
  if (NCU.read(46)) {

    NCU.loadTela(nameChannelsNCU, minChannelsNCU, maxChannelsNCU, optionChannelsNCU, wxChannelsNCU, wyChannelsNCU, unitsNCU);
    background(255, 255, 255);
    NCU.updateDevice(Values);

    for (int i=0; i<blocks.size(); i++) {
      Block part = blocks.get(i);
      part.display();
    }


    //button("DRS", 4*width/5, height-100, 50);
    //button("CheckCan", 4*width/5, height-100, 50);


    float textsize= width*height/40000;

    textSize(textsize);
    textAlign(CENTER);
    fill(200, 100, 0);
    text("Electrical", width/4, height/10);
    textSize(textsize);
    textAlign(CENTER);
    fill(200, 100, 0);
    text("Network Control Unit (NCU)", 3*width/4, height/10);
  } else if (loading) {
    telaTrasiction() ;
  }

  cabecalho(NCU.mySerial);

  if (keyReleased) {
    if (key==ENTER||key==RETURN) {//se a tecla digitada não for enter ou return vai concatenando cada tecla
      resset=finalResult;
      println(resset);
      delay(1000);
      ressetSerial(NCU.mySerial);
    }
  }
}
String resset = "";
