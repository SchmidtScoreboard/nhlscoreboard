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
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
try:
    from rgbmatrix import graphics, RGBMatrixOptions, RGBMatrix
    log.info("Running in production mode")
except:
    testing = True
    log.info("Running in test mode")
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

    def interrupt():
        global render_thread
        render_thread.cancel()

    def draw_image():
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
        with open(settings_path) as out:
            data = json.load(out)
            return jsonify(data)

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
            interrupt()
            content = request.get_json()
            common_data[screen_on] = content["screen_on"]
            draw()
            with open(settings_path) as f:
                settings = json.load(f)
                settings["screen_on"] = common_data[screen_on]
            with open(settings_path, "w+") as f:
                json.dump(settings, f)
        resp = jsonify(settings)
        return resp
    

    @app.route('/setSport', methods=['POST'])
    def setSport():
        global common_data
        global data_lock
        with data_lock:
            interrupt()
            common_data[active_screen] = ActiveScreen.REFRESH
            common_data[screen_on] = True
            draw()
            content = request.get_json()
            new_screen = ActiveScreen(content["sport"])
            common_data[active_screen] = ActiveScreen(content["sport"])
            #Update the file    
            with open(settings_path) as f:
                settings = json.load(f)
                settings["active_screen"] = common_data[active_screen].value
                settings["screen_on"] = common_data[screen_on]
            with open(settings_path, "w+") as f:
                json.dump(settings, f)

        resp = jsonify(settings)
        return resp

    @app.route


    @app.route('/wifi', methods=['POST'])
    def setup_wifi():
        content = request.get_json()
        with open(wpa_template, "r") as template:
            wpa_content = Template(template.read())
            substituted = wpa_content.substitute(ssid=content['ssid'], psk=content['psk'])
            with open(wpa_path, "w+") as wpa_supplicant:
                wpa_supplicant.write(substituted)
                subprocess.Popen([hotspot_off])
        resp = jsonify(success=True)
        return resp

    @app.route('/reset_wifi', methods=['POST'])
    def reset_wifi():
        subprocess.Popen([hotspot_on])
        resp = jsonify(success=True)
        return resp

    def get_settings():
        with open(settings_path) as f:
            settings = json.load(f) 
        return settings
    def write_settings(new_settings):
        with open(settings_path, "w+") as f:
            json.dump(settings, f)

    common_data[screen_on] = True # Starting the service ALWAYS turns the screen on
    settings = get_settings()
    settings["screen_on"] = True
    write_settings(settings)
    draw()
    log.info("Refreshing Sports")
    mlb = MLB()
    log.info("Got MLB")
    nhl = NHL()
    log.info("Got NHL")
    with data_lock:
        common_data[screens][ActiveScreen.NHL] = nhl
        common_data[screens][ActiveScreen.MLB] = mlb
        common_data[screens][ActiveScreen.QR] = QRScreen()
        common_data[screens][ActiveScreen.HOTSPOT] = WifiHotspot()
        #common_data[active_screen] = ActiveScreen(get_settings()["active_screen"])
        #common_data[active_screen] = ActiveScreen.HOTSPOT
        common_data[active_screen] = ActiveScreen.QR
    log.info("Done setup")
    atexit.register(interrupt)
    return app

def run_webserver():
    create_app().run(host='0.0.0.0', port=5005)

if __name__ == '__main__':
    
    options = RGBMatrixOptions()
    options.brightness = 100
    options.rows = 32
    options.cols = 64
    options.hardware_mapping = "adafruit-hat"

    with data_lock:
        common_data[active_screen] = ActiveScreen.REFRESH 
        common_data[screens] = {ActiveScreen.REFRESH: InfoScreen("Starting")}
        common_data[matrix] = RGBMatrix(options=options)

    if not testing:
        run_webserver()
    else:
        web_thread = threading.Thread(target=run_webserver)
        web_thread.start()
        common_data[matrix].master.mainloop()

