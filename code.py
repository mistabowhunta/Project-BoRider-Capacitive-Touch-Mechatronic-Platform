#!/usr/bin/env python3
import sys
import time
import logging
from multiprocessing import Process

import error_controller as logger
import audio_controller as audio
sys.path.append("sensors")
sys.path.append("lights")
sys.path.append("motors")
from sensors import touch
from lights import LEDs as leds
from motors import dc_motor

multiprocessing.log_to_stderr(logging.DEBUG)

def reset_system(p_low_led):
    """Handles system reset without recursive calls."""
    leds.turn_all_off()
    audio.turn_off()
    if p_low_led and p_low_led.is_alive():
        p_low_led.terminate()
    dc_motor.override_stop()

def main():
    logger.msg('code.py', 'main()', "PROGRAM START")
    
    # Fix: Pass function reference, don't execute it
    p_low_led = Process(target=leds.turn_all_on_low_white)
    p_low_led.start()
    
    is_music_playing = False

    while True:
        try:
            sensor_touched = touch.main()
            logger.msg('code.py', 'main()', "INSIDE LOOP")
            
            if sensor_touched == 'error':
                reset_system(p_low_led)
                is_music_playing = False
                continue  # Jumps back to the top of the while loop safely

            if not is_music_playing:
                is_music_playing = True
                logger.msg('code.py', 'main()', "STARTING AV SUBSYSTEMS")
                
                # Ideally, leds.main() should be non-blocking
                Process(target=leds.main).start() 
                audio.main(category='background_music')
                time.sleep(1)

            elif is_music_playing:
                logger.msg('code.py', 'main()', "EXECUTING MOVEMENT")
                audio.main(category='sfx')
                
                # Ensure this motor command doesn't block sensor reads for 2 full seconds
                move_success = dc_motor.main(move_duration_seconds=2) 
                
                if not move_success:
                    reset_system(p_low_led)
                    is_music_playing = False
                    continue

        except Exception as e:
            logger.one_variable('code.py', 'main()', "Error: ", str(e))
            audio.play_wav('error_beep')
            reset_system(p_low_led)
            is_music_playing = False
            time.sleep(1) # Brief pause before the loop restarts
            continue

if __name__ == '__main__':
    main()