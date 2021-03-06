import config
import logging
import socket
from files import *
import os
import sys
import json
import subprocess
import time
import atexit
import threading
import version
import wlan
from common import *
from setup_screens import *
from error import *
from info import *
from mlb import *
from nhl import *
from clock import *
from PIL import Image, ImageDraw, ImageFont
from string import Template
from flask import jsonify
from flask import request
from flask import Flask


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[
                        logging.FileHandler(log_path, "a"),
                        logging.StreamHandler(sys.stdout)
                    ])
log = logging.getLogger(__name__)
try:
    from rgbmatrix import graphics, RGBMatrixOptions, RGBMatrix
    log.info("")
    log.info("--------------------------")
    log.info("Starting in production mode")
    log.info("--------------------------")
    log.info("")
except:
    config.testing = True
    log.info("Running in test mode")
    from fake_matrix import *
    hotspot_on = os.path.join(root_path, "hotspot_on_test.sh")
    hotspot_off = os.path.join(root_path, "hotspot_off_test.sh")

app = Flask(__name__)


common_data = {}


data_lock = threading.RLock()
render_thread = threading.Thread()


def create_app():
    app = Flask(__name__)

    def draw_image():
        # First, manage the setup state
        with data_lock:
            if common_data[SCREEN_ON_KEY]:
                common_data[SCREENS_KEY][common_data[ACTIVE_SCREEN_KEY]].refresh()
                image = common_data[SCREENS_KEY][common_data[ACTIVE_SCREEN_KEY]].get_image(
                )
                # common_data[MATRIX_KEY].Clear()
                common_data[MATRIX_KEY].SetImage(
                    image.convert("RGB"), unsafe=False)
            else:
                common_data[MATRIX_KEY].Clear()

    def draw():
        global common_data
        global render_thread
        draw_image()
        try:
            render_thread.cancel()
        except Exception as e:
            pass  # Do nothing, there is no thread to cancel
        render_thread = threading.Timer(
            common_data[SCREENS_KEY][common_data[ACTIVE_SCREEN_KEY]].get_sleep_time(), draw, ())

        render_thread.start()

    @app.route('/', methods=['GET'])
    def root():
        settings = get_settings()
        return jsonify(settings)

    @app.route('/configure', methods=['POST'])
    def configure():
        global common_data
        global data_lock
        with data_lock:
            interrupt()
            content = request.get_json()
            old_settings = get_settings()
            merged = {**old_settings, **content}
            log.info("Got settings: {}\n, Old Settings:  {}\n, Merged: {}\n".format(
                content, old_settings, merged))
            write_settings(merged)
            initScreens()
            interrupt()
            draw()

        resp = jsonify(get_settings())
        return resp

    @app.route('/setPower', methods=['POST'])
    def setPower():
        global common_data
        global data_lock
        with data_lock:
            log.info(f"Logging wifi status {wlan.get_name_strength_map()}")
            settings = get_settings()
            if settings[SETUP_STATE_KEY] == SetupState.READY.value:
                interrupt()
                content = request.get_json()
                common_data[SCREEN_ON_KEY] = content[SCREEN_ON_KEY]
                current_screen = common_data[ACTIVE_SCREEN_KEY]
                if common_data[SCREEN_ON_KEY] and common_data[SCREENS_KEY][current_screen].is_stale():
                    log.info("Drawing refresh screen!")
                    common_data[ACTIVE_SCREEN_KEY] = ActiveScreen.REFRESH
                    draw()
                common_data[ACTIVE_SCREEN_KEY] = current_screen

                common_data[SCREENS_KEY][current_screen].is_initialized = False

                draw()
                # Update the settings file
                settings[SCREEN_ON_KEY] = common_data[SCREEN_ON_KEY]
                write_settings(settings)
            else:
                log.error("Cannot power off, scoreboard is not ready")
        resp = jsonify(settings)
        return resp

    @app.route('/setSport', methods=['POST'])
    def setSport():
        global common_data
        global data_lock
        with data_lock:
            log.info(f"Logging wifi status {wlan.get_name_strength_map()}")
            settings = get_settings()
            if settings[SETUP_STATE_KEY] == SetupState.READY.value or settings[SETUP_STATE_KEY] == SetupState.SYNC.value:
                settings[SETUP_STATE_KEY] = SetupState.READY.value
                interrupt()
                content = request.get_json()
                target_screen = ActiveScreen(content["sport"])
                if common_data[SCREENS_KEY][target_screen].is_stale():
                    log.info("Drawing refresh screen!")
                    common_data[ACTIVE_SCREEN_KEY] = ActiveScreen.REFRESH
                    common_data[SCREEN_ON_KEY] = True
                    draw()
                common_data[ACTIVE_SCREEN_KEY] = target_screen

                common_data[SCREENS_KEY][target_screen].is_initialized = False

                draw()
                # Update the file
                settings[ACTIVE_SCREEN_KEY] = common_data[ACTIVE_SCREEN_KEY].value
                settings[SCREEN_ON_KEY] = common_data[SCREEN_ON_KEY]
                write_settings(settings)
            else:
                log.error("Cannot set sport, scoreboard is not ready")
        resp = jsonify(settings)
        return resp

    # Used to set the wifi configuration
    @app.route('/wifi', methods=['POST'])
    def setupWifi():
        global common_data
        global data_lock
        with data_lock:
            content = request.get_json()
            with open(wpa_template, "r") as template:
                wpa_content = Template(template.read())
                substituted = wpa_content.substitute(
                    ssid=content['ssid'], psk=content['psk'])
                log.info(f"Setting up wifi with subsituted conf {substituted}")
                common_data[SCREENS_KEY][ActiveScreen.WIFI_DETAILS].begin_countdown(
                    substituted)
                interrupt()
                common_data[ACTIVE_SCREEN_KEY] = ActiveScreen.REBOOT
                draw()
            return jsonify(settings)

    # Used to fetch logs
    @app.route('/logs', methods=['GET'])
    def fetchLogs():
        global common_data
        global data_lock
        with data_lock:
            ret = []
            with open(log_path, "r") as logs:
                for line in logs:
                    ret.append(line)
            print(ret)
            return jsonify(ret)

    @app.route('/showSync', methods=['POST'])
    def showSync():
        global common_data
        global data_lock
        with data_lock:
            settings = get_settings()
            log.info("Showing sync screen")
            if settings[SETUP_STATE_KEY] == SetupState.READY.value:
                interrupt()
                settings[SETUP_STATE_KEY] = SetupState.SYNC.value
                settings[ACTIVE_SCREEN_KEY] = ActiveScreen.SYNC.value
                common_data[ACTIVE_SCREEN_KEY] = ActiveScreen.SYNC
                common_data[SCREEN_ON_KEY] = True
                settings[SCREEN_ON_KEY] = True
                draw()
                write_settings(settings)
                return jsonify(settings)
            elif settings[SETUP_STATE_KEY] == SetupState.SYNC.value:
                settings[SETUP_STATE_KEY] = SetupState.READY.value
                interrupt()
                common_data[ACTIVE_SCREEN_KEY] = ActiveScreen.REFRESH
                common_data[SCREEN_ON_KEY] = True
                settings[SCREEN_ON_KEY] = True
                draw()
                settings[ACTIVE_SCREEN_KEY] = ActiveScreen.NHL.value
                common_data[ACTIVE_SCREEN_KEY] = ActiveScreen.NHL
                write_settings(settings)
                return jsonify(settings)
            else:
                return jsonify(success=False)

    @app.route('/reboot', methods=['POST'])
    def reboot():
        global data_lock
        global common_data
        with data_lock:
            log.info("About to reboot")
            interrupt()
            settings = get_settings()
            common_data[ACTIVE_SCREEN_KEY] = ActiveScreen.REBOOT
            draw()
            content = request.get_json()
            if content is None or content.get(RESTART_KEY, True):
                send_restart_signal()
            if content is not None and content.get(REBOOT_MESSAGE_KEY) is not None:
                common_data[SCREENS_KEY][ActiveScreen.REBOOT].set_message(
                    content.get(REBOOT_MESSAGE_KEY))
            else:
                common_data[SCREENS_KEY][ActiveScreen.REBOOT].set_message(
                    "Rebooting...")
            return jsonify(settings)

    # Used on Sync screen. When the app parses the IP code, it will send this API request
    @app.route('/sync', methods=['POST'])
    def sync():
        global common_data
        global data_lock
        with data_lock:
            settings = get_settings()
            log.info("Received sync command")
            if settings[SETUP_STATE_KEY] == SetupState.SYNC.value:
                settings[SETUP_STATE_KEY] = SetupState.READY.value
                interrupt()
                common_data[ACTIVE_SCREEN_KEY] = ActiveScreen.REFRESH
                common_data[SCREEN_ON_KEY] = True
                draw()
                settings[ACTIVE_SCREEN_KEY] = ActiveScreen.NHL.value
                common_data[ACTIVE_SCREEN_KEY] = ActiveScreen.NHL
                write_settings(settings)
                return jsonify(settings)
            else:
                return jsonify(success=False)
    # Used on Hotspot state. When app connects to scoreboard, move to Wifi connect state
    @app.route('/connect', methods=['POST'])
    def connect():
        global common_data
        global data_lock
        global log
        with data_lock:
            settings = get_settings()
            log.info("Got connection command, setupstate = {}".format(
                settings[SETUP_STATE_KEY]))
            if settings[SETUP_STATE_KEY] == SetupState.HOTSPOT.value:
                settings[SETUP_STATE_KEY] = SetupState.WIFI_CONNECT.value
                settings[ACTIVE_SCREEN_KEY] = ActiveScreen.WIFI_DETAILS.value
                interrupt()
                common_data[ACTIVE_SCREEN_KEY] = ActiveScreen.WIFI_DETAILS
                common_data[SCREEN_ON_KEY] = True
                draw()
                write_settings(settings)
                return jsonify(settings)
            elif settings[SETUP_STATE_KEY] == SetupState.WIFI_CONNECT.value:
                # Allow wifi connect success on this screen, too
                return jsonify(settings)
            else:
                response = jsonify(success=False)
                response.status_code = 500
                return response

    # Starting the service ALWAYS turns the screen on
    common_data[SCREEN_ON_KEY] = True
    settings = get_settings()
    settings[SCREEN_ON_KEY] = True
    if settings[SETUP_STATE_KEY] == SetupState.FACTORY.value:
        settings[SETUP_STATE_KEY] = SetupState.HOTSPOT.value
    elif settings[SETUP_STATE_KEY] == SetupState.SYNC.value:
        if get_ip_address() == "":
            # Got empty string, which means it failed to connect. Display something funky and make the user reset
            log.error("Failed to connect to wifi")
            common_data[SCREENS_KEY][ActiveScreen.ERROR] = ErrorScreen(
                "Could not connect to WiFi", ["Reset your", "Scoreboard"])
            settings[ACTIVE_SCREEN_KEY] = ActiveScreen.ERROR.value
        else:
            settings[ACTIVE_SCREEN_KEY] = ActiveScreen.SYNC.value
    settings[MAC_ADDRESS_KEY] = get_mac_address()
    write_settings(settings)

    draw()  # Draw the refresh screen
    initScreens()
    log.info("Done setup")
    atexit.register(interrupt)
    return app


