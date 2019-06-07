from flask import Flask
from flask import request
from flask import jsonify
from string import Template
from PIL import Image, ImageDraw, ImageFont
testing = False
from nhl import *
from mlb import *
from info import *
from setup_screens import *
from common import *
import threading
import atexit
import time
import subprocess
import json
import sys
import os
from files import *
import socket
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
try:
    from rgbmatrix import graphics, RGBMatrixOptions, RGBMatrix
    log.info("Running in production mode")
except:
    testing = True
    log.info("Running in test mode")
    hotspot_on = os.path.join(root_path, "hotspot_on_test.sh")
    hotspot_off = os.path.join(root_path, "hotspot_off_test.sh")
    from fake_matrix import *

app = Flask(__name__)


common_data = {}


active_screen = "ACTIVE_SCREEN"
screens = "SCREENS"
matrix = "MATRIX"
screen_on = "SCREEN_ON"
nhl = "NHL"
mlb = "MLB"
data_lock = threading.RLock()
render_thread = threading.Thread()

def create_app():
    app = Flask(__name__)
    
    def get_ip_address():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        except:
            return ""

    def interrupt():
        global render_thread
        render_thread.cancel()

    def draw_image():
        # First, manage the setup state
        with data_lock:
            if common_data[screen_on]:
                common_data[screens][common_data[active_screen]].refresh()
                image = common_data[screens][common_data[active_screen]].get_image()
                common_data[matrix].Clear()
                common_data[matrix].SetImage(image.convert("RGB")) 
            else:
                common_data[matrix].Clear()
        

    def draw():
        global common_data
        global render_thread
        draw_image()
        render_thread = threading.Timer(common_data[screens][common_data[active_screen]].get_sleep_time(), draw, ())
            
        render_thread.start()

    @app.route('/', methods = ['GET'])
    def root():
        settings = get_settings()
        return jsonify(settings)

    @app.route('/configure', methods= ['POST'])
    def configure():
        global common_data
        global data_lock
        with data_lock:
            log.info("configuring")
            content = request.get_json()
            with open(settings_path, "w+") as out:
                json.dump(content, out)
            # TODO restart the entire thing?
        resp = jsonify(success=True)
        return resp

    @app.route('/setPower', methods=['POST'])
    def setPower():
        global common_data
        global data_lock
        with data_lock:
            settings = get_settings()
            if settings["setup_state"] == SetupState.READY.value:
                interrupt()
                content = request.get_json()
                common_data[screen_on] = content["screen_on"]
                draw()
                settings["screen_on"] = common_data[screen_on]
                write_settings(settings)
        resp = jsonify(settings)
        return resp
    

    @app.route('/setSport', methods=['POST'])
    def setSport():
        global common_data
        global data_lock
        with data_lock:
            settings = get_settings()
            if settings["setup_state"] == SetupState.READY.value:
                interrupt()
                common_data[active_screen] = ActiveScreen.REFRESH
                common_data[screen_on] = True
                draw()
                content = request.get_json()
                new_screen = ActiveScreen(content["sport"])
                common_data[active_screen] = ActiveScreen(content["sport"])
                #Update the file    
                settings["active_screen"] = common_data[active_screen].value
                settings["screen_on"] = common_data[screen_on]
                write_settings(settings)

        resp = jsonify(settings)
        return resp

    # Used to set the wifi configuration
    @app.route('/wifi', methods=['POST'])
    def setup_wifi():
        global common_data
        global data_lock
        with data_lock:
            content = request.get_json()
            with open(wpa_template, "r") as template:
                wpa_content = Template(template.read())
                substituted = wpa_content.substitute(ssid=content['ssid'], psk=content['psk'])
                log.info(hotspot_off)
                common_data[screens][ActiveScreen.WIFI_DETAILS].begin_countdown(substituted, hotspot_off)
            return jsonify(settings)

    # This should also happen when the button is pressed and held for ten seconds
    @app.route('/reset_wifi', methods=['POST'])
    def reset_wifi():
        global common_data
        global data_lock
        with data_lock:
            settings = get_settings()
            settings["active_screen"] = ActiveScreen.HOTSPOT.value
            settings["setup_state"] = SetupState.HOTSPOT.value
            write_settings(settings)
            subprocess.Popen([hotspot_on])
            return jsonify(settings)
    
    # Used on ScanQR screen. When the app scans the QR code, it will send this API request
    @app.route('/sync', methods=['POST'])
    def sync():
        global common_data
        global data_lock
        with data_lock:
            settings = get_settings()
            if settings["setup_state"] == SetupState.SYNC.value:
                settings["setup_state"] = SetupState.READY.value
                settings["active_screen"] = ActiveScreen.NHL.value
                common_data[active_screen] = ActiveScreen.NHL
                write_settings(settings)
                return jsonify(settings)
            else:
                return jsonify(success=False) # TODO find a better way to return failure
    # Used on Hotspot state. When app connects to scoreboard, move to Wifi connect state
    @app.route('/connect', methods=['POST'])
    def connect():
        global common_data
        global data_lock
        global log
        with data_lock:
            settings = get_settings()
            log.info(settings)
            log.info("Got connection command, setupstate = {}".format(settings["setup_state"]))
            if settings["setup_state"] == SetupState.HOTSPOT.value:
                settings["setup_state"] = SetupState.WIFI_CONNECT.value
                settings["active_screen"] = ActiveScreen.WIFI_DETAILS.value
                interrupt()
                common_data[active_screen] = ActiveScreen.WIFI_DETAILS
                common_data[screen_on] = True
                draw()
                write_settings(settings)
                return jsonify(settings)
            else:
                return jsonify(success=False) # TODO find a better way to return failure

    common_data[screen_on] = True # Starting the service ALWAYS turns the screen on
    settings = get_settings()
    settings["screen_on"] = True
    if settings["setup_state"] == SetupState.FACTORY.value:
        settings["setup_state"] = SetupState.HOTSPOT.value
    write_settings(settings)

    draw() # Draw the refresh screen
    log.info("Refreshing Sports")
    mlb = MLB()
    log.info("Got MLB")
    nhl = NHL()
    log.info("Got NHL")
    with data_lock:
        common_data[screens][ActiveScreen.NHL] = nhl
        common_data[screens][ActiveScreen.MLB] = mlb
        common_data[active_screen] = ActiveScreen(get_settings()["active_screen"])
        #common_data[active_screen] = ActiveScreen.HOTSPOT
        #common_data[active_screen] = ActiveScreen.QR
        #common_data[active_screen] = ActiveScreen.WIFI_DETAILS
    log.info("Done setup")
    atexit.register(interrupt)
    return app

def run_webserver():
    create_app().run(host='0.0.0.0', port=5005)

if __name__ == '__main__':
    # Set up the matrix options
    options = RGBMatrixOptions()
    options.brightness = 100
    options.rows = 32
    options.cols = 64
    options.hardware_mapping = "adafruit-hat" #TODO use the hack to remove flicker

    # Add the refreshing screen
    with data_lock:
        common_data[active_screen] = ActiveScreen.REFRESH 
        common_data[screens] = {ActiveScreen.REFRESH: InfoScreen("Refreshing...")}
        common_data[matrix] = RGBMatrix(options=options)
        common_data[screens][ActiveScreen.QR] = QRScreen()
        common_data[screens][ActiveScreen.HOTSPOT] = WifiHotspot()
        common_data[screens][ActiveScreen.WIFI_DETAILS] = ConnectionScreen()

    if not testing:
        run_webserver()
    else: #This is a terrible hack but it helps keep things running in test mode
        web_thread = threading.Thread(target=run_webserver)
        web_thread.start()
        common_data[matrix].master.mainloop()

