ArrayList<Block> blocks = new ArrayList<Block>();

class Block {

  //variáveis de tamanho e posições
  float xpos, ypos, xtam, ytam, xtpos, ytpos, xtammin=150, ytammin=150, xtammax=350, ytammax=350;

  //for future development
  //  rightButton rb;

  boolean proportion = false;
  boolean constant = true;
  boolean move = false;

  String units; 

  PImage disp, rightbdisplay;
  int index, type; //indicator=1, horizontal bar=3, vertical bar=4

  //canal associado
  channel ch;
  int opt;
  ArrayList<channel> chs;
  ArrayList<String> unitS;
  ArrayList<Integer> indexs;

  color cor;

  //construtor do bloco
  Block(float option, float wherex, float wherey, int ind, channel a, String u) {
    //move=true;
    units=u;
    opt=int(option);
    if (int((option-int(option))*10)==1) {
      cor = color(0, 255, 0);
    } else if (int((option-int(option))*10)==2) {
      cor = color(0, 0, 255);
    } else if (int((option-int(option))*10)==3) {
      cor = color(255, 255, 0);
    } else if (int((option-int(option))*10)==4) {
      cor = color(0, 255, 255);
    } else if (int((option-int(option))*10)==5) {
      cor = color(255, 0, 255);
    } else if (int((option-int(option))*10)==6) {
      cor = color(0, 0, 0);
    } else {
      cor = color(255, 0, 0);
    }
    ch=a;
    index = ind; //indice no vetor
    xpos=wherex;
    ypos=wherey;
    xtpos=0;
    ytpos=0;
    if (opt == 1) {//pointer
      xtam=width/6;
      ytam=height/6;
    } else if (opt == 2) {
      xtam =width/7;
      ytam= height/14;
    } else if (opt == 3) {
      xtam =width/7;
      ytam= height/14;
    } else if (opt == 4) {//warning
      xtam=height/8;
      ytam=height/8;
    } else if (opt == 5) {//vertical bar complete
      xtam=width/18;
      ytam=height/4;
    } else if (opt == 6) {//vertical bar ball
      xtam=width/15;
      ytam=height/4;
    } else if (opt == 7) {//digital
      xtam =width/10;
      ytam= height/15;
    } else if (opt == 9) {
      xtam =width/10;
      ytam= height/20;
    } else if (opt == 8) {
      xtam =3*width/8;
      ytam= height/9;
    }

    if (constant) {
      ytammin=ytam;
      ytammax=ytam;
      xtammin=xtam;
      xtammax=xtam;
    }
  }

  //Block(int option, float wherex, float wherey, ArrayList<Integer> ind, ArrayList<channel> as, ArrayList<String> u) {
  //  //move=true;
  //  unitS=u;
  //  opt=8;
  //  chs=as;
  //  indexs = ind; //indice no vetor
  //  xpos=wherex;
  //  ypos=wherey;
  //  xtpos=0;
  //  ytpos=0;

  //  xtam =width/3;
  //  ytam= height/5;

  //  if (constant) {
  //    ytammin=ytam;
  //    ytammax=ytam;
  //    xtammin=xtam;
  //    xtammax=xtam;
  //  }
  //}
  //Block(int option, PImage imagerdisplay, float wherex, float wherey, int ind, channel a) {
  //  //move=true;
  //  opt=option;
  //  ch=a;
  //  rightbdisplay=imagerdisplay;
  //  index = ind; //indice no vetor
  //  xpos=wherex;
  //  ypos=wherey;
  //  xtpos=0;
  //  ytpos=0;
  //  xtam=300;
  //  ytam=200;
  //  rb = new rightButton(rightbdisplay, 0); // cria o display para botão direito
  //  if (constant) {
  //    ytammin=ytam;
  //    ytammax=ytam;
  //    xtammin=xtam;
  //    xtammax=xtam;
  //  }
  //}

  //modifica o tamanho e move o display do objeto
  void move() { 
    if (move) {
      if (mousePressed && (mouseButton == LEFT)) {
        if (mouseX<xpos+xtam+10 && mouseX>xpos-10 && mouseY>ypos-10 && mouseY<ypos+ytam+10) {
          cursor(MOVE);

          float deltaX = pmouseX-mouseX;
          float deltaY = pmouseY-mouseY;

          if (mouseX<xpos+10 && mouseX>xpos-10) {
            cursor(TEXT);

            xtam=xtam+deltaX;

            xpos=xpos-(deltaX);
            xtpos=mouseX-xpos;
          }
          if (mouseX<xpos+xtam+10 && mouseX>xpos+xtam-10) {
            cursor(TEXT);
            xtam=xtam-deltaX;
          }

          if (mouseY<ypos+10 && mouseY>ypos-10) {
            cursor(TEXT);
            ytam=ytam+deltaY;

            ypos=ypos-(deltaY);
            ytpos=mouseY-ypos;
          }
          if (mouseY<ypos+ytam+10 && mouseY>ypos+ytam-10) {
            cursor(TEXT);
            ytam=ytam-deltaY;
          }
          if (mouseX<xpos+xtam-10 && mouseX>xpos+10 && mouseY>ypos+10 && mouseY<ypos+ytam-10) {
            xpos=xpos-(deltaX);
            ypos=ypos-(deltaY);

            xtpos=mouseX-xpos;
            ytpos=mouseY-ypos;
          }
        }
      } else {
        cursor(ARROW);
      }
    }
  }

  ArrayList<Float> graphxValues = new ArrayList<Float>();

