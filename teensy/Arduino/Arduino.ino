#include <ArduinoJson.h>
#include "SerialTransfer.h"
// Progrma para la <expo 2022
int arr_Param[2]; //ARREGLO QUE MANEJA EL VALOR DE TENSION INICIAL Y UN
// VALOR 1 DE START 0 DE STOP
SerialTransfer myTransfer;
char Labels[5][6] = {"100-1", "101-1", "102-0", "103-0", "104-0"};
long test_started = false;
bool led_state = true;


//Variables globales
unsigned long t_temp = 0;
unsigned long t_print = 0;
unsigned long Tini;
float convt = 3.3 / 4095;

// Contadores
int i;

// Tensiones
int m = 1024;
int V1_read[1024];
int V2_read[1024];
int V3_read[1004];
float aux1 = 0;

// Coeficiente
float a[3] = {0.01925927420234,  0.01925927420234, 0};
float b[3] = {1, -0.9614814515953, 0};

// Variables Filtro de Tensión
float xV1[2] = {0, 0};
float yV1[2] = {0, 0};
float xV2[2] = {0, 0};
float yV2[2] = {0, 0};
float xV3[2] = {0, 0};
float yV3[2] = {0, 0};

//Variables de lectura
int T1_read = 0;
int T2_read = 0;
int T3_read = 0;
int T4_read = 0;
int T5_read = 0;
int T6_read = 0;

// Variables de temperatura
float T1 = 0;
float T2 = 0;
float T3 = 0;
float T4 = 0;
float T5 = 0;
float T6 = 0;

//Filtro de temperatura
float alpha = 0.2543;
float EMA_T1 = 0;
float EMA_T2 = 0;
float EMA_T3 = 0;
float EMA_T4 = 0;
float EMA_T5 = 0;
float EMA_T6 = 0;

//
struct __attribute__((__packed__)) STRUCT {
  long recieve_id;
  long potentiometer_value;
  float value;
  char label[6];
} workingstruct;


void setup() {

  Serial.begin(115200);
  myTransfer.begin(Serial);
  analogReadResolution(12);
  
  pinMode(13, OUTPUT);
  
  t_temp = millis();
  t_print = millis();
  Tini = millis();
  
}

