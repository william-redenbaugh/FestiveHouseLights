#include <Arduino.h>

#include <Adafruit_NeoPixel.h>
#define PIN 18

// Parameter 1 = number of pixels in strip
// Parameter 2 = Arduino pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
//   NEO_RGBW    Pixels are wired for RGBW bitstream (NeoPixel RGBW products)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(400, PIN, NEO_GRB + NEO_KHZ800);


// Rainbow cycle along whole strip. Pass delay time (in ms) between frames.
void rainbow(int start_led, int end_led, int wait) {
  // Hue of first pixel runs 5 complete loops through the color wheel.
  // Color wheel has a range of 65536 but it's OK if we roll over, so
  // just count from 0 to 5*65536. Adding 256 to firstPixelHue each time
  // means we'll make 5*65536/256 = 1280 passes through this outer loop:
  for(long firstPixelHue = 0; firstPixelHue < 5*65536; firstPixelHue += 256) {
    for(int i=start_led; i<end_led; i++) { // For each pixel in strip...
      // Offset pixel hue by an amount to make one full revolution of the
      // color wheel (range of 65536) along the length of the strip
      // (strip.numPixels() steps):
      int pixelHue = firstPixelHue + (i * 65536L / (end_led - start_led));
      // strip.ColorHSV() can take 1 or 3 arguments: a hue (0 to 65535) or
      // optionally add saturation and value (brightness) (each 0 to 255).
      // Here we're using just the single-argument hue variant. The result
      // is passed through strip.gamma32() to provide 'truer' colors
      // before assigning to each pixel:
      strip.setPixelColor(i, strip.gamma32(strip.ColorHSV(pixelHue)));
    }
    delay(wait);  // Pause for a moment
  }
}

// Some functions of our own for creating animated effects -----------------

// Fill strip pixels one after another with a color. Strip is NOT cleared
// first; anything there will be covered pixel by pixel. Pass in color
// (as a single 'packed' 32-bit value, which you can get by calling
// strip.Color(red, green, blue) as shown in the loop() function above),
// and a delay time (in milliseconds) between pixels.
void colorWipe(uint32_t color, int wait, int start_led, int end_led) {
  for(int i=start_led; i<end_led; i++) { // For each pixel in strip...
    strip.setPixelColor(i, color);         //  Set pixel's color (in RAM)
    delay(wait);                           //  Pause for a moment
  }
}

void update_led_strip(void *parameters){
  for(;;){
    strip.show(); 
    delay(15);
  }
}

void led_one_thread(void *parameters){
  for(;;){
    rainbow(0, 200, 10);
  }
}

void setup() {
  // put your setup code here, to run once:
  strip.begin();
  strip.setBrightness(30);
  strip.show(); // Initialize all pixels to 'off'

  xTaskCreate(update_led_strip, "LED update thread", 4000, NULL, 1, NULL);
  xTaskCreate(led_one_thread, "LED update thread", 4000, NULL, 1, NULL);
}

void loop() {
  // Fill along the length of the strip in various colors...
  colorWipe(strip.Color(255,   0,   0), 50, 201, 400); // Red
  colorWipe(strip.Color(  0, 255,   0), 50, 201, 400); // Green
  colorWipe(strip.Color(  0,   0, 255), 50, 201, 400); // Blue
}