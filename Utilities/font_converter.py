from PIL import BdfFontFile
from PIL import PcfFontFile
import sys
font_file_path = sys.argv[1]


with open(font_file_path, 'rb') as fp:
    p = BdfFontFile.BdfFontFile(fp)  # PcfFontFile if you're reading PCF files
    # won't overwrite, creates new .pil and .pdm files in same dir
    p.save(font_file_path)
