import os
import sys
import pytesseract
import pyperclip 
from PIL import Image

img_path = sys.argv[1]
img = Image.open(img_path)
print(f'Image {img_path} loaded!')
text = pytesseract.image_to_string(img)
pyperclip.copy(text)
print('Image content copied to clipboard!')
os.remove(img_path)
