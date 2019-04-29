from flask import Flask
from flask import request
from flask import jsonify
import json
app = Flask(__name__)
settings_path = "/home/pi/nhlscoreboard/scoreboard_settings.json"

@app.route('/', methods = ['GET'])
def root():
    global settings_path
    with open(settings_path) as out:
        data = json.load(out)
        return jsonify(data)

@app.route('/configure', methods= ['POST'])
def configure():
    global settings_path
    content = request.get_json()
    with open(setting_path) as out:
        json.dump(content, out)
    resp = jsonify(success=True)
    return resp

@app.route('/wifi', methods=['POST'])
def setup_wifi():
    content = request.get_json()
    with open("/home/pi/nhlscoreboard/wifi.json") as out:
        json.dump(content, out)
    resp = jsonify(success=True)
    return resp

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=5005)
