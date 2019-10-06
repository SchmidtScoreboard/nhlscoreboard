from PIL import Image, ImageDraw, ImageFont, ImageTk
from info import *
import tkinter as tk
import time

class RGBMatrix():
    def __init__(self, options=None):
        self.master = tk.Tk()
        self.width = 512
        self.height = 256
        self.window = tk.Canvas(self.master, width=self.width, height=self.height)
        self.window.pack()
    def SetImage(self, img):
        img = img.resize((self.width, self.height), Image.NEAREST)
        tkimg = ImageTk.PhotoImage(img)
        self.window.create_image(0, 0, anchor="nw", image=tkimg)
        self.window.image = tkimg
        self.window.pack()
    def Clear(self):
        pass

class RGBMatrixOptions():
    def __init__(self):
        pass