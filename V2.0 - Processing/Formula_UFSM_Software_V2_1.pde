//for future development
//rightButton generalRB;
//PImage imagegeneralRB;
//PImage blockRB;

/*Change Log:
 Tela de carregamento
 
 Next Updates: 
 
 1. Botões para se comunicar com Telemetria (Marcar Posição Inicial)
 2. Botões para Scanner no NCU
 3. Guias diferentes para subsistemas na aba de telemetria, exibindo dados de preferência por subsistema
 */


PFont fonte; //<>//
channel[] channels= new channel[10];

int tela;

PImage lateral, frontal;
PImage logoFormula, logoSAE, logoUFSM, logoSefton, logoGallo;
PImage dv1, dv2, dv3, dv4, dv5, dv6;

PImage back, exitPNG, save, download;

PImage add, remove, cone, raceFlag, record, offCourse;

PrintWriter telemetryLog, logScales;
PImage steeringImage;
PrintWriter stopWatch;

int d, m, y, s, min, h;

PImage scan;

void setup() {

  //Definições básica de tela e processamento:  
  size(1200, 720);
  //fullScreen(2);
  tela = 0;
  fonte = createFont("Fonts/TitilliumWeb-SemiBold.ttf", 20);
  surface.setResizable(true);
  frameRate(100);

  //for future development
  //carrega as imagens
  //imagegeneralRB= loadImage("generaldisp.png");
  //blockRB = loadImage("rbBlock.png"); 
  //botão direito na tela geral
  //generalRB = new rightButton(imagegeneralRB, -1);

  fu = loadImage("Icons/sefton.png");

  //carrega os icones da tela inicial
  dv1= loadImage("Icons/sd.png"); 
  dv2= loadImage("Icons/ncu.png"); 
  dv3= loadImage("Icons/tele.png"); 
  dv4= loadImage("Icons/scale.png"); 
  dv5= loadImage("Icons/stop.png");
  dv6= loadImage("Icons/tele.png"); 

  //Para a tela das balanças: carrega imagens do fu-18
  lateral = loadImage("Icons/lateralp.png");
  frontal = loadImage("Icons/frontalp.png");

  //carrega as logos e imagens importante
  logoFormula = loadImage("Icons/formula.png");
  logoSAE = loadImage("Icons/SAE.png");
  logoUFSM = loadImage("Icons/ufsm.png");

  logoSefton = loadImage("Icons/logoSefton.png");
  logoGallo = loadImage("Icons/logoGallo.png");

  //imagens de icones de comando
  back = loadImage("Icons/back-arrow.png");
  exitPNG = loadImage("Icons/flag.png");
  save = loadImage("Icons/save.png");
  download = loadImage("Icons/download.png");
  scan = loadImage("Icons/Scan/security.png");

  //imagens de icones dos cronômetros
  add = loadImage("stopWatch/add.png");
  remove = loadImage("stopWatch/remove.png");
  cone = loadImage("stopWatch/cone.png");
  raceFlag = loadImage("stopWatch/racingFlag.png");
  record = loadImage("stopWatch/record.png");
  offCourse = loadImage("stopWatch/offCourse.png");

  //inicia os "devices": dispositivos programados
  datalogger = new devices(dv1, "Datalogger");
  NCU = new devices(dv2, "Network Control Unit");
  telemetry= new devices(dv3, "Telemetry"); 
  scales= new devices(dv4, "Weight Scales"); 
  cronometers= new devices(dv5, "Stopwatch");
  telemetry2= new devices(dv6, "Telemetry"); 

  setupSound();
  //myServer = new Server(this, port); // Starts a server on port 10002

  d = day();    // Values from 1 - 31
  m = month();  // Values from 1 - 12
  y = year();   // 2003, 2004, 2005, etc.
  s = second();  // Values from 0 - 59
  min = minute();  // Values from 0 - 59
  h = hour();    // Values from 0 - 23
  telemetryLog = createWriter("logs/Telemetry/telemetryLog"+h+"_"+min+"_"+s+"_"+d+"_"+m+"_"+y+".csv");
  steeringImage = loadImage("Icons/Telemetry/steeringImage.png");

  headerDatalogger = createWriter("logs/Datalogger/header/header"+h+"_"+min+"_"+s+"_"+d+"_"+m+"_"+y+".txt");
  
  logScales = createWriter("logs/Scales/Scales"+h+"_"+min+"_"+s+"_"+d+"_"+m+"_"+y+".txt");
  
  println(myServer.ip());
  localIP = myServer.ip();
}

