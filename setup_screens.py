
import json
from collections import namedtuple
from PIL import Image, ImageDraw, ImageFont
from common import * 
from files import *
import subprocess
import qrcode
import time
from enum import Enum

class SetupState(Enum):
    FACTORY = 0
    HOTSPOT = 1
    WIFI_CONNECT = 2
    SYNC = 3
    READY = 10

class SetupScreen(Screen):
    def __init__(self, text):
        super().__init__()
        self.width = 64
        self.height = 32
        self.text = text
        self.text_start = self.width

    def get_sleep_time(self):
        return 0.05

class WifiHotspot(SetupScreen):
    def __init__(self):
        super().__init__("Open the Scoreboard App and connect to WiFi:")

    def get_image(self):
        image = Image.new("RGB", (self.width, self.height))
        draw = ImageDraw.Draw(image)
        renderer = Renderer(self.width, self.height)
        image, draw, self.text_start = renderer.get_scrolling_text(self.text_start, image, self.text)
        draw.point(renderer.draw_pixels(wifi, 8, 8))
        renderer.draw_text("Network:", x=24, y=12, color=(255,255,255), image=image)
        renderer.draw_text("Scoreboard42", x=8, y=22, color=(255,255,255), image=image)
       
        return image

class QRScreen(SetupScreen):
    def __init__(self):
        super().__init__("Scan the QR code using the Scoreboard App")
        self.message = get_ip_address()
        self.qr_image = qrcode.make(self.message, version=1, box_size=1, border=4)

    def get_image(self):
        image = Image.new("RGB", (self.width, self.height))

        w = self.qr_image.width + 4 * 2
        draw = ImageDraw.Draw(image)
        draw.bitmap((self.width/2 - w/2,5), self.qr_image)
        renderer = Renderer(self.width, self.height)
        image, draw, self.text_start = renderer.get_scrolling_text(self.text_start, image, self.text)

        return image

class ConnectionScreen(SetupScreen):
    def __init__(self):
        super().__init__("Send your home wifi details using the Scoreboard app")
        self.start_countdown = False
        self.timer = 0

    def begin_countdown(self, supplicant, script):
        self.timer = time.time()
        self.start_countdown = True
        self.restart_message = "3..."
        self.supplicant = supplicant
        self.fired = False
        self.script = script

    def refresh(self):
        if self.start_countdown:
            time_spent = time.time() - self.timer
            if self.fired:
                return
            elif time_spent > 3.0 and not self.fired:
                # time to restart
                settings = get_settings()
                settings["setup_state"] = SetupState.SYNC.value
                settings["active_screen"] = ActiveScreen.QR.value
                #Don't change the loaded screen because we are restarting
                write_settings(settings)
                log.info(settings)
                with open(wpa_path, "w+") as wpa_supplicant:
                    wpa_supplicant.write(self.supplicant)
                    self.fired = True
                    subprocess.Popen([self.script])
                    
            elif time_spent > 2.0:
                self.restart_message = "3...2...1..."
            elif time_spent > 1.0:
                self.restart_message = "3...2..."
        

    def get_image(self):
        image = Image.new("RGB", (self.width, self.height))
        renderer = Renderer(self.width, self.height)
        image, draw, self.text_start = renderer.get_scrolling_text(self.text_start, image, self.text)
        if not self.start_countdown:
            renderer.draw_text("Waiting on", x=4, y=10, color=(255,255,255), image=image)
            renderer.draw_text("wifi...", x=4, y=17, color=(255,255,255), image=image)
        else:
            renderer.draw_text("Got wifi,", x=4, y=10, color=(255,255,255), image=image)
            renderer.draw_text("restarting in", x=4, y=17, color=(255,255,255), image=image)
            renderer.draw_text(self.restart_message, x=4, y=24, color=(255,255,255), image=image)
        return image
