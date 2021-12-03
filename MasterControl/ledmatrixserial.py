import serial 
from hsv_kelvin_rgb_conv import convert_K_to_RGB
import threading
import colorsys 

class LEDMatrix:
    def __init__(self, port, num_leds):
        self.serial = serial.Serial(port, 921600, timeout=1)
        self.data_arr = [0] * num_leds * 3
        self.num_leds = num_leds
        self.lock = threading.Lock()

    def update(self):
        self.lock.acquire()
        self.serial.write(bytearray(self.data_arr))
        self.lock.release()
    
    def set_led(self, r, g, b, n):
        if r > 254:
            r = 254
        if g > 254: 
            g = 254
        if b > 254:
            b = 254

        self.lock.acquire()
        self.data_arr[n * 3] = r
        self.data_arr[n * 3 + 1] = g
        self.data_arr[n * 3 + 2] = b
        self.lock.release()
    
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

    def set_all_led(self, r, g, b):
        for i in range(self.num_leds):
            self.set_led(r, g, b, i)

    def set_all_led_hsv(self, r, g, b):
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
        self.set_all_led(int(n[0] * 255), int(n[1] * 255), int(n[2] * 255))
        

    def set_led_kelvin(self, kelvin):
        r, g, b = convert_K_to_RGB(kelvin)
        for i in range(self.num_leds):
            self.set_led(int(r), int(g), int(b), i)

class VirtualLEDStrip:
    def __init__(self, strip, start_pos, end_pos):
        self.strip = strip
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.num_leds = end_pos - start_pos
    def set_led(self, r, g, b, n):
        if n >= self.num_leds:
            return
        if n < 0:
            return 
        new_pos = n + self.start_pos
        self.strip.set_led(r, g, b, new_pos)
    
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

    def set_led_kelvin(self, kelvin):
        r, g, b = convert_K_to_RGB(kelvin)
        for i in range(self.num_leds):
            self.set_led(int(r), int(g), int(b), i)
