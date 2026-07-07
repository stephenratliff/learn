// Program: mcu_sketch.ino
// This runs on the MCU (the real-time side).

#include <Arduino.h>
#include <Bridge.h> // Include the Bridge library

void setup() {
  // Set pin A0 as an input. This is where you would connect a sensor,
  // like a potentiometer or a photoresistor.
  pinMode(A0, INPUT);

  // Initialize the Bridge
  Bridge.begin();

  // Register the function "readSensor" so Python can call it.
  // The function that will be called is localReadSensor().
  Bridge.register_handler("readSensor", localReadSensor);
}

void loop() {
  // The main loop can be empty, as we are letting Python
  // trigger the sensor read on demand.
  delay(500);
}

// This is the function that Python will trigger.
// It must return a Bridge-compatible type, like a String.
String localReadSensor() {
  // Read the value from the analog pin (will be 0-1023).
  int sensorValue = analogRead(A0);

  // Return the value as a String so the Bridge can send it.
  return String(sensorValue);
}