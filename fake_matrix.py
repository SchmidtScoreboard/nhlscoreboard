from PIL import Image, ImageDraw, ImageFont, ImageTk
from refresh import *
import tkinter as tk
import time

class FakeMatrix(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.window = tk.Canvas(root, width=400, height=400)
        self.pack()
        self.window.pack()
    def SetImage(self, img):
        img = RefreshScreen("text").get_image()
        tkimg = ImageTk.PhotoImage(img)
        self.window.create_image(0, 0, anchor="nw", image=tkimg)
        self.window.pack()
    def Clear(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    matrix = FakeMatrix(root)
    matrix.SetImage("blah")
    matrix.mainloop()
