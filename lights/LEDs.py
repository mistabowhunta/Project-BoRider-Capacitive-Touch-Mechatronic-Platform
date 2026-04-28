import time
import RPi.GPIO as GPIO
import random
import neopixel
import board
import error_controller
from multiprocessing import Process

num_pixels = 60
num_pixels_circling = 2
pixels1 = neopixel.NeoPixel(board.D12, num_pixels, brightness=0.6)
x=0
logger = error_controller
p_main_led = Process()

def main():
    p_main_led = Process(target=main_lights)
    p_main_led.daemon = False
    p_main_led.start()
    return

def main_lights():
    global x
    global pixels1
    logger.msg('LEDs.py','main()', "INSIDE MAIN LED")
    pixels1 = neopixel.NeoPixel(board.D12, num_pixels, brightness=0.6)
    pixels1.fill((255, 255, 255))
    while True:
        while x < num_pixels - num_pixels_circling:
            for i in range(x, x + num_pixels_circling - 1, 1):
                pixels1[i] = (255, 0, 0)
            if x > num_pixels_circling:
                pixels1[x - num_pixels_circling] = (255, 255, 255)
            x = x+1

            time.sleep(0.05)

        while x >= 0:
            for i in range(x, x - num_pixels_circling - 1, -1):
                pixels1[i] = (255, 0, 0)
            if x > num_pixels_circling:
                pixels1[x - num_pixels_circling] = (255, 255, 255)
            x = x-1
        time.sleep(0.2)

def turn_all_off():
    global pixels1
    global p_main_led
    OFF = (0,0,0)
    pixels1.fill(OFF)
    p_main_led.kill()

def turn_all_on_low_white():
    global pixels1
    logger.msg('LEDs.py','turn_all_on_low_white()', "INSIDE turn_all_on_low_white")
    WHITE = (255,255,255)
    pixels1 = neopixel.NeoPixel(board.D12, num_pixels, brightness=0.2)
    pixels1.fill(WHITE)

def turn_all_on_high_white():
    global pixels1
    WHITE = (255,255,255)
    pixels1 = neopixel.NeoPixel(board.D12, num_pixels, brightness=0.6)
    pixels1.fill(WHITE)

if __name__ == '__main__':
    main()