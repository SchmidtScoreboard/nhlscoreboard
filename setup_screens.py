
import json
from collections import namedtuple
from PIL import Image, ImageDraw, ImageFont
from common import *
from files import *
import subprocess
import threading
import time
import config
from enum import Enum
from code_converter import *


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
        image, draw, self.text_start = renderer.get_scrolling_text(
            self.text_start, image, self.text)
        draw.point(renderer.draw_pixels(wifi, 8, 8))
        renderer.draw_text("Network:", x=24, y=12,
                           color=(255, 255, 255), image=image)
        renderer.draw_text("Scoreboard42", x=8, y=22,
                           color=(255, 255, 255), image=image)

        return image


class SyncScreen(SetupScreen):
    def __init__(self):
        super().__init__("Enter the code below in the Scoreboard App")
        try:
            log.info("IP is: {}".format(get_ip_address()))
            self.code = ip_to_code(get_ip_address())
        except:
            self.error = True
            self.error_message = "Could not connect"
            self.error_title = "Failed to connect to the internet, reset/restart scoreboard to continue setup"

    def get_image(self):
        image = Image.new("RGB", (self.width, self.height))
        renderer = Renderer(self.width, self.height)
        if not self.error:
            image, draw, self.text_start = renderer.get_scrolling_text(
                self.text_start, image, self.text)
            # center offset by 6 to center in scrolling text frame
            renderer.draw_text(self.code, height=32+6, centered=True,
                               font_filename=biggest_font, image=image)
        else:
            image, draw = renderer.draw_error(
                self.error_title, scrollingText=self.error_message)
        return image


class ConnectionScreen(SetupScreen):
    def __init__(self):
        super().__init__("Send your home wifi details using the Scoreboard app")
        self.start_countdown = False

    def begin_countdown(self, supplicant):
        self.start_countdown = True
        settings = get_settings()
        settings["setup_state"] = SetupState.SYNC.value
        settings["active_screen"] = ActiveScreen.SYNC.value
        # Don't change the loaded screen because we are restarting
        write_settings(settings)
        log.info(settings)
        with open(wpa_path, "w+") as wpa_supplicant:
            wpa_supplicant.write(supplicant)
            log.info("Sending signal to setup wifi and restart")
            restart_thread = threading.Timer(5, send_wifi_signal)
            restart_thread.start()

    def get_image(self):
        image = Image.new("RGB", (self.width, self.height))
        renderer = Renderer(self.width, self.height)
        image, draw, self.text_start = renderer.get_scrolling_text(
            self.text_start, image, self.text)
        if not self.start_countdown:
            renderer.draw_text("Use app to", x=4, y=10,
                               color=(255, 255, 255), image=image)
            renderer.draw_text("send wifi", x=4, y=17,
                               color=(255, 255, 255), image=image)
            renderer.draw_text("and password", x=4, y=24,
                               color=(255, 255, 255), image=image)
        else:
            renderer.draw_text("Got wifi,", x=4, y=10,
                               color=(255, 255, 255), image=image)
            renderer.draw_text("restarting...", x=4, y=17,
                               color=(255, 255, 255), image=image)
            renderer.draw_text("Please wait", x=4, y=24,
                               color=(255, 255, 255), image=image)
        return image
