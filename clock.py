import json
from collections import namedtuple
from PIL import Image, ImageDraw, ImageFont
from common import *
from files import *
import subprocess
import time
import config
import datetime

class ClockScreen(Screen):

    def __init__(self):
        self.width = 64
        self.height = 32
        self.refresh()

    def refresh(self):
        now = datetime.datetime.now()
        self.current_time = now.strftime("%I:%M %p")

    def get_sleep_time(self):
        return 30

    def get_image(self):
        image = Image.new("RGB", (self.width, self.height))
        draw = ImageDraw.Draw(image)
        renderer = Renderer(self.width, self.height)
        renderer.draw_text(self.current_time,
                           color=(255, 255, 255), image=image, centered=True, font_filename=biggest_font)

        return image