from posix import NGROUPS_MAX
from ledmatrixserial import *
import time 
import colorsys
import math 
import threading
import copy
import atexit
from json_parse import *
import random
import json

kill_all = False

led = LEDMatrix('/dev/ttyUSB1', 400)
led2 = LEDMatrix('/dev/ttyUSB0', 100)

office_door_strip = VirtualLEDStrip(copy.copy(led), 290, 303)
living_room_strip = VirtualLEDStrip(copy.copy(led), 0, 238)
couch_underglow = VirtualLEDStrip(copy.copy(led2), 51, 99)
home_theater_underglow = VirtualLEDStrip(copy.copy(led2), 0, 49)
left_hallway = VirtualLEDStrip(led, 239, 289)
right_hallway = VirtualLEDStrip(led, 304, 399)

def update_strip_thread():
    global led, led2, kill_all
    while True: 
        led.update()
        led2.update()
        if kill_all:
            return
        time.sleep(0.01)

def hallway_rainbow():
    global left_hallway, right_hallway, kill_all
    while True:
        for n in range(255):
            for j in range(100):
                left_hallway.set_led_hsv((n + j)%255, 255, 255, j)
                right_hallway.set_led_hsv((n + j)%255, 255, 255, j)
            if kill_all:
                return
            time.sleep(0.03)


def exploding_colors():
    global living_room_strip
    hsv = [0] * living_room_strip.num_leds * 3
    while True:
        n = random.randint(0, living_room_strip.num_leds-1)
        h = random.randint(0, 255)
        hsv[n * 3] = 85
        hsv[n * 3 + 1] = 255
        hsv[n * 3 + 2] = 255

        n = random.randint(0, living_room_strip.num_leds-1)
        h = random.randint(0, 255)
        hsv[n * 3] = 85
        hsv[n * 3 + 1] = 0
        hsv[n * 3 + 2] = 255

        n = random.randint(0, living_room_strip.num_leds-1)
        h = random.randint(0, 255)
        hsv[n * 3] = 0
        hsv[n * 3 + 1] = 255
        hsv[n * 3 + 2] = 255

        # Decrement
        for i in range(living_room_strip.num_leds):
            if hsv[i * 3 + 2] > 6:
                hsv[i * 3 + 2] = (hsv[i * 3 + 2]) - 6
            else:
                hsv[i * 3 + 2] = 0

        for i in range(living_room_strip.num_leds):
            living_room_strip.set_led_hsv(hsv[i * 3], hsv[i * 3 + 1], hsv[i * 3 + 2], i)
        
        time.sleep(0.01)

free_busy_empty = 0
def busy_free_thread():
    global office_door_strip, free_busy_empty, kill_all

    while True:
        if free_busy_empty == 0:
            for v in range(0, 255, 15): 
                for n in range(13):
                    office_door_strip.set_led_hsv(85, 255, v, n)
                time.sleep(0.03)
            for v in range(255, 0, -15): 
                for n in range(13):
                    office_door_strip.set_led_hsv(85, 255, v, n)
                time.sleep(0.03)

        if free_busy_empty == 1:
            for v in range(255, 15): 
                for n in range(13):
                    office_door_strip.set_led_hsv(0, 255, v, n)
                time.sleep(0.03)
            for v in range(255, 0, -15): 
                for n in range(13):
                    office_door_strip.set_led_hsv(0, 255, v, n)
                time.sleep(0.03)

        if free_busy_empty == 2:
            for n in range(13): 
                office_door_strip.set_led(0, 0, 0, n)
                time.sleep(0.2)
        
        if kill_all:
            return


def ambient_led_thread():
    global living_room_strip, couch_underglow, home_theater_underglow, led2, kill_all
    while True: 
        for h in range(2200, 7000, 20):
            living_room_strip.set_led_kelvin(h)
            couch_underglow.set_led_kelvin(h)
            if kill_all: 
                return
            time.sleep(0.01)
           
        for h in range(7000, 2200, -20):
            living_room_strip.set_led_kelvin(h)
            couch_underglow.set_led_kelvin(h)
            time.sleep(0.01)
            if kill_all:
                return

def web_interaction_thread():
    localIP     = "127.0.0.1"
    localPort   = 8080
    bufferSize  = 1024
    msgFromServer       = "Hello UDP Client"
    bytesToSend         = str.encode(msgFromServer)
    # Create a datagram socket
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # Bind to address and ip
    UDPServerSocket.bind((localIP, localPort))
    print("UDP server up and listening")
    # Listen for incoming datagrams
    while(True):
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        json_data = parse_input_json(message)

        if(json_data["office_door_state"] == "free"):
            free_busy_empty = 0

        if(json_data["office_door_state"] == "busy"):
            free_busy_empty = 1

        if(json_data["office_door_state"] == "empty"):
            free_busy_empty = 2

update_thread_handler = threading.Thread(target=update_strip_thread)
ambient_thread_handler = threading.Thread(target=exploding_colors)
rainbow_thread_handler = threading.Thread(target=hallway_rainbow)
busy_free_thread_handler = threading.Thread(target=busy_free_thread)
network_thread_handler = threading.Thread(target=web_interaction_thread)
update_thread_handler.start()
ambient_thread_handler.start()
rainbow_thread_handler.start()
busy_free_thread_handler.start()

def exit_handler():
    global kill_all
    print("exiting")
    kill_all = True
    update_thread_handler.join()
    ambient_thread_handler.join()
    rainbow_thread_handler.join()
    busy_free_thread_handler.join()

    led.set_all_led(0, 0, 0)
    led.update()
    led2.set_all_led(0, 0, 0)
    led2.update()

atexit.register(exit_handler)