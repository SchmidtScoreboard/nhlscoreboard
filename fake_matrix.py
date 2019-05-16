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
        self.master.update()
    def SetImage(self, img):
        img = RefreshScreen("blah").get_image()
        img = img.resize((self.width, self.height), Image.ANTIALIAS)
        tkimg = ImageTk.PhotoImage(img)
        self.window.create_image(0, 0, anchor="nw", image=tkimg)
        self.window.image = tkimg
        self.window.pack()
        self.master.update()
    def Clear(self):
        pass

class RGBMatrixOptions():
    def __init__(self):
        pass

if __name__ == "__main__":
    matrix = RGBMatrix()
    matrix.SetImage("blah")
    matrix.master.mainloop()
