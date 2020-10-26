unsigned long int lastmillis = 0;

void setup() {
  // put your setup code here, to run once:

  Serial.begin(115200);

}

void loop() {
  // put your main code here, to run repeatedly:
  if ((millis() - lastmillis) > 5) {
    Serial.print(millis()); Serial.print(',');
    Serial.print(random(1000, 1011)); Serial.print(',');
    for (int i = 0; i < 8; i++) {
      Serial.print(random(0, 6)); Serial.print(',');
    }
    Serial.print('\n');
    lastmillis = millis();
  }
}
