#include "HX711.h"

//#define calibration_factor 30270
#define calibration_factor 31403
#define DOUT 3
#define CLK 2

HX711 scale;

void setup() {
  Serial.begin(9600);
  //Serial.println("HX711 scale reader");

  scale.begin(DOUT, CLK);
  scale.set_scale(calibration_factor);
  //scale.tare();

  //Serial.println("Readings:");
}

void loop() {
  //Serial.print("Reading: ");
  double weight = scale.get_units(15); //Returns a float
  String output_weight = String(weight, 2);
  int len = output_weight.length();
  Serial.println(output_weight);
  //Serial.print(output_weight);
  //Serial.print(" lbs");
  //delay(500);
  //Serial.println();
}
