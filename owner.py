import time
import logging
import requests
import config
import git
import subprocess
from common import *
from setup_screens import *
from files import *
import signal
import threading
import sys
try:
    from gpiozero import Button
    config.testing = False
except:
    config.testing = True
    hotspot_on = os.path.join(root_path, "hotspot_on_test.sh")
    hotspot_off = os.path.join(root_path, "hotspot_off_test.sh")
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


def restart_scoreboard():
    if config.testing:
        log.info("About to reboot, test mode")
        os.kill(os.getpid(), signal.SIGINT)
    else:
        log.info("About to reboot, production mode")
        os.system('sudo shutdown -r now')


def resetWifi():
    settings = get_settings()
    settings[ACTIVE_SCREEN_KEY] = ActiveScreen.HOTSPOT.value
    settings[SETUP_STATE_KEY] = SetupState.HOTSPOT.value
    write_settings(settings)
    subprocess.call([hotspot_on])
    restart_scoreboard()


def setupWifi():
    subprocess.call([hotspot_off])
    restart_scoreboard()


def execute_long_press():
    print("Long Press")
    resetWifi()


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
        release_time = now
        if now - press_time > LONG_PRESS_TIME:
            execute_long_press()
        elif not double_press:
            t = threading.Timer(DOUBLE_PRESS_DEBOUNCE, press_helper)
            t.start()


def handler(signum, frame):
    print('Signal handler called with signal', signum)
    if signum == signal.SIGUSR1:
        pass  # restart
    elif signum == signal.SIGUSR2:
        pass  # set wifi
    else:
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
        button = Button(25, pull_up=False)
        button.when_pressed = button_pressed
        button.when_released = button_released
        signal.pause()
    else:
        while(True):
            line = input("L for long, S for short, D for double").rstrip()
            if line == "L":
                execute_long_press()
            elif line == "S":
                execute_short_press()
            elif line == "D":
                execute_double_press()
