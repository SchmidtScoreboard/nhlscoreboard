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

    nhl_renderer = NHLRenderer(64, 32)
    nhl = NHL()

    mlb_renderer = MLBRenderer(64, 32)
    mlb = MLB()
    
    active_screen = ActiveScreen.MLB

    if active_screen == ActiveScreen.NHL:
        renderer = nhl_renderer
        league = nhl
    elif active_screen == ActiveScreen.MLB:
        renderer = mlb_renderer
        league = mlb

    rotate_games = True
    active_index = 0
    refresh_count = 0

    #main loop
    while(True):
        if refresh_count > 20:
            print("Full refresh")
            league.__init__()
            refresh_count = 0
        blues = league.team_playing(19)
        if blues !=  None: #if blues are playing, stick to one page
            rotate_games = False
            active_index = blues
        image = renderer.render(league.games[active_index % len(league.games)]) if len(nhl.games) > 0 else renderer.render_no_games()
        matrix.Clear()
        matrix.SetImage(image.convert("RGB"))
        if rotate_games:
            active_index += 1
            time.sleep(10)
        else:
            time.sleep(1)
        league.refresh()
        refresh_count += 1
    matrix.Clear()
