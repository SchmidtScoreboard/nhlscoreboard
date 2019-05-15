from PIL import Image, ImageDraw, ImageFont
from refresh import *
class FakeMatrix():
    
    def __init__(self, options=None):
        pass
    
    def SetImage(self, image):
        image = RefreshScreen("text").get_image()
        image.show()

    def Clear(self):
        pass

if __name__ == "__main__":
    matrix = FakeMatrix()
    matrix.SetImage("asdf")