//for future development
//int option=0;
//void create(channel a) {
//  if (!checkBlockOnMouse(blocks)) {
//    if(option>0){
//    blocks.add(new Block(option, blockRB, mouseX, mouseY, blocks.size(), a));//adicionar bloco
//    option=0;
//    created++;
//    //remover bloco
//    }
//  }
//}

//void removeblock(int c) {
//  if (checkBlockOnMouse(blocks)) {
//    if (blocks.size()>=c) {
//      blocks.remove(c);//remover bloco
//      atualizarIndices();
//    }
//  }
//}

//void sendToBack(int c) {
//  Block part = blocks.get(c);
//  blocks.add(part);
//  blocks.remove(c);
//  for ( int i=0; i+1<blocks.size(); i++) {
//    Block part2 = blocks.get(0);
//    blocks.add(part2);
//    blocks.remove(0);
//    atualizarIndices();
//  }
//  atualizarIndices();
//}

//void bringToFront(int c) {
//  Block part = blocks.get(c);
//  blocks.add(part);
//  blocks.remove(c);
//  atualizarIndices();
//}

//void atualizarIndices() {
//  for (int i =0; i<blocks.size(); i++) {
//    Block part = blocks.get(i);
//    part.index=i;
//  }
//}

/////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////

//boolean checkBlockConflict(int c, ArrayList<Block> a) {
//  boolean check=false;
//  Block test = a.get(c);
//  for (int i=0; i<a.size(); i++) {
//    Block tested = a.get(i);
//    if (!(test == tested)) {
//    }
//    if ((test.xpos+test.xtam)<tested.xpos && (test.ypos+test.ytam)<tested.ypos && test.xpos>(tested.xpos+tested.xtam) && test.ypos>(tested.ypos+tested.ytam)) {
//      check=false;
//    } else {
//      check=true;
//      break;
//    }
//  }

//  return check;
//}

//Block BlockConflict(ArrayList<Block> a) {
//  Block check = new Block();
//  for (int i=0; i<a.size(); i++) {
//    Block test = a.get(i);
//    for (int j=i+1; j+1<a.size(); j++) {
//      Block tested = a.get(j);
//      if ((test.xpos+test.xtam)<tested.xpos && (test.ypos+test.ytam)<tested.ypos && test.xpos>(tested.xpos+tested.xtam) && test.ypos>(tested.ypos+tested.ytam)) {
//      } else {
//        check=blocks.get(j);
//        break;
//      }
//    }
//  }
//  return check;
//}

//boolean checkBlockOnMouse(ArrayList<Block> a) {
//  boolean check=false;
//  for (int i=0; i<a.size(); i++) {
//    Block test = a.get(i);
//    if (mouseX>test.xpos && (test.ypos+test.ytam)>mouseY && test.xpos+test.xtam>mouseX && test.ypos<mouseY) {
//      check=true;
//      break;
//    } else {
//      check=false;
//    }
//  }
//  return check;
//}
