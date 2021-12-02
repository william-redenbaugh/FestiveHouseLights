import serial 
import time 
import colorsys

class LEDMatrix:
    def __init__(self):
        self.serial = serial.Serial('/dev/ttyUSB1', 921600, timeout=1)
        self.data_arr = [0] * 400 * 3

    def update(self):
        self.serial.write(bytearray(self.data_arr))
    
    def set_led(self, r, g, b, n):
        if r > 254:
            r = 254
        if g > 254: 
            g = 254
        if b > 254:
            b = 254

        self.data_arr[n * 3] = r
        self.data_arr[n * 3 + 1] = g
        self.data_arr[n * 3 + 2] = b
    
    def set_led_hsv(self, h, s, v, pos):
        if h > 255:
            h = 255
        if s > 255:
            s = 255
        if v > 255:
            v = 255

        hue = h/255
        saturation = s/255
        value = v/255
        n = colorsys.hsv_to_rgb(hue, saturation, value)
        self.set_led(int(n[0] * 255), int(n[1] * 255), int(n[2] * 255), pos)
    
led = LEDMatrix()

while True: 
    for h in range(255):
        for p in range(400):
            led.set_led_hsv((h + p)%255, 255, 255, p)
        led.update()
        time.sleep(0.01)