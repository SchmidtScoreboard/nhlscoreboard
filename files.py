import os, sys
root_path = os.path.dirname(os.path.realpath(sys.argv[0]))
print(root_path)
settings_path = os.path.join(root_path, "scoreboard_settings.json")
wpa_template = "/home/pi/nhlscoreboard/wpa_supplicant.conf.template"
wpa_path = "/home/pi/nhlscoreboard/wpa_supplicant.conf"
hotspot_on = "/home/pi/nhlscoreboard/hotspot_on.sh"
hotspot_off = "/home/pi/nhlscoreboard/hotspot_off.sh"
small_font = os.path.join(root_path, "fonts/4x6.pil")
big_font = os.path.join(root_path, "fonts/5x8.pil")