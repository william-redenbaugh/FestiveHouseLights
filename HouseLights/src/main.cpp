#include <Arduino.h>
#include <WiFi.h>
#include <Adafruit_NeoPixel.h>

#include <WiFiUdp.h>

/* WiFi network name and password */
const char * ssid = "dd-wrt";
const char * pwd = "0000000000";

const int udpPort = 44444;
//create UDP instance
WiFiUDP udp;

#define PIN 18
#define NUM_LEDS 400
// Parameter 1 = number of pixels in strip
// Parameter 2 = Arduino pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
//   NEO_RGBW    Pixels are wired for RGBW bitstream (NeoPixel RGBW products)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_LEDS, PIN, NEO_GRB + NEO_KHZ800);

void update_led_strip(void *parameters){
  for(;;){
    strip.show(); 
    delay(15);
  }
}

void setup() {
  Serial.begin(921600);
  // put your setup code here, to run once:
  strip.begin();
  strip.setBrightness(200);
  strip.show(); // Initialize all pixels to 'off'

  xTaskCreate(update_led_strip, "LED update thread", 4000, NULL, 1, NULL);
}

int led = 0;
void loop() {
restart:
  if(led == 399)
    led = 0; 
  uint8_t red = 0; 
  uint8_t green = 0; 
  uint8_t blue = 0; 

  uint8_t data = Serial.read(); 
  if(data == 255){
    led = 0;
    goto restart;     
  }
  red = data; 

  data = Serial.read(); 
  if(data == 255){
    led = 0;    
    goto restart; 
  }
  green = data; 

  data = Serial.read(); 
  if(data == 255){
    led = 0;    
    goto restart; 
  }
  blue = data; 

  strip.setPixelColor(led, green, red, blue); 
  led++; 
}