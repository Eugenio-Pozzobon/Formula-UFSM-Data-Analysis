Table logDatalogger;
Table configTable;
Table logFinal;
float[] values ;

String configTableDecimalHeader = "Casas decimais";
String configTableIDHeader = "ID";
String configTableBytesHeader = "Bytes";

void getLog(String file) {
  logDatalogger = loadTable(file);
  configTable = loadTable("Datalogger/configTable.csv", "header");
  values = new float[configTable.getRowCount()];
  logFinal = new Table();
  logFinal.addColumn("Time");

  for (TableRow row : configTable.rows()) {
    String channel = row.getString("Channel");
    logFinal.addColumn(channel);
  }
  int andamento=0;
  println("Line Lenght of Data: " + logDatalogger.getRowCount());
  delay(100);
  for (TableRow row : logDatalogger.rows()) {   
    TableRow newRow = logFinal.addRow();
    newRow.setFloat("Time", row.getFloat(9));

    int id = row.getInt(0);
    float[] rxBuf = new float[]{row.getFloat(1), row.getFloat(2), row.getFloat(3), row.getFloat(4), row.getFloat(5), row.getFloat(6), row.getFloat(7), row.getFloat(8)};

    println(row.getInt(0)+" | " +row.getFloat(1)+","+ row.getFloat(2)+","+  row.getFloat(3)+","+  row.getFloat(4)+","+  row.getFloat(5)+","+  row.getFloat(6)+","+  row.getFloat(7)+","+  row.getInt(8));

    for (TableRow rowConfig : configTable.findRows(str(id), "ID")) {
      float idRow=rowConfig.getFloat(configTableIDHeader);
      rowConfig.print();
      if (id==idRow) {
        int bitMask = rowConfig.getInt("Bit_Mask");
        if (bitMask==1) {
          values[rowConfig.getInt("Indice")]=rxBuf[rowConfig.getInt(configTableBytesHeader)]*256+rxBuf[rowConfig.getInt(configTableBytesHeader)+1];
          values[rowConfig.getInt("Indice")]=values[rowConfig.getInt("Indice")]/(pow(10, rowConfig.getInt("Casas_decimais")));
        } else {
          values[rowConfig.getInt("Indice")]=rxBuf[rowConfig.getInt(configTableBytesHeader)];
          values[rowConfig.getInt("Indice")]=values[rowConfig.getInt("Indice")]/(pow(10, rowConfig.getInt("Casas_decimais")));
        }
      }
    }

    int i_newChannelLog=0;
    for (TableRow rowConfig : configTable.rows()) {
      newRow.setFloat(rowConfig.getString("Channel"), values[i_newChannelLog]);
      i_newChannelLog++;
    }
    andamento++;
    float porcent =andamento/float(logDatalogger.getRowCount())*100;
    println("Linha: " + andamento + " de " + logDatalogger.getRowCount()+" | Carregando... " + round(porcent) + "%");
  }

  int d = day();    // Values from 1 - 31
  int m = month();  // Values from 1 - 12
  int y = year();   // 2003, 2004, 2005, etc.
  int s = second();  // Values from 0 - 59
  int min = minute();  // Values from 0 - 59
  int h = hour();    // Values from 0 - 23

  saveTable(logFinal, "logs/Datalogger/Converted/logFinal"+h+"_"+min+"_"+s+"_"+d+"_"+m+"_"+y+".csv");
  tela=0;
}

//configuração dos arquivos logs e seu número máximo
ArrayList<PrintWriter> DataloggerLog = new ArrayList<PrintWriter>(); 
PrintWriter headerDatalogger; //arquivo do cabeçalho do arduino
long lapExtractionTime; //variável para guardar tempo inicial da extração de dados
String header; //dados do cabeçalho na inicialização do arduino
boolean  readHeader=false; //informa se um cabeçalho de arquivo novo foi lido ou não
long sumLogBytes=0; //soma de todos os bytes recebidos
int numValues=10; //número de valores separados nas linhas da tabela
int log=0; //log atual em gravação
//cria o arquivo de cabeçalho do programa

