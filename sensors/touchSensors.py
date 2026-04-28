#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import error_controller
import audio_controller

logger = error_controller
audio = audio_controller

# Set GPIO numbering mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pwr = 21
touch = 17
touch2 = 27
touch3 = 22
touch4 = 16
touch5 = 20
GPIO.setup(pwr, GPIO.OUT)
GPIO.output(pwr, GPIO.HIGH)
GPIO.setup(touch,GPIO.IN)
GPIO.setup(touch2,GPIO.IN)
GPIO.setup(touch3,GPIO.IN)
GPIO.setup(touch4,GPIO.IN)
GPIO.setup(touch5,GPIO.IN)

def main():

    try:
        logger.msg('touch.py','main()', "BEFORE LOOP")
        while True:
            if GPIO.input(touch):
                logger.msg('touch.py','main()', "touch")
                return 'Touch'
            elif GPIO.input(touch2):
                logger.msg('touch.py','main()', "touch2")
                return 'Touch2'
            elif GPIO.input(touch3):
                logger.msg('touch.py','main()', "touch3")
                return 'Touch3'
            elif GPIO.input(touch4):
                logger.msg('touch.py','main()', "touch4")
                return 'Touch4'
            elif GPIO.input(touch5):
                logger.msg('touch.py','main()', "touch5")
                return 'Touch5'
    except KeyboardInterrupt as e:
        logger.one_variable('touch.py','main() keyboard interrupt', "Error: ", str(e))
        GPIO.output(pwr, GPIO.LOW)
    except Exception as e:
        logger.one_variable('touch.py','main()', "Error: ", str(e))
        audio.play_wav('error_beep')
        return 'error'

if __name__ == '__main__':
    main()
        