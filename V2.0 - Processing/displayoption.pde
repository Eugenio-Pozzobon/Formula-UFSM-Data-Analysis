void displayOption(int option, float min, float max, float val, float wx, float wy) {
  if (option==1) { //pannel indicator 
    ponter(wx, wy, val, 10, min, max);
  } else if (option==2) { //horizontal bar completed
    bar(option, wx, wy, val, min, max);
  } else if (option==3) {  //horizontal bar circle
    bar(option, wx, wy, val, min, max);
  } else if (option==4) { //warning
    warning(wx, wy, val, min, max);
  } else if (option==5) { //vertical bar completed
    vbar(5, wx, wy, val, min, max);
  } else if (option==6) {  //vertical bar circle  
    vbar(6, wx, wy, val, min, max);
  } else if (option==7) { //digital
    digital(wx, wy, val, min, max);
  } else if (option == 8) {// just value
  } else if (option == 9) {// just value
  }
}
void graphx(color c, float min, float max, ArrayList<Float> graphxV, float wx, float wy) {
  stroke(0);
  fill(0);
  pushMatrix();
  translate(50, 4*wy/3);
  line(0, -wy+5, 0, wy/2+2);
  line(+2, wy/2-5, wx-50, wy/2-5);
  noFill();
  beginShape();
  for (int i = 1; i<graphxV.size()-1; i++) {
    stroke(c);
    line(i*((wx-50)/graphxV.size()), map(graphxV.get(i), min, max, wy/2-5, -wy+5), (i+1)*((wx-50)/graphxV.size()), map(graphxV.get(i+1), min, max, wy/2-5, -wy+5));
    stroke(50);
    beginShape(POINTS);
    for (float j = -wy+5; j<wy/2-5; j=j+9) {
      vertex(i*((wx-50)/graphxV.size()), j);
    }
    endShape();
    
  }
  endShape();

  stroke(100);
  beginShape(POINTS);
  for (int i=0; i<wx-50; i=i+3) {
    vertex(i, -wy+5);
    vertex(i, ((-wy+5)+(wy/2+2))/2);
  }
  endShape();

  if (graphxV.size()>60) {
    graphxV.remove(1);
  }
  fill(0);
  textAlign(RIGHT, CENTER);
  textSize(14);
  text(round(max), -5, -wy+5); 
  text(round(min), -5, wy/2-5); 
  popMatrix();
}


//graph y(x)
//void displayOption(int option, float min, float max, float[][] val, float wx, float wy) {
//  if (option==10) {
//  }
//}

ArrayList<PVector> lastGPS = new ArrayList<PVector>();
ArrayList<PVector> lastMapGPS = new ArrayList<PVector>();
PVector initialGPS;
PVector mapGPS;
int c=0;

void gpsTrack(PVector GPS, float x, float y, float w, float h) {  

  if (c==0) {
    initialGPS = GPS;
    c++;
    mapGPS = new PVector(0, 0);
  } else {
    mapGPS = GPS.add(initialGPS.mult(-1));
  }

  lastMapGPS.add(mapGPS);
  fill(255);
  textAlign(CENTER, BOTTOM);
  textSize(sqrt(width*height/( width+height )));
  fill(0);
  text("GPS ONLINE TRACKING", (x+w)/2, y);
  fill(200);
  rect(x, y, w, h);
  noFill();
  pushMatrix();
  translate(x+w/2, y+h/2);
  beginShape();
  if (mapGPS.x>w/2) {
    for (int i=0; i<lastMapGPS.size(); i++) {
      lastMapGPS.get(i).add(-5, 0);
    }
  }
  if (mapGPS.y>h/2) {
    for (int i=0; i<lastMapGPS.size(); i++) {
      lastMapGPS.get(i).add(0, -5);
    }
  }
  if (mapGPS.x<-w/2) {
    for (int i=0; i<lastMapGPS.size(); i++) {
      lastMapGPS.get(i).add(5, 0);
    }
  }
  if (mapGPS.y<-h/2) {
    for (int i=0; i<lastMapGPS.size(); i++) {
      lastMapGPS.get(i).add(0, 5);
    }
  }
  for (int i=0; i<lastMapGPS.size(); i++) {
    vertex(lastMapGPS.get(i).x, lastMapGPS.get(i).y);
  }
  endShape();
  popMatrix();
}


