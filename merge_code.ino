#include "DHT.h"
#include <LiquidCrystal.h>

#define DHT11_PIN 4 // pin for o/p in dht11
#define sensor_pin A0 // pin   for i/p in soil moisture sensor

DHT dht11(DHT11_PIN, DHT11);
LiquidCrystal lcd(7, 9, 10, 11, 12, 13); // function to which pins are connected

void setup() {
  Serial.begin(9600);
  dht11.begin(); // initialize the DHT11 sensor
  pinMode(sensor_pin, INPUT); // initialize the soil moisture sensor pin
  lcd.begin(16, 2); // initialize the LCD screen
}

void loop() {
  int humi = dht11.readHumidity();
  float tempC = dht11.readTemperature();
  float tempF = dht11.readTemperature(true);
  int sensor_analog = analogRead(sensor_pin);
  float moisture_percentage = 100 - ((sensor_analog / 1023.00) * 100);

  if (isnan(humi) || isnan(tempC)) {
    Serial.println("Failed to read from DHT11 sensor!");
  } else {
    Serial.print("H:");
    Serial.print(humi);
    Serial.print("%, ");
    Serial.print("T:");
    Serial.print(tempC);
    Serial.print("C");
    

    lcd.setCursor(0, 0);
    lcd.print("H:");
    lcd.print(humi);
    lcd.print("%");
    lcd.setCursor(8, 0);
    lcd.print("T:");
    lcd.print(tempC);
    lcd.print("C");

    lcd.setCursor(0, 2);
    lcd.print("M:");
    lcd.print(moisture_percentage);
    lcd.print("%");
  }

  Serial.print(", M:");
  Serial.print(moisture_percentage);
  Serial.print("%");
  Serial.println();

  delay(2000);
}


