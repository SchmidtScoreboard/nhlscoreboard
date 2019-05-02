from PIL import Image, ImageDraw, ImageFont
from rgbmatrix import graphics, RGBMatrixOptions, RGBMatrix 
from nhl import * 
from mlb import *
from common import *
import time
from enum import Enum

class ActiveScreen(Enum):
    NHL = 1,
    MLB = 2


if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.brightness = 100
    options.rows = 32
    options.cols = 64
    options.hardware_mapping = "adafruit-hat"
    matrix = RGBMatrix(options = options)

    nhl = NHL()

    mlb = MLB()
    
    active_screen = ActiveScreen.MLB

    if active_screen == ActiveScreen.NHL:
        league = nhl
    elif active_screen == ActiveScreen.MLB:
        league = mlb

    rotate_games = True

    #main loop
    while(True):
        image = league.get_image()
        matrix.Clear()
        matrix.SetImage(image.convert("RGB"))
        time.sleep(league.get_sleep_time())
        league.refresh()

    matrix.Clear()
