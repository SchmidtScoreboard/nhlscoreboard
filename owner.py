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
LONG_PRESS_TIME = 5
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


def reset_wifi():
    settings = get_settings()
    settings[ACTIVE_SCREEN_KEY] = ActiveScreen.HOTSPOT.value
    settings[SETUP_STATE_KEY] = SetupState.HOTSPOT.value
    write_settings(settings)
    r = requests.post(url=localAddress + "reboot",
                      json={RESTART_KEY: False, REBOOT_MESSAGE_KEY: "Setting up..."})
    print(r.status_code)
    subprocess.call(["rm", settings_path])
    subprocess.call([hotspot_on])
    restart_scoreboard()


def setup_wifi():
    subprocess.call([hotspot_off])
    restart_scoreboard()


def execute_long_press():
    print("Long Press")
    reset_wifi()


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


def button_held():
    global is_pressed
    is_pressed = False  # Cancel the pending button release
    execute_long_press()


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
        if not double_press:
            t = threading.Timer(DOUBLE_PRESS_DEBOUNCE, press_helper)
            t.start()


def int_handler(signum, frame):
    print('Int handler called')
    subprocess.call(["kill", "-9", str(process.pid)])
    exit(0)


def usr1_handler(signum, frame):
    print("SIGUSR1 called")
    restart_scoreboard()


def usr2_handler(signum, frame):
    print("SIGUSR2 called")
    setup_wifi()


if __name__ == "__main__":
    # First, get a new version
    print("Running at pid {}".format(os.getpid()))
    root_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    try:
        repo = git.Repo(root_path)
        repo.git.pull()
    except:
        print("Unable to pull from git, running with out of date software")

    if not config.testing:
        subprocess.call([sys.executable, "-m", "pip",
                         "install", "-r", requirements_path])

    signal.signal(signal.SIGINT, int_handler)
    signal.signal(signal.SIGUSR1, usr1_handler)
    signal.signal(signal.SIGUSR2, usr2_handler)
    get_settings()

    app_path = os.path.join(root_path, "app.py")
    print("Starting app at " + app_path)
    if not config.testing:
        print("Starting in production mode")
        subprocess.call(["touch", settings_path])
        subprocess.call(["touch", wpa_path])
        subprocess.call(["touch", secrets_path])
        subprocess.call(["chmod", "777", root_path])
        subprocess.call(["chmod", "777", settings_path])
        subprocess.call(["chmod", "777", secrets_path])
        subprocess.call(["chmod", "777", wpa_path])
        subprocess.call(["chmod", "777", settings_template_path])
        process = subprocess.Popen(["python3", app_path])
    else:
        print("Starting in testing mode")
        process = subprocess.Popen(["python3", app_path])
    print("App started at pid {}".format(process.pid))
    if not config.testing:
        button = Button(25, pull_up=False, hold_time=5)
        button.when_pressed = button_pressed
        button.when_released = button_released
        button.when_held = button_held
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
