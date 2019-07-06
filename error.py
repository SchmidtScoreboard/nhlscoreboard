import json
from collections import namedtuple
from PIL import Image, ImageDraw, ImageFont
from common import * 
from files import *

class ErrorScreen(Screen):
    def __init__(self, message):
        super().__init__()
        self.width = 64
        self.height = 32
        self.message = message
        self.text_start = self.width

    def get_sleep_time(self):
        return 0.05

    def get_image(self):
        renderer = Renderer(64, 32)
        image, draw = renderer.draw_border(color = (255,0,0))

        image, draw, self.text_start = renderer.get_scrolling_text(self.text_start, image, self.message, (255,0,0),(0,0,0))
        return image


        

