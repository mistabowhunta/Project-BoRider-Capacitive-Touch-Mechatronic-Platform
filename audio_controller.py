#!/usr/bin/env python3
import os
import sys
import random
import subprocess
from multiprocessing import Process

import error_controller as logger

def main(category, wav_file=None):
    logger.one_variable('audio_controller.py', 'main()', "category: ", str(category))
    
    if category == 'background_music':
        # Spawns a single background process that loops music indefinitely
        p_music = Process(name="music_loop", target=background_music_loop)
        p_music.daemon = True # Ensures audio dies if the main robot script crashes
        p_music.start()
        return p_music # Returns the process object so main code can terminate it

    elif category == 'sfx':
        sfx_wavs()

def background_music_loop():
    """Continuously plays background music without recursive process spawning."""
    list_music = ['Green_Gray', 'Runaround', 'the_fun_run']
    
    while True:
        song = random.choice(list_music)
        try:
            wav_file = f'/home/BoPi/audio/{song}.wav'
            # os.system is acceptable here because we WANT this background thread 
            # to wait until the song finishes before looping to the next one.
            os.system(f'sudo /usr/bin/aplay -q {wav_file}')
        except Exception as e:
            logger.one_variable('audio_controller.py', 'background_music_loop()', "Error: ", str(e))
            play_wav('error_beep')
            break

def sfx_wavs():
    list_sfx = ['booDies', 'booLaugh']
    play_wav(random.choice(list_sfx))

def turn_off():
    """Kills any currently playing audio via aplay."""
    os.system('sudo killall aplay')

def play_wav(filename):
    """Plays short sound effects without freezing the main robot loop."""
    try:
        wav_file = f'/home/BoPi/audio/{filename}.wav'
        # subprocess.Popen is non-blocking. It fires the audio command to the OS 
        # and instantly returns control to your script to keep reading sensors.
        subprocess.Popen(['sudo', '/usr/bin/aplay', '-q', wav_file])
        
    except Exception as e:
        logger.one_variable('audio_controller.py', 'play_wav()', "Error: ", str(e))
        wav_file_error = '/home/BoPi/audio/error_beep.wav'
        subprocess.Popen(['sudo', '/usr/bin/aplay', '-q', wav_file_error])

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])