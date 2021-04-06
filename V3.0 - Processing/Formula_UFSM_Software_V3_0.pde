//for future development //<>//
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


PFont fonte;
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
    if (checkUser()) {
      frameRate(10);
    } else {
      frameRate(1);
    }
  } else if (tela==1) {
    tela=0;
    telaTrasiction();
  } else if (tela==2) {
    if (checkUser()) {
      frameRate(20);
    } else {
      frameRate(1);
    }
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
    } 
  }
  keyReleased=false;
  mouseReleased=false;
}

boolean mouseReleased;
void mouseReleased() {
  frameRate(60);
  mouseReleased=true;
}

//boolean alauso;
int state = 0, keyCounter=0; 
String result=""; 
String finalResult=""; 
int intResult=0;
boolean keyReleased;

void keyReleased() {
  frameRate(60);
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