void loop() {

  if (myTransfer.available()) {
    // Receive buffer
    uint16_t recSize = 0;
    recSize = myTransfer.rxObj(arr_Param, recSize);
  }
  
  // Lecturas de Tensión
  for (i = 0; i < m; i++) {
    V1_read[i] = analogRead(A3) - 2048 ;
    V2_read[i] = analogRead(A4) - 2048 ;
    V3_read[i] = analogRead(A5) - 2048 ;
  }
  
  // Filtrado de Tesnión.
  for (i = 0; i < m; i++) {
    //V1
    xV1[0] = V1_read[i] * convt * 927 ;
    yV1[0] = a[0] * xV1[0] + a[1] * xV1[1] - b[1] * yV1[1];
    xV1[1] = xV1[0];
    yV1[1] = yV1[0];
    // V2
    xV2[0] = V2_read[i] * convt * 927 ;
    yV2[0] = a[0] * xV2[0] + a[1] * xV2[1] - b[1] * yV2[1];
    xV2[1] = xV2[0];
    yV2[1] = yV2[0];
    // V3
    xV3[0] = V3_read[i] * convt * 927 ;
    yV3[0] = a[0] * xV3[0] + a[1] * xV3[1] - b[1] * yV3[1];
    xV3[1] = xV3[0];
    yV3[1] = yV3[0];
    //
    //Impresión de tensión
    //    Serial.print(yV1[0]);
    //    Serial.print(" ");
    //    Serial.print(yV2[0]);
    //    Serial.print(" ");
    //    Serial.println(yV3[0] );
    //    delay(10);
  }
  
  //Lectura de Temepraturas.
  if (millis() - t_temp > 55) {
    t_temp = millis();
    T1_read = analogRead(A10);
    T2_read = analogRead(A11);
    T3_read = analogRead(A12);
    T4_read = analogRead(A13);
    //T5_read = analogRead(A14);
    //T6_read = analogRead(A15);
    EMA_T1 = alpha * T1_read * convt + (1 - alpha) * EMA_T1;
    EMA_T2 = alpha * T2_read * convt + (1 - alpha) * EMA_T2;
    EMA_T3 = alpha * T3_read * convt + (1 - alpha) * EMA_T3;
    EMA_T4 = alpha * T4_read * convt + (1 - alpha) * EMA_T4;
    //EMA_T5 = alpha * T5_read * convt + (1 - alpha) * EMA_T5;
    //EMA_T6 = alpha * T6_read * convt + (1 - alpha) * EMA_T6;
  }
  
  //Temperatura.
  T1 = 2.05 * EMA_T1 * EMA_T1 + 58.51 * EMA_T1 - 1.052;
  T2 = 2.05 * EMA_T2 * EMA_T2 + 58.51 * EMA_T2 - 1.052;
  T3 = 2.05 * EMA_T3 * EMA_T3 + 58.51 * EMA_T3 - 1.052;
  T4 = 2.05 * EMA_T4 * EMA_T4 + 58.51 * EMA_T4 - 1.052;
  //T5 = 2.05 * EMA_T5 * EMA_T5 + 58.51 * EMA_T5 - 1.052;
  //T6 = 2.05 * EMA_T6 * EMA_T6 + 58.51 * EMA_T6 - 1.052;



  // Transmisiòn de datos




  if (arr_Param[0] == 1) {

    //digitalWrite(13, HIGH);

    if (millis() - Tini > 400) {
      // Set data POTENCIOMETRO
      workingstruct.recieve_id = 1;
      if (digitalRead(2) == LOW) aux1 = 0;
      workingstruct.potentiometer_value = T1;
      //      workingstruct.potentiometer_value = arr_Param[1];
      //
      // Send buffer 100 T1
      workingstruct.value = float(T1); // Temperatura 1.
      strcpy(workingstruct.label, "100-1");
      //
      myTransfer.sendDatum(workingstruct);
      workingstruct.recieve_id += 1;
      //
      // Send buffer 101 T2
      workingstruct.value = float(T2); // Temperatura 2.
      strcpy(workingstruct.label, "101-1");
      //
      myTransfer.sendDatum(workingstruct);
      workingstruct.recieve_id += 1;
      //
      //
      myTransfer.sendDatum(workingstruct);
      workingstruct.recieve_id += 1;
      //
      // Send buffer 300 iF1F2
      workingstruct.value = float(T3);
      strcpy(workingstruct.label, "200-0");
      //
      myTransfer.sendDatum(workingstruct);
      workingstruct.recieve_id += 1;
      //
      // Send buffer 301 VF1F2
      workingstruct.value = float(T4);
      strcpy(workingstruct.label, "300-0");
      //
      myTransfer.sendDatum(workingstruct);
      workingstruct.recieve_id += 1;
      //
      // Send buffer 400 RPM
      //workingstruct.value = float(T5);
      //strcpy(workingstruct.label, "400-0");
      //
      myTransfer.sendDatum(workingstruct);
      workingstruct.recieve_id += 1;
      //



      Tini = millis();
    }
    
  }else{
    
    //digitalWrite(13, LOW);
    
  }

  

  // Impresión de temperatura monitor serie
  if (millis() - t_print > 500) {

    Serial.print("T1d=" + String(T1));
    Serial.print("  ");
    Serial.print("T2=" + String(T2));
    Serial.print("  ");
    Serial.print("T3=" + String(T3));
    Serial.print("  ");
    Serial.print("T4=" + String(T4));
    Serial.print("  ");
    Serial.print("T5=" + String(T5));
    Serial.print("  ");
    Serial.println("T6=" + String(T6));
    t_print = millis();
  }

}
