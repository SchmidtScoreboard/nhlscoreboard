from PIL import Image, ImageDraw, ImageFont, ImageTk
from refresh import *
import tkinter as tk
import time

class RGBMatrix():
    def __init__(self, options=None):
        self.master = tk.Tk()
        self.width = 256
        self.height = 128
        self.window = tk.Canvas(self.master, width=self.width, height=self.height)
        self.window.pack()
    def SetImage(self, img):
        img = img.resize((self.width, self.height), Image.BILINEAR)
        tkimg = ImageTk.PhotoImage(img)
        self.window.create_image(0, 0, anchor="nw", image=tkimg)
        self.window.image = tkimg
        self.window.pack()
    def Clear(self):
        pass

class RGBMatrixOptions():
    def __init__(self):
        pass

if __name__ == "__main__":
    matrix = RGBMatrix()
    matrix.SetImage("blah")
    matrix.master.mainloop()
