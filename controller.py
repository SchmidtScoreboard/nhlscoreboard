from PIL import Image, ImageDraw, ImageFont
from rgbmatrix import graphics, RGBMatrixOptions, RGBMatrix 
from backend import Game, NHL
from view import Renderer
import time

if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.brightness = 100
    options.rows = 32
    options.cols = 64
    options.hardware_mapping = "adafruit-hat"
    matrix = RGBMatrix(options = options)
    renderer = Renderer(64, 32)
    nhl = NHL()

    rotate_games = True
    active_index = 0
    refresh_count = 0

    #main loop
    while(True):
        if refresh_count > 20:
            print("Full refresh")
            nhl = NHL()
            refresh_count = 0
        blues = nhl.team_playing(19)
        if blues !=  None: #if blues are playing, stick to one page
            rotate_games = False
            active_index = blues
        image = renderer.render(nhl.games[active_index % len(nhl.games)]) if len(nhl.games) > 0 else renderer.render_no_games()
        matrix.Clear()
        matrix.SetImage(image.convert("RGB"))
        if rotate_games:
            active_index += 1
            time.sleep(10)
        else:
            time.sleep(1)
        nhl.refresh()
        refresh_count += 1
    matrix.Clear()
