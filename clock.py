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

    def __init__(self, timezone):
        self.width = 64
        self.height = 32
        self.timezone = timezone
        self.refresh()

    def refresh(self):
        utc_time = datetime.datetime.utcnow()
        local_time = pytz.utc.localize(
            utc_time, is_dst=None).astimezone(pytz.timezone(self.timezone))
        self.current_time = local_time.strftime("%-I:%M %p")

    def get_sleep_time(self):
        return 30

    def get_image(self):
        image = Image.new("RGB", (self.width, self.height))
        renderer = Renderer(self.width, self.height)
        renderer.draw_text(self.current_time,
                           color=(255, 255, 255), image=image, centered=True, font_filename=biggest_font)

        return image
