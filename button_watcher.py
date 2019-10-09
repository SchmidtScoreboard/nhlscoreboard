import time
import logging
import requests
import config
from common import *
try:
    import RPi.GPIO as GPIO
except:
    from fake_gpio import *
    config.testing = True
log = logging.getLogger(__name__)

is_pressed = False
press_time = 0
release_time = 0
double_press = False

localAddress = "http://127.0.0.1:5005/"

#TODO update these times
LONG_PRESS_TIME = 10 
DOUBLE_PRESS_WINDOW = 0.5
DOUBLE_PRESS_DEBOUNCE = 0.6

def long_press():
    print("Long Press")
    # TODO do request to reset everything
    r = requests.request(requests.post, localAddress + "resetWifi" )
    print(r.status_code)

def short_press():
    print("Short press")
    settings = get_settings()
    r = requests.request(requests.post, localAddress + "setPower", json={SCREEN_ON_KEY: not settings[SCREEN_ON_KEY]})
    print(r.status_code)

def double_press():
    print("Double press")
    r = requests.request(requests.post, localAddress + "sync" )
    print(r.status_code)


def button_pressed():
    print("Pressed")
    if not is_pressed:
        is_pressed = True
        now = time.time()
        if now - release_time < DOUBLE_PRESS_WINDOW:
            double_press = True
        else:
            double_press = False
        press_time = now

def press_helper():
    if double_press:
        double_press()
    else:
        short_press()
    double_press = False

def button_released():
    print("Released")
    if is_pressed: 
        is_pressed = False
        now = time.time()
        if now - press_time > LONG_PRESS_TIME:
            long_press()
        elif not double_press:
            threading.Timer(DOUBLE_PRESS_DEBOUNCE, short_press_helper)


if __name__  == "__main__":
    if not config.testing:
        log.setLevel(logging.DEBUG)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.add_event_detect(7, GPIO.RISING, callback=button_pressed, bouncetime=300)
        GPIO.add_event_detect(7, GPIO.FALLING, callback=button_released, bouncetime=300)
        while(True):
            time.sleep(500) # Infinitely loop
    else:
        long_press()