import time
import logging
import requests
import config
import git
import subprocess
from common import *
from files import *
import signal
import threading
import sys
try:
    from gpiozero import Button
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


def execute_long_press():
    print("Long Press")
    r = requests.post(url=localAddress + "resetWifi")
    print(r.status_code)


def execute_short_press():
    print("Short press")
    settings = get_settings()
    r = requests.post(url=localAddress + "setPower",
                      json={SCREEN_ON_KEY: not settings[SCREEN_ON_KEY]})
    print(r.status_code)


def execute_double_press():
    print("Double press")
    r = requests.post(url=localAddress + "showSync")
    print(r.status_code)


def button_pressed():
    global is_pressed
    global release_time
    global double_press
    global press_time
    if not is_pressed:
        is_pressed = True
        now = time.time()
        if now - release_time < DOUBLE_PRESS_WINDOW:
            double_press = True
        else:
            double_press = False
        press_time = now


def press_helper():
    global is_pressed
    global release_time
    global double_press
    global press_time
    if double_press:
        execute_double_press()
    else:
        execute_short_press()
    double_press = False


def button_released():
    global is_pressed
    global release_time
    global double_press
    global press_time
    if is_pressed:
        is_pressed = False
        now = time.time()
        if now - press_time > LONG_PRESS_TIME:
            execute_long_press()
        elif not double_press:
            t = threading.Timer(DOUBLE_PRESS_DEBOUNCE, press_helper)
            t.start()


def handler(signum, frame):
    print('Signal handler called with signal', signum)
    subprocess.call(["kill", "-9", str(process.pid)])
    exit(0)


if __name__ == "__main__":
    # First, get a new version
    root_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    try:
        repo = git.Repo(root_path)
        repo.git.pull()
    except:
        print("Unable to pull from git, running with out of date software")

    if not config.testing:
        subprocess.call([sys.executable, "-m", "pip",
                         "install", "-r", requirements_path])

    signal.signal(signal.SIGINT, handler)
    get_settings()

    app_path = os.path.join(root_path, "app.py")
    print("Starting app at " + app_path)
    if not config.testing:
        print("Starting in production mode")
        subprocess.call(["chmod", "777", settings_path])
        process = subprocess.Popen(["python3", app_path])
    else:
        print("Starting in testing mode")
        process = subprocess.Popen(["python3", app_path])
    print("App started at pid {}".format(process.pid))
    if not config.testing:
        button = Button(25)
        button.when_pressed = button_pressed
        button.when_released = button_released
        signal.pause()
    else:
        while(True):
            line = input("L for long, S for short, D for double").rstrip()
            if line == "L":
                long_press()
            elif line == "S":
                short_press()
            elif line == "D":
                double_press()
