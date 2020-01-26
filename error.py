import json
from collections import namedtuple
from PIL import Image, ImageDraw, ImageFont
from common import * 
from files import *

class ErrorScreen(Screen):
    def __init__(self, scrolling_message, instructions):
        super().__init__()
        self.width = 64
        self.height = 32
        self.message = scrolling_message
        self.instructions = instructions
        self.renderer = Renderer(self.width, self.height)

    def get_sleep_time(self):
        return 0.05

    def get_image(self):
        image =  self.renderer.draw_error(None, scrollingText=self.message)
        for index, instruction in enumerate(self.instructions):
            self.renderer.draw_text(instruction, x=4, y=10 + 7*index, color=(255, 0, 0), image=image)
        return image


        

