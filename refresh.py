import requests
import json
from collections import namedtuple
from PIL import Image, ImageDraw, ImageFont
from common import * 

class RefreshScreen(Screen):
    def __init__(self, text):
        super().__init__()
        self.iteration = 0
        self.width = 64
        self.height = 32
        self.text = text

    def get_sleep_time(self):
        return 0.03

    def get_point(self):
        #starting in top left, move one point clockwise each iteration
        x = self.iteration % self.width
        y = 0
        return x, y
    def get_image(self):
        font = ImageFont.load("/home/pi/nhlscoreboard/fonts/4x6.pil")
        image = Image.new("RGB", (self.width, self.height))
        draw = ImageDraw.Draw(image)
        draw.rectangle([(0,0), (self.width-1, self.height-1)], outline=(255, 255, 255), fill=(0, 0, 0))
        draw.point(self.get_point(), fill=(0,0,0))
        
        display_text = "Refreshing {}...".format(self.text)
        w, h = font.getsize(display_text)
        if w > 60:
            display_text = "Refreshing\n{}...".format(self.text)
            w, h = font.getsize(display_text)
        x = self.width/2 - w/2
        y = self.height/2 - h/2
        draw.text((x,y), display_text, font=font, fill=(128, 128, 128))

        self.iteration = (self.iteration + 1) % (self.height)

        return image

        

