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

    def get_sleep_time(self):
        return 2

    def get_image(self):
        renderer = Renderer(64, 32)
        image = renderer.draw_error(self.message)
        return image


        

