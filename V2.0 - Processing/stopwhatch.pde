int bestLap=0, bestTime=10000, lastTime, averageTime=0, sumTime=0;

int stopConfig=0; //0=show values, 1=key pilot, 2=key test

String[] pilotOptions = new String[]{"Daniel Schreiner", "Ângelo Baratto", "Vícthor", "Felipe Balbom"};

String pilotActing;

String event = "";

String[] testOptions = new String[]{"Enduro", "AutoCross", "Brake Test", "Aceleration", "SkidPad"};

String testType;

boolean logingSW=false;

int coneCounter=0, conePenality = 2, totalcone=0;
int penalidadeTotal=0, OffCourseCounter=0, totalOffCourse=0, ocPenality =20;
boolean startRace=false, coneFall=false;

void telaSTOPWHATCH() {
  cronometers.lineHeader=0;
  cronometers.callSerial();
  //colocar nome do evento
  if (stopConfig==1) {
    background(255);
    cabecalho(cronometers.mySerial);
    textAlign(CENTER);
    textSize(42);
    fill(0);
    text("Key the name of the event and press enter\nEx.: Cruz Alta, Quadra GPMOT,...", width/2, height/2);

    if (keyReleased && (key==ENTER||key==RETURN)) {//se a tecla digitada não for enter ou return vai concatenando cada tecla
      text(finalResult, width/2, height/2+50);
      event=finalResult;
      //println(event);
      stopConfig=2;
    } else {
      fill(0, 0, 100);
      text(result, width/2, height/2+250);
    }
  }
  //Colocar o nome do Piloto
  if (stopConfig==2) {
    background(255);
    cabecalho(cronometers.mySerial);
    textAlign(CENTER, CENTER);
    textSize(30);
    fill(0);
    text("Select the Driver", width/2, 2*height/5);
    push();
    translate(width/2, 0);
    rectMode(CENTER);
    for (int i=0; i<pilotOptions.length; i++) {
      if (mousePressed) {
        if (mouseX>width/2+150*(i-pilotOptions.length/2)-50 && mouseX<width/2+150*(i-pilotOptions.length/2)+50 && mouseY>3*height/5-25 && mouseY< 3*height/5+25) {
          fill(0, 200, 0);
          pilotActing=pilotOptions[i];
          stopConfig=3;
        } else {
          fill(220);
        }
      } else {
        fill(220);
      }
      fill(255);
      rect(150*(i-pilotOptions.length/2), 3*height/5, 125, 50, 3);
      fill(0);
      textSize(16);
      text(pilotOptions[i], 150*(i-pilotOptions.length/2), 3*height/5 );
    }

    pop();
  }
  //Tipo da Prova
  if (stopConfig==3) {
    background(255);
    cabecalho(cronometers.mySerial);

    textAlign(CENTER, CENTER);
    textSize(30);
    fill(0);
    text("Select the Test", width/2, height/2);

    push();
    translate(width/2, 0);
    rectMode(CENTER);
    for (int i=0; i<testOptions.length; i++) {
      if (mousePressed) {
        if (mouseX>width/2+150*(i-testOptions.length/2)-50 && mouseX<width/2+150*(i-testOptions.length/2)+50 && mouseY>4*height/5-25 && mouseY< 4*height/5+25) {
          testType=testOptions[i];
          fill(0, 200, 0);
          stopConfig=4;
        } else {
          fill(220);
        }
      } else {
        fill(220);
      }

      rect(150*(i-testOptions.length/2), 4*height/5, 125, 50, 5);
      fill(0);
      textSize(16);
      text(testOptions[i], 150*(i-testOptions.length/2), 4*height/5 );
    }

    pop();
  }
  if (stopConfig==4) {
    stopWatch = createWriter("logs/StopWhatch/stopWhatch" + "_" + event + "_" + testType + "_" + pilotActing + "_" + logIndexStopw + ".txt");
    logingSW=true;
    stopConfig=0;
    stopWatch.println("Event: " + event + ";" + "Test: " +  testType + ";" + "Pilot: " +  pilotActing);
    stopWatch.flush();
  }

  if (stopConfig==0) {
    if (cronometers.read(2)) {
      stopWatch.print(int(float(Values[0])));
      stopWatch.print(";");
      stopWatch.print(int(float(Values[1])));
      stopWatch.print(";");
      stopWatch.print(coneCounter);
      stopWatch.print(";");
      stopWatch.print(OffCourseCounter);
      stopWatch.print(";");
      //stopWatch.println(PENALIDADE TOTAL); ///////////////////////////////ADICIONAR
      stopWatch.flush();
      
      totalcone=coneCounter+totalcone; 
      totalOffCourse = totalOffCourse + OffCourseCounter;

      coneCounter=0;
      OffCourseCounter=0;
      if (float(Values[1])< bestTime && int(float(Values[0]))>0) {
        bestTime=int(float(Values[1]));
        bestLap=int(float(Values[0]));
        sumTime=sumTime + int(float(Values[1]));
        averageTime=sumTime/int(float(Values[0]));
      }
      startRace=true;
    }
    if (startRace) {

      background(255);
      float textsize= width*height/30000;
      textSize(textsize);
      textAlign(CENTER);
      fill(200, 100, 0);
      text("Peripheral", width/4, height/10);
      textSize(textsize);
      textAlign(CENTER);
      fill(200, 100, 0);
      text("Stopwatch", 3*width/4-10, height/10);
      imageMode(CORNER);
      int sz=25;
      textSize(sz);
      textLeading(5*sz/3);
      textAlign(LEFT, CENTER);
      //Mostrar tempos, contador de volta
      float icontam=100*width/2000;
      image(raceFlag, width/30, height/4, icontam, icontam);
      fill(0);
      text("Lap: " +int(float(Values[0])) + "\nTime: " +int(float(Values[1]))+"s", width/30+icontam+10, height/4+icontam/2);

      //Mostrar melhor tempo e melhor volta
      image(record, width/30, 2*height/4, 2*icontam, 2*icontam);
      fill(0, 10, 0);
      text(bestTime+"s"+ " in lap: " + bestLap, width/30+ 2*icontam, 2*height/4+icontam);

      //Marcador e contador de Cone
      penalidadeTotal = totalcone*conePenality+totalOffCourse*ocPenality;

      String coneString = "Cones= "+coneCounter + "                Total = " + totalcone + "\nPenality = " + coneCounter*conePenality + "                 Total = " + penalidadeTotal;
      float  bracing = textWidth(coneString)+15*width/30+2*icontam+20+30;
      image(add, bracing, height/4+icontam/2, icontam/2, icontam/2);
      image(remove, bracing, height/4+icontam+5, icontam/2, icontam/2);
      if (mouseReleased) {
        if (mouseX>bracing && mouseX<(bracing+icontam/2) && mouseY>(height/4+icontam/2) && mouseY<(height/4+icontam/2+icontam/2)) {
          coneCounter++;
          coneFall = true;
        } else if (mouseX>bracing && mouseX<(bracing+icontam/2) && mouseY>(height/4+icontam+5) && mouseY<(height/4+icontam+5+icontam/2)) {
          coneCounter--;
        }
        delay(60);
      }

      //imagem do cone, se aumentou o número, anima o cone caindo
      if (mouseX>bracing && mouseX<(bracing+icontam/2) && mouseY>(height/4+icontam/2) && mouseY<(height/4+icontam/2+icontam/2)) {
        coneFall = true;
      }
      if (coneFall) {
        push();
        translate(15*width/30+icontam, height/4+icontam);
        rotate(2*PI/3);
        image(cone, -icontam, -icontam, 2*icontam, 2*icontam);
        //rotate(-PI/2);
        pop();
        coneFall=false;
      } else {
        image(cone, 15*width/30, height/4, 2*icontam, 2*icontam);
      }
      fill(200, 0, 0);
      text(coneString, 15*width/30+2*icontam+20, height/4+icontam);

      //Marcador e contador de off course - ADICIONAR E EDITAR -> IMAGEM = (offCourse)
      penalidadeTotal = totalcone*conePenality+totalOffCourse*ocPenality;
      String ocString = "Off Course= "+OffCourseCounter + "                Total = " + totalOffCourse*ocPenality + "\nPenality = " + coneCounter*conePenality + "                 Total = " + penalidadeTotal;
      float  bracing2 = textWidth(coneString)+15*width/30+2*icontam+20+30;
      image(add, bracing2, 2*height/4+icontam/2, icontam/2, icontam/2);
      image(remove, bracing2, 2*height/4+icontam+5, icontam/2, icontam/2);
      if (mouseReleased) {
        if (mouseX>bracing && mouseX<(bracing+icontam/2) && mouseY>(2*height/4+icontam/2) && mouseY<(2*height/4+icontam/2+icontam/2)) {
          OffCourseCounter++;
        } else if (mouseX>bracing && mouseX<(bracing+icontam/2) && mouseY>(2*height/4+icontam+5) && mouseY<(2*height/4+icontam+5+icontam/2)) {
          OffCourseCounter--;
        }
        delay(60);
      }

      //imagem do cone, se aumentou o número, anima o cone caindo


      image(offCourse, 15*width/30, 2*height/4, 2*icontam, 2*icontam);

      fill(200, 0, 0);
      text(ocString, 15*width/30+2*icontam+20, 2*height/4+icontam);


      //colocar na tela as informações q foram solicitadas inicialmente
      fill(0);
      textAlign(CENTER);
      text("Evento: " + event + "    - - -    " + "Teste: " +  testType + "    - - -    " + "Piloto: " +  pilotActing, width/2, 3.95*height/4);


      //Se sair, logar melhor volta
    }
  }

  cabecalho(cronometers.mySerial);
}
