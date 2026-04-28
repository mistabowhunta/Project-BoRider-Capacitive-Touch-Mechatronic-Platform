#!/usr/bin/env python3
import time
import board
import pwmio
import error_controller
import audio_controller
import RPi.GPIO as GPIO

# Set GPIO numbering mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

logger = error_controller
audio = audio_controller
motor1_LEN = 23#board.D23
motor1_REN = 24#board.D24
motor1_pin_a = board.D13  # pick any pwm pins on their own channels
motor1_pin_b = board.D19
motor1a = pwmio.PWMOut(motor1_pin_a, frequency=50)
motor1b = pwmio.PWMOut(motor1_pin_b, frequency=50)
GPIO.setup(motor1_LEN, GPIO.OUT)
GPIO.output(motor1_LEN, GPIO.HIGH)
GPIO.setup(motor1_REN, GPIO.OUT)
GPIO.output(motor1_REN, GPIO.HIGH)

def main(move_duration_seconds):
    global motor1a
    global motor1b
    motor1a.duty_cycle= 0
    motor1b.duty_cycle= 0
    logger.msg('dc_motor.py','main()', "MOVING FORWARD")

    try:
        motor1a.duty_cycle= 0
        motor1b.duty_cycle= 65535

        time.sleep(move_duration_seconds)

        motor1a.duty_cycle= 0
        motor1b.duty_cycle= 0
    except Exception as e:
        logger.one_variable('dc_motor.py','main()', "Error: ", str(e))
        audio.play_wav('error_beep') # Unknown error
        return False
    return True

def override_stop():
    global motor1a
    global motor1b
    motor1a.duty_cycle= 0
    motor1b.duty_cycle= 0

if __name__ == '__main__':
    main()