void bar(int option, float w, float h, float v, float min, float max) {
  pushMatrix();
  translate (w, h);
  stroke(0);
  fill(255);
  rect(-w, 0, 2*w, h-10);
  if (option==3) {
    fill(200, 0, 200);
    stroke(255);
    ellipse(map(v, min, max, -w+h/2, w-h/2), h/2-5, h-5, h-5);
  } else if (option==2) {
    fill(200, 200, 0);
    stroke(255);
    rect(-w, 0, map(v, min, max, 0, 2*w), h-10);
  }
  popMatrix();
  stroke(0);
}

void vbar(int option, float w, float h, float v, float min, float max) {
  pushMatrix();
  //translate(w,h);
  stroke(0);
  fill(255);
  rect(1, 1, w-2, h-2);
  if (option==6) {
    fill(200, 0, 200);
    stroke(255);
    ellipse(map(v, min, max, -w+h/2, w-h/2), h/2-1, h-1, h-1);
  } else if (option==5) {
    fill(0, 0, 200);
    stroke(255);
    rect(1, h, w, map(v, min, max, -1, -h+2));
  }
  popMatrix();
  stroke(0);
}

boolean warning(float w, float h, float v, float min, float max) {
  textAlign(CENTER, CENTER);
  pushMatrix();
  translate (w, h);
  stroke(255);
  if (v>=min && v<max) {
    fill(0, 200, 0);
  } else {
    fill(255, 0, 0);
  }
  ellipse(0, h/10, w, h);
  fill(0);
  textSize(3*sqrt(w*h/(w+h)));
  if (v>min && v<max) {
    text("OK", 0, 0);
  } else {
    text("ERROR", 0, 0); 
    warningSound();
  }
  popMatrix();
  stroke(0);

  if (v>min && v<max) {
    return true;
  } else {
    return false;
  }
}

void digital(float w, float h, float v, float min, float max) {
  float textSize=25;
  pushMatrix();
  translate (w, h);
  textAlign(CENTER);
  if (v==1) {
    stroke(255);
    fill(0, 200, 0);
    rect(-w, 0, 2*w, h);
    fill(0);
    stroke(0);
    textSize(textSize);
    text("Enable", 0, h/2+textSize/2);
  } else {
    stroke(255);
    fill(255, 0, 0);
    rect(-w, 0, 2*w, h);
    fill(0);
    textSize(textSize);
    text("Disable", 0, h/2+textSize/2);
  }
  popMatrix();
  stroke(0);
}

void ponter(float w, float h, float v, float l, float min, float max) {
  float lineD=l; //tamanho da linha extra do ponteiro

  pushMatrix();
  translate (w, 2*h);
  fill(255);
  strokeWeight(2);
  arc(0, 0, w+lineD, 2*h+lineD, PI, 2*PI);
  arc(0, 0, w, 2*h, PI, 2*PI);
  line(0, -h/2-lineD, 0, -h/2);
  line(-w/2-lineD, 0, w/2 +lineD, 0);

  fill(0);
  textSize(15);
  textAlign(RIGHT);
  text(round(min), -w/2-lineD, 0);
  textAlign(LEFT);
  text(round(max), w/2+lineD, 0);
  textAlign(CENTER);
  text(round((min+max)/2), 0, -h-lineD);
  popMatrix();

  pushMatrix();
  translate(w, 2*h);
  rotate(map(v, min, max, PI/2, 3*PI/2));
  fill(255, 0, 0);
  strokeWeight(1);
  triangle(-l/4, 0, 0, h+l, l/4, 0);
  ellipse(0, 0, -l, l);
  rotate(-map(v, min, max, PI/2, PI));
  popMatrix();
}
