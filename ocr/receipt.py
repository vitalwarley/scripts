import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import pytesseract
from pytesseract import Output

def showimg(img, wname):
    while True:
        cv.imshow(wname, img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            cv.destroyAllWindows()
            break


img = cv.imread('data/receipt/1.jpg', cv.IMREAD_GRAYSCALE)
showimg(img, 'img')

thresh = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 
                              25, 10)
showimg(thresh, 'thresh')

d = pytesseract.image_to_data(thresh, output_type=Output.DICT, lang='por')
n_boxes = len(d['level'])
for i in range(n_boxes):
    (x, y, w, h) = (d['left'][i],
                    d['top'][i],
                    d['width'][i],
                    d['height'][i])
    img = cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

showimg(img, 'img')


text = pytesseract.image_to_string(thresh, lang='por')
text = pytesseract.image_to_string(img, lang='por')
