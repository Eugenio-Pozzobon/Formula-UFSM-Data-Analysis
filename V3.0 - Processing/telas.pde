PImage fu;
devices datalogger, NCU, telemetry, telemetry2, scales, cronometers;

int logIndexStopw = 0 ;

void telaInicial() {
  background(255);
  imageMode(CORNER);

  cabecalho();

  textAlign(CENTER);
  float textsize= width*height/20000;
  textSize(textsize);
  fill(#ED7A37);
  text("Electrical System", width/2, logoFormula.height/20+textsize );
  textSize(10);
  textAlign(RIGHT);
  text("Formula UFSM 2019 All right reseved", width, height-1);
  imageMode(CORNER);
  image(logoGallo, width-logoSefton.width*0.1-10, height/6, logoGallo.width*0.1, logoGallo.height*0.1);
  image(logoSefton, 10, height-logoGallo.height*0.1-10, logoGallo.width*0.1, logoGallo.height*0.1);


  imageMode(CENTER);
  selectCOM() ;
  pushMatrix();
  translate(width/2, height/5*3);
  float a = 75*height/fu.height;
  image(fu, 0, 0, 500*width/fu.width, 500*height/fu.height);
  image(NCU.icone, -300*width/fu.width, -75*height/fu.height, a, a);
  image(telemetry.icone, -250*width/fu.width, 100*height/fu.height, a, a);
  image(datalogger.icone, 0, +250*height/fu.height, a, a);
  image(scales.icone, 250*width/fu.width, 100*height/fu.height, a, a);
  image(cronometers.icone, 300*width/fu.width, -75*height/fu.height, a, a);

  textSize(16);
  textAlign(RIGHT);

  //ncu
  if (mouseX>width/2 -300*width/fu.width-a/2 && mouseX<width/2-300*width/fu.width+a/2 && mouseY<height/5*3-75*height/fu.height+a/2 && mouseY>height/5*3-75*height/fu.height-a/2) {
    if (Serial.list().length>0 || clientSelected) {
      fill(0, 255, 0);
    } else {
      fill(255, 0, 0);
    }
    if (mousePressed) {
      tela=2;
      NCU.display = true;
      if (!NCU.isSelected) {
        NCU.COM_INDEX = selectedCOM;
        NCU.isSelected=true;
      }
    }
  } else {
    fill(0);
  }
  text(NCU.name, -300*width/fu.width-a/2-5, -75*height/fu.height);

  //telemetry
  if (mouseX>width/2 -250*width/fu.width-a/2 && mouseX<width/2-250*width/fu.width+a/2 && mouseY<height/5*3+100*height/fu.height+a/2 && mouseY>height/5*3+100*height/fu.height-a/2) {
    if (Serial.list().length>0|| clientSelected) {
      fill(0, 255, 0);
    } else {
      fill(255, 0, 0);
    }
    if (mousePressed) {
      tela=2;
      telemetry.display = true;
      if (!NCU.isSelected) {
        telemetry.COM_INDEX = selectedCOM;
        telemetry.isSelected=true;
      }
    }
  } else {
    fill(0);
  }  
  text(telemetry.name, -250*width/fu.width-a/2-5, 100*height/fu.height);

  textAlign(CENTER);

  //datalogger
  if (mouseX>width/2-a/2 && mouseX<width/2+a/2 && mouseY<height/5*3+250*height/fu.height+a/2 && mouseY>height/5*3+250*height/fu.height-a/2) {
    if (Serial.list().length>0|| clientSelected) {
      fill(0, 255, 0);
    } else {
      fill(255, 0, 0);
    }
    if (mousePressed) {
      tela=2;
      datalogger.display = true;
      if (!datalogger.isSelected) {
        datalogger.COM_INDEX = selectedCOM;
        datalogger.isSelected=true;
      }
    }
  } else {
    fill(0);
  }
  text(datalogger.name, 0, +(500*height/fu.height)/2+a/2+5);

  textAlign(LEFT);
  //scales
  if (mouseX>width/2 +250*width/fu.width-a/2 && mouseX<width/2+250*width/fu.width+a/2 && mouseY<height/5*3+100*height/fu.height+a/2 && mouseY>height/5*3+100*height/fu.height-a/2) {
    if (Serial.list().length>0|| clientSelected) {
      fill(0, 255, 0);
    } else {
      fill(255, 0, 0);
    }
    if (mousePressed) {
      tela=2;
      scales.display = true;
      if (!scales.isSelected) {
        scales.COM_INDEX = selectedCOM;
        scales.isSelected=true;
      }
    }
  } else {
    fill(0);
  }
  text(scales.name, 250*width/fu.width+a/2+5, 100*height/fu.height);

  //cronometrers
  if (mouseX>width/2 +300*width/fu.width-a/2 && mouseX<width/2+300*width/fu.width+a/2 && mouseY<height/5*3-75*height/fu.height+a/2 && mouseY>height/5*3-75*height/fu.height-a/2) {
    if (Serial.list().length>0|| clientSelected) {
      fill(0, 255, 0);
    } else {
      fill(255, 0, 0);
    }
    if (mousePressed) {
      tela=2;
      cronometers.display = true;
      stopConfig=1; 
      logIndexStopw++;
      if (!cronometers.isSelected) {
        cronometers.COM_INDEX = selectedCOM;
        cronometers.isSelected=true;
      }
    }
  } else {
    fill(0);
  }
  text(cronometers.name, 300*width/fu.width+a/2+5, -75*height/fu.height);
  popMatrix();
}

int moveX=0, moveY=0;
boolean checkUser() {
  if ((moveX!=mouseX) || (moveY!=mouseY)) {
    moveX=mouseX;
    moveY=mouseY;
    return true;
  } else {
    moveX=mouseX;
    moveY=mouseY;
    return false;
  }
}
void cabecalho() {
  //checkCom();
  imageMode(CORNER);
  image(logoUFSM, 10, 10, logoUFSM.width/3, logoUFSM.height/3);
  image(exitPNG, width-width/30-width/40, height/20, width/40, width/40);
  if (tela!=0) {
    image(back, width-width*2/30-width/40, height/20, width/40, width/40);
  }
  imageMode(CENTER);
  //image(logoFormula, width/2, (logoFormula.height/2)*( width*height/40000000), logoFormula.width*( width*height/40000000), logoFormula.height*( width*height/40000000));
  image(logoFormula, width/2, (logoFormula.height/2)/25, logoFormula.width/25, logoFormula.height/25);

  if (mousePressed) {
    if (tela!=0) {
      if (mouseX<width-2*width/30 && mouseX>width-2*width/30-width/40 && mouseY>height/20 && mouseY<height/20+width/40) {
        telemetryLog.close();
        tela=0;
        valuesCounter=0;
        online=false;

        cronometers.display=false;
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
      }
    }
    if (mouseX<width-width/30 && mouseX>width-width/30-width/40 && mouseY>height/20 && mouseY<height/20+width/40) {
      telemetryLog.close();
      exit();
    }
  }
}

void cabecalho(Serial s) {
  if (!clientSelected) {
    checkCom(s);
  }
  imageMode(CORNER);
  image(logoUFSM, 10, 10, logoUFSM.width/3, logoUFSM.height/3);
  image(exitPNG, width-width/30-width/40, height/20, width/40, width/40);
  if (tela!=0) {
    image(back, width-width*2/30-width/40, height/20, width/40, width/40);
  }

  imageMode(CENTER);
  image(logoFormula, width/2, (logoFormula.height/2)/25, logoFormula.width/25, logoFormula.height/25);

  //IP
  if (serverSelected) {
    textAlign(LEFT, UP);
    textSize(15);
    fill(0);
    float aux=textWidth(localIP);
    text(localIP, width-aux, height/50);
  }

  //Botões
  if (mousePressed) {
    if (tela!=0) {
      if (mouseX<width-2*width/30 && mouseX>width-2*width/30-width/40 && mouseY>height/20 && mouseY<height/20+width/40) {
        telemetryLog.close();
        logScales.close();
        //launch("/logs/Telemetry/telemetryLog"+h+"_"+min+"_"+s+"_"+d+"_"+m+"_"+y+".csv");

        if (cronometers.display) {
          if (stopConfig==0) {
            stopWatch.println();
            stopWatch.println(bestTime+"s"+ " na volta: " + bestLap);
            stopWatch.println("Tempo Médio: " + averageTime + "s");
            stopWatch.println("Total de Cone: "+ totalcone+ "; Penalidade:" + totalcone*conePenality);
            stopWatch.println("Total de Slip Cour: "+ totalcone+ "; Penalidade:" + totalcone*conePenality);
            penalidadeTotal = totalcone*conePenality+totalOffCourse*ocPenality;
            stopWatch.println("Total de Penalidade: "+ penalidadeTotal);
            stopWatch.flush();
          }
        }
        if (!clientSelected) {
          s.clear();
          s.write("out");
          s.clear();
          s.stop();
        }
        tela=0;
        online=false;

        NCU.display=false;
        telemetry.display=false;
        datalogger.display=false;
        scales.display=false;
        cronometers.display=false;

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

        //StopWhatch Var
        OffCourseCounter=0;
        bestLap=0;
        bestTime=0; 
        lastTime=0; 
        averageTime=0; 
        sumTime=0;
        coneCounter=0;
        totalcone=0;
        penalidadeTotal=0;
        totalOffCourse=0;
        startRace=false;
      }
    }
    if (mouseX<width-width/30 && mouseX>width-width/30-width/40 && mouseY>height/20 && mouseY<height/20+width/40) {
      telemetryLog.close();
      if (logingSW) {
        if (stopConfig==0) {
          stopWatch.println();
          stopWatch.println(bestTime+"s"+ " na volta: " + bestLap);
          stopWatch.println("Tempo Médio: " + averageTime + "s");
          stopWatch.println("Total de Cone: "+ totalcone+ "; Penalidade:" + totalcone*conePenality);
          stopWatch.println("Total de Slip Cour: "+ totalcone+ "; Penalidade:" + totalcone*conePenality);
          penalidadeTotal = totalcone*conePenality+totalOffCourse*ocPenality;
          stopWatch.println("Total de Penalidade: "+ penalidadeTotal);
          stopWatch.close();
          logingSW=false;
        }
      }
      exit();
    }
  }
}

boolean changeCOM = false;
int selectedCOM = 0;
void selectCOM() { //seleciona a COM PORT para comunicação serial e seleciona o modo de operação cliente ou servidor
  push();
  float widthWindow = width/18;

  translate(width-widthWindow, height/2);

  int txtSize = 20;
  changeCOM = true;
  String[] portName = Serial.list();
  textAlign(CENTER);
  fill(255);
  rect(-75, -5, widthWindow, portName.length*(txtSize*2+1));
  fill(0);
  textSize(txtSize);
  textLeading(txtSize+1);
  text("CHECK THE COM PORT \n FOR COMUNICATION!", (widthWindow)/2 -75, -40);
  line( -100, -10, widthWindow-50, -10);  
  textLeading(txtSize);
  for (int i=0; i<portName.length; i++) {
    if (mousePressed) {
      if (mouseX>width-widthWindow-75 && mouseX<width-75 && mouseY > height/2+(i)*(txtSize+5) && mouseY < height/2+(i+1)*(txtSize+5)) {
        selectedCOM=i;
        fill(0);
      }
    }
    if (selectedCOM==i) {
      fill(10, 255, 10);
    } else {
      fill(255, 10, 10);
    }
    textSize(txtSize-5);
    text("["+i+"]"+portName[i], (widthWindow)/2 -75, (i+1)*(txtSize+5));
    //println("Selected: " + selectedCOM);
  }

  //selecionar modo de servidor no WEBSERVER
  fill(0);
  txtSize=16;
  textSize(txtSize);
  text("SELECT A WEBSERVER MODE", (widthWindow)/2 -85, height/4);
  line( -105, -10+txtSize+height/4, widthWindow-50, -10+txtSize+height/4);

  if (serverSelected) {
    fill(0, 255, 0);
  } else {
    fill(255, 0, 0);
  }
  rect(-100, txtSize+height/4, (widthWindow)/3, (widthWindow)/3);
  fill(0);
  textAlign(LEFT, CENTER);
  text("Server", -100+(widthWindow)/2, (txtSize+height/4+(widthWindow)/6) );

  if (clientSelected) {
    fill(0, 255, 0);
  } else {
    fill(255, 0, 0);
  }
  rect(-100, txtSize+height/4+(widthWindow)/2, (widthWindow)/3, (widthWindow)/3);
  fill(0);
  text("Client", -100+ (widthWindow)/2, (txtSize+height/4+(widthWindow)/2+ (widthWindow)/6) );
  //botões

  if (mousePressed) {
    if (mouseX>width-widthWindow-100 && mouseX<width-widthWindow-100+(widthWindow)/3 && mouseY<height/2+txtSize+height/4+(widthWindow)/3 && mouseY>height/2+txtSize+height/4) {
      serverSelected=!serverSelected;
      //println(serverSelected);
      delay(100);
    }
    if (mouseX>width-widthWindow-100 && mouseX<width-widthWindow-100+(widthWindow)/3 && mouseY<height/2+txtSize+height/4+(widthWindow)/3+(widthWindow)/2 && mouseY>height/2+txtSize+height/4+(widthWindow)/2) {
      clientSelected=!clientSelected;
      //println(clientSelected);
      delay(100);
      finalResult="";
      result="";
    }
  }

  if (clientSelected) {
    text("Key the server IP:", -100+ (widthWindow)/2, (txtSize+height/4+(widthWindow)/2+ 3*(widthWindow)/6) );
    if (key==ENTER||key==RETURN) {//se a tecla digitada não for enter ou return vai concatenando cada tecla
      fill(0, 100, 0);
      localIP = finalResult;
      text(localIP, width/2, height/2+50);
      //println(localIP);
    } else {
      fill(0, 0, 100);
      text(result, -100+ (widthWindow)/2, (txtSize+height/4+(widthWindow)/2+ 4*(widthWindow)/6) );
    }
  }
  if (serverSelected && clientSelected) {
    serverSelected=!serverSelected;
    clientSelected=!clientSelected;
  }

  pop();
  //fazer device entrar na COM selecionada e ver como selecionar ela
}

int zcounter=0;
long timeTransiction=0;
void telaTrasiction() {
  if (millis()-timeTransiction<1000) {
    if (telemetry.display) {
      zcounter=zcounter+10;
    } else if (datalogger.display) {
      zcounter=zcounter+1;
    }
    background(255);
    cabecalho();

    push();
    translate(width/2, height/2);

    //x^2+y^2=rm^2

    fill(50);
    int rm=50, ri=10;
    ellipse(0, 0, 1, 1);
    float x, y, passo=2*rm/8;

    for (int i=-4; i<5; i++) {
      x=i*passo+zcounter;
      float c=rm*rm-x*x;
      y=-sqrt(c);
      ellipse(x, y, ri, ri);
    }

    for (int i=-4; i<5; i++) {
      x=i*passo-zcounter;
      float c=rm*rm-x*x;
      y=sqrt(c);
      ellipse(x, y, ri, ri);
    }

    pop();

  } else {
    timeTransiction=millis();
    zcounter=0;
  }
}