  //mostra o objeto e seus displays secundários
  void display() {
    move();
    if (opt!=0) {
      pushMatrix();
      translate(xpos, ypos);

      if (xtam<xtammin) {
        xtam=xtammin;
      }
      if (ytam<ytammin) {
        ytam=ytammin;
      }
      if (xtam>xtammax) {
        xtam=xtammax;
      }
      if (ytam>ytammax) {
        ytam=ytammax;
      }

      noFill();
      stroke(0);
      rect(-1, -1, xtam+2, ytam+2);

      //text(ch.name+": " + ch.value + " "+ units, xtam/2, 5*sqrt(xtam*ytam/(xtam+ytam)) );
      if (opt!=9 && opt!=7 && opt!=5 && opt!=6 && opt!=8) {
        displayOption(opt, ch.minValue, ch.maxValue, ch.value, xtam/2, ytam/2);
        textAlign(CENTER);
        textFont(fonte);
        textSize(8/3*sqrt(xtam*ytam/(xtam+ytam)));
        fill(0);
        textLeading(8/3*sqrt(xtam*ytam/(xtam+ytam)));  // Set leading to 10

        if (opt==4) {//realiza a quebra de linha do cabeçalho do bloco, colocando o valor do canal na linha de baixo.
          text(ch.name+": \n" + ch.value + " "+ units, xtam/2, 8/3*sqrt(xtam*ytam/(xtam+ytam)) );
        } else {
          text(ch.name+": " + ch.value + " "+ units, xtam/2, 8/3*sqrt(xtam*ytam/(xtam+ytam)) );
        }
      } else if (opt==7) {
        displayOption(opt, ch.minValue, ch.maxValue, ch.value, xtam/2, ytam/2);
        textAlign(CENTER);
        textFont(fonte);
        textSize(3*sqrt(xtam*ytam/(xtam+ytam)));
        fill(0);
        textLeading(3*sqrt(xtam*ytam/(xtam+ytam)));
        text(ch.name, xtam/2, 3*sqrt(xtam*ytam/(xtam+ytam)) );
      } else if (opt==9) { // JUST VALUE
        textAlign(CENTER, CENTER);
        textFont(fonte);
        textSize(3*sqrt(xtam*ytam/(xtam+ytam)));
        textLeading(3*sqrt(xtam*ytam/(xtam+ytam)));
        if (ch.value>ch.minValue && ch.value<ch.maxValue) {
          fill(0);
        } else {
          fill(255, 0, 0);
        }
        text(ch.name + ": " + ch.value, xtam/2, ytam/2 );
      }
      if (opt==8) {
        graphxValues.add(ch.value);
        //print(graphxValues.size());
        graphx(cor, ch.minValue, ch.maxValue, graphxValues, xtam, ytam/2);
        textAlign(RIGHT);
        textFont(fonte);
        textSize(8/3*sqrt(xtam*ytam/(xtam+ytam)));
        fill(0);
        textLeading(8/3*sqrt(xtam*ytam/(xtam+ytam)));  // Set leading to 10
        text(ch.name+": " + ch.value + " "+ units, xtam, 8/3*sqrt(xtam*ytam/(xtam+ytam)) );
        contValues++;
        text(contValues/4 +"s", xtam, ytam);
      }

      if (opt==5 || opt==6) {
        displayOption(opt, ch.minValue, ch.maxValue, ch.value, xtam, ytam);
        textAlign(CENTER);
        textFont(fonte);
        textSize(8/3*sqrt(xtam*ytam/(xtam+ytam)));
        fill(0);
        textLeading(2*8/3*sqrt(xtam*ytam/(xtam+ytam)));
        text(ch.name+":\n" + ch.value + " "+ units, xtam/2, -8/3*sqrt(xtam*ytam/(xtam+ytam)) );
      }

      popMatrix();
      //for future development
      //rb.display(xpos, ypos, xtam+xpos, ypos+ytam, index);
    }
  }
  int contValues=0;
}

//PFont formula;

//stroke(0);
//pushMatrix();
//translate(width/2+400, height/2-250, 0);
//fill(255, 0, 0);
//line(0, -100, 0, 100);
//line(-10, 0, width-100, 0);
//fill(0);
//text("X AXIX", 0, 110);
//noFill();
//stroke(255, 0, 0);
//for (int v=1; v<c; v++) {
//  line(v*10, map(ax[v-1], -4, 4, -100, 100), (v+1)*10, map(ax[v], -4, 4, -100, 100));
//}
//popMatrix();
//stroke(0);
//pushMatrix();
//translate(width/2+400, height/2, 0);
//fill(255, 0, 0);
//line(0, -100, 0, 100);
//line(-10, 0, width-100, 0);
//fill(0);
//text("Y AXIX", 0, 110);
//noFill();
//stroke(0, 255, 0);
//beginShape();
//for (int v=1; v<c; v++) {
//  line(v*10, map(ay[v-1], -4, 4, -100, 100), (v+1)*10, map(ay[v], -4, 4, -100, 100));
//}
//endShape();
//popMatrix();
//stroke(0);
//pushMatrix();
//translate(width/2+400, height/2+250, 0);
//fill(255, 0, 0);
//line(0, -100, 0, 100);
//line(-10, 0, width-100, 0); 
//fill(0);
//text("Z AXIX", 0, 110);
//noFill();
//stroke(0, 0, 255);
//beginShape();
//for (int v=1; v<c; v++) {
//  line(v*10, map(az[v-1], -4, 4, -100, 100), (v+1)*10, map(az[v], -4, 4, -100, 100));
//}
//endShape();
//popMatrix();
//stroke(0);
//for (int v=0; v<59; v++) {
//  ax[v]=ax[v+1];
//  ay[v]=ay[v+1];
//  az[v]=az[v+1];
//}

//ax[59]=float(Values[0]);
//ay[59]=float(Values[1]);
//az[59]=float(Values[2]);

//c++;
//if (c>58) {
//  c=0;
//}
//numv++;
//println(numv);
