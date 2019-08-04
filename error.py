import json
from collections import namedtuple
from PIL import Image, ImageDraw, ImageFont
from common import * 
from files import *

class ErrorScreen(Screen):
    def __init__(self, message, title="Error"):
        super().__init__()
        self.width = 64
        self.height = 32
        self.title = title
        self.message = message
        self.renderer = Renderer(self.width, self.height)

    def get_sleep_time(self):
        return 0.05

    def get_image(self):
        return self.renderer.draw_error(self.title, scrollingText=self.message)


        

