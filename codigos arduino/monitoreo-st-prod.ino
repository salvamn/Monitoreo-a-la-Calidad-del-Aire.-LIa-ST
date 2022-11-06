// By Salvador Mellado

#include <ESP8266WiFi.h>
#include <DHT.h>
#include <DHT_U.h>
#include <SoftwareSerial.h>
#include <SDS011.h>
#include <ArduinoJson.h>
#include <LittleFS.h>
#include <PubSubClient.h>
#include "NTPClient.h"

#define DHTPIN D1
#define DHTTYPE DHT22
#define SDS_PIN_RX D7
#define SDS_PIN_TX D6
#define MSG_BUFFER_SIZE (1024)

DHT sensor_dht(DHTPIN, DHTTYPE);
SoftwareSerial serialSDS(SDS_PIN_RX, SDS_PIN_TX );
DynamicJsonDocument doc(1024);
DynamicJsonDocument doc_sistema_archivos(1024);
WiFiClient espClient;
PubSubClient client(espClient);
SDS011 my_sds;

float humedad;
float temperatura;
int uv_pin = A0;
int nivel_uv;
float p10,p25;
int error;

const char* ssid = "tu red wifi";
const char* password = "tu contraseña";

const char* mqtt_server = "tu servidor";

const char* topico_entrada = "tu topico";
const char* topico_entrada_verificar_conexion = "tu topico";

char v1[10];
char v2[10];
char v3[10];

unsigned long tiempo = 0;
unsigned long HoraSegundos = 150000;  // 3.600.000 = 1 hora, 10000 = 10 segundos, 600.000 = 10 minutos
char verificacion[1024] = "Conexion realizada con exito";
char data[1024];

void setup() {
  Serial.begin(115200);
  if (!LittleFS.begin()) {
    return;
  }
  delay(5000);
  WiFi.begin(ssid, password);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  if (!client.connected()) {
    reconnect();
  }
  my_sds.begin(2,6);
  sensor_dht.begin();
  pinMode(A0, INPUT);
  leerDatos();

  client.publish(topico_entrada_verificar_conexion, verificacion);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  
  if (millis() - tiempo >= 100000) { // tiempo = 0, horasegundos = 600.000 10 minutos
    tiempo = millis();
    leerDht();
    leerUv();
    leerSds();
    serializeJson(doc, data);
    client.publish(topico_entrada, data);
    Serial.println(data);
  }
}

void leerDatos() {
  File file = LittleFS.open("datos.json", "r");
  if (!file) {
    return;
  }
  if (file.available()) {
    String json_serializado = file.readString();
    deserializeJson(doc_sistema_archivos, json_serializado);
    String ubicacion = doc_sistema_archivos["ubicacion"];
    String administrador = doc_sistema_archivos["admin"];
    doc["ubicacion"] = ubicacion;
    doc["admin"] = administrador;
  }
  file.close();
}

void setup_wifi() {
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  Serial.print("WiFi conectado - Direccion IP: ");
  Serial.println(WiFi.localIP());
  //doc["ip"] = WiFi.localIP();
}

void callback(char* topic, byte* payload, unsigned int length) {
  for (int i = 0; i < length; i++) {
    Serial.println((char)payload[i]);
  }
}

void reconnect() {
  while (!client.connected()) {
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    if (client.connect(clientId.c_str())) {
      client.subscribe(topico_entrada);
      //client.publish(topico_salida, "Hello World");
    } else {
      delay(5000);
    }
  }
}

void leerDht() {
  humedad = sensor_dht.readHumidity();
  temperatura = sensor_dht.readTemperature();
  if (isnan(humedad) && isnan(temperatura)) {
    return;
  }
  doc["humedad"] = humedad;
  doc["temperatura"] = temperatura;
}

void leerSds() {
  error = my_sds.read(&p25,&p10);
  if (! error) {
    doc["PM25"] = p25;
    doc["sPM10"] = p10;
  }

}

void leerUv() {
  nivel_uv = averageAnalogRead(A0);
  float outputVoltage = 3.3 * nivel_uv / 1024;
  float uvIntensity = mapfloat(outputVoltage, 0.99, 2.9, 0.0, 15.0);
  doc["lectura"] = nivel_uv;
  doc["intensidad_uv"] = uvIntensity;
}

int averageAnalogRead(int pinToRead)
{
  byte numberOfReadings = 8;
  unsigned int runningValue = 0;
  for (int x = 0 ; x < numberOfReadings ; x++)
    runningValue += analogRead(pinToRead);
  runningValue /= numberOfReadings;
  return (runningValue);
}

float mapfloat(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
