#include "mainv2.h"
#include "buzzrgb.h"

char* ssid = "FPWOM";
char* password = "NHl7g371#0";
char* server_url = "http://192.168.100.18:8080/api/recv";

// Associate a solenoid with a pin, this is made to make programming less prone to errors
short int solenoid_1 = 27;
short int solenoid_2 = 26;
short int solenoid_3 = 25;
short int solenoid_4 = 33;

short int solenoids[HOLDER_CAPACITY] = {solenoid_1, solenoid_2, solenoid_3, solenoid_4}; // This array holds each solenoid's pin, ORDER MATTERS

int machine_status = 0;
// Status codes:
// 0 : Machine starting
// 1 : Neutral (Empty)
// 2 : Neutral (Busy)
// -1 : Emergency Mode

const int LidCheck = 0;

MFRC522 mfrc522(SS_PIN, RST_PIN);

bool connectToWiFi() {
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 10) {
    delay(750);
    Serial.println("Retrying...");
    attempts++;
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("WiFi connected");
    return true;
  } else {
    Serial.println("Failed to connect to WiFi");
    return false;
  }
}


void open_solenoid(int slot_position){
  Serial.print("\tOpening slot: " + String(slot_position)+ "\n");
  digitalWrite(solenoids[slot_position], 1);
  delay(SOLENOID_OPEN_TIME);
  digitalWrite(solenoids[slot_position], LOW);
  Serial.print("\tSlot closed\n");
  }

void controller(const String& code, int slot_position){
  if (code == "0.1"){ // Code to add bicycle to holder
    machine_status = 2;
    rgb_set(1, 1, 1); // Set LED color to White
    success_buzzer_sound();
    open_solenoid(slot_position);
  } else if (code == "1.1"){ // Code to remove bicycle from holder
    machine_status = 1;
    rgb_set(1, 1, 1); // Set LED color to White
    success_2_buzzer_sound();
    open_solenoid(slot_position);
  } else{
    Serial.print("No bicycle change.\n");
    rgb_set(1, 1, 0); // Set LED color to Yellow
    error_buzzer_sound();
  }
  delay(500); // Short delay after output message or action
}

bool sendUUID(const String& uuid, const String& ip) {
  Serial.println("Sending UUID to server...");
  JSONVar dataObject;
  dataObject["uuid"] = uuid;
  dataObject["ip"] = ip;
  String jsonString = JSON.stringify(dataObject);
  HTTPClient http;
  http.begin(server_url);
  http.addHeader("Content-Type", "application/json");
  int httpResponseCode = http.POST(jsonString);
  String response_data = http.getString();
  http.end();

  JSONVar response_data_json = JSON.parse(response_data);

  controller(response_data_json["code"], response_data_json["slot_to_open"]);

  if (httpResponseCode == HTTP_CODE_OK) {
    Serial.println("UUID sent successfully");
    return true;
  } 
  Serial.print("Failed to send UUID. Error code: ");
  Serial.println(httpResponseCode);
  return false;
}

String readRFID() {
  if (!mfrc522.PICC_IsNewCardPresent()) {
    return "";
  }
  if (!mfrc522.PICC_ReadCardSerial()) {
    return "";
  }
  String uuid = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    uuid += String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
    uuid += String(mfrc522.uid.uidByte[i], HEX);
  }
  mfrc522.PICC_HaltA();
  return uuid;
}

void setup() {
  Serial.begin(115200);
  SPI.begin();
  mfrc522.PCD_Init(); // Init mfcr522
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(LidCheck, INPUT);
  while (!Serial) {}
  
  for(int i=0; i<HOLDER_CAPACITY; i++){
    pinMode(solenoids[i], OUTPUT); // Set every solenoid pin as OUTPUT
  }
  
  connectToWiFi();
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    rgb_set(1, 0, 0);
    connectToWiFi();
  }
  switch (machine_status){
    case -1:
      rgb_set(1,0,0);
      break;
    case 1:
      rgb_set(0, 1, 0);
      break;
    case 2:
      rgb_set(0, 0, 1);
      break;
  }

  // Check if lid is open
  if (LidCheck !=1){
    machine_status = -1;
  }
  
  String uuid = readRFID();
  if (uuid != "") {
    emit_sound(4, 1); // Short sound to notify the user that the tag has been scaned
    String ip = WiFi.localIP().toString();
    if (sendUUID(uuid, ip)) {
      delay(200); // Delay to avoid sending data too frequently
    }
  }
  delay(20); // Delay between RFID scans
}