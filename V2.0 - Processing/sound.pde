import processing.sound.*;

TriOsc triOsc;
Env env;

float attackTime = 0.01;
float sustainTime = 0.004;
float sustainLevel = 0.3;
float releaseTime = 0.4;

void setupSound() {
  // Create triangle wave
  triOsc = new TriOsc(this);

  // Create the envelope 
  env  = new Env(this);
}
long t=0;
boolean ressetError=false;
void warningSound() {
  //triOsc.play();
  //env.play(triOsc, attackTime, sustainTime, sustainLevel, releaseTime);
}
