import time
import logging
import requests
import config
import git
import subprocess
from common import *
from files import *
import signal
import sys
try:
    import RPi.GPIO as GPIO
    config.testing = False
except:
    config.testing = True
log = logging.getLogger(__name__)

is_pressed = False
press_time = 0
release_time = 0
double_press = False

localAddress = "http://127.0.0.1:5005/"

# TODO update these times
LONG_PRESS_TIME = 10
DOUBLE_PRESS_WINDOW = 0.5
DOUBLE_PRESS_DEBOUNCE = 0.6

process = None


def long_press():
    print("Long Press")
    r = requests.post(url=localAddress + "resetWifi")
    print(r.status_code)


def short_press():
    print("Short press")
    settings = get_settings()
    r = requests.post(url=localAddress + "setPower",
                      json={SCREEN_ON_KEY: not settings[SCREEN_ON_KEY]})
    print(r.status_code)


def double_press():
    print("Double press")
    r = requests.post(url=localAddress + "showSync")
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


def handler(signum, frame):
    print('Signal handler called with signal', signum)
    subprocess.call(["sudo", "kill", "-9", str(process.pid)])
    exit(0)


if __name__ == "__main__":
    # First, get a new version
    root_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    repo = git.Repo(root_path)
    repo.git.pull()

    signal.signal(signal.SIGINT, handler)
    get_settings()

    app_path = os.path.join(root_path, "app.py")
    print("Starting app at " + app_path)
    if not config.testing:
        print("Starting in production mode")
        subprocess.call(["sudo", "chmod", "777", settings_path])
        process = subprocess.Popen(["sudo", "python3", app_path])
    else:
        print("Starting in testing mode")
        process = subprocess.Popen(["python3", app_path])
    print("App started at pid {}".format(process.pid))
    if not config.testing:
        pass
        # GPIO.setmode(GPIO.BOARD)
        #GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # GPIO.add_event_detect(
        #    7, GPIO.RISING, callback=button_pressed, bouncetime=300)
        # GPIO.add_event_detect(
        #    7, GPIO.FALLING, callback=button_released, bouncetime=300)
    while(True):
        if config.testing:
            line = input("L for long, S for short, D for double").rstrip()
            if line == "L":
                long_press()
            elif line == "S":
                short_press()
            elif line == "D":
                double_press()
        else:
            time.sleep(1)
