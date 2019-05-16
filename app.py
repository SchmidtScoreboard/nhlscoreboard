from flask import Flask
from flask import request
from flask import jsonify
from string import Template
from PIL import Image, ImageDraw, ImageFont
testing = False
try:
    from rgbmatrix import graphics, RGBMatrixOptions, RGBMatrix
    print("Running in production mode")
except:
    testing = True
    print("Running in test mode")
    from fake_matrix import *

from nhl import *
from mlb import *
from refresh import *
from common import *
import threading
import atexit
import time
import subprocess
import json
import sys
import os
from files import *

app = Flask(__name__)


common_data = {}


active_screen = "ACTIVE_SCREEN"
screens = "SCREENSj"
matrix = "MATRIX"
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
            image = common_data[screens][common_data[active_screen]].get_image()
            common_data[matrix].Clear()
            common_data[matrix].SetImage(image.convert("RGB")) 
            common_data[screens][common_data[active_screen]].refresh()
        

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
            print("configuring")
        content = request.get_json()
        with open(settings_path, "w+") as out:
            json.dump(content, out)
        resp = jsonify(success=True)
        return resp

    @app.route('/setSport', methods=['POST'])
    def setSport():
        global common_data
        global data_lock
        with data_lock:
            content = request.get_json()
            common_data[active_screen] = ActiveScreen(content["sport"])
            print("Swapping to sport: {}".format(common_data[active_screen]))
            common_data[leagues][common_data[active_screen]].refresh()
            draw_image()
            print("Done swapping")

        resp = jsonify(success=True)
        return resp


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
    draw()
    print("Refreshing Sports")
    mlb = MLB()
    print("Got MLB")
    nhl = NHL()
    print("Got NHL")
    with data_lock:
        common_data[screens][ActiveScreen.NHL] = nhl
        common_data[screens][ActiveScreen.MLB] = mlb
        common_data[active_screen] = ActiveScreen.NHL
    print("Done setup")
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
        common_data[screens] = {ActiveScreen.REFRESH: RefreshScreen("Refreshing")}
        common_data[matrix] = RGBMatrix(options=options)

    if not testing:
        run_webserver()
    else:
        web_thread = threading.Thread(target=run_webserver)
        web_thread.start()
        common_data[matrix].master.mainloop()