/* Percorre cada uma das telas. 
 Tela 0: tela inicial, com botões para selecionar com qual dispositivo o pc irá se conectar. 
 Caso mais de um esteja conectado, seleciona o especifico na tela 1, 
 e na tela 2 aparece o resultado da conexão graficamente
 */


void draw() {
  //println(tela);

  checkSurface();

  textFont(fonte);
  if (tela==0) {
    telaInicial();
  } else if (tela==1) {
    tela=0;
    telaTrasiction();
  } else if (tela==2) {
    if (NCU.display) {

      telaNCU();

      cronometers.display=false;
      telemetry.display=false;
      datalogger.display=false;
      scales.display=false;

      cronometers.isSelected=false;
      telemetry.isSelected=false;
      datalogger.isSelected=false;
      scales.isSelected=false;

      cronometers.load=false;
      telemetry.load=false;
      datalogger.load=false;
      scales.load=false;
    } else if (scales.display) {

      telaSCALE();

      cronometers.display=false;
      NCU.display=false;
      telemetry.display=false;
      datalogger.display=false;

      cronometers.isSelected=false;
      NCU.isSelected=false;
      telemetry.isSelected=false;
      datalogger.isSelected=false;

      cronometers.load=false;
      NCU.load=false;
      telemetry.load=false;
      datalogger.load=false;
    } else if (telemetry.display) {

      telaTelemetry();

      cronometers.display=false;
      NCU.display=false;
      datalogger.display=false;
      scales.display=false;

      cronometers.isSelected=false;
      NCU.isSelected=false;
      datalogger.isSelected=false;
      scales.isSelected=false;

      cronometers.load=false;
      NCU.load=false;
      datalogger.load=false;
      scales.load=false;
    } else if (cronometers.display) {

      telaSTOPWHATCH();

      NCU.display=false;
      telemetry.display=false;
      datalogger.display=false;
      scales.display=false;

      NCU.isSelected=false;
      telemetry.isSelected=false;
      datalogger.isSelected=false;
      scales.isSelected=false;

      NCU.load=false;
      telemetry.load=false;
      datalogger.load=false;
      scales.load=false;
    } else if (datalogger.display) {

      telaDatalogger();

      NCU.display=false;
      telemetry.display=false;
      cronometers.display=false;  
      scales.display=false;

      cronometers.isSelected=false;
      NCU.isSelected=false;
      telemetry.isSelected=false;
      scales.isSelected=false;

      cronometers.load=false;
      NCU.load=false;
      telemetry.load=false;
      scales.load=false;
    }
  }
  keyReleased=false;
  mouseReleased=false;
}

boolean mouseReleased;
void mouseReleased() {
  mouseReleased=true;
}

//boolean alauso;
int state = 0, keyCounter=0; 
String result=""; 
String finalResult=""; 
int intResult=0;
boolean keyReleased;

void keyReleased() {
  keyReleased=true;
  if (key==ENTER||key==RETURN) {//se a tecla digitada não for enter ou return vai concatenando cada tecla
    state++;
    keyCounter=0;
    finalResult=result;
    //serial.write(result);
    //println(finalResult);
    result="";
  } else if (key==BACKSPACE) {
    println(keyCounter);
    char[] res;
    res = result.toCharArray();
    keyCounter--;
    result="";
    for (int i=0; i<keyCounter; i++) {
      result = result + res[i];
    }
    delay(150);
  } else {
    keyCounter++;
    result = result + key;
  }
  
}

