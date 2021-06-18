// 2-dimensional array of row pin numbers:
int R[] = {2,7,A5,5,13,A4,12,A2};  
// 2-dimensional array of column pin numbers:
int C[] = {6,11,10,3,A3,4,8,9};
char Matrix_list[65];
String process_array[4];
String data_rec;
int Time_counter = 0;
int time_delay = 1;
bool blink_flag = true;
bool flag_filling = false;
unsigned char Matrix[8][8]={
  0,0,0,0,0,0,0,0,  
  0,0,0,0,0,0,0,0,  
  0,0,0,0,0,0,0,0,  
  0,0,0,0,0,0,0,0,  
  0,0,0,0,0,0,0,0,  
  0,0,0,0,0,0,0,0,  
  0,0,0,0,0,0,0,0,  
  0,0,0,0,0,0,0,0, 
};

  
unsigned char blink_matrix[8][8] =      
{  
  0,0,0,0,0,0,0,0,  
  0,0,0,0,0,0,0,0,  
  0,0,0,0,0,0,0,0,  
  0,0,0,0,0,0,0,0,  
  0,0,0,0,0,0,0,0,  
  0,0,0,0,0,0,0,0,  
  0,0,0,0,0,0,0,0,  
  0,0,0,0,0,0,0,0,  
};  

unsigned char smile[8][8]=
{  
  0,0,1,1,1,1,0,0,  
  0,1,0,0,0,0,1,0,  
  1,0,1,0,0,1,0,1,  
  1,0,0,0,0,0,0,1,  
  1,0,1,0,0,1,0,1,  
  1,0,0,1,1,0,0,1,  
  1,0,0,0,0,0,0,1,  
  0,1,1,1,1,1,1,0,  
};  
unsigned char sad[8][8]=
{  
  0,0,1,1,1,1,0,0,  
  0,1,0,0,0,0,1,0,  
  1,0,1,0,0,1,0,1,  
  1,0,0,0,0,0,0,1,  
  1,0,0,0,0,0,0,1,  
  1,0,0,1,1,0,0,1,  
  1,0,1,0,0,1,0,1,  
  0,1,1,1,1,1,1,0,  
};  
unsigned char T[8][8]=
{  
  1,1,1,1,1,1,1,1,  
  1,1,1,1,1,1,1,1,  
  0,0,0,1,1,0,0,0,  
  0,0,0,1,1,0,0,0,  
  0,0,0,1,1,0,0,0,  
  0,0,0,1,1,0,0,0,  
  0,0,0,1,1,0,0,0,  
  0,0,0,1,1,0,0,0,  
}; 
unsigned char E[8][8]=
{  
  1,1,1,1,1,1,1,0,  
  1,1,1,1,1,1,1,0,  
  1,1,0,0,0,0,0,0,  
  1,1,1,1,1,1,1,0,  
  1,1,1,1,1,1,1,0,  
  1,1,0,0,0,0,0,0,  
  1,1,1,1,1,1,1,0,  
  1,1,1,1,1,1,1,0,  
}; 
unsigned char C_letter[8][8]=
{  
  0,0,1,1,1,1,1,0,  
  0,1,1,1,1,1,1,1,  
  1,1,0,0,0,0,0,0,  
  1,1,0,0,0,0,0,0,  
  1,1,0,0,0,0,0,0,  
  1,1,0,0,0,0,0,0,  
  0,1,1,1,1,1,1,1,  
  0,0,1,1,1,1,1,0,  
};
unsigned char corazon_grande[8][8]=
{  
  0,1,1,0,0,1,1,0,  
  1,1,1,1,1,1,1,1,  
  1,1,1,1,1,1,1,1,  
  1,1,1,1,1,1,1,1,  
  0,1,1,1,1,1,1,0,  
  0,0,1,1,1,1,0,0,  
  0,0,0,1,1,0,0,0,  
  0,0,0,0,0,0,0,0,  
};
unsigned char corazon_peke[8][8]=
{  
  0,0,0,0,0,0,0,0,  
  0,0,1,0,0,1,0,0,  
  0,1,1,1,1,1,1,0,  
  0,1,1,1,1,1,1,0,  
  0,0,1,1,1,1,0,0,  
  0,0,0,1,1,0,0,0,  
  0,0,0,0,0,0,0,0,  
  0,0,0,0,0,0,0,0,  
};
//corazon, carita, TEC
void setup()  
{  

  for(int i = 0; i < 65; i++){
    Matrix_list[i]='0';
  }
  
  Serial.begin(57600);
  // iterate over the pins:
  for(int i = 0;i<8;i++)  
  // initialize the output pins:
  {  
    pinMode(R[i],OUTPUT);  
    pinMode(C[i],OUTPUT);  
  }  
}  

void change_Matrix(unsigned char dat[8][8]){
  for(int i = 0; i < 8; i++){
    for(int j = 0; j < 8; j++){
      Matrix[i][j]=dat[i][j];
    }
  }
}
void reset_matrix(){
  for(int i = 0; i < 8; i++){
    for(int j = 0; j < 8; j++){
      Matrix[i][j]=0;
    }
  }
}
void change_blink_matrix(unsigned char dat[8][8]){
  for(int i = 0; i < 8; i++){
    for(int j = 0; j < 8; j++){
      blink_matrix[i][j]=dat[i][j];
    }
  }
}
void Display()    
{  
  Clear();
  for(int c = 0; c<8;c++)  
  {  
    digitalWrite(C[c],LOW);//use thr column 
    //loop
    for(int r = 0;r<8;r++)  
    {  
      digitalWrite(R[r],Matrix[r][c]);  
    }    
    Clear();  //Remove empty display light
  } 
   
}  
  
