from posix import NGROUPS_MAX
import serial 
import time 
import colorsys
import math 

def convert_K_to_RGB(colour_temperature):
    """
    Converts from K to RGB, algorithm courtesy of 
    http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/
    """
    #range check
    if colour_temperature < 1000: 
        colour_temperature = 1000
    elif colour_temperature > 40000:
        colour_temperature = 40000
    
    tmp_internal = colour_temperature / 100.0
    
    # red 
    if tmp_internal <= 66:
        red = 255
    else:
        tmp_red = 329.698727446 * math.pow(tmp_internal - 60, -0.1332047592)
        if tmp_red < 0:
            red = 0
        elif tmp_red > 255:
            red = 255
        else:
            red = tmp_red
    
    # green
    if tmp_internal <=66:
        tmp_green = 99.4708025861 * math.log(tmp_internal) - 161.1195681661
        if tmp_green < 0:
            green = 0
        elif tmp_green > 255:
            green = 255
        else:
            green = tmp_green
    else:
        tmp_green = 288.1221695283 * math.pow(tmp_internal - 60, -0.0755148492)
        if tmp_green < 0:
            green = 0
        elif tmp_green > 255:
            green = 255
        else:
            green = tmp_green
    
    # blue
    if tmp_internal >=66:
        blue = 255
    elif tmp_internal <= 19:
        blue = 0
    else:
        tmp_blue = 138.5177312231 * math.log(tmp_internal - 10) - 305.0447927307
        if tmp_blue < 0:
            blue = 0
        elif tmp_blue > 255:
            blue = 255
        else:
            blue = tmp_blue
    
    return red, green, blue

class LEDMatrix:
    def __init__(self, port, num_leds):
        self.serial = serial.Serial(port, 921600, timeout=1)
        self.data_arr = [0] * num_leds * 3
        self.num_leds = num_leds

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

    def set_led_kelvin(self, kelvin):
        r, g, b = convert_K_to_RGB(kelvin)
        for i in range(self.num_leds):
            self.set_led(int(r), int(g), int(b), i)
    
led = LEDMatrix('/dev/ttyUSB1', 400)
led2 = LEDMatrix('/dev/ttyUSB0', 100)

while True: 
    for h in range(2200, 7000, 20):
        led.set_led_kelvin(h)
        led2.set_led_kelvin(h)
        led.update()
        led2.update()
        time.sleep(0.01)
    for h in range(7000, 2200, -20):
        led.set_led_kelvin(h)
        led2.set_led_kelvin(h)
        led2.update()
        led.update()
        time.sleep(0.01) 