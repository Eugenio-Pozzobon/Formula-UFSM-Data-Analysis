//for future development
//class rightButton {
//  boolean displaythisRB;
//  float x, y, xtam, ytam;//variáveis que indicam como será o meu display, tamanho etc.
//  PImage disp; //imagem mostrada como display
//  int index, master; //verifica o layer
//  //contador de blocos criados
//  //float whereX, whereY; //Onde que esse display especifico pode ser chamado

//  //construtor
//  rightButton(PImage a, int i) {
//    disp=a;
//    xtam=disp.width;
//    ytam=disp.height;
//    created=0;
//    master = i;
//  }

//  void display(float xmin, float ymin, float xmax, float ymax, int ind) {
//    index=ind;
//    if (mousePressed && (mouseButton == RIGHT)) {//insere o display
//      if (mouseX>xmin && mouseX<xmax && mouseY <ymax && mouseY>ymin) {
//        x=mouseX;
//        y=mouseY;
//        displaythisRB=true;
//      }
//    }

//    if (mousePressed && (mouseButton == LEFT)) {
//      if ((mouseX<x+xtam && mouseX>x && mouseY>y && mouseY<y+ytam && displaythisRB)) {

//        if (index==-1) { 
//          dispOptions=true;
//        } else if (index>=0) {
//          if (mouseY>y && mouseY<y+30) {
//            removeblock(index);
//          }
//          if (mouseY>y+30 & mouseY<y+60) {
//            bringToFront(index);
//          }
//          if (mouseY>y+60 && mouseY<y+90) {
//            sendToBack(index);
//          }
//        }
//      }
//      displaythisRB=false;
//    }
//    if (displaythisRB) {//desenha o display
//      created=0;
//      //fill(150, 150, 150);
//      //rect(x, y, xtam, ytam); se n usar imagem pronta
//      image(disp, x, y);
//    }
//  }
//}

//////////////////// END OF CLASS ///////////////////////////////