int lastWidth=0, lastHeight=0;
void checkSurface() {//mantem a tela numa largura e altura minimas para não dar bug de visualização.
  if (width < 1200) {
    surface.setSize(1200, height);
  }
  if (height < 720) {
    surface.setSize(width, 720);
  }
  if (lastWidth!=width || lastHeight!=height) {
    lastWidth=width;
    lastHeight=height;
    cronometers.load=false;
    NCU.load=false;
    telemetry.load=false;
    scales.load=false;
    datalogger.load=false;
  }
}

//for future development
//    background(255, 255, 255);
//    for (int i=0; i<blocks.size(); i++) {
//      Block part = blocks.get(i);
//      part.move();
//      part.display();
//    }
//    if (!checkBlockOnMouse(blocks)) {
//      generalRB.display(0, 0, width, height, -1);
//    }
//    dispChannels();
//    if (!(mouseState==mouseState2));
//    displayOptions();
//  }
//boolean mouseState, mouseState2;

//int created;
//boolean dispOptions;
//void displayOptions() {//mostra as opções de gages na tela, se uma for selecionada, cria uma nova gage
//  delay(20);
//  if (dispOptions) {
//    fill(255, 255, 255);
//    rect(width/3-10, height/3-10, width/3+10, height/3+10);
//    fill(0, 0, 0);
//    textSize(width/60+height/60);
//    textAlign(CENTER);
//    text("Select Your gage mode", width/2, height/3+width/60+height/60);

//    if (mousePressed && (mouseButton == LEFT)) {

//      if (mouseX>4*width/12 && mouseX<4*width/12+width/13 && mouseY>height/2.5 && mouseY<height/2.5+height/7) {
//        option=1;
//        dispOptions=false;
//        dispChannel=true;
//      } else if (mouseX>5*width/12 && mouseX<5*width/12+width/13 && mouseY>height/2.5 && mouseY<height/2.5+height/7) {
//        option=2;
//        dispOptions=false;
//        dispChannel=true;
//      } else if (mouseX>6*width/12 && mouseX<6*width/12+width/13 && mouseY>height/2.5 && mouseY<height/2.5+height/7) {
//        option=3;
//        dispOptions=false;
//        dispChannel=true;
//      } else if (mouseX>7*width/12 && mouseX<7*width/12+width/13 && mouseY>height/2.5 && mouseY<height/2.5+height/7) {
//        option=4;
//        dispOptions=false;
//        dispChannel=true;
//      }
//    } else if (mouseButton == RIGHT) {
//      dispOptions=false;
//    }
//    if (mousePressed) {
//      mouseState=mousePressed;
//    }
//  } else {
//    mouseState=false;
//  }
//}

//boolean dispChannel;

//void dispChannels() {
//  if (dispChannel) {
//    fill(255, 255, 255);
//    rect(width/3-10, height/3-height/40, width/3+20, height/3+2*height/40);
//    fill(0, 0, 0);
//    textSize(width/60+height/60);
//    textAlign(CENTER);
//    text("Select a Channel to show", width/2, height/3-(width/60+height/60));

//    //mostra botões para selecionar os canais
//    pushMatrix();
//    translate(width/3, height/3);
//    int c=0;
//    for (int i = 0; i <channels.length/5; i++) {
//      for (int j = 0; j <channels.length/2; j++) {
//        fill(255);
//        rect(i*width/6, j*height/15, width/6, height/15);
//        textAlign(CENTER);
//        textSize(width/90+height/90);
//        fill(0);
//        text(channels[c].name, (2*i+1)*width/12, (j)*height/15+width/60 );
//        c++;
//      }
//    }
//    popMatrix();

//    delay(20);
//    //checa se foram precionados
//    if (mousePressed && (mouseButton == LEFT)) {

//      c=0;
//      for (int i = 0; i <channels.length/5; i++) {
//        for (int j = 0; j <channels.length/2; j++) {
//          fill(255);
//          if (mouseX>i*width/6+width/3 && mouseX<i*width/6+width/6+width/3 && mouseY>j*height/15+height/3 && mouseY<j*height/15+height/15+height/3) {
//            if (created==0) { 
//              dispChannel=false;  
//              create(channels[c]);
//            }
//          }
//          c++;
//        }
//      }
//    } else if (mouseButton == RIGHT) {
//      dispChannel=false;
//    }
//  }
//}
