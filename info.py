import json
from collections import namedtuple
from PIL import Image, ImageDraw, ImageFont
from common import * 
from files import *

class InfoScreen(Screen):
    def __init__(self, text):
        super().__init__()
        self.iteration = 0
        self.width = 64
        self.height = 32
        self.text = text

    def get_sleep_time(self):
        return 2

    def get_image(self):
        renderer = Renderer(64, 32)
        image, draw = renderer.draw_info(self.text)
        return image


        

