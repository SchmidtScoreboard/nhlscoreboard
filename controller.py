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

    rotateGames = True
    activeIndex = 0

    #main loop
    while(True):
        blues = nhl.team_playing(19)
        if blues: #if blues are playing, stick to one page
            rotateGames = False
            activeIndex = blues
        image = renderer.render(nhl.games[activeIndex % len(nhl.games)]) if len(nhl.games) > 0 else renderer.render_no_games()
        matrix.Clear()
        matrix.SetImage(image.convert("RGB"))
        if rotateGames:
            activeIndex += 1
            time.sleep(10)
        else:
            time.sleep(1)
        nhl.refresh()
    matrix.Clear()
