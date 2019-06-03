
import json
from collections import namedtuple
from PIL import Image, ImageDraw, ImageFont
from common import * 
from files import *
import qrcode

class SetupScreen(Screen):
    def __init__(self, text):
        super().__init__()
        self.width = 64
        self.height = 32
        self.text = text
        self.text_start = self.width

    def get_sleep_time(self):
        return 0.05

    def get_scrolling_text(self, image=None):
        renderer = Renderer(self.width, self.height)
        if image is None:
            image = Image.new("RGB", (self.width, self.height))
        draw = ImageDraw.Draw(image) #  let's draw on this image
        draw.rectangle(((0,0), (64,6)), fill=(255, 255,255))
        font = ImageFont.load(small_font)
        w, h = font.getsize(self.text)
        text_end = self.text_start + w
        secondary_start = text_end + 16
    
        renderer.draw_text(self.text, x=self.text_start, y=1, color=(0,0,0), image=image)
        renderer.draw_text(self.text, x=secondary_start, y=1, color=(0,0,0), image=image)

        self.text_start -= 1
        if text_end <= 0:
            self.text_start = secondary_start - 1
        return image

class WifiHotspot(SetupScreen):
    def __init__(self):
        super().__init__("Open the Scoreboard Controller app and connect to WiFi:")

    def get_image(self):
        return super().get_scrolling_text()

class QRScreen(SetupScreen):
    def __init__(self):
        super().__init__("Scan the QR code to sync with the Scoreboard Controller app")
        self.message = "QR CODE MESSAGE HERE"
        self.qr_image = qrcode.make(self.message, version=1, box_size=1, border=4)

    def get_image(self):
        image = Image.new("RGB", (self.width, self.height))

        w = self.qr_image.width + 4 * 2
        draw = ImageDraw.Draw(image)
        draw.bitmap((self.width/2 - w/2,5), self.qr_image)
        super().get_scrolling_text(image)

        return image