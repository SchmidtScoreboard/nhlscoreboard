from flask import Flask
from flask import request
from flask import jsonify
from string import Template
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

data_lock = threading.Lock()
render_thread = threading.Thread()

def create_app():
    app = Flask(__name__)

    def interrupt():
        global render_thread
        with data_lock:
            render_thread.cancel()

    def draw():
        global common_data
        global render_thread
        with data_lock:
            common_data["elem"] += 1
            print(common_data["elem"])
            
        render_thread = threading.Timer(REFRESH_TIME, draw(), ())
        render_thread.start()
    
    def start_draw():
        global render_thread()

        render_thread = threading.Timer(REFRESH_TIME, draw(), ())
        render_thread.start()

    start_draw()
    atexit.register(interrupt)
    return app



@app.route('/', methods = ['GET'])
def root():
    with open(settings_path) as out:
        data = json.load(out)
        return jsonify(data)

@app.route('/configure', methods= ['POST'])
def configure():
    content = request.get_json()
    with open(settings_path, "w+") as out:
        json.dump(content, out)
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

if __name__ == '__main__':
    create_app().run(host = '0.0.0.0', port=5005)