def interrupt():
    global render_thread
    render_thread.cancel()


def initScreens():
    screen_settings = get_settings()["screens"]
    try:
        mlb_settings = next(
            screen for screen in screen_settings if screen["id"] == ActiveScreen.MLB.value)
        nhl_settings = next(
            screen for screen in screen_settings if screen["id"] == ActiveScreen.NHL.value)
    except:
        log.info("Something went wrong while parsing screen settings")
    log.info(nhl_settings)
    log.info(mlb_settings)
    api_key = get_api_key()
    mlb = MLB(mlb_settings, api_key, get_settings()["timezone"])
    nhl = NHL(nhl_settings, api_key, get_settings()["timezone"])
    clock = ClockScreen(get_settings()["timezone"])
    with data_lock:
        common_data[SCREENS_KEY][ActiveScreen.NHL] = nhl
        common_data[SCREENS_KEY][ActiveScreen.MLB] = mlb
        common_data[SCREENS_KEY][ActiveScreen.CLOCK] = clock
        if api_key is None:
            common_data[SCREENS_KEY][ActiveScreen.ERROR] = ErrorScreen(
                "No API Key found", ["Please", "contact", "support"])
            common_data[ACTIVE_SCREEN_KEY] = ActiveScreen.ERROR
        else:
            common_data[ACTIVE_SCREEN_KEY] = ActiveScreen(
                get_settings()[ACTIVE_SCREEN_KEY])
    log.info("Done initScreens")
    log.info(f"Logging wifi status {wlan.get_name_strength_map()}")