void createlog(int log) {
  datalogger.lineHeader=10;
  PrintWriter newLog;
  newLog=createWriter("logs/Datalogger/raw/log"+h+"_"+min+"_"+s+"_"+d+"_"+m+"_"+y+".csv");
  newLog.print("");
  DataloggerLog.add(log, newLog);
  sumLogBytes=0;
  linhaDados=0;
}
long timeLog=0;
//realiza a leitura dos dados enviados pelo cartão sd
boolean lendoSD(Serial input) {
  PrintWriter log = DataloggerLog.get(DataloggerLog.size()-1);
  int available = input.available();
  if (input.available() > 0 ) { //Se receber um valor na porta serial
    String value = input.readStringUntil('\n'); //Le o valor recebido até a quebra de linha do arquivo

    //se o valor recebido não for nulo, separa a linha os dados separadamente
    if (value != null) {
      Values = (splitTokens(value, ","));
      linhaDados++; //incrementa o contador da quantidade de dados

      if (linhaDados> datalogger.lineHeader && Values.length==10) {
        //guarda os dados no arquivo
        sumLogBytes=sumLogBytes+available;
        timeLog=millis();
        loadDataText=("Extraindo dados do cartão SD. \n Linha atual:" + linhaDados + "\n Bytes Extraídos: "+ sumLogBytes);
  
        log.print(value);
      } else if (linhaDados< datalogger.lineHeader) { //se os dados pertencem ao cabeçalho de informações que iniciam com o arduino, separa eles em um arquivo de texto separadamente
        headerDatalogger.println(value);
        headerDatalogger.flush();

        //fazer botão para vizualizar cabeçalho do programa enquanto o arquivo é gerado
      }
    }
    return true;
  } else {

    if (millis()-timeonlog<50 || input.available() > 0 ) {
      timeonlog=millis();
      return true;
    } else {
      println("endlog");
      println("timelog:" + (timeLog-timeCall));
      println("b/s:" + sumLogBytes/((timeLog-timeCall)/1000));
      return false;
    }
  }
}
boolean logCreated = false;
int logCounter=0;
long timeonlog;
int optionDataMode=0;
String loadDataText;
void telaDatalogger() {
  if (optionDataMode==0) {

    background(255);
    textAlign(CENTER, CENTER);
    textSize(48);
    fill(0);
    text("Select a Software Mode", width/2, height/2);
    push();
    rectMode(CENTER);
    String button1 = "Get Log in SD Card";
    String button2 = "Convert CAN Log";
    textSize(20);
    fill(255);
    rect(width/3, 2*height/3, textWidth(button1), 35);
    rect(2*width/3, 2*height/3, textWidth(button1), 35);
    fill(0);
    text(button1, width/3, 2*height/3); 
    text(button2, 2*width/3, 2*height/3);
    if (mousePressed) {
      if (mouseX>width/3-textWidth(button1) &&  mouseX<width/3+textWidth(button1) && mouseY<2*height/3+13 && mouseY>2*height/3-13) {
        optionDataMode=1;
      } else if (mouseX>2*width/3-textWidth(button1) &&  mouseX<2*width/3+textWidth(button1) && mouseY<2*height/3+13 && mouseY>2*height/3-13) {
        optionDataMode=2;
      }
    }
    pop();
  } else if (optionDataMode==1) {
    background(255);
    if (!logCreated) {
      createlog(logCounter++); 
      logCreated=true;
    }
    datalogger.lineHeader=20;
    datalogger.callSerial();

    cabecalho(datalogger.mySerial);
    if (lendoSD(datalogger.mySerial)) {
      gettingLogScreem();
    } else {
      endDataloggerScreem();
      tela=0;
      valuesCounter=0;
      optionDataMode=0;
      online=false;
      datalogger.display=false;
      datalogger.isSelected=false;
      datalogger.load=false;
      logCreated = false;
      datalogger.mySerial.write('s');
      datalogger.mySerial.stop();
      datalogger.mySerial.clear();
    }
  } else if (optionDataMode==2) {
    selectInput("Select a file to open:", "fileSelected");
    optionDataMode=3;
  } else if (optionDataMode==3) {
    telaTrasiction();
  }
}

void gettingLogScreem() {
  telaTrasiction();
}

void endDataloggerScreem() {
}

String getUserLogSelection;
void fileSelected(File selection) {
  if (selection == null) {
    println("Window was closed or the user hit cancel.");
    tela=0;
  } else {
    println("User selected " + selection.getAbsolutePath());
    getUserLogSelection = selection.getAbsolutePath();
    getLog(getUserLogSelection);
  }
}
