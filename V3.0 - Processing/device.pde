boolean loading;

class devices {
  //String[] nameChannelsNCU = new String[]
  String name;

  int COM_INDEX=0;

  boolean isSelected;

  Serial mySerial;

  PImage icone;

  boolean load = false;

  boolean display = false;

  ArrayList<channel> CANAIS = new ArrayList<channel>();

  int lineHeader = 30;

  devices(PImage a, String b) {
    icone=a;
    name = b;
    isSelected=false;
  }
  void loadTela(String[] a, float[] min, float[] max, float[] option, float[] wherex, float[] wherey, String[] u) {
    if (display && tela ==2) {
      if (!load) {
        blocks.clear();
        CANAIS.clear();
        if ((a.length == min.length )&& ( a.length == max.length) &&( a.length == option.length )&& (a.length == wherex.length )&& (a.length == wherey.length)) {
          for (int i=0; i< a.length; i++) {

            CANAIS.add(new channel(a[i], min[i], max[i]));
            channel Canal = CANAIS.get(i);
            blocks.add(new Block(option[i], wherex[i], wherey[i], i+1, Canal, u[i]));
          }
        } else {
          println("Error loading scream:" + " "+ a.length + "|"+ min.length + "|"+ max.length + "|"+ option.length + "|"+ wherex.length + "|"+ wherey.length);
        }
        load=true;
        //println("im here");
      }
    }
  }

  void updateDevice(String[] a) {
    if (display && tela ==2) {
      if (a.length == blocks.size()) {
        for (int i=0; i<blocks.size(); i++) {
          Block part = blocks.get(i);
          channel partCh = CANAIS.get(i);
          part.ch.update(float(a[i]));
          partCh.update(float(a[i]));
        }
      } else {
        println("Will not update: " + a.length);
      }
    }
  }

  void callSerial() {
    if (!clientSelected) {
      mySerial = chamarOnline(mySerial, COM_INDEX);
      loading=false;
    } else {
      setupClient();
      loading=false;
      
    }
  }

  boolean read(int i) {
    if (!clientSelected) {
    return onlineReading(i, mySerial, lineHeader, true);
    }else{
      return clientReading(i, lineHeader);
    }
  }
}
