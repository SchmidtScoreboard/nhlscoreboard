# from pynput import Key, Listener
import time
import logging
from pynput.keyboard import Key, Listener
log = logging.getLogger(__name__)

class GPIO:

    BOARD = "board"
    IN = "in"
    OUT = "out"
    PUD_DOWN = "pud_down"
    RISING = "rising"
    FALLING = "falling"

    @staticmethod
    def setmode(arg):
        print("Setting mode on GPIO")

    @staticmethod
    def setup(pin_num, in_out, pull_up_down):
        print("Setting up GPIO")

    @staticmethod
    def add_event_detect(pin_num, rising_falling, callback, bouncetime):
        print("Adding event detector ", pin_num, rising_falling)
        if rising_falling == GPIO.RISING:
            GPIO.rising_callback = callback
        elif rising_falling == GPIO.FALLING:
            GPIO.falling_callback = callback

    @staticmethod
    def test_rising(key):
        print("{0} pressed".format(key))

    @staticmethod
    def test_falling(key):
        print("{0} released".format(key))
        if key == Key.esc:
            return False

    @staticmethod
    def detect_keys():
        print("Detecting keys")
        while True:
            with Listener(on_press=GPIO.test_rising, on_release=GPIO.test_falling) as listener:
                listener.join()