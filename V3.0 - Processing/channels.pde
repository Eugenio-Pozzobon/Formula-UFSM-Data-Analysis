class channel {

  float minValue, maxValue, value;
  String name;
  channel(String a) {
    name=a;
    maxValue=100;
    minValue=0;
    value=0;
  }

  channel(String a, float min, float max) {
    name=a;
    maxValue=max;
    minValue=min;
    value=0;
  }

  void update(float newValue) {
    value=newValue;
  }
}
