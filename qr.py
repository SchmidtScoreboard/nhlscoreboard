import qrcode

import json
from collections import namedtuple
from PIL import Image, ImageDraw, ImageFont
from common import * 
from files import *

class QRScreen(Screen):
    def __init__(self, text, message):
        super().__init__()
        self.width = 64
        self.height = 32
        self.text = text
        self.message = message #message will be stored and displayed in the QR code

    def get_sleep_time(self):
        return 2

    def get_image(self):
        renderer = Renderer(64, 32)
        qr_image = qrcode.make(self.message, version=2, box_size=1, border=4)
        w = qr_image.width + 4 * 2
        image = Image.new("RGB", (self.width, self.height))
        draw = ImageDraw.Draw(image)
        draw.bitmap((self.width - w,0), qr_image)

        # TODO add text/image to left panel


        return image
