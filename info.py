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
        return 1

    def get_image(self):
        font = ImageFont.load(small_font)
        image = Image.new("RGB", (self.width, self.height))
        draw = ImageDraw.Draw(image)
        draw.rectangle([(0,0), (self.width-1, self.height-1)], outline=(255, 255, 255), fill=(0, 0, 0))
        
        w, h = font.getsize(self.text)
        x = self.width/2 - w/2
        y = self.height/2 - h/2
        draw.text((x,y), self.text, font=font, fill=(255, 255, 255))

        self.iteration = (self.iteration + 1) % (self.height)

        return image

        