def run_webserver():
    from waitress import serve
    serve(create_app(), host="0.0.0.0", port=5005)

    # create_app().run(host='0.0.0.0', port=5005)


if __name__ == '__main__':
    # Set up the matrix options
    log.info("In app main")
    options = RGBMatrixOptions()
    options.brightness = 100
    options.rows = 32
    options.cols = 64
    options.hardware_mapping = "adafruit-hat-pwm"
    options.gpio_slowdown = 4

    with data_lock:
        common_data[ACTIVE_SCREEN_KEY] = ActiveScreen.REFRESH
        common_data[SCREENS_KEY] = {
            ActiveScreen.REFRESH: InfoScreen("Loading...")}
        common_data[SCREENS_KEY][ActiveScreen.REBOOT] = InfoScreen(
            "Rebooting...")
        common_data[MATRIX_KEY] = RGBMatrix(options=options)
        common_data[SCREENS_KEY][ActiveScreen.SYNC] = SyncScreen()
        common_data[SCREENS_KEY][ActiveScreen.HOTSPOT] = WifiHotspot()
        common_data[SCREENS_KEY][ActiveScreen.WIFI_DETAILS] = ConnectionScreen()
        common_data[SCREENS_KEY][ActiveScreen.ERROR] = ErrorScreen(
            "Dummy Error Message", ["Error"])

    if not config.testing:
        run_webserver()
    else:  # This is a terrible hack but it helps keep things running in test mode
        web_thread = threading.Thread(target=run_webserver)
        web_thread.start()
        common_data[MATRIX_KEY].master.mainloop()
