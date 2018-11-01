import cv2
import numpy as np
import pytesseract
from PIL import Image
from pytesseract import image_to_string
import os


def read_img(path):
    """Given a path to an image file, returns a cv2 array

    str -> np.ndarray"""
    if os.path.isfile(path):
        return cv2.imread(path)
    else:
        raise ValueError('Path provided is not a valid file: {}'.format(path))

# Path of working folder on Disk

def get_string(img_path):
    # Read image with opencv
    img = read_img(img_path)
    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    img = cv2.blur(img,(3,3))
    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    # Write image after removed noise
    # cv2.imwrite(src_path + "removed_noise.png", img)

    #  Apply threshold to get image with only black and white
    #img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    # Write the image after apply opencv to do some ...
    cv2.imwrite(img_path + "thres.png", img)

    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(Image.open(img_path + "thres.png"), lang='eng')

    # Remove template file
    #os.remove(temp)

    return result

