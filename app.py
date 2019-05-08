from flask import Flask
from flask import request
from flask import jsonify
from string import Template
from PIL import Image, ImageDraw, ImageFont
from rgbmatrix import graphics, RGBMatrixOptions, RGBMatrix
from nhl import *
from mlb import *
from common import *
import threading
import atexit
import time
import subprocess
import json
app = Flask(__name__)
settings_path = "/home/pi/nhlscoreboard/scoreboard_settings.json"
wpa_template = "/home/pi/nhlscoreboard/wpa_supplicant.conf.template"
wpa_path = "/home/pi/nhlscoreboard/wpa_supplicant.conf"
hotspot_on = "/home/pi/nhlscoreboard/hotspot_on.sh"
hotspot_off = "/home/pi/nhlscoreboard/hotspot_off.sh"

REFRESH_TIME = 10

common_data = { "elem": 0 }


active_screen = "ACTIVE_SCREEN"
leagues = "LEAGUES"
matrix = "MATRIX"
nhl = "NHL"
mlb = "MLB"
data_lock = threading.Lock()
render_thread = threading.Thread()

def create_app():
    app = Flask(__name__)

    def interrupt():
        global render_thread
        render_thread.cancel()

    def draw():
        global common_data
        global render_thread
        with data_lock:
            print("About to draw scheduled")
            image = common_data[leagues][common_data[active_screen]].get_image()
            common_data[matrix].Clear()
            common_data[matrix].SetImage(image.convert("RGB")) 
            common_data[leagues][common_data[active_screen]].refresh()
            print("Done drawing scheduled")
        render_thread = threading.Timer(REFRESH_TIME, draw, ())
            
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
            image = common_data[leagues][common_data[active_screen]].get_image()
            common_data[matrix].Clear()
            common_data[matrix].SetImage(image.convert("RGB")) 
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
    options = RGBMatrixOptions()
    options.brightness = 100
    options.rows = 32
    options.cols = 64
    options.hardware_mapping = "adafruit-hat"
    with data_lock:
        common_data[active_screen] = ActiveScreen.MLB #TODO get this from configuration
        common_data[leagues] = {}
        print("Refreshing Sports")
        common_data[leagues][ActiveScreen.NHL] = NHL()
        print("Got NHL")
        common_data[leagues][ActiveScreen.MLB] = MLB() 
        print("Got MLB")
        common_data[matrix] = RGBMatrix(options = options)
    draw()
    atexit.register(interrupt)
    return app




if __name__ == '__main__':
    create_app().run(host = '0.0.0.0', port=5005)