void Clear()                            
{  
  for(int i = 0;i<8;i++)  
  {  
    digitalWrite(R[i],0);  
    digitalWrite(C[i],1);  
  }  
} 
void list_to_matrix(){
  for(int i = 0;i<64;i++){
    int col = i%8;
    int row = i/8;
    Matrix[row][col] = Matrix_list[i]-'0';
    if (i == 63){
      if (Matrix_list[i]-'0' != 1){
        Matrix[row][col] = 0;
      }
    }
  }
}

void process_msg(String data){
  //Fill the matrix
  if(data.substring(0,11)=="fill_matrix"){
    time_delay = 1;
    int part = data.substring(12,13).toInt();
    int row = data.substring(12,13).toInt();
    char mat_data[48] = {0};
    data.substring(14).toCharArray(mat_data,48);
    if(part == 0){
      for(int i = 0;i<4;i++){
        for(int j = 0;j<8;j++){
          Matrix[i][j] = mat_data[i*8+j]-'0';
        }
      }
      flag_filling = true;
      
      Serial.println("1");
      Serial.flush();
    }
    else if(part == 1){
      for(int i = 4;i<8;i++){
        for(int j = 0;j<8;j++){
          Matrix[i][j] = mat_data[(i-4)*8+j]-'0';
        }
      }
      Serial.print("8");
      Serial.flush();
      flag_filling = false;
    }
    
  }
  //Change function to excecute
  else if (data.substring(0,5) == "blink"){
    String Time, time_unit, state;
    int index_coma= data.substring(6).indexOf(",");
    Time = data.substring(6,6+index_coma);
    time_unit = data.substring(index_coma+7, index_coma+8);
    state =  data.substring(index_coma+9);
    process_array[0] = "blink";
    process_array[1] = Time; 
    process_array[2] = time_unit;
    process_array[3] = state;
    change_blink_matrix(Matrix);
    set_delay();
    if(state == "0"){
      clear_blink();
    }
  }
  else if (data.substring(0,5) == "smile"){
    process_array[0] = "smile";
    process_array[1] = "0";
    time_delay = 700;
    Serial.println("2");
  }else if (data.substring(0,3) == "tec"){
    process_array[0] = "tec";
    process_array[1] = "0";
    time_delay = 700;
    Serial.println("2");
  }else if (data.substring(0,5) == "heart"){
    process_array[0] = "heart";
    process_array[1] = "0";
    time_delay = 700;
    Serial.println("2");
  }
  
}
void clear_blink(){
  process_array[0] = "";
  time_delay = 1;
  reset_matrix();
  change_Matrix(Matrix);
}
void set_delay(){
  if(process_array[2] == "0"){//milisegunods
    time_delay = process_array[1].toInt();
  }else if(process_array[2] == "1"){//segundos
    time_delay = process_array[1].toInt()*1000;
  }else if(process_array[2] == "2"){//min
    time_delay = (process_array[1].toInt()*60000);
  }
}

void _blink(bool state){
    if(blink_flag == false){
      blink_flag = true;
      change_Matrix(blink_matrix);
    }else{
      blink_flag = false;
      reset_matrix();
      Clear();
    }
  
}
void loop()  
{  
  if(Serial.available()>0){
    data_rec = Serial.readString();
    process_array[0] = "";
    process_msg(data_rec);
  }
  if(!flag_filling){
    Time_counter+=1;
    delay(1);
    //blink
    if(process_array[0] == "blink" && Time_counter >= time_delay){
      Time_counter = 0;
      _blink(true);
    }
    //smile animation
    else if(process_array[0] == "smile" && Time_counter >= time_delay){
      Time_counter = 0;
      if (process_array[1] == "1"){
        change_Matrix(smile);
        process_array[1] = "0";
      }else{
        process_array[1] = "1";
        change_Matrix(sad);
      }
    }
    //
    else if(process_array[0] == "tec"&& Time_counter >= time_delay){
      Time_counter = 0;
      if (process_array[1] == "0"){
        change_Matrix(T);
        process_array[1] = "1";
      }else if(process_array[1] == "1"){
        process_array[1] = "2";
        change_Matrix(E);
      }else{
        process_array[1] = "0";
        change_Matrix(C_letter);
      }
    }else if(process_array[0] == "heart" && Time_counter >= time_delay){
      Time_counter = 0;
      if (process_array[1] == "1"){
        change_Matrix(corazon_grande);
        process_array[1] = "0";
      }else{
        process_array[1] = "1";
        change_Matrix(corazon_peke);
      }
    }
    Display();
  }
  //se agrega esta validacion ya que el ultimo led se enciende al terminar la conexion con el puerto serial;
  /*  
  change_Matrix(smalllove);
  for(int i = 0 ; i < 50 ; i++)         //Loop display 50 times
  {     
    Display();                 //Display the "small Heart" 
  }
  change_Matrix(smile);
  for(int i = 0 ; i < 50 ; i++)         //Loop display 50 times
  {  
    Display();                 //Display the "small Heart" 
  }
  */
}  
 
