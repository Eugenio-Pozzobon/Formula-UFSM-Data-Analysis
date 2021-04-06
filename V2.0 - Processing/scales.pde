String[] nameChannelsS = new String[]{
  "Scale GL", 
  "Scale GR", 
  "Scale DL", 
  "Scale DR"
};
float[] optionChannelsS = new float[]{
  1, 
  1, 
  1, 
  1
};

float[] minChannelsS = new float[]{
  0, 
  0, 
  0, 
  0
};
float[] maxChannelsS = new float[]{
  200, 
  200, 
  200, 
  200
};

String[] unitsScale = new String[]{
  "Kg", 
  "Kg", 
  "Kg", 
  "Kg"
};

float mt, de, dd, te, td, dep, ddp, tep, tdp;

boolean logingScales = false;
void telaSCALE() {
  scales.lineHeader=1;
  float[] wxChannelsS = new float[]{
    width/10, 
    3*width/10, 
    width/10, 
    3*width/10
  };
  float[] wyChannelsS = new float[]{
    height/6, 
    height/6, 
    4*height/6, 
    4*height/6
  };

  scales.callSerial();
  if (scales.read(4)) {

    scales.loadTela(nameChannelsS, minChannelsS, maxChannelsS, optionChannelsS, wxChannelsS, wyChannelsS, unitsScale);
    background(255, 255, 255);
    scales.updateDevice(Values);

    de=float(Values[0]);
    dd=float(Values[1]);
    te=float(Values[2]);
    td=float(Values[3]);

    mt = de + dd + te + td;

    if (mt == 0) {
      mt++;
    }

    dep = de / mt *100;
    ddp = dd / mt *100;
    tep = te / mt *100;
    tdp = td / mt *100;

    for (int i=0; i<blocks.size(); i++) {
      Block part = blocks.get(i);
      part.display();
    }
    textAlign(RIGHT);
    textFont(fonte);
    textSize(width*height/50000);
    fill(200, 100, 0);
    text(round(dep)+"%  ", width/10, height/6+(height/6)/2);
    text(round(tep)+"%  ", width/10, 4*height/6+(height/6)/2);
    textAlign(LEFT);
    text("  "+round(ddp)+"%  ", 3*width/10+width/6, height/6+(height/6)/2);
    text("  "+round(tdp)+"%  ", 3*width/10+width/6, 4*height/6+(height/6)/2);
    textAlign(CENTER);
    fill(250, 0, 0);
    textSize(width*height/45000);
    text("Corner Weight Scales \n Total Mass: " + mt, (width/4+width/20)-20, height/2);
    imageMode(CENTER);
    image(lateral, 3*width/4, 1*height/3, lateral.width/5, lateral.height/5 );
    image(frontal, 3*width/4, 2*height/3, lateral.width/5, lateral.height/4 );


    fill(0);
    textSize(width*height/50000);
    textAlign(CENTER); 
    text("Longitudinal Distribution", 3*width/4, 4*height/20);
    text("Lateral Distribution", 3*width/4, 11*height/20); 

    fill(200, 50, 0);
    textSize(width*height/45000);
    textAlign(RIGHT);
    text("Back "+ round(tep+tdp) + "%", 3*width/4-lateral.width/10, 1*height/3);
    text("Left "+ round(tep+dep) + "%", 3*width/4-lateral.width/10, 2*height/3);
    textAlign(LEFT);
    text("Front "+ round(dep+ddp) + "%", 3*width/4+frontal.width/10, 1*height/3);
    text("Right "+ round(tdp+ddp) + "%", 3*width/4+lateral.width/10, 2*height/3);
    imageMode(CORNER);

    if (!logingScales) {
    } else {
      image(download, width-width/30-3.5*width/40, height/50, width/45, width/45);
    }
    image(save, width-width/30-3.5*width/40, height/18, width/45, width/45);

    if (mousePressed) {
      if (mouseX>width-width/30-3.5*width/40 && mouseX<width-width/30-3.5*width/40 +width/45 && mouseY>height/18&& mouseY<height/18+width/45) {
        logingScales=!logingScales;
      }
    }
    if (logingScales) {
      String logprint =("\nDE = " + de + "\nDD = " + dd + "\nTE = " + te + "\nTD = " + td +"\n Back "+ round(tep+tdp) + "%" + "\n Left "+ round(tep+dep) + "%" + "\n Front "+ round(dep+ddp) + "%" + "\n Right "+ round(tdp+ddp) + "%");
      logScales.println(logprint);
      logScales.println();
      logingScales=false;
    }
    //cabecalho(scales.mySerial);
  }
  cabecalho(scales.mySerial);
  //textSize(60);
  //textAlign(CENTER);
  //fill(200, 100, 0);
  //text("Weight Scales", width/2, height/4);
}